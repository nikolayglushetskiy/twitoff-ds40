'''
Twitoff DS40 by Nikolay Glushetskiy
Study projet
'''
from flask import Flask, render_template
from twitoff.models import DB, User, Tweet
from twitoff.twitter import add_or_update_user, update_all_users

app = Flask(__name__)


def create_app():
    '''
    Initializing twitoff app
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    # app title
    app_title = "Twitoff DS40 by Nikolay Glushetskiy"

    # Homepage of our app
    @app.route("/")
    def root():
        users = User.query.all()
        return render_template('base.html', title=app_title, users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        print('''The database has been reseted. 
                <a href='/'>Go to Home</a>
                <a href='/reset'>Go to reset</a>
                <a href='/populate'>Go to populate</a>
               ''')
        return render_template('base.html', title=app_title, message='Testre')

    @app.route('/populate')
    def populate():
        add_or_update_user('elonmusk')
        add_or_update_user('nasa')
        return '''Created some users. 
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>'''

    @app.route('/update')
    def update():
        '''Updates all users'''
        usernames = update_all_users()
        for username in usernames:
            add_or_update_user(username)
        return render_template('base.html', title=app_title)

    # Return app object with all routines
    return app

    