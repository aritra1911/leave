from flask import (
    Blueprint, flash, request, redirect, render_template, url_for
)
from leave import db
from leave.models import Employee
from leave.auth import login_required

bp = Blueprint('employee', __name__, url_prefix='/masters/employee')


@bp.route('/')
@login_required
def master():
    employee = Employee.query.order_by(Employee.empcd).first()
    if not employee:
        return redirect(url_for('employee.create'))

    return redirect(url_for('employee.view', empcd=employee.empcd))


@bp.route('/<empcd>')
@login_required
def view(empcd):
    employee = Employee.query.filter_by(empcd=empcd).first()
    if employee is None:
        flash(f"Employee with code {empcd} doesn't exist", category='error')
        return redirect(url_for('employee.master'))

    return render_template('masters/employee/view.html', employee=employee)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        empcd = request.form['empcd']
        name = request.form['name']
        desg = request.form['desg']
        dept = request.form['dept']

        existing_employee = Employee.query.filter_by(empcd=empcd).first()
        error = None

        if empcd and name and desg and dept and not existing_employee:
            employee = Employee(
                empcd=empcd, name=name, designation=desg, department=dept
            )
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for('employee.view', empcd=empcd))

        if existing_employee:
            error = f'Employee with code {empcd} already exists'
        else:
            error = 'One or more field(s) were caught blank'

        flash(error, category='error')

    return render_template('masters/employee/create.html')


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
