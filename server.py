from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_cors import CORS
from modules import user_manager
from modules import math_helper
from modules import gk_helper
from modules.nlp_manager import NLPManager
from modules import pdf_helper
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Enable CORS
CORS(app)

# Create tables if not exists
user_manager.create_tables()

# ===== INIT NLP MANAGER =====
nlp_manager = NLPManager()  # Loads tokenized dataset & model

# ===== UPLOAD CONFIG =====
BASE_UPLOAD_FOLDER = "uploads"
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = BASE_UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ===== ROUTES =====
@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_email = request.form['username_email']
        password = request.form['password']
        success, message, user_data = user_manager.login_user(username_email, password)
        if success:
            session['user_id'] = user_data['id']
            session['username'] = user_data['username']
            session['email'] = user_data['email']
            return jsonify({"success": True, "message": message})
        return jsonify({"success": False, "message": message})
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        success, message, user_data = user_manager.signup_user(username, email, password)
        if success:
            session['user_id'] = user_data['id']
            session['username'] = user_data['username']
            session['email'] = user_data['email']
            return jsonify({"success": True, "message": message})
        return jsonify({"success": False, "message": message})
    return render_template('signup.html')

@app.route('/chatmate')
def chatmate():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('chatmate.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/login_history')
def login_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    records = user_manager.get_login_history()
    return render_template('login_history.html', records=records)

# ===== CHATMATE API =====
@app.route('/ask', methods=['POST'])
def ask():
    if 'user_id' not in session:
        return jsonify({"success": False, "reply": "Please login first."})

    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"success": False, "reply": "Please enter a question."})

    try:
        predicted_label, confidence = nlp_manager.predict(user_message)

        if predicted_label is None:
            return jsonify({"success": True, "reply": "Sorry, I cannot answer that right now."})

        reply_text = ""
        if predicted_label == "math":
            conv_result = math_helper.handle_conversion(user_message)
            if conv_result.get("handled"):
                reply_text = conv_result["reply"]
            else:
                math_result = math_helper.handle_math_query(user_message)
                reply_text = math_result["reply"] if math_result.get("handled") else "I cannot solve this math problem."
        elif predicted_label == "gk":
            gk_result = gk_helper.handle_gk_query(user_message)
            reply_text = gk_result["reply"] if gk_result.get("handled") else "I cannot answer this GK question."
        elif predicted_label == "pdf":
            reply_text = "Please upload a PDF file to process this query."
        else:
            reply_text = nlp_manager.get_response(predicted_label)

        return jsonify({
            "success": True,
            "reply": f"{reply_text} (Confidence: {confidence:.2f})"
        })

    except Exception as e:
        return jsonify({"success": False, "reply": f"Error processing your query: {e}"})

# ===== PDF UPLOAD & PROCESS =====
@app.route('/ask_pdf', methods=['POST'])
def ask_pdf():
    if 'user_id' not in session:
        return jsonify({"success": False, "reply": "Please login first."})

    user_message = request.form.get("message", "").strip()
    pdf_file = request.files.get("pdf_file", None)
    pdf_path = None

    if pdf_file:
        if allowed_file(pdf_file.filename):
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(session['user_id']))
            os.makedirs(user_folder, exist_ok=True)
            filename = secure_filename(pdf_file.filename)
            pdf_path = os.path.join(user_folder, filename)
            pdf_file.save(pdf_path)
        else:
            return jsonify({"success": False, "reply": "Only PDF files are allowed."})

    try:
        pdf_result = pdf_helper.handle_pdf_query(user_message, pdf_path)
        reply_text = pdf_result["reply"] if pdf_result.get("handled") else "Cannot process this PDF request."
        return jsonify({"success": True, "reply": reply_text})
    except Exception as e:
        return jsonify({"success": False, "reply": f"Error processing PDF query: {e}"})

if __name__ == '__main__':
    print("🚀 Starting ChatMate server on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
