'''The routes module is used to retrieve links from the broser.
In the current format the routes below assume start after the heading localhost:5000'''

from flask import render_template, flash, redirect, url_for
from studycards import app, db, session
from studycards.forms import CardSetForm, CardEntryForm,SelectCardSet
from studycards.models import CardSet, Card


@app.route('/',methods=['GET','POST'])
def home():
    '''This route displays the Cardset selection form so user can select a cardset'''
    form = SelectCardSet()
    #run update method to load new or updated cardsets
    form.update()
    if form.validate_on_submit():
        the_selected_cardset = CardSet.query.get(form.selected_cardset.data)
        session['cardset_id'] = the_selected_cardset.id
        return redirect(url_for('cardmenu'))
#   If there are no cardsets then the link returns,until a cardset is created
    session['cardset_id']=""
    return render_template('home.html', title="Create or Select A Card Set ", form=form)

@app.route('/about')
def about():
    '''This route displays the About (help) page'''
    return render_template('about.html', title="About")

@app.route('/cardset', methods=['GET','POST'])
def cardset():
    '''This route is used to add the new cardset to the database'''
    form = CardSetForm()
    if form.validate_on_submit():
        newcardset = CardSet(title=form.title.data, description=form.description.data)
        db.session.add(newcardset)
        db.session.commit()
        flash(f'Card Set {form.title.data} has been created!', 'success')
        return redirect (url_for('home'))
    return render_template('cardset.html', title="Card Set Definition", form=form)


@app.route('/newcard', methods=['GET','POST'])
def newcard():
    '''This route is used for creating a new card within a specific cardset'''
    form = CardEntryForm()
    if form.validate_on_submit():
        #Save new card to database
        newcard = Card(keyword_one=form.keyword_one.data,
                       keyword_two=form.keyword_two.data,
                       definition=form.definition.data,
                       cardset_id=session['cardset_id'])
        db.session.add(newcard)
        db.session.commit()

        if form.submit.data:
            return redirect (url_for('newcard'))
        if form.finish.data:
            flash(f'New Card {form.keyword_one.data} has been created!', 'success')
            return redirect (url_for('cardmenu'))
    return render_template('newcard.html', title="Add New Card", form=form)


@app.route('/cardmenu',methods=['GET','POST'] )
def cardmenu():
    '''This route displays the current cardset and displays menu for individual cards'''
    cardset_title = ""
    session['current_card_number'] = 0
    if session['cardset_id']:
        my_cardset = CardSet.query.get(session['cardset_id'])
        cardset_title = my_cardset.title
        cardset_description = my_cardset.description
    return render_template('cardmenu.html', title="Card Menu",cardset_title=cardset_title, cardset_description = cardset_description)

@app.route('/reviewcards',methods=['GET','POST'])
def reviewcards():
    '''This route displays individual cards within a cardset'''
    form = Card
    my_value = session['cardset_id']
    these_cards = Card.query.filter(Card.cardset_id == my_value)
    session['number_of_cards'] = these_cards.count()
    this_card = these_cards[session['current_card_number']]
    return render_template('reviewcards.html',
                           form = form,
                           this_card = this_card,
                           number_of_cards = session['number_of_cards'],
                           current_card_number = int(session['current_card_number'])+1)
    return redirect(url_for('cardmenu'))

@app.route('/nextcard')
def nextcard():
    '''This route adds one to the count of these_cards. Then starts over'''
    if session['current_card_number']+1 < session['number_of_cards']:
        session['current_card_number'] = session['current_card_number']+1
    else:
        session['current_card_number'] = 0
    return redirect(url_for('reviewcards'))

@app.route('/prevcard')
def prevcard():
    '''This route subtracts one from the count of these_cards unless at 0'''
    if session['current_card_number']>0:
        session['current_card_number'] = session['current_card_number'] -1
    else:
        session['current_card_number'] = session['number_of_cards']-1
    return redirect(url_for('reviewcards'))

