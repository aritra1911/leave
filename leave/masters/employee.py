from flask import (
    Blueprint, flash, request, redirect, render_template, url_for
)
from leave import db
from leave.models import Employee
from leave.auth import login_required
from leave.forms import EmployeeMasterCreateForm, EmployeeMasterUpdateForm

bp = Blueprint('employee', __name__, url_prefix='/masters/employee')


@bp.route('/')
@login_required
def master():
    employee = Employee.query.order_by(Employee.empcd).first()
    if not employee:
        return redirect(url_for('employee.create'))

    return redirect(url_for('employee.view', empcd=employee.empcd))


def get_employee(empcd):
    return Employee.query.filter_by(empcd=empcd).first_or_404(
        f"Employee with code {empcd} not found"
    )


@bp.route('/<empcd>')
@login_required
def view(empcd):
    employee = get_employee(empcd)
    return render_template('masters/employee/view.html', employee=employee)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EmployeeMasterCreateForm()
    if form.validate_on_submit():
        existing_employee = Employee.query.filter_by(
            empcd=form.empcd.data
        ).first()
        if not existing_employee:
            employee = Employee(
                empcd=form.empcd.data, name=form.name.data,
                designation=form.desg.data, department=form.dept.data
            )
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for('employee.view', empcd=form.empcd.data))

        flash(
            f'Employee with code {form.empcd.data} already exists',
            category='error'
        )

    return render_template('masters/employee/create.html', form=form)


@bp.route('/<empcd>/next')
@login_required
def next(empcd):
    next_employee = Employee.query.filter(Employee.empcd > empcd).order_by(
        Employee.empcd
    ).first()

    if next_employee:
        return redirect(
            url_for('employee.view', empcd=next_employee.empcd)
        )

    return redirect(url_for('employee.master'))


@bp.route('/<empcd>/prev')
@login_required
def prev(empcd):
    prev_employee = Employee.query.filter(Employee.empcd < empcd).order_by(
        Employee.empcd.desc()
    ).first()

    if prev_employee:
        return redirect(
            url_for('employee.view', empcd=prev_employee.empcd)
        )

    return redirect(url_for('employee.eof'))


@bp.route('/eof')
@login_required
def eof():
    last_employee = Employee.query.order_by(Employee.empcd.desc()).first()
    if last_employee:
        return redirect(
            url_for('employee.view', empcd=last_employee.empcd)
        )

    return redirect(url_for('employee.master'))


@bp.route('/<empcd>/update', methods=['GET', 'POST'])
@login_required
def update(empcd):
    employee = get_employee(empcd)
    form = EmployeeMasterUpdateForm()
    if form.validate_on_submit():
        employee.name = form.name.data
        employee.desg = form.desg.data
        employee.dept = form.dept.data
        db.session.commit()
        return redirect(url_for('employee.view', empcd=employee.empcd))

    form.name.data = employee.name
    form.desg.data = employee.designation
    form.dept.data = employee.department
    return render_template(
        '/masters/employee/update.html', empcd=empcd, form=form
    )


@bp.route('/<empcd>/delete', methods=['POST',])
@login_required
def delete(empcd):
    employee = Employee.query.filter_by(empcd=empcd).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('employee.next', empcd=employee.empcd))
