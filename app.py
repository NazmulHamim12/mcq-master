from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, db
import random
import os
import json

# ✅ Firebase setup (Local and Render—দু জায়গাতেই কাজ করবে)
if not firebase_admin._apps:
    try:
        firebase_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
        if firebase_json:
            cred_dict = json.loads(firebase_json)
            cred = credentials.Certificate(cred_dict)
        else:
            with open("new.json") as f:
                cred = credentials.Certificate(json.load(f))

        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://lenden-37532-default-rtdb.firebaseio.com/'
        })

    except Exception as e:
        print("Firebase init error:", e)

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # Session এর জন্য এটা অবশ্যই লাগবে

# Home/Register route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code_ref = db.reference("code")
        data = code_ref.get()

        x = data["val"]
        val = x + 1
        code_ref.update({"val": val})

        user_name = request.form['name']
        user_number = request.form['phone']
        user_class = request.form['clas']
        user_aca = request.form['academi']
        user_pass = request.form['pass']

        user_ref = db.reference(f'mcq app/users/{user_name.lower()}')
        user_ref.update({
            'name': user_name.lower(),
            'class': user_class,
            'academi': user_aca,
            'email': user_number,
            'password': user_pass,
            'id': val,
            'point': 0
        })
    return render_template('index.html')

# Login route
@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        user_name = request.form['name']
        user_pass = request.form['pass']

        ref = db.reference(f'mcq app/users/{user_name.lower()}')
        data = ref.get()

        if data and data['name'] == user_name.lower() and data['password'] == user_pass:
            # Save to session
            session['name'] = data['name']
            session['id'] = data['id']
            session['points'] = data['point']
            return redirect("/dash")
    return render_template('login.html')

# Dashboard route
@app.route('/dash')
def user():
    user_name = session.get('name')
    user_numb = session.get('id')
    ref = db.reference(f'mcq app/users/{user_name}')
    data = ref.get()
    user_pas = data['point']

    if not user_name:
        return redirect('/log')  # Session নাই, redirect back
    
    ref = db.reference('mcq app/users')
    data = ref.get()

    if data:
        players = list(data.values())
        sorted_players = sorted(players, key=lambda x: x["point"], reverse=True)
        top_5 = sorted_players[:1]
    else:
        top_5 = []


    return render_template('dash.html', name=user_name.upper(), numb=user_numb, passw=user_pas,x=top_5)

# Exam route (Math)
@app.route('/matrix', methods=['GET', 'POST'])
def matrix():
    ref = db.reference('quiz/math-1st/chapter-1')
    data = ref.get()

    all_qu = []
    all_c = []
    all_index = []

    i = 1
    while i < len(data):
        ref_2 = db.reference(f'quiz/math-1st/chapter-1/{i}')
        d = ref_2.get()
        question = d['question']
        correct = d['correct']
        all_qu.append(question)
        all_c.append(correct)
        all_index.append(i)
        i += 1

    main_qu = []
    main_c = []
    main_idx = []

    while True:
        ran = random.randrange(0, len(all_qu))
        main_qu.append(all_qu[ran])
        main_c.append(all_c[ran])
        main_idx.append(all_index[ran])
        all_qu.pop(ran)
        all_c.pop(ran)
        all_index.pop(ran)
        if len(main_qu) == 20:
            break

    session['correct_answers'] = main_c

    op = {}
    for j in range(20):
        q_index = main_idx[j]
        question_ref = db.reference(f'quiz/math-1st/chapter-1/{q_index}')
        data = question_ref.get()
        op[j + 1] = data['options']

    return render_template("matrix.html", op=op, question=main_qu)

