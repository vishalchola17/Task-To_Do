from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from test import Password

app = Flask(__name__, template_folder='templates')

app.secret_key = "scjndjsandiidbdhdccddcc"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qazplm@localhost:5432/list_to_do'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
pw = Password()
class Users_t(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    #tasks = db.relationship('Task', backref='owner', lazy=True)

class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    task_text = db.Column(db.String(2000), nullable=False)
    done = db.Column(db.Integer, default=0, nullable=False)
    lastdate = db.Column(db.Date, nullable=False)
    #user = db.relationship('User_t', backref='tasks', lazy=True)

with app.app_context():
    db.create_all()





@app.route('/', methods=["POST", "GET"])
def login():
    if "email" in session:  # and username_exists(session["email"], user_d, session["password"]):
        user = Users_t.query.filter_by(email=session["email"]).first()
        return redirect(url_for("task", user_id = user.user_id))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        check_email = Users_t.query.filter_by(email=email).first()
        if check_email:
            pww = check_email.password
            if pw.check_password(password, pww):
                user_id = check_email.user_id
                session["email"] = email
                print("session")
                return redirect(url_for("task", user_id=user_id))
            flash("enter correct password")
            return render_template('login.html')
        flash("enter correct data or register")
    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if "email" in session:  # and username_exists(session["email"], user_d, session["password"]):
        user = Users_t.query.filter_by(email=session["email"]).first()
        return redirect(url_for("task", user_id=user.user_id))
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        check_existance = Users_t.query.filter_by(email=email).first()
        if not check_existance:
            Hash_password = pw.hash_password(plain_text_password=password)
            new_user = Users_t(name=name, email=email, password=Hash_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Done!")
            return redirect(url_for("login"))
        flash("email already exists!")
    return render_template('register.html')


@app.route('/task/<int:user_id>')
def task(user_id):
    if "email" not in session:
        return redirect(url_for("login"))
    user = Users_t.query.filter_by(user_id=user_id).first()
    user_name = user.name
    lists = Task.query.filter_by(user_id=user_id).order_by(Task.lastdate).all()
    all_li = [{"text": x.task_text, "task_id": x.task_id, "done":x.done, "date":x.lastdate} for x in lists]
    return render_template('task.html', all_li=all_li, user_id=user_id, user_name=user_name)


@app.route('/edit/<int:user_id>/<int:task_id>', methods=["POST", "GET"])
def edit(user_id, task_id):
    if "email" not in session:
        return redirect(url_for("login"))
    task = Task.query.get(task_id)
    old_text = task.task_text
    if request.method == "POST":
        text = request.form['text']
        task.task_text = text
        db.session.commit()
        return redirect(url_for('task', user_id=user_id))

    return render_template('edit.html', old_text=old_text)


@app.route('/delete/<int:user_id>/<int:task_id>', methods=["DELETE", "GET", "POST"])
def delete(task_id, user_id):
    if "email" not in session:
        return redirect(url_for("login"))
    if request.method == "GET":
        task = Task.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('task', user_id=user_id))


@app.route('/logout', methods=["POST", "GET"])
def logout():
    session.pop("email", None)
    session.clear()
    print("session out")
    return redirect(url_for("login"))


@app.route('/add/<int:user_id>', methods=["POST", "GET"])
def add(user_id):
    if "email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        get_text = request.form.get('task')
        get_date = request.form.get('date')
        new_task = Task(user_id=user_id, task_text=get_text, lastdate=get_date)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('task', user_id=user_id))

    return redirect(url_for("task", user_id=user_id))

@app.route('/dorw/<int:user_id>/<int:task_id>', methods=["GET", "POST"])
def dorw(user_id, task_id):
    if "email" not in session:
        return redirect(url_for("login"))

    present = Task.query.get(task_id)
    if present.done == 1:
        present.done = 0
    else:
        present.done =1
    db.session.commit()
    return redirect(url_for("task", user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)
