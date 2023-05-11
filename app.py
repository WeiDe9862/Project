from flask import Flask,render_template,request
import sqlite3 as sql
from flask import g

DATABASE = 'database.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method =="POST":
        name=request.form.get("Account")
        password = request.form.get("Password")
        if name=="admin" and password=="1234":
            type="登入成功"
            return render_template("page2.html",id=name,ps=password,type=type)
        else:
            type="登入失敗"
            return render_template('login.html',id=name,ps=password,type=type)
    else:
        return render_template('login.html')

@app.route("/name/<name>")
def name(name):
    print('Type:',type(name))
    return name

@app.route("/number/<int:number>")
def number(number):
    print('Type:',type(number))
    return f'{number}'

@app.route("/page")
def page():
    x="1234"
    dict1={"abc":1324,"name":"Alex"}
    return render_template("page.html",x=x,dict1=dict1)
    
@app.route("/users")
def users():
    with get_db() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor()
        cur.execute('select * from Users')
        data = cur.fetchall()
        cur.close()
    return render_template("users.html",data = data)

if __name__=='__main__':
    app.run(debug=True)