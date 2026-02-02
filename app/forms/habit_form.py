from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class HabitForm(FlaskForm):
    name = StringField(
        'Habit Name',
        validators=[DataRequired(message="Please enter a habit name"), Length(max=120)],
        render_kw={"placeholder": "Enter new habit"}  # UX-friendly placeholder
    )
    submit = SubmitField('Add Habit', render_kw={"class": "btn btn-primary"})

