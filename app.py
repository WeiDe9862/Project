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
def email():
    email = request.args.get('email')
    password = request.args.get('password')
    return f"{email},{password}"

if __name__=='__main__':
    app.run(debug=True)