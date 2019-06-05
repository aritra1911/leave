from flask import (
    Blueprint, flash, request, redirect, render_template, url_for
)
from leave import db
from leave.models import Organization
from leave.auth import login_required

bp = Blueprint('organization', __name__, url_prefix='/masters/organization')


@bp.route('/')
@login_required
def view():
    organization = Organization.query.first()
    if not organization:
        return redirect(url_for('organization.update'))

    return render_template(
        'masters/organization/view.html', organization=organization
    )


@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    organization = Organization.query.first()
    if request.method == 'POST':
        name = request.form['name']
        add1 = request.form['add1']
        add2 = request.form['add2']
        add3 = request.form['add3']
        city = request.form['city']
        state = request.form['state']
        pin = request.form['pin']
        phone = request.form['phone']
        email = request.form['email']

        if name and add1 and city and state and pin:
            if organization:
                organization.name = name
                organization.add1 = add1
                organization.add2 = add2
                organization.add3 = add3
                organization.city = city
                organization.state = state
                organization.pin = pin
                organization.phone = phone
                organization.email = email
                db.session.commit()
            else:
                new_organization = Organization(
                    name=name, add1=add1, add2=add2, add3=add3, city=city,
                    state=state, pin=pin, phone=phone, email=email
                )
                db.session.add(new_organization)
                db.session.commit()

            return redirect(url_for('organization.view'))

        flash('One or more required field(s) were caught blank.')

    return render_template(
        'masters/organization/update.html', organization=organization
    )
