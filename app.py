from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finances.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    memo = db.Column(db.String(50), nullable=False)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    memo = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    total_income = db.session.query(db.func.sum(Income.amount)).scalar() or 0
    total_expense = db.session.query(db.func.sum(Expense.amount)).scalar() or 0

    # メッセージの生成
    if total_income > total_expense:  # 収入 > 支出のとき
        if total_income > total_expense * 2: 
            message = "やるやん？ちゃんと貯金してるのは素晴らしいけど、何か趣味や興味を持つのも大事だよ。"  # 収入 > 支出の2倍のとき (絶好調)
        else:
            message = "貯金できるって素晴らしいけど、もう少しリスクを取っても良いんじゃないですか？"  # 支出が収入の50%以上100%未満 (好調)
    elif total_income < total_expense:  # 収入 < 支出のとき
        if total_income * 2 < total_expense: 
            message = "なんで貯金できないのか明日までに考えておいてください。そしたら何かが見えてくるはずです。ほなまた明日。"  # 収入の2倍 < 支出のとき (絶不調)
        else:
            message = "たかが節約、そう思ってないですか？それやったら、明日も赤字になりますよ？"  # 収入 < 支出のとき (その他)
    else:  # 収入 == 支出のとき
        if total_income == 0 and total_expense == 0:
            message = "つまんない人生"  # 収入も支出もゼロのとき
        else:
            message = "経済を回してくれてあざーーーーす"  # 収入 == 支出 (その他)

    # すべての収入と支出を取得
    expenses = Expense.query.all()
    incomes = Income.query.all()

    return render_template(
        'new_index.html',
        total_income=total_income,
        total_expense=total_expense,
        message=message,
        expenses=expenses,
        incomes=incomes
    )


@app.route('/new_income', methods=['GET', 'POST'])
def income():
    if request.method == 'POST':
        date = request.form.get('date')
        amount = request.form.get('amount')
        memo = request.form.get('content')
        new_income = Income(date=date, amount=int(amount),memo = memo)
        db.session.add(new_income)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_income.html')

@app.route('/new_expense', methods=['GET', 'POST'])
def expense():
    if request.method == 'POST':
        date = request.form.get('date')
        amount = request.form.get('amount')
        memo = request.form.get('content')
        new_expense = Expense(date=date, amount=int(amount), memo = memo)
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_expense.html')

@app.route('/edit_expense/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    if request.method == 'POST':
        expense.date = request.form.get('date')
        expense.amount = request.form.get('amount')
        expense.memo = request.form.get('content')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_expense.html', expense=expense)

@app.route('/edit_income/<int:id>', methods=['GET', 'POST'])
def edit_income(id):
    income = Income.query.get_or_404(id)
    if request.method == 'POST':
        income.date = request.form.get('date')
        income.amount = request.form.get('amount')
        income.memo = request.form.get('content')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_income.html', income=income)

@app.route('/delete_expense/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_income/<int:id>', methods=['POST'])
def delete_income(id):
    income = Income.query.get_or_404(id)
    db.session.delete(income)
    db.session.commit()
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)
