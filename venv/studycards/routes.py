from flask import render_template
from studycards import app
#from studycards.forms import Registration, LoginFrom
#from studycards.models import User, Post

posts = [
    {
        'author': 'John Demaree',
        'title': 'Blog Post 1',
        'content': 'First blog post content'
    },
    {
        'author': 'Jennifer Demaree',
        'title': 'Blog Post 2',
        'content': 'Second blog post content'
    }
]


@app.route('/')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/cardset')
def cardset():
    form = CardSetForm()
    return render_template('cardset.html', title="Card Set Definition", form=form)
