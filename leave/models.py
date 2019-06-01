from leave import db


class OrganizationMaster(db.Model):
    name = db.Column(db.String(64), primary_key=True)
    add1 = db.Column(db.String(64), nullable=False)
    add2 = db.Column(db.String(64))
    add3 = db.Column(db.String(64))
    city = db.Column(db.String(16), nullable=False)
    state = db.Column(db.String(16), nullable=False)
    pin = db.Column(db.String(8), nullable=False)
    phone = db.Column(db.String(16))
    email = db.Column(db.String(64))

    def __repr__(self):
        return '<Organization %r>' % self.name


class LeaveMaster(db.Model):
    el = db.Column(db.Integer, primary_key=True)
    cl = db.Column(db.Float)
    sl = db.Column(db.Integer)

    def __repr__(self):
        return '<Leave %r>' % self.el


class EmployeeMaster(db.Model):
    empcd = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    designation = db.Column(db.String(64))
    department = db.Column(db.String(32))
    opening_bal = db.relationship(
        'opening_balance',
        backref=db.backref('employee_master', lazy='joined'),
        lazy='joined'
    )

    def __repr__(self):
        return '<Employee %r>' % self.name


class OpeningBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_cd = db.Column(
        db.Integer, db.ForeignKey('employee_master.empcd'), nullable=False
    )
    leave_cat = db.Column(db.String)
    period_code = db.Column(
        db.Integer, db.ForeignKey('period_master.periodcd'), nullable=False
    )
    leave_balance = db.Column(db.Integer)

    def __repr__(self):
        return '<OpeningBalance %r>' % self.id


class PeriodMaster(db.Model):
    periodcd = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    opening_bal = db.relationship(
        'opening_balance',
        backref=db.backref('period_master', lazy='joined'),
        lazy='joined'
    )

    def __repr__(self):
        return '<Period %r>' % self.periodcd
