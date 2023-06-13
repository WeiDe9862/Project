from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
from flask import g
import os
import uuid
import hashlib

DATABASE = 'database.db'

UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg' }

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

def allowed_file(filename):
    x=''
    if '.' in filename and  filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        x = filename.rsplit('.',1)[1].lower()
    return x

def sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        type = '登入失敗'
        name = request.form.get("account")
        password = request.form.get("password")
        password = sha256(password)
        with get_db() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute('select * from Users')
            data = cur.fetchall()
            cur.close()
        for i in data:
            if name == i['account'] and password == i['password']:
                type = '成功'
                return render_template("page2.html",id=name,ps=password,type=type)
        else:
            return render_template('login.html',type=type)
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

@app.route("/deleteuser/<int:id>",methods=['POST'])
def deleteuser(id):
    with get_db() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor()
        cur.execute(f'DELETE FROM Users where id={id}')
        #cur.execute('select * from Users')
        #data = cur.fetchall()
        cur.close()
    flash('刪除成功')
    return redirect(url_for('users'))
    #return render_template("users.html",data = data)

@app.route("/createuser", methods=['POST'])
def createuser():
    name = request.form.get('username')
    if name == '':name = 'User'
    account = request.form.get('account')
    password = request.form.get('password')
    password = sha256(password)
    with get_db() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor()
        cur.execute(f"INSERT INTO Users (name, account, password)VALUES ('{name}','{account}','{password}');")
        cur.close()
    flash('新增成功')
    return redirect(url_for('users'))

@app.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    if request.method == 'POST':
        name = request.form.get('username')
        account = request.form.get('account')
        password = request.form.get('password')
        password = sha256(password)
        with get_db() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute(f'UPDATE Users SET name="{ name }", account="{account}", password="{password}" WHERE id = "{id}";')
            data = cur.fetchone()
            cur.close()
        flash('修改成功')
        return redirect(url_for('users'))
    else:
        with get_db() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute(f'select * from Users where id = {id}')
            data = cur.fetchone()
            #cur.execute('select * from Users')
            #data = cur.fetchall()
            cur.close()
            return render_template("edit.html",data = data)
    #return render_template("users.html",data = data)

@app.route("/upload",methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        #print(f.filename)
        f.filename = allowed_file(f.filename)
        name = str(uuid.uuid4())+"."+f.filename
        if f.filename == '':
            type = '附檔名不符'
        else:
            type = '新增成功'
            with get_db() as cur:
                cur.row_factory = sql.Row
                cur = cur.cursor()
                cur.execute(f"INSERT INTO Pictures (p_name)VALUES ('{name}');")
                cur.close()
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
        return render_template('upload.html',type=type)
    return render_template('upload.html')

@app.route("/show")
def show():
        with get_db() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute('select * from Pictures order by p_order')
            data = cur.fetchall()
            cur.close()
        return render_template("show.html",data=data)

@app.route("/pictures")
def pictures():
        with get_db() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute('select * from Pictures')
            data = cur.fetchall()
            length = len(data)
            cur.close()
        return render_template("pictures.html",data=data,len=length)

@app.route("/manager_pictures",methods=['POST'])
def manager_pictures():
    id = request.form.get('id')
    fun = request.form.get('fun')
    if fun == "修改":
        p_order = request.form.get('p_order')
        with get_db() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute(f'UPDATE Pictures SET p_order="{ p_order }" WHERE id = "{id}";')
            cur.close()
        flash('修改成功')
    else:
        p_name = request.form.get('p_name')
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], p_name))
        with get_db() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor()
            cur.execute(f'DELETE FROM Pictures WHERE id ="{id}";')
            cur.close()
        flash('刪除成功')
    return redirect(url_for('pictures'))

if __name__=='__main__':
    app.secret_key = "Your Key"
    app.run(debug=True)