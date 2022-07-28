'''
Twitoff DS40 by Nikolay Glushetskiy
Study projet
'''
from flask import Flask, render_template, request
from twitoff.models import DB, User, Tweet
from twitoff.twitter import add_or_update_user, update_all_users
from twitoff.predict import predict_user

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
        return render_template('base.html', title='Reset Database')

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
        return "All users have been updated"

    @app.route('/user', methods=['POST'])
    def add_user():
        username = request.values['user_name']
        add_or_update_user(username)
        db_user = User.query.filter(User.username == username).one()
        return render_template(
            'user.html',
            title=username, 
            message=f'{username} added',
            tweets=db_user.tweets
        )
        # return render_template('user.html', title='title', message='oops')

    @app.route('/user/<username>')
    def user(username=None):
        db_user = User.query.filter(User.username == username).one()
        return render_template(
            'user.html', 
            title=username, 
            message='',
            tweets=db_user.tweets
        )

    @app.route('/compare', methods=['POST'])
    def compare():
        username0 = request.values['user0']
        username1 = request.values['user1']
        hypo_tweet_text = request.values['tweet_text']

        if username0 == username1:
            message = 'Cannot compare users to themselves!'
        else:
            prediction = predict_user(username0, username1, hypo_tweet_text)
            if prediction:
                predicted_user = username1
            else:
                predicted_user = username0
            message = f'This tweet was more likely written by {predicted_user}'
        
        return render_template(
            'prediction.html', 
            title='Prediction', 
            message=message
        )

    # Return app object with all routines
    return app

    