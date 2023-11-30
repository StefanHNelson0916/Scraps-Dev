import scraps_dev.query_builders as qb
import scraps_dev.db as db
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is requred'
        elif not password:
            error = 'Password is required'

        if error is None:
            query = qb.add_user()
            password = generate_password_hash(password)
            values = (username, password)
            db.add_user(query, values) 
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        query = qb.get_user_by_username(username)
        user = db.get_one(query)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('search.ingredients_search'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        query = qb.get_user_by_id(user_id)
        g.user = db.get_one(query)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))