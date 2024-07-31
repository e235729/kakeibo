from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('new_index.html')


@app.route('/new_income')#そのhtmlに飛ぶコード
def income(): #incomeに変更
    return render_template('new_income.html')

@app.route('/new_expense')#そのhtmlに飛ぶコード
def expense(): 
    return render_template('new_expense.html')

@app.route('/submit_registration', methods=['POST'])#フォームを出すコード
def submit_registration():
    # フォームからのデータを取得
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    return f"Registration Received: Username - {username}, Email - {email}"

if __name__ == '__main__':
    app.run(debug=True)