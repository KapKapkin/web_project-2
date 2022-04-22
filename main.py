import flask
import flask_login
import jwt
from datetime import datetime, timedelta

from flask_restful import Api
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from sqlalchemy import or_

from data import db_session

from api import register_resources
from api import login_resources
from api import users_resources
from api import dialogs_resources
from api import messages_resources
from api import posts_resources


from forms.register import RegisterForm
from forms.login import LoginForm
from forms.message import SendMessageForm

from data.users import Users
from data.messages import Messages
from data.dialogs import Dialogs
from data.posts import Posts
from data.comments import Comments

from data.token import token_required
import os

os.chdir(os.getcwd())

app = flask.Flask(__name__, template_folder='static/html')

app.config.update(
    SECRET_KEY='very_secret_key_word_for_flask_XDDDD'
)



login_manager = flask_login.LoginManager()
login_manager.init_app(app)

api = Api(app)
admin = Admin(app)

@login_manager.user_loader
def load_user(users_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(users_id)


@app.route('/')
def index():
    return flask.redirect('/main')


@app.route('/main')
def main():
    print(flask.session)
    return flask.render_template('feed.html')


@app.route('/jwttest')
@token_required
def jwt_test(user):
    return 'Works!'


@app.route('/dialogs')
def dialogs():
    db_sess = db_session.create_session()
    dialogs = db_sess.query(Dialogs).filter(
        or_(Dialogs.user_one == flask_login.current_user, Dialogs.user_two == flask_login.current_user)).all()
    return flask.render_template('dialogs.html')


@token_required
@app.route('/dialogs/<int:users_id>', methods=['GET', 'POST'])
def get_dialog(users_id):
    form = SendMessageForm()
    db_sess = db_session.create_session()
    users = db_sess.query(Users).get(users_id)
    current_user = int(flask.session['_user_id'])
    if users and current_user != users.id:
        dialogs = db_sess.query(Dialogs).filter(Dialogs.user_one_id.in_(
            [current_user, users_id]), Dialogs.user_two_id.in_([current_user, users_id])).first()
        flask.session['_recipient'] = users_id
        if dialogs:
            return flask.render_template('dialog.html', dialog=dialogs, form=form)
        dialogs = Dialogs(
            user_one_id=current_user,
            user_two_id=users_id,
        )
        db_sess.add(dialogs)
        db_sess.commit()

        return flask.render_template('dialog.html', dialog=dialogs, form=form)

    return flask.redirect('/dialogs')


@app.route('/<int:users_id>')
def page(users_id):

    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.id == users_id).first()

    if user:
        return flask.render_template('page.html', user=user.to_dict(
            only=('name', 'surname', 'email', 'age', 'tags')), posts=user.posts)
    else:
        flask.abort(404)


@app.route('/register', methods=['GET', 'POST'])
def reqister():

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return flask.render_template('register.html', title='Регистрация',
                                         form=form,
                                         message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            return flask.render_template('register.html', title='Регистрация',
                                         form=form,
                                         message="Такой пользователь уже есть")
        user = Users(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            tags=form.tags.data,
        )

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return flask.redirect('/login')
    return flask.render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(
            Users.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            flask.session['logged_in'] = True
            token = jwt.encode({
                'user': user.id,
                'email': user.email,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(hours=24)},
                app.config['SECRET_KEY'])
            flask.session['_user_id'] = user.id
            flask.session['_token'] = token
            flask_login.login_user(user, remember=form.remember_me.data)
            return flask.redirect("/")

        return flask.render_template('login.html',
                                     message="Неправильный логин или пароль",
                                     form=form)
    return flask.render_template('login.html', title='Авторизация', form=form)

@token_required
@app.route('/logout')
def logout():
    flask.session['logged_id'] = False
    flask_login.logout_user()
    return flask.redirect("/")


def main():
    
    app.run(port=5000, host='127.0.0.1', debug=True,
            use_reloader=True, threaded=True)


if __name__ == '__main__':
    db_session.global_init('db/blogs.sqlite')

    db_sess = db_session.create_session()

    db_sess.commit()

    admin.add_view(ModelView(Users, db_sess))
    admin.add_view(ModelView(Dialogs, db_sess))
    admin.add_view(ModelView(Messages, db_sess))
    admin.add_view(ModelView(Posts, db_sess))
    admin.add_view(ModelView(Comments, db_sess))

    api.add_resource(users_resources.UsersListResource, '/api/users')
    api.add_resource(users_resources.UsersResource,
                     '/api/users/<int:users_id>')

    api.add_resource(dialogs_resources.DialogsListResource, '/api/dialogs')

    api.add_resource(messages_resources.MessagesResource, '/api/messages')

    api.add_resource(posts_resources.PostsListResource, '/api/posts')

    api.add_resource(login_resources.LoginResource, '/api/login')

    api.add_resource(register_resources.RegisterResource, '/api/register')

    main()
