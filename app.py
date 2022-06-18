from datetime import datetime
from stat import UF_OPAQUE
from flask import Flask, redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


from sqlalchemy import desc
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/products",methods=['GET','POST'])
def products():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    # print(allTodo)
    return render_template('index.html',allTodo=allTodo)

    
@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/products")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

    
@app.route("/delete/<int:sno>")
def delete(sno):
    deletetodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(deletetodo)
    db.session.commit()
    return redirect("/products")

@app.route("/")
def HelloWorld():
    return "Hello, Welcome to my first Flask program!  Here you will learn some basic Flask, python, Bootstrap, html functionality. And please don't forget to go to /product page for the developed website."


if __name__ == "__main__":
    app.run(debug=True,port=8000)