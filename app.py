from datetime import datetime
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method  == 'POST':
        title = request.form['title']
        content = request.form['content']
        todo = Todo(title=title,content=content)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    # todo = Todo(title="First Todo", content="Learn flask")
    # db.session.add(todo)
    # db.session.commit()
    return render_template("index.html",allTodo=allTodo)

@app.route('/show')
def products():
    return "Hello"

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    print(todo)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>',methods=["POST","GET"])
def update(sno):
    if request.method=="POST":
        title=request.form['title']
        content=request.form['content']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.content = content
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        
    todo = Todo.query.filter_by(sno=sno).first()
    print(todo)
    return render_template('update.html',todo=todo)

if __name__=="__main__":
    app.run(debug=True,port=8000)
    