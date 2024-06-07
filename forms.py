from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    task_name = StringField(label="New Task", validators=[DataRequired()])
    created_date = DateField(format='%d-%m-%Y', default=date.today())
    submit = SubmitField('Add')
