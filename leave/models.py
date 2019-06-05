from leave import db


class Organization(db.Model):
    __tablename__ = 'organization_master'

    name = db.Column(db.String(32), primary_key=True)
    add1 = db.Column(db.String(25), nullable=False)
    add2 = db.Column(db.String(25), nullable=True)
    add3 = db.Column(db.String(25), nullable=True)
    city = db.Column(db.String(16), nullable=False)
    state = db.Column(db.String(16), nullable=False)
    pin = db.Column(db.String(8), nullable=False)
    phone = db.Column(db.String(16), nullable=True)
    email = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return '<Organization %r>' % self.name


class Leave(db.Model):
    __tablename__ = 'leave_master'

    el = db.Column(db.Integer, primary_key=True)
    cl = db.Column(db.Float, nullable=False)
    sl = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Leave %r, %r, %r>' % (self.el, self.cl, self.sl)


class Employee(db.Model):
    __tablename__ = 'employee_master'

    empcd = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    designation = db.Column(db.String(25), nullable=False)
    department = db.Column(db.String(30), nullable=False)
    opening_bal = db.relationship(
        'OpeningBalance', backref='employee', lazy=True
    )

    def __repr__(self):
        return '<Employee %r>' % self.name


class OpeningBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_cd = db.Column(
        db.String(6), db.ForeignKey('employee_master.empcd'), nullable=False
    )
    leave_cat = db.Column(db.String(2), nullable=False)
    period_code = db.Column(
        db.Integer, db.ForeignKey('period_master.periodcd'), nullable=False
    )
    leave_balance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<OpeningBalance %r>' % self.id


class Period(db.Model):
    __tablename__ = 'period_master'

    periodcd = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    opening_bal = db.relationship(
        'OpeningBalance', backref='period', lazy=True
    )

    def __repr__(self):
        return '<Period %r>' % self.periodcd
