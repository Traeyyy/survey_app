import os
import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/survey")
def survey():
    return render_template("survey.html")

@app.route("/submit", methods=["POST"])
def submit():
    score = 0
    
    answers = []
    for i in range(1, 6):
        answer = int(request.form.get(f"q{i}", 0))
        answers.append(answer)
        score += answer

    # 存数据
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "data.db")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            q1 INTEGER, q2 INTEGER, q3 INTEGER, q4 INTEGER, q5 INTEGER,
            score INTEGER
        )
    """)

    c.execute(
        "INSERT INTO responses (q1,q2,q3,q4,q5,score) VALUES (?,?,?,?,?,?)",
        (*answers, score)
    )

    conn.commit()
    conn.close()

    return render_template("result.html", score=score)

@app.route("/admin")
def admin():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "data.db")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT * FROM responses")
    data = c.fetchall()

    # 👉 在这里加（重点）
    scores = [row[-1] for row in data]
    avg_score = sum(scores) / len(scores) if scores else 0

# 👉 统计分数出现次数（做柱状图用）
    score_counts = {}
    for s in scores:
        score_counts[s] = score_counts.get(s, 0) + 1

    conn.close()

    return render_template(
    "admin.html",
    data=data,
    avg=avg_score,
    score_counts=score_counts
)
   

if __name__ == "__main__":
    app.run(debug=True, port=5001)