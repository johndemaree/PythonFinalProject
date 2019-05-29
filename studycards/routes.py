"""The routes module is used to retrieve links from the broser.
In the current format the routes below assume start after the heading localhost:5000"""

from flask import render_template, flash, redirect, url_for
from studycards import app, db, session
from studycards.forms import CardSetForm, CardEntryForm, SelectCardSet, FlashCardSelection
from studycards.models import CardSet, Card
"""External imports outside of studycards and flask """
from PIL import Image
import random  # used to shuffle cards for flash
import secrets # used to add hex characters as image_one file names
import os #used to seperate image file name from extension


"""#################################################
      CARDSET MENU/CREATION/MAINTENANCE ROUTES
   #################################################"""

@app.route('/',methods=['GET','POST'])
def home():
    """This route displays the Cardset selection form so user can select a cardset"""
    form = SelectCardSet()

    """run update method to load new or updated cardsets"""
    form.update()
    if form.validate_on_submit():

        """set session variable with selected cardset id"""
        selected_cardset = CardSet.query.get(form.selected_cardset.data)
        session['cardset_id'] = selected_cardset.id

        if form.edit.data:
            return redirect (url_for('editcardset'))
        return redirect(url_for('cardmenu'))

    """if there are no cardsets then the link returns to home,
    until a cardset is created"""
    session['cardset_id']=""
    return render_template('home.html', title="Create or Select A Card Set ", form=form)


@app.route('/cardset', methods=['GET','POST'])
def cardset():
    """This route is used to add a new Card Set to the database"""
    form = CardSetForm()
    if form.validate_on_submit():
        newcardset = CardSet(title=form.title.data, description=form.description.data)
        db.session.add(newcardset)
        db.session.commit()
        flash(f'Card Set {form.title.data} has been created!', 'success')
        return redirect (url_for('home'))
    return render_template('cardset.html', title="Card Set text_one", form=form)


@app.route('/editcardset', methods=['GET','POST'])
def editcardset():
    """THis route is used to edit the title and description for a Card Set"""
    form =CardSetForm()
    selected_cardset = CardSet.query.get(session['cardset_id'])

    if form.validate_on_submit():

        """If the form is valid it is saved to the database"""
        selected_cardset.title = form.title.data
        selected_cardset.description = form.description.data
        selected_cardset.id = session['cardset_id']

        """Write data to database"""
        db.session.add(selected_cardset)
        db.session.commit()
        return redirect(url_for('cardmenu'))

    form.title.data = selected_cardset.title
    form.description.data = selected_cardset.description
    return render_template('editcardset.html', title="Edit Card Set", form=form)


@app.route('/about')
def about():
    """This route displays the About (help) page"""
    return render_template('about.html', title="About")


"""#################################################
          CARD MENU/CREATION/MAINTENANCE ROUTES
   #################################################"""

def save_image (image_one_form):
    """This function saves the uploaded picture so the database can find it.
    This is used by newcard and editcard routes"""
    random_hex = secrets.token_hex(10)
    _, file_ext = os.path.splitext(image_one_form.filename)
    """create random hex file name in case user uploads two files with same name"""
    image_filename = random_hex + file_ext
    image_path = os.path.join(app.root_path, "static/images", image_filename)
    """Use the Pillow library  PIL import to resize the image"""
    output_size = (300,300)
    image = Image.open(image_one_form)
    image.thumbnail(output_size)
    image.save(image_path)
    return image_filename


@app.route('/cardmenu',methods=['GET','POST'] )
def cardmenu():
    """This route displays the current cardset and displays menu for individual cards"""

    """set default values for title and current_card_number"""
    cardset_title = ""
    session['current_card_number'] = 0

    """if the cardset_id is set"""
    if session['cardset_id']:

        """query cardset to get title and description
        then render webpage cardmenu.html"""
        my_cardset = CardSet.query.get(session['cardset_id'])
        cardset_title = my_cardset.title
        cardset_description = my_cardset.description
    return render_template('cardmenu.html', title="Card Menu",cardset_title=cardset_title, cardset_description = cardset_description)


@app.route('/newcard', methods=['GET','POST'])
def newcard():
    """This route is used for creating a new card within a specific cardset"""
    form = CardEntryForm()
    image_file = "default.png"# default image file

    if form.validate_on_submit():
        if form.image_one.data:

            """if an image file name was added then save image"""
            image_file = save_image(form.image_one.data)

        """retrieve values from submitted form
        and adds row to database"""
        addcard = Card(keyword_one=form.keyword_one.data,
                       keyword_two=form.keyword_two.data,
                       text_one=form.text_one.data,
                       image_one=image_file,
                       cardset_id=session['cardset_id'])

        """add new card to database"""
        db.session.add(addcard)
        db.session.commit()

        """if the submit button was used automatically return to
        add another new card"""
        if form.submit.data:
            return redirect (url_for('newcard'))

        """if the finish button was used exit and go to card menu"""
        if form.finish.data:
            flash(f'New Card {form.keyword_one.data} has been created!', 'success')
            return redirect (url_for('cardmenu'))
    return render_template('newcard.html', title="Add New Card", form=form)


