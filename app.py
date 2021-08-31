from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
import os

project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir,"mydatabase.db"))

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=database_file
db=SQLAlchemy(app)

class Expense(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.String(50),nullable=False)
    expensename=db.Column(db.String(50),nullable=False)
    amount=db.Column(db.Integer(),nullable=False)
    category=db.Column(db.String(50),nullable=False)

@app.route('/')
def add():
    return render_template('add.html')


# delete

@app.route('/delete/<int:id>')
def delete(id):
    expense=Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect("/expenses")


# edit


@app.route('/edit/<int:id>')
def edit(id):
    expense=Expense.query.filter_by(id=id).first()
    return render_template('edit.html',expense=expense)


# update

@app.route('/update',methods=['POST'])
def update():
    id=request.form['id']
    date=request.form['date']
    category=request.form['category']
    expensename=request.form['expensename']
    amount=request.form['amount']

    expense=Expense.query.filter_by(id=id).first()
    expense.date=date
    expense.category=category
    expense.expensename=expensename
    expense.amount=amount

    db.session.commit()
    return redirect('/expenses')



# expenses page

@app.route('/expenses')
def expenses():
    expenses=Expense.query.all()
    total=0
    t_food=0
    t_business=0
    t_entertainment=0
    t_transportation=0
    t_other=0
    for expense in expenses:
        total+=expense.amount
        if expense.category=='business':
            t_business+=expense.amount
        elif expense.category=='food':
            t_food+=expense.amount
        elif expense.category=='transportation':
            t_transportation+=expense.amount
        elif expense.category=='entertainment':
            t_entertainment+=expense.amount
        elif expense.category=='other':
            t_other+=expense.amount
  
    return render_template('expenses.html',expenses=expenses,
    total=total,
    t_food=t_food,
    t_business=t_business,
    t_transportation=t_transportation,
    t_entertainment=t_entertainment,
    t_other=t_other)


# add expense post

@app.route('/addexpense',methods=['POST'])
def addexpense():
    date=request.form['date']
    category=request.form['category']
    expensename=request.form['expensename']
    amount=request.form['amount']
    expense=Expense(date=date,expensename=expensename,amount=amount,category=category)
    db.session.add(expense)
    db.session.commit()
    return redirect('/')

# add view

@app.route('/addview',methods=['GET','POST'])
def addview():
    if request.method=='GET':
        expenses=Expense.query.all()
        total=0
        t_food=0
        t_business=0
        t_entertainment=0
        t_transportation=0
        t_other=0
        for expense in expenses:
            total+=expense.amount
            if expense.category=='business':
                t_business+=expense.amount
            elif expense.category=='food':
                t_food+=expense.amount
            elif expense.category=='transportation':
                t_transportation+=expense.amount
            elif expense.category=='entertainment':
                t_entertainment+=expense.amount
            elif expense.category=='other':
                t_other+=expense.amount
    
    elif request.method=='POST':
        date=request.form['date']
        category=request.form['category']
        expensename=request.form['expensename']
        amount=request.form['amount']
        expense=Expense(date=date,expensename=expensename,amount=amount,category=category)
        db.session.add(expense)
        db.session.commit()
        return redirect('/addview')
        

    return render_template('addview.html',expenses=expenses,
    total=total,
    t_food=t_food,
    t_business=t_business,
    t_transportation=t_transportation,
    t_entertainment=t_entertainment,
    t_other=t_other)


if __name__ == '__main__':
    app.run(debug=True)