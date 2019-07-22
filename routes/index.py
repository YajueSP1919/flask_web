import os
import uuid

<<<<<<< HEAD
=======
import redis
>>>>>>> error fixed and gif added
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory,
<<<<<<< HEAD
    current_app)
=======
    current_app, flash)
>>>>>>> error fixed and gif added
from werkzeug.datastructures import FileStorage

import config
from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import current_user, cache
<<<<<<< HEAD
=======
from task_queue import send_mail_async
>>>>>>> error fixed and gif added
from utils import log

main = Blueprint('index', __name__)

"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)




@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
<<<<<<< HEAD
=======
        flash("用户名或密码错误")
>>>>>>> error fixed and gif added
        return redirect(url_for('.index'))
    else:
        session_id = str(uuid.uuid4())
        key = 'session_id_{}'.format(session_id)
        log('index login <{}>  <{}>'.format(key,u.id))
        cache.set(key, u.id)

        redirect_to_index = redirect(url_for('topic.index'))
        response = current_app.make_response(redirect_to_index)
        response.set_cookie('session_id', value=session_id)
        # 转到 topic.index 页面
        return response

@main.route("/userlogin")
def user_login():
    u = current_user()
    return render_template("userlogin.html", user=u)



@main.route("/setting")
def setting():
    u = current_user()
    board_id = int(request.args.get('board_id', -1))
    return render_template("setting.html",u=u,bid=board_id)

@main.route("/setting/password", methods=['POST'])
def change_password():
    form = request.form.to_dict()
    # 用类函数来判断
    user = current_user()
    u = User.confirm_password(form,user)
    return redirect(url_for('.setting'))


@main.route("/setting/username", methods=['POST'])
def change_username():
    form = request.form.to_dict()
    # 用类函数来判断
    user = current_user()
    u = User.confirm_username(form)
    return redirect(url_for('.setting'))

<<<<<<< HEAD
tokens = {}

def create_token(form):
    username = form['username']
    uid = User.one(username=username)
    if uid is None:
        return None
    token = str(uuid.uuid4())
    tokens[token] = uid
=======
# tokens = {}
tokens = redis.StrictRedis()

def create_token(form):
    username = form['username']
    u = User.one(username=username)
    uid = int(u.id)
    if uid is None:
        return None
    token = str(uuid.uuid4())
    # tokens[token] = uid
    tokens.set(token, uid)
>>>>>>> error fixed and gif added
    return token

@main.route("/lostpassword")
def lost_password():
    u = current_user()
    return render_template("lostpassword.html", user=u)


@main.route("/reset/send", methods=['POST'])
def reset_send():
    form = request.form.to_dict()
    # 用类函数来判断
    token = create_token(form)
    title = '重置密码'
<<<<<<< HEAD
    content = 'http://148.70.34.62/reset/view?token={}'.format(token)
    send_mail(
=======
    content = 'http://148.70.34.62//reset/view?token={}'.format(token)
    send_mail_async(
>>>>>>> error fixed and gif added
        subject=title,
        author=config.admin_mail,
        to=config.test_mail,
        content=content,
    )
    return redirect(url_for('.index'))


@main.route("/reset/view")
def reset_view():
    token = request.args['token']
    # 用类函数来判断
    print('reset_views token',token, tokens)
<<<<<<< HEAD
    if token in tokens:
=======
    if tokens.exists(token):
>>>>>>> error fixed and gif added
        return render_template("reset_view.html",token=token)
    else:
        return redirect(url_for('.index'))


@main.route('/reset/update', methods=['POST'])
def reset_update():
    token = request.args['token']
<<<<<<< HEAD
    user_id = tokens.get(token, None)
    print('reset_update token', token, tokens)
    if user_id is None:
        return redirect(url_for('.index'))
    else:
        print('reset_update password',request.form['password'])
        password = User.salted_password(request.form['password'])
        User.update(id=user_id, password=password)
=======
    user_id = int(tokens.get(token))
    print('user_id,,', user_id)
    print('reset_update token', token, tokens)
    if tokens.exists(token):
        new_pass = request.form.get('password')
        print('reset_update password', new_pass)
        User.update(user_id, password=User.salted_password(new_pass))
        tokens.delete(token)
        return redirect('/')
    else:
>>>>>>> error fixed and gif added
        return redirect(url_for('.index'))


def created_topic(user_id):
    # O(n)
    ts = Topic.all(user_id=user_id)
    return ts
    #
    # k = 'created_topic_{}'.format(user_id)
    # if cache.exists(k):
    #     v = cache.get(k)
    #     ts = json.loads(v)
    #     return ts
    # else:
    #     ts = Topic.all(user_id=user_id)
    #     v = json.dumps([t.json() for t in ts])
    #     cache.set(k, v)
    #     return ts


def replied_topic(user_id):
    # O(k)+O(m*n)
    rs = Reply.all(user_id=user_id)
    ts = []
    for r in rs:
        t = Topic.one(id=r.topic_id)
        ts.append(t)
    return ts
    #
    # k = 'replied_topic_{}'.format(user_id)
    # if cache.exists(k):
    #     v = cache.get(k)
    #     ts = json.loads(v)
    #     return ts
    # else:
    #     rs = Reply.all(user_id=user_id)
    #     ts = []
    #     for r in rs:
    #         t = Topic.one(id=r.topic_id)
    #         ts.append(t)
    #
    #     v = json.dumps([t.json() for t in ts])
    #     cache.set(k, v)
    #
    #     return ts


@main.route('/profile')
def profile():
    print('running profile route')
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        created = created_topic(u.id)
        replied = replied_topic(u.id)
        return render_template(
            'profile.html',
            user=u,
            created=created,
            replied=replied
        )


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        return render_template('profile.html', user=u)


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file: FileStorage = request.files['avatar']
    # file = request.files['avatar']
    # filename = file.filename
    # ../../root/.ssh/authorized_keys
    # images/../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    # filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    filename = str(uuid.uuid4())
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.profile'))


@main.route('/images/<filename>')
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # http://localhost:2000/images/..%5Capp.py
    # path = os.path.join('images', filename)
    # print('images path', path)
    # return open(path, 'rb').read()
    # if filename in os.listdir('images'):
    #     return
    return send_from_directory('images', filename)