@app.route('/editcard', methods=['GET', 'POST'])
def editcard():
    """This route is used for editing a card within a specific cardset"""

    """select current card in set"""
    form = CardEntryForm()
    these_cards = Card.query.filter(Card.cardset_id == session['cardset_id'])
    current_card = these_cards[session['current_card_number']]

    if form.validate_on_submit():

        """if the finish button was used to submit form"""
        if form.finish.data:
            flash(f'This Card has been updated!', 'success')

            """update card"""
            if form.image_one.data:
                """if an image file name was added then save image"""
                current_card.image_one = save_image(form.image_one.data)

            current_card.keyword_one = form.keyword_one.data
            current_card.keyword_two = form.keyword_two.data
            current_card.text_one = form.text_one.data
            current_card.cardset_id = session['cardset_id']

            db.session.add(current_card)
            db.session.commit()

            """uses hidden checkbox to conform delete action requested
            delete checkbox is set by javascript when user clicks ok on message box"""
        elif form.delete:
            db.session.delete(current_card)
            db.session.commit()
            flash(f'The Card has been deleted!', 'warning')

        return redirect (url_for('reviewcards'))

    """fill card with existing values"""
    form.keyword_one.data = current_card.keyword_one
    form.keyword_two.data = current_card.keyword_two
    form.text_one.data = current_card.text_one
    form.image_one.data = current_card.image_one

    return render_template('editcard.html', title="Add New Card", form=form)


"""#################################################
                REVIEW CARD ROUTES
   #################################################"""

@app.route('/reviewcards',methods=['GET','POST'])
def reviewcards():
    """This route displays individual cards within a cardset"""
    form = Card
    my_value = session['cardset_id']

    """select cards based on current cardset.id"""
    review_cards = Card.query.filter(Card.cardset_id == my_value)

    """count cards in current set"""
    session['number_of_cards'] = review_cards.count()

    """if there is at least 1 card in the set
    then set current_card to the current card and 
    then display the card"""
    if session['number_of_cards'] > 0:
        current_card = review_cards[session['current_card_number']]

        return render_template('reviewcards.html',
                                   form = form,
                                   current_card = current_card,
                                   number_of_cards = session['number_of_cards'],
                                   current_card_number = int(session['current_card_number'])+1)
    else:
        """if there are no cards in the set display error message
        and return to card menu"""
        flash(f'There are no cards. Please add a card first', 'warning')

    return redirect(url_for('cardmenu'))


@app.route('/nextcard')
def nextcard():
    """This route adds one to the count of these_cards. Then starts over"""
    if session['current_card_number']+1 < session['number_of_cards']:
        session['current_card_number'] = session['current_card_number']+1
    else:
        session['current_card_number'] = 0
    return redirect(url_for('reviewcards'))


@app.route('/prevcard')
def prevcard():
    """This route subtracts one from the count of these_cards unless at 0"""
    if session['current_card_number']>0:
        session['current_card_number'] = session['current_card_number'] -1
    else:
        session['current_card_number'] = session['number_of_cards']-1
    return redirect(url_for('reviewcards'))


"""#################################################
                 FLASH CARD ROUTES
   #################################################"""

@app.route('/flashmenu', methods=['GET', 'POST'])
def flashmenu():

    """This route displays the Flash Card Menu"""
    form = FlashCardSelection()

    """Select Set of Cards Then Shuffle Them"""
    my_value = session['cardset_id']
    flash_cards = Card.query.filter(Card.cardset_id == my_value)

    """Check to make sure there are are cards in the set
     return to menu if there are 0 cards in the card set"""
    if flash_cards.count() == 0:
        flash(f'There are no cards. Please add a card first', 'warning')
        return redirect(url_for('cardmenu'))

    if form.validate_on_submit():

        """make list of ids from current set of cars"""
        flash_ids = []
        for flash_card in flash_cards:
            flash_ids.append(flash_card.id)

        """randomly shuffle list of IDs"""
        random.shuffle(flash_ids)

        """save shuffled list of IDs into session variable"""
        session['flash_ids'] = flash_ids

        """save number of cards into session variable"""
        session['number_of_cards'] = len(flash_ids)

        """reset session variables for viewing front and back"""
        session['front_key_1'] = session['front_key_2'] = session['front_image_1'] = session['front_text_1'] = False
        session['back_key_1'] = session['back_key_2'] = session['back_image_1'] = session['back_text_1'] = False

        """Set session variable for viewing front and back"""
        if form.front_key_1.data:
            session['front_key_1'] = True
        if form.front_key_2.data:
            session['front_key_2'] = True
        if form.front_image_1.data:
            session['front_image_1'] = True
        if form.front_text_1.data:
            session['front_text_1'] = True
        if form.back_key_1.data:
            session['back_key_1'] = True
        if form.back_key_2.data:
            session['back_key_2'] = True
        if form.back_image_1.data:
            session['back_image_1'] = True
        if form.back_text_1.data:
            session['back_text_1'] = True

        """set session variable which counts cards"""
        session['current_card_number'] = 0

        """go to first card front"""
        return redirect (url_for('flashfront'))

    """if first call render form flashselect.html"""
    return render_template('flashselect.html', title="Flash Card Menu",form=form)


