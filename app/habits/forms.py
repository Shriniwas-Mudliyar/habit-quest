from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class HabitForm(FlaskForm):
    name = StringField("Habit Name", validators=[DataRequired()])
    submit = SubmitField("Create Habit")

class CompleteHabitForm(FlaskForm):
    submit = SubmitField("Complete")

class DeleteHabitForm(FlaskForm):
    submit = SubmitField("Delete")

