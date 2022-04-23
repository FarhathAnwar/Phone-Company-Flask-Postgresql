import dbconn
import random
import jinja2

from flask import Flask, render_template, request, url_for, redirect, session
import datetime

app = Flask(__name__)
app.secret_key = 'UNIQUE_SECRET_KEY'

@app.route('/')
def index():
    #return 'Hello world!'

    # connect to 
    conn = dbconn.get_db_connection();

    products = executeTest(conn);
    conn.close;

    return render_template('index.html', products=products);


def executeTest(conn):
    cur = conn.cursor();
    cur.execute('SELECT * FROM product LIMIT 10;');
    customers = cur.fetchall();
    cur.close();
    return customers;


@app.route('/signin/', methods=('GET', 'POST'))
def signin():
    session['username'] = ''
    session['cid'] = 0
    session['pid_of_placed_order'] = 0
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = dbconn.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM customer WHERE email=(%s)"+"limit 1;", (email, ))
        #cur.commit()
        query_result = cur.fetchall()
        cur.close()
        conn.close()

        cmp = query_result[0]  # ('password', )

        if(cmp[0] == password):
            print('matched')
            session['username'] = getFirstName(email, password)
            session['cid'] = getCID(email, password)
            #print(session['username'])
            return redirect('http://127.0.0.1:5000/browse')
        else:
            print('query ressult: ', cmp[0])  
            print('password: ', password)      
    
    return render_template('signin.html');



@app.route('/browse/', methods=('GET', 'POST'))
def browse():
    conn = dbconn.get_db_connection()

    products = executeTest(conn)
    conn.close

    user = session['username']
    return render_template('browse.html', products=products, user=user);


@app.route('/create_account/', methods=('GET', 'POST'))
def create_account():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        cid = random.randint(2000, 99999)

        conn = dbconn.get_db_connection()
        cur = conn.cursor()
        cur.execute('Insert into customer(cid, first_name, last_name, phone_number, password, email) overriding system value Values(%s , %s, %s, %s, %s, %s)',(cid, fname, lname, phone, password, email))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('http://127.0.0.1:5000/browse')

        #test start

        #test end
    return render_template('create_acc.html');


@app.route('/buy/<int:pid>', methods=('GET', 'POST'))
def buy(pid):
    conn = dbconn.get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM product WHERE pid=(%s);', (pid, ))
    conn.commit()
    selected_product = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        delivery_addr = request.form['address']
        order_quantity = 1
        order_date = datetime.datetime.today()
        delivery_date = datetime.datetime.today() + datetime.timedelta(days=1)
        total_price = getPriceFromPID(pid)
        cid = session['cid']

        session['pid_of_placed_order'] = pid

        conn = dbconn.get_db_connection()
        cur = conn.cursor()
        cur.execute('Insert into buys(b_cid, b_pid, delivery_address, order_date, delivery_date, order_quantity, total_price) Values(%s , %s, %s, %s, %s, %s, %s)',(cid, pid, delivery_addr, order_date, delivery_date, order_quantity, total_price))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('http://127.0.0.1:5000/confirmation')

    user = session['username']
    return render_template('buy.html', user=user, products=selected_product)



@app.route('/confirmation/', methods=('GET', 'POST'))
def confirmation():
    return render_template('confirmation.html')


def getFirstName(email, password):
    conn = dbconn.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT first_name FROM customer WHERE email=(%s) AND password=(%s) "+"limit 1;", (email, password))
    #cur.commit()
    query_result = cur.fetchall()
    cur.close()
    conn.close()

    name_list = query_result[0]
    first_name = name_list[0]
    return first_name


def getCID(email, password):
    conn = dbconn.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT cid FROM customer WHERE email=(%s) AND password=(%s) "+"limit 1;", (email, password))
    #cur.commit()
    query_result = cur.fetchall()
    cur.close()
    conn.close()

    cid_list = query_result[0]
    cid = cid_list[0]
    return cid

def getPriceFromPID(pid):
    price = 0
    conn = dbconn.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT price FROM product WHERE pid=(%s);", (pid, ))
    #cur.commit()
    query_result = cur.fetchall()
    cur.close()
    conn.close()

    price_list = query_result[0]
    price = price_list[0]
    return price