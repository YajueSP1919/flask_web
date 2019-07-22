import uuid
from functools import wraps

import redis
from flask import  session,request, abort

from models.user import User
from utils import log



def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        # s = Session.one_for_session_id(session_id=session_id)
        key = 'session_id_{}'.format(session_id)
        user_id = cache.get(key)
        if user_id is None :
            return User.guest()
        else:
            u = User.one(id=user_id)
            if u is None:
                return User.guest()
            else:
                return u
    else:
        return User.guest()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        k = 'token_{}'.format(token)
        log('k:', k)
        log('cache.get(k):',int(cache.get(k)),u.id)
        if cache.exists(k) and int(cache.get(k)) == u.id:
            log('cache:',cache)
            cache.delete(k)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    k = 'token_{}'.format(token)
    v = u.id
    cache.set(k,v)
    return token


cache = redis.StrictRedis()