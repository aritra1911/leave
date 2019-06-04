from flask import (
    Blueprint, flash, request, redirect, render_template, url_for
)
from leave import db
from leave.models import Employee
from leave.auth import login_required

bp = Blueprint('masters', __name__, url_prefix='/masters/employee')


@bp.route('/')
@login_required
def employee_master():
    employee = Employee.query.order_by(Employee.empcd).first()
    if not employee:
        return redirect(url_for('masters.employee_create'))

    return redirect(url_for('masters.employee_view', empcd=employee.empcd))


@bp.route('/<empcd>')
@login_required
def employee_view(empcd):
    employee = Employee.query.filter_by(empcd=empcd).first()
    if employee is None:
        flash(f"Employee with code {empcd} doesn't exist", category='error')
        return redirect(url_for('masters.employee_master'))

    return render_template('masters/employee_view.html', employee=employee)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def employee_create():
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
            return redirect(url_for('masters.employee_view', empcd=empcd))

        if existing_employee:
            error = f'Employee with code {empcd} already exists'
        else:
            error = 'One or more field(s) were caught blank'

        flash(error, category='error')

    return render_template('masters/employee_create.html')


@bp.route('/<empcd>/next')
@login_required
def employee_next(empcd):
    next_employee = Employee.query.filter(Employee.empcd > empcd).order_by(
        Employee.empcd
    ).first()
    if next_employee:
        return redirect(
            url_for('masters.employee_view', empcd=next_employee.empcd)
        )

    return redirect(url_for('masters.employee_master'))


@bp.route('/<empcd>/prev')
@login_required
def employee_prev(empcd):
    prev_employee = Employee.query.filter(Employee.empcd < empcd).order_by(
        Employee.empcd.desc()
    ).first()
    if prev_employee:
        return redirect(
            url_for('masters.employee_view', empcd=prev_employee.empcd)
        )

    return redirect(url_for('masters.employee_eof'))


@bp.route('/eof')
@login_required
def employee_eof():
    last_employee = Employee.query.order_by(Employee.empcd.desc()).first()
    if last_employee:
        return redirect(
            url_for('masters.employee_view', empcd=last_employee.empcd)
        )

    return redirect(url_for('masters.employee_master'))