# Exam route (Physics)
@app.route('/vector', methods=['GET', 'POST'])
def vector():
    ref = db.reference('quiz/physics-1st/chapter-2')
    data = ref.get()

    all_qu = []
    all_c = []
    all_index = []

    i = 1
    while i < len(data):
        ref_2 = db.reference(f'quiz/physics-1st/chapter-2/{i}')
        d = ref_2.get()
        question = d['question']
        correct = d['correct']
        all_qu.append(question)
        all_c.append(correct)
        all_index.append(i)
        i += 1

    main_qu = []
    main_c = []
    main_idx = []

    while True:
        ran = random.randrange(0, len(all_qu))
        main_qu.append(all_qu[ran])
        main_c.append(all_c[ran])
        main_idx.append(all_index[ran])
        all_qu.pop(ran)
        all_c.pop(ran)
        all_index.pop(ran)
        if len(main_qu) == 20:
            break

    session['correct_answers'] = main_c

    op = {}
    for j in range(20):
        q_index = main_idx[j]
        question_ref = db.reference(f'quiz/physics-1st/chapter-2/{q_index}')
        data = question_ref.get()
        op[j + 1] = data['options']

    return render_template("vector.html", op=op, question=main_qu)





#ICT

@app.route('/cprog', methods=['GET', 'POST'])
def cprog():
    ref = db.reference('quiz/ict/chapter-5')
    data = ref.get()

    all_qu = []
    all_c = []
    all_index = []

    i = 1
    while i < len(data):
        ref_2 = db.reference(f'quiz/ict/chapter-5/{i}')
        d = ref_2.get()
        question = d['question']
        correct = d['correct']
        all_qu.append(question)
        all_c.append(correct)
        all_index.append(i)
        i += 1

    main_qu = []
    main_c = []
    main_idx = []

    while True:
        ran = random.randrange(0, len(all_qu))
        main_qu.append(all_qu[ran])
        main_c.append(all_c[ran])
        main_idx.append(all_index[ran])
        all_qu.pop(ran)
        all_c.pop(ran)
        all_index.pop(ran)
        if len(main_qu) == 20:
            break

    session['correct_answers'] = main_c

    op = {}
    for j in range(20):
        q_index = main_idx[j]
        question_ref = db.reference(f'quiz/ict/chapter-5/{q_index}')
        data = question_ref.get()
        op[j + 1] = data['options']

    return render_template("cprog.html", op=op, question=main_qu)







@app.route('/medi', methods=['GET', 'POST'])
def medi():
    ref = db.reference('quiz/biochem/medical')
    data = ref.get()

    all_qu = []
    all_c = []
    all_index = []

    i = 1
    while i < len(data):
        ref_2 = db.reference(f'quiz/biochem/medical/{i}')
        d = ref_2.get()
        question = d['question']
        correct = d['correct']
        all_qu.append(question)
        all_c.append(correct)
        all_index.append(i)
        i += 1

    main_qu = []
    main_c = []
    main_idx = []

    while True:
        ran = random.randrange(0, len(all_qu))
        main_qu.append(all_qu[ran])
        main_c.append(all_c[ran])
        main_idx.append(all_index[ran])
        all_qu.pop(ran)
        all_c.pop(ran)
        all_index.pop(ran)
        if len(main_qu) == 20:
            break

    session['correct_answers'] = main_c

    op = {}
    for j in range(20):
        q_index = main_idx[j]
        question_ref = db.reference(f'quiz/biochem/medical/{q_index}')
        data = question_ref.get()
        op[j + 1] = data['options']

    return render_template("medi.html", op=op, question=main_qu)










@app.route('/lead')
def leaderboard():
    ref = db.reference('mcq app/users')
    data = ref.get()

    if data:
        players = list(data.values())
        sorted_players = sorted(players, key=lambda x: x["point"], reverse=True)
        top_5 = sorted_players[:5]
    else:
        top_5 = []

    return render_template('leader.html', players=top_5)











# Submit route
@app.route('/submit', methods=['POST'])
def submit():
    name = session.get('name')
    ref = db.reference(f'mcq app/users/{name}')
    data = ref.get()
    points = data['point']
    correct = session.get('correct_answers', [])
    user_ans = []
    wrong_info = []

    score = 0
    for i in range(1, 21):
        user_input = request.form.get(f'q{i}')
        user_ans.append(user_input)

        if user_input == correct[i - 1]:
            score += 1
        else:
            wrong_info.append({
                'q_no': i,
                'user_ans': user_input,
                'correct_ans': correct[i - 1]
            })

    points += score
    ref.update({'point': points})

    return render_template('result.html', score=score, total=20, wrong_info=wrong_info)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
