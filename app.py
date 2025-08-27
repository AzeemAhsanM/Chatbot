from flask import Flask, render_template, request, jsonify, send_file
import io
from datetime import datetime

app = Flask(__name__)


QUESTIONS = [
    {"id": "name", "text": "What's your name?"},
    {"id": "role", "text": "What is your current role?"},
    {"id": "skills", "text": "Awesome! What skills are you most confident in?"},
    {"id": "type", "text": "How do you like to work?"},
    {"id": "exp", "text": "How many years of experience do you have?"},
    {"id": "contact", "text": "please enter your email id?"},
]

user_data = {}
current_index = 0


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get_question", methods=["GET"])
def get_question():
    global current_index
    if current_index < len(QUESTIONS):
        if QUESTIONS[current_index]["id"] =="role" and "name" in user_data:
            QUESTIONS[current_index]["text"] = f"Hi {user_data['name']}, " + QUESTIONS[current_index]["text"]
        return jsonify({
            "done": False,
            "question": QUESTIONS[current_index]["text"],
            "id": QUESTIONS[current_index]["id"]
        })
    else:
        return jsonify({"done": True})


@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    global current_index, user_data
    data = request.get_json()
    qid = data.get("id")
    answer = data.get("answer","").strip()


    if qid == "name" and not answer.isalpha():
        return jsonify({"success": False, "error": "Name should only contain letters."})
    if qid == "role" and not answer.isalpha():
        return jsonify({"success": False, "error": "should only contain letters."})
    if qid == "exp":
        if not answer.isdigit():
            return jsonify({"success": False, "error": "Experience must be a number."})

    if qid == "contact" and "@" not in answer:
        return jsonify({"success": False, "error": "Please provide a valid email address."})
    if qid:
        user_data[qid] = answer
        current_index += 1
    return jsonify({"success": True})


@app.route("/download_report")
def download_report():
    global user_data
    # Create report text
    report = f"User Profile Report\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    for q in QUESTIONS:
        answer = user_data.get(q["id"], "Not answered")
        report += f"{q['text']}\nAnswer: {answer}\n\n"

    # Return as downloadable text file
    buffer = io.BytesIO()
    buffer.write(report.encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="chatbot_profile.txt",
        mimetype="text/plain"
    )


@app.route("/reset", methods=["POST"])
def reset():
    global user_data, current_index
    user_data = {}
    current_index = 0
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
