from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
db = SQLAlchemy(app)

# data class -> row of data
class MyTask(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer,default=0)
    created = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self) -> str:
        return f"Task {self.id}"

@app.route('/',methods=["POST","GET"])
def index():
    if request.method == "POST":
        curr = request.form['content']
        if curr.strip() != "":
            new_task = MyTask(content=curr)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except Exception as e:
                print("ERROR:{e}")
                return f"ERROR:{e}"
        all_tasks = MyTask.query.order_by(MyTask.created).all()   
        return render_template('index.html', tasks=all_tasks, error=True)
    else:
        all_tasks = MyTask.query.order_by(MyTask.created).all()   
        return render_template('index.html', tasks=all_tasks, error=False)
    
@app.route('/delete/<int:id>')
def delete(id):
    del_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(del_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"    

@app.route("/edit/<int:id>", methods=["POST","GET"])
def edit(id):    
    ed_task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        ed_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template('edit.html', task=ed_task) 

@app.route("/completed/<int:id>")
def complete(id):
    com_task = MyTask.query.get_or_404(id)
    if com_task.complete == 0:
        com_task.complete = 1     
    else:
        com_task.complete = 0
    try:
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"
        
    # return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)