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
    return render_template('new_index.html', total_income=total_income, total_expense=total_expense)

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
