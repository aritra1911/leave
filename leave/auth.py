import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        error = None
        if password == 'leave123':
            session.clear()
            session['logged_in'] = True
            return redirect(url_for('index'))

        error = 'Please enter a valid password'
        flash(error)

    if g.logged_in:
        return redirect(url_for('index'))

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    g.logged_in = session.get('logged_in')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):

        if not session.get('logged_in'):
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
