from datetime import datetime
from flask import render_template, redirect, url_for, session
from . import main
from .forms import NameForm
from flask_sqlalchemy import get_debug_queries
from . import main
from .. import db
from ..models import User,Permission
from ..decorators  import admin_required, permission_required
from flask_login import login_required


@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''

        return redirect(url_for('.index'))
    return render_template('user.html', form=form, name=session.get('name'),
                           known=session.get('known', False))
@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "for administrators!"

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment Moderators!"


