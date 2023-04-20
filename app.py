from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/index")
def index():
    return render_template('index.html')

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
    
if __name__=='__main__':
    app.run(debug=True)