import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from leave import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        password = request.form['password']
        error = None
        if password == 'leave123':
            session.clear()
            session['authenticated'] = True
            return redirect(url_for('index'))

        error = 'Please enter a valid password'
        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session['authenticated']:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
