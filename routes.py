from datetime import date

from flask import redirect, url_for, render_template, request, Blueprint


from db_connexion import table_name, connexion, cursor
from forms import TaskForm

simple_page = Blueprint('simple_page', __name__)


@simple_page.route('/', methods=["GET", "POST"])
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
        return redirect(url_for('simple_page.home'))

    return render_template('index.html', form=task_form, list=results, title=table_title.title())


@simple_page.route('/complete_task', methods=["GET", "POST"])
def complete_task():
    task_id = request.args.get('id')
    today = date.today()
    formatted_date = today.strftime('%Y-%m-%d')
    cursor.execute(
        f"UPDATE {table_name} SET is_complete = True, complete_date = '{formatted_date}' WHERE task_id = {task_id}")
    connexion.commit()
    return redirect(url_for('simple_page.home'))


@simple_page.route('/delete_task', methods=["GET", "POST"])
def delete_task():
    task_id = request.args.get('id')
    cursor.execute(f"DELETE FROM {table_name} WHERE task_id = {task_id}")
    connexion.commit()
    return redirect(url_for('simple_page.home'))