@app.route('/flashfront', methods=['GET', 'POST'])
def flashfront():
    """This route displays the front of flashcard"""

    """makes sure there are still cards to show"""
    if session['current_card_number'] == session['number_of_cards']:
        """if there are no cards or last card already shown return to menu"""
        return redirect (url_for('cardmenu'))

    """get id of current card"""
    current_card_id = session['flash_ids'][session['current_card_number']]

    """use card id to query full card info"""
    current_card = Card.query.filter(Card.id == current_card_id).first()

    """test if query was successful then proceed"""
    if current_card:

        """Get Cardset.title to display on webpage"""
        my_cardset = CardSet.query.get(session['cardset_id'])
        cardset_title = my_cardset.title

        """reset = keys display card fields on webpage"""
        key_1 = key_2 = text_1 = " "
        image_1 = "blank.jpg"

        """display value if selected for front of card -OR-
           display ? if selected only for back of card"""
        if session['front_key_1']:
            key_1 = current_card.keyword_one
        elif session['back_key_1']:
            key_1 = "?"
        if session['front_key_2']:
            key_2 = current_card.keyword_two
        elif session['back_key_2']:
            key_2 = "?"
        if session['front_image_1']:
            image_1 = current_card.image_one
        elif session['back_image_1']:
            image_1 = "question.jpg"
        if session['front_text_1']:
            text_1 = current_card.text_one
        elif session['back_text_1']:
            text_1 = "?"
        return render_template('flashfront.html',
                               cardset_title=cardset_title,
                               current_card=current_card,
                               cardset=my_cardset,
                               key_1=key_1, key_2=key_2,
                               image_1=image_1, text_1=text_1,
                               number_of_cards=session['number_of_cards'],
                               current_card_number=int(session['current_card_number']) + 1)

    """if query was not successful return to card menu"""
    return redirect (url_for('cardmenu'))


@app.route('/flashback', methods=['GET', 'POST'])
def flashback():
    """THis route displays the back of flashcard"""

    """Get Cardset.title to display on webpage"""
    current_id = session['flash_ids'][session['current_card_number']]
    current_card = Card.query.filter(Card.id == current_id).first()

    """advance current card number in anticipation of showing next card"""
    session['current_card_number'] += 1

    """test if query was successful then proceed"""
    if current_card:

        """Get Cardset.title to display on webpage"""
        my_cardset = CardSet.query.get(session['cardset_id'])
        cardset_title = my_cardset.title

        """reset keys for diplay information on webpage"""
        key_1 = key_2 = text_1 = " "
        image_1 = "blank.jpg"

        """display value if selected for back of card -OR-
           adds '?' if selected only for front of card
           this is used in the template to gray the text"""
        if session['back_key_1']:
            key_1 = current_card.keyword_one
        elif session['front_key_1']:
            key_1 = "?"+current_card.keyword_one
        if session['back_key_2']:
            key_2 = current_card.keyword_two
        elif session['front_key_2']:
            key_2 = "?"+current_card.keyword_two
        if session['back_image_1']:
            image_1 = current_card.image_one
        elif session['front_image_1']:
            image_1 = "?"+current_card.image_one
        if session['back_text_1']:
            text_1 = current_card.text_one
        elif session['front_text_1']:
            text_1 = "?"+current_card.text_one
        return render_template('flashback.html',
                               cardset_title=cardset_title,
                               current_card=current_card,
                               cardset=my_cardset,
                               key_1=key_1, key_2=key_2,
                               image_1=image_1, text_1=text_1,
                               number_of_cards=session['number_of_cards'],
                               current_card_number=session['current_card_number'])
    """if the query fails return to cardmenu"""
    return redirect (url_for('cardmenu'))