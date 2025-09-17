from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task modeli
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="yeni")  # yeni, onay, tamamlandı

# Ana sayfa
@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

# Yeni görev ekleme
@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    if title:
        task = Task(title=title)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for("index"))

# Görev durumu güncelleme
@app.route("/update/<int:id>", methods=["POST"])
def update_task(id):
    task = Task.query.get_or_404(id)
    status = request.form.get("status")
    if status:
        task.status = status
        db.session.commit()
    return redirect(url_for("index"))

# Görev silme
@app.route("/delete/<int:id>", methods=["POST"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
