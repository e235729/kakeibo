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

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    total_income = db.session.query(db.func.sum(Income.amount)).scalar() or 0
    total_expense = db.session.query(db.func.sum(Expense.amount)).scalar() or 0

    # メッセージの生成
    if total_income > total_expense: #収入>支出のとき
        if  total_income >total_expense*2 : 
            message = "絶好調"#　収入　>　支出の２倍　のとき(絶好調)
        message = "好調"#支出が収入の50%以上100%未満(好調)
    elif total_income < total_expense:#収入<支出のとき
        if total_income < total_expense:#収入の２倍<支出のとき(絶不調)
            if total_income*2 < total_expense:
                message = "絶不調"
            message ="不調"
    else:
        if total_income==0 and total_expense==0:
            message="E"
        message = "F"

    return render_template('new_index.html', total_income=total_income, total_expense=total_expense, message=message)

@app.route('/new_income', methods=['GET', 'POST'])
def income():
    if request.method == 'POST':
        date = request.form.get('date')
        amount = request.form.get('amount')
        new_income = Income(date=date, amount=int(amount))
        db.session.add(new_income)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_income.html')

@app.route('/new_expense', methods=['GET', 'POST'])
def expense():
    if request.method == 'POST':
        date = request.form.get('date')
        amount = request.form.get('amount')
        new_expense = Expense(date=date, amount=int(amount))
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_expense.html')

if __name__ == '__main__':
    app.run(debug=True)
