from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
#setting up database for the storage purpose
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


#creating a class for the input fields
class ToDo( db.Model ):
    sno = db.Column( db.Integer , primary_key = True )
    name = db.Column( db.String(200) , nullable = False )
    desc = db.Column( db.String( 500 ) , nullable = False )
    date = db.Column( db.DateTime , default = datetime.utcnow )
    
    # def __repr__(self) -> str:
    #     return f"{self.sno} - {self.name}"
@app.route("/" , methods = ["GET" , "POST"])
def helloWorld():
    if request.method == 'POST':
        title = request.form['name']
        desc = request.form['desc']
        todo = ToDo( name = title , desc = desc )
        db.session.add( todo )
        db.session.commit()
   
    allToDo = ToDo.query.all() # nothing to be related to the above commands
    return render_template("index.html", allToDo = allToDo )
    # return "Hello World!"

@app.route("/show")
def showQueries():
    allToDo = ToDo.query.all()
    return "this page will show all the ToDo"

@app.route("/delete/<int:sno>")
def delete(sno):
    delToDo = ToDo.query.filter_by(sno=sno).first() #.first() is used to make sure to select the first query related to it
    db.session.delete(delToDo)
    db.session.commit()
    return redirect('/')
@app.route("/update/<int:sno>",methods = ["GET" , "POST"])
def update(sno):
    if request.method == "POST":
        name = request.form['name']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(sno=sno).first()
        todo.name = name
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        redirect('/')
    todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
        

if __name__ == "__main__":
    app.run( debug = True , port  = 8000)