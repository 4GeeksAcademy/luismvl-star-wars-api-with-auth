from flask import jsonify, url_for
from models import db, User, Character, Planet


class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" +
                         y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <img style="max-height: 80px" src='https://storage.googleapis.com/breathecode/boilerplates/rigo-baby.jpeg' />
        <h1>Rigo welcomes you to your API!!</h1>
        <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
        <p>Start working on your proyect by following the <a href="https://start.4geeksacademy.com/starters/flask" target="_blank">Quick Start</a></p>
        <p>Remember to specify a real endpoint path like: </p>
        <ul style="text-align: left;">"""+links_html+"</ul></div>"


def get_all_users():
    users = User.query.all()
    return users


def get_user_by_id(id):
    user = User.query.get(id)
    return user


def save_new_user(username, email, password, is_active):
    user = User(username=username, email=email,
                password=password, is_active=is_active)
    db.session.add(user)
    db.session.commit()
    return user


def validate_user(user_dict):
    required_values = ['username', 'email', 'password']
    missing_values = []
    for key in required_values:
        if key not in user_dict:
            missing_values.append(key)
    return missing_values


def update_user_by_id(id, properties):
    user = User.query.get(id)

    if ('username') in properties:
        user.username = properties['username']

    if ('email') in properties:
        user.email = properties['email']

    if ('password') in properties:
        user.password = properties['password']

    if ('is_active') in properties:
        user.is_active = properties['is_active']

    db.session.commit()
    return user


def delete_user_by_id(id):
    user = User.query.get(id)
    if user is None:
        return False
    db.session.delete(user)
    db.session.commit()
    return True
