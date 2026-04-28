from flask import Flask, render_template, request, jsonify, session, redirect, url_for  # type: ignore
import sqlite3
import hashlib
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'quiz_platform_secret_2024'

DB_PATH = 'quiz.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Users table
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Categories table
    cur.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        icon TEXT DEFAULT '📚'
    )''')

    # Questions table
    cur.execute('''CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        difficulty TEXT DEFAULT 'medium',
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )''')

    # Results table
    cur.execute('''CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        total INTEGER NOT NULL,
        percentage REAL NOT NULL,
        time_taken INTEGER DEFAULT 0,
        taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )''')

    # Seed categories
    cur.execute("SELECT COUNT(*) FROM categories")
    if cur.fetchone()[0] == 0:
        categories = [
            (1, 'Python Dasturlash', '🐍'),
            (2, 'Matematika', '🔢'),
            (3, 'Tarix', '🏛️'),
            (4, 'Ingliz tili', '🌍'),
            (5, 'Kompyuter Fanlari', '💻'),
        ]
        cur.executemany("INSERT INTO categories (id, name, icon) VALUES (?,?,?)", categories)

    # Seed questions
    cur.execute("SELECT COUNT(*) FROM questions")
    if cur.fetchone()[0] == 0:
        questions = [
            # Python
            (1, "Python'da ro'yxat (list) yaratish uchun qaysi belgi ishlatiladi?", "{ }", "[ ]", "( )", "< >", "B", "easy"),
            (1, "Python'da funksiya e'lon qilish uchun qaysi kalit so'z ishlatiladi?", "function", "def", "func", "define", "B", "easy"),
            (1, "Python'da 'print' funksiyasi nima qiladi?", "Ma'lumot o'chiradi", "Ma'lumot saqlaydi", "Ekranga chiqaradi", "Fayldan o'qiydi", "C", "easy"),
            (1, "Python'da qaysi tip o'zgarmas (immutable)?", "list", "dict", "tuple", "set", "C", "medium"),
            (1, "len([1,2,3,4,5]) necha qaytaradi?", "4", "5", "6", "3", "B", "easy"),
            (1, "Python'da for loop qanday yoziladi?", "for i in range(5):", "for(i=0;i<5;i++)", "foreach i in 5:", "loop i to 5:", "A", "easy"),
            (1, "Python'da qaysi metod ro'yxatga element qo'shadi?", "add()", "insert()", "append()", "push()", "C", "easy"),
            (1, "Python'da 'None' nima?", "0 qiymati", "Bo'sh satr", "Qiymat yo'qligi", "False qiymati", "C", "medium"),

            # Matematika
            (2, "2^10 qancha?", "512", "1024", "2048", "256", "B", "medium"),
            (2, "Agar x^2 = 144 bo'lsa, x = ?", "11", "12", "13", "14", "B", "easy"),
            (2, "Pi (π) ning taxminiy qiymati?", "3.14159", "3.12345", "3.16789", "3.11111", "A", "easy"),
            (2, "100 ning 15% i qancha?", "10", "15", "20", "25", "B", "easy"),
            (2, "Uchburchak ichki burchaklari yig'indisi?", "90°", "180°", "270°", "360°", "B", "easy"),
            (2, "√256 = ?", "14", "15", "16", "17", "C", "easy"),
            (2, "Fibonacci ketma-ketligining 7-elementi? (1,1,2,3,5...)", "11", "12", "13", "8", "C", "hard"),
            (2, "log₂(64) = ?", "5", "6", "7", "8", "B", "medium"),

            # Tarix
            (3, "O'zbekiston mustaqilligini qachon qo'lga kiritdi?", "1990", "1991", "1992", "1993", "B", "easy"),
            (3, "Amir Temur qaysi yili tug'ilgan?", "1326", "1336", "1346", "1356", "B", "medium"),
            (3, "Birinchi jahon urushi qachon boshlangan?", "1912", "1913", "1914", "1915", "C", "easy"),
            (3, "Ikkinchi jahon urushi qachon tugagan?", "1943", "1944", "1945", "1946", "C", "easy"),
            (3, "Samarqand qaysi asrda Temuriylar poytaxti bo'lgan?", "XIII asr", "XIV asr", "XV asr", "XVI asr", "B", "medium"),
            (3, "Al-Xorazmiy qaysi soha olimi?", "Fizika", "Matematika", "Kimyo", "Biologiya", "B", "easy"),
            (3, "Buyuk Ipak yo'li qaysi shaharlarni bog'lagan?", "Rim-Hindiston", "Xitoy-Evropa", "Arab-Afrika", "Gretsiya-Xitoy", "B", "medium"),
            (3, "Ibn Sino qaysi soha mutafakkiri?", "Matematika", "Astronomiya", "Tibbiyot", "Kimyo", "C", "easy"),

            # Ingliz tili
            (4, "'Beautiful' so'zining ma'nosi?", "Kuchli", "Chiroyli", "Aqlli", "Tez", "B", "easy"),
            (4, "Qaysi so'z fe'l (verb)?", "Happy", "Quickly", "Run", "Beautiful", "C", "easy"),
            (4, "'I ___ to school every day' bo'shliqni to'ldiring", "goes", "go", "gone", "going", "B", "easy"),
            (4, "'Yesterday I ___ a book' bo'shliqni to'ldiring", "read", "reads", "reading", "readed", "A", "medium"),
            (4, "Qaysi jumla to'g'ri?", "She don't like it", "She doesn't likes it", "She doesn't like it", "She not like it", "C", "easy"),
            (4, "'Vocabulary' so'zining ma'nosi?", "Grammatika", "Talaffuz", "So'z boyligi", "Yozuv", "C", "easy"),
            (4, "Qaysi so'z antonim: 'ancient'?", "Old", "Historic", "Modern", "Traditional", "C", "medium"),
            (4, "Past Perfect Tense qanday yasaladi?", "had + V3", "have + V3", "has + V3", "did + V3", "A", "medium"),

            # CS
            (5, "HTML ning to'liq nomi?", "Hyper Text Markup Language", "High Text Machine Language", "Hyper Text Making Links", "High Tech Modern Language", "A", "easy"),
            (5, "CPU nima?", "Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Core Processing Unit", "A", "easy"),
            (5, "RAM nimani anglatadi?", "Read Access Memory", "Random Access Memory", "Run All Memory", "Real Access Module", "B", "easy"),
            (5, "Ikkilik sanoq sistemasida 1010 o'nlik sanoqda?", "8", "9", "10", "11", "C", "medium"),
            (5, "HTTP qanday protokol?", "Email protokoli", "Web protokoli", "FTP protokoli", "SSH protokoli", "B", "easy"),
            (5, "SQL qanday til?", "Dasturlash tili", "Ma'lumotlar bazasi tili", "Markup tili", "Skript tili", "B", "easy"),
            (5, "OOP'da 'encapsulation' nima?", "Meros olish", "Ma'lumotni yashirish", "Ko'p shakllilik", "Abstraksiya", "B", "medium"),
            (5, "Git 'commit' buyrug'i nima qiladi?", "Faylni o'chiradi", "O'zgarishlarni saqlaydi", "Repozitoriyni klonlaydi", "Yangi branch yaratadi", "B", "easy"),
        ]
        cur.executemany("""INSERT INTO questions 
            (category_id, question, option_a, option_b, option_c, option_d, correct_answer, difficulty)
            VALUES (?,?,?,?,?,?,?,?)""", questions)

    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ─── AUTH ROUTES ───────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')
    email = data.get('email', '').strip()

    if not username or not password:
        return jsonify({'error': 'Username va parol majburiy'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Parol kamida 6 ta belgi bo\'lishi kerak'}), 400

    conn = get_db()
    try:
        conn.execute("INSERT INTO users (username, password, email) VALUES (?,?,?)",
                     (username, hash_password(password), email))
        conn.commit()
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({'success': True, 'username': username})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Bu username band'}), 400
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '')
    password = data.get('password', '')

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username=? AND password=?",
                        (username, hash_password(password))).fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({'success': True, 'username': username})
    return jsonify({'error': 'Username yoki parol noto\'g\'ri'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

# ─── DASHBOARD ──────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/api/dashboard-data')
def dashboard_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    conn = get_db()

    categories = conn.execute("SELECT * FROM categories").fetchall()

    results = conn.execute("""
        SELECT r.*, c.name as category_name, c.icon
        FROM results r JOIN categories c ON r.category_id = c.id
        WHERE r.user_id = ?
        ORDER BY r.taken_at DESC LIMIT 10
    """, (user_id,)).fetchall()

    stats = conn.execute("""
        SELECT COUNT(*) as total_tests,
               AVG(percentage) as avg_score,
               MAX(percentage) as best_score,
               SUM(score) as total_correct
        FROM results WHERE user_id = ?
    """, (user_id,)).fetchone()

    conn.close()

    return jsonify({
        'username': session['username'],
        'categories': [dict(c) for c in categories],
        'results': [dict(r) for r in results],
        'stats': dict(stats) if stats else {}
    })

# ─── QUIZ ROUTES ────────────────────────────────────────────────
@app.route('/quiz/<int:category_id>')
def quiz(category_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('quiz.html')

@app.route('/api/questions/<int:category_id>')
def get_questions(category_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    category = conn.execute("SELECT * FROM categories WHERE id=?", (category_id,)).fetchone()
    questions = conn.execute("""
        SELECT id, question, option_a, option_b, option_c, option_d, difficulty
        FROM questions WHERE category_id=?
        ORDER BY RANDOM() LIMIT 8
    """, (category_id,)).fetchall()
    conn.close()

    if not category:
        return jsonify({'error': 'Kategoriya topilmadi'}), 404

    return jsonify({
        'category': dict(category),
        'questions': [dict(q) for q in questions]
    })

@app.route('/api/submit', methods=['POST'])
def submit_quiz():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json(silent=True) or {}
    category_id = data.get('category_id')
    answers = data.get('answers', {})
    time_taken = data.get('time_taken', 0)

    conn = get_db()
    score: int = 0
    total: int = len(answers)
    feedback = []

    for q_id, user_ans in answers.items():
        q = conn.execute("SELECT * FROM questions WHERE id=?", (int(q_id),)).fetchone()
        if q:
            is_correct = user_ans.upper() == q['correct_answer'].upper()
            if is_correct:
                score += 1  # type: ignore
            feedback.append({
                'question': q['question'],
                'user_answer': user_ans,
                'correct_answer': q['correct_answer'],
                'is_correct': is_correct,
                'options': {
                    'A': q['option_a'], 'B': q['option_b'],
                    'C': q['option_c'], 'D': q['option_d']
                }
            })

    percentage = round(float(score) / total * 100, 1) if total > 0 else 0.0  # type: ignore

    conn.execute("""INSERT INTO results (user_id, category_id, score, total, percentage, time_taken)
                    VALUES (?,?,?,?,?,?)""",
                 (session['user_id'], category_id, score, total, percentage, time_taken))
    conn.commit()
    conn.close()

    return jsonify({
        'score': score,
        'total': total,
        'percentage': percentage,
        'feedback': feedback
    })

# ─── PROFILE ────────────────────────────────────────────────────
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('profile.html')

@app.route('/api/profile')
def get_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    conn = get_db()

    user = conn.execute("SELECT id, username, email, created_at FROM users WHERE id=?", (user_id,)).fetchone()

    results = conn.execute("""
        SELECT r.*, c.name as category_name, c.icon
        FROM results r JOIN categories c ON r.category_id = c.id
        WHERE r.user_id = ? ORDER BY r.taken_at DESC
    """, (user_id,)).fetchall()

    category_stats = conn.execute("""
        SELECT c.name, c.icon, COUNT(*) as attempts,
               AVG(r.percentage) as avg_score, MAX(r.percentage) as best_score
        FROM results r JOIN categories c ON r.category_id = c.id
        WHERE r.user_id = ? GROUP BY r.category_id
    """, (user_id,)).fetchall()

    conn.close()

    return jsonify({
        'user': dict(user),
        'results': [dict(r) for r in results],
        'category_stats': [dict(s) for s in category_stats]
    })

try:
    from pyngrok import ngrok
except ImportError:
    ngrok = None  # pyngrok not installed; ngrok tunnel will be disabled

if __name__ == '__main__':
    init_db()
    print("[OK] Ma'lumotlar bazasi tayyor!")
    # ----- ngrok tunnel -----
    if os.getenv('NGROK_TUNNEL') and ngrok:
        public_url = ngrok.connect(5000, "http")
        print(f"[NGROK] Public URL: {public_url}")
    print("[START] Server ishga tushdi: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', debug=True, port=5000)

# If you want the app to be reachable from outside your local network (e.g., from a different Wi‑Fi or mobile data), you can start an ngrok tunnel.
# Set the environment variable NGROK_TUNNEL=1 before running the server, or simply uncomment the block below.
# Remember to configure your ngrok auth token (ngrok authtoken <your-token>) once.

if __name__ == '__main__':
    init_db()
    print("[OK] Ma'lumotlar bazasi tayyor!")
    # ----- ngrok tunnel -----
    if os.getenv('NGROK_TUNNEL'):
        public_url = ngrok.connect(5000, "http")
        print(f"[NGROK] Public URL: {public_url}")
    print("[START] Server ishga tushdi: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', debug=True, port=5000)
