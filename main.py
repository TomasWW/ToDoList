from datetime import date
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired

table_name = "tasks"
connexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="todolist"
)
cursor = connexion.cursor()
app = Flask(__name__)
app.config["SECRET_KEY"] = "Mi_clave_Ultra_Secreta"
Bootstrap(app)


class TaskForm(FlaskForm):
    task_name = StringField(label="New Task", validators=[DataRequired()])
    created_date = DateField(format='%d-%m-%Y', default=date.today())
    submit = SubmitField('Add')





@app.route('/', methods=["GET", "POST"])
def home():
    task_form = TaskForm()
    cursor.execute(f"SELECT * FROM {table_name}")
    results = cursor.fetchall()
    table_title = table_name

    if task_form.validate_on_submit():
        task_name = task_form.task_name.data

        created_date = task_form.created_date.data
        cursor.execute(f"INSERT INTO {table_name} (task_name, create_date) VALUES ('{task_name}', '{created_date}')")
        connexion.commit()
        return redirect(url_for('home'))

    return render_template('index.html', form=task_form, list=results,title=table_title.title())


@app.route('/complete_task', methods=["GET", "POST"])
def complete_task():
    task_id = request.args.get('id')
    today = date.today()
    formatted_date = today.strftime('%Y-%m-%d')
    cursor.execute(f"UPDATE {table_name} SET is_complete = True, complete_date = '{formatted_date}' WHERE task_id = {task_id}")
    connexion.commit()
    return redirect(url_for('home'))


@app.route('/delete_task', methods=["GET", "POST"])
def delete_task():
    task_id = request.args.get('id')
    cursor.execute(f"DELETE FROM {table_name} WHERE task_id = {task_id}")
    connexion.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=8080)
