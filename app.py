from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # React'ten erişim için
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="onay_bekliyor")  # onay_bekliyor, devam, tamamlandı

db.create_all()

# Tüm görevleri al
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "status": t.status} for t in tasks])

# Yeni görev ekle
@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.json
    task = Task(title=data["title"], status=data.get("status", "onay_bekliyor"))
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "status": task.status})

# Görev güncelle
@app.route("/api/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.json
    task.status = data.get("status", task.status)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "status": task.status})

# Görev sil
@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    app.run(debug=True)
