from flask import (
    Blueprint, flash, request, redirect, render_template, url_for
)
from leave import db
from leave.models import Organization
from leave.forms import OrganizationMasterUpdateForm
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


def set_organization_details_from_form(organization, form):
    organization.name = form.name.data
    organization.add1 = form.add1.data
    organization.add2 = form.add2.data
    organization.add3 = form.add3.data
    organization.city = form.city.data
    organization.state = form.state.data
    organization.pin = form.pin.data
    organization.phone = form.phone.data
    organization.email = form.email.data


@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    organization = Organization.query.first()
    form = OrganizationMasterUpdateForm()
    if form.validate_on_submit():
        if not organization:
            new_organization = Organization()
            set_organization_details_from_form(new_organization, form)
            db.session.add(new_organization)
        else:
            set_organization_details_from_form(organization, form)

        db.session.commit()
        return redirect(url_for('organization.view'))

    if organization:
        form.name.data = organization.name
        form.add1.data = organization.add1
        form.add2.data = organization.add2
        form.add3.data = organization.add3
        form.city.data = organization.city
        form.state.data = organization.state
        form.pin.data = organization.pin
        form.phone.data = organization.phone
        form.email.data = organization.email

    return render_template('masters/organization/update.html', form=form)
