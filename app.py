from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# --- Veritabanı ayarları ---
# Yerelde SQLite, bulutta PostgreSQL
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///tasks.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- Model ---
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="yeni")  # yeni, onay_bekliyor, tamamlandi
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- Rotalar ---
@app.route("/")
def index():
    yeni = Task.query.filter_by(status="yeni").all()
    onay = Task.query.filter_by(status="onay_bekliyor").all()
    tamam = Task.query.filter_by(status="tamamlandi").all()
    return render_template("index.html", yeni=yeni, onay=onay, tamam=tamam)

@app.route("/ekle", methods=["POST"])
def ekle():
    title = request.form.get("title")
    if title:
        yeni_is = Task(title=title)
        db.session.add(yeni_is)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/guncelle/<int:task_id>/<string:status>")
def guncelle(task_id, status):
    task = Task.query.get_or_404(task_id)
    task.status = status
    db.session.commit()
    return redirect(url_for("index"))

# Veritabanı oluşturmak için komut
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Veritabanı oluşturuldu!")

if __name__ == "__main__":
    app.run(debug=True)

from flask import jsonify, request

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "status": t.status} for t in tasks])

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    new_task = Task(title=data["title"], status="yeni")
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added"}), 201

@app.route("/api/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()
    task = Task.query.get(id)
    if task:
        task.status = data.get("status", task.status)
        db.session.commit()
        return jsonify({"message": "Task updated"})
    return jsonify({"message": "Task not found"}), 404

from flask_cors import CORS

app = Flask(__name__)
CORS(app)



