import dbconn
import random

from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)
@app.route('/')
def index():
    #return 'Hello world!'

    # connect to 
    conn = dbconn.get_db_connection();

    customers = executeTest(conn);
    conn.close;

    return render_template('index.html', customers=customers);


def executeTest(conn):
    cur = conn.cursor();
    cur.execute('SELECT * FROM customer LIMIT 10;');
    customers = cur.fetchall();
    cur.close();
    return customers;


@app.route('/signin/', methods=('GET', 'POST'))
def signin():
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
            return redirect('http://127.0.0.1:5000/browse')
        else:
            print('query ressult: ', cmp[0])  
            print('password: ', password)      
    
    return render_template('signin.html');



@app.route('/browse/', methods=('GET', 'POST'))
def browse():
    return "browse";


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