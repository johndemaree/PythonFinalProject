from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validoators import DataRequired, Length

class CardSetForm(StudyCards):
    title = StringField('Title', validators=[DataRequired(),Length(min=1, max=20)])
    description = StringField('Description')
    submit = SubmitField('Create New Card Set')

class CardEntryForm(StudyCards):
    keyword_one = StringField('Keyword 1', validators=[DataRequired(),Length(min=1, max=20)])
    keyword_two = StringField('Keyword 2', validators=[Length(min=1,max=20)])
    submit = SubmitField('Add Card')