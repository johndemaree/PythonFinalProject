"""The forms module is used to dynamically create html forms using python classes.
The flask_wtf and wtforms dependencies are the main libraries for this operation"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField,TextAreaField,SelectField,BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from studycards.models import CardSet


class CardSetForm(FlaskForm):
    """This form is used to create a new Cardset."""
    title = StringField('Title', validators=[DataRequired(),Length(min=2, max=20)])
    description = TextAreaField('Description', validators=[Length(min=1, max=100)])
    submit = SubmitField('Create New Card Set')
    savedit = SubmitField('Save Edits')
    def validate_title(self, title):
        card = CardSet.query.filter_by(title=title.data).first()
        if card:
            raise ValidationError('A Cardset by this name already exists. Please choose a different title.')


class CardEntryForm(FlaskForm):
    """This form is used to enter data into a new card."""
    keyword_one = StringField('Keyword 1', validators=[DataRequired(), Length(min=1, max=20)])
    keyword_two = StringField('Keyword 2', validators=[Length(min=1, max=20)])
    text_one = TextAreaField('Definition', validators=[Length(min=1, max=100)])
    image_one = FileField('Add/Update Photo', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Add Another Card')
    finish = SubmitField('Finish')
    delete = BooleanField('Delete') #used as hidden indicator delete button was used

class SelectCardSet(FlaskForm):
    """This form is used to select an active Card Set before any Card activity.
    The list of Card Sets is obtained dynamically in the select_list variable"""
    selected_cardset = SelectField('Select a Cardset',choices = [])

    def update (self):
        """update method reloads the choices to include any new or updated
        cardsets"""
        sets_of_cards = CardSet.query.all()
        select_list = [(str(i.id),i.title) for i in sets_of_cards]
        self.selected_cardset.choices=select_list
        return
    submit = SubmitField('Select Cardset')
    edit = SubmitField('Edit Cardset')

class FlashCardSelection (FlaskForm):
    """This form is used to select which items will appear on the front and back
    of the flash cards. """
    front_key_1 = BooleanField('Key 1')
    front_key_2 = BooleanField('Key 2')
    front_text_1 = BooleanField('Text')
    front_image_1 = BooleanField('Image')
    back_key_1 = BooleanField('Key 1')
    back_key_2 = BooleanField('Key 2')
    back_text_1 = BooleanField('Text')
    back_image_1 = BooleanField('Image')
    submit = SubmitField('Submit')