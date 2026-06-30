# -*- coding: utf-8 -*-
# 医院管理系统 - 主程序
# 课程作业：数据库管理系统项目
# 小组成员：XXX, XXX, XXX

import os
from datetime import datetime, date, timedelta
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import csv
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hms_' + os.urandom(16).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录系统'

# ==================== 数据库模型 ====================

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, doctor, patient
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 医生特有字段
    department = db.Column(db.String(100))  # 科室
    title = db.Column(db.String(50))  # 职称
    description = db.Column(db.Text)  # 简介
    
    # 病人特有字段
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)


class Department(db.Model):
    """科室模型"""
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    



class Appointment(db.Model):
    """预约挂号模型"""
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    appointment_date = db.Column(db.Date, nullable=False, index=True)
    time_slot = db.Column(db.String(20), nullable=False)  # 上午/下午
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    symptom = db.Column(db.Text)  # 症状描述
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    patient = db.relationship('User', foreign_keys=[patient_id], backref='appointments_as_patient')
    doctor = db.relationship('User', foreign_keys=[doctor_id], backref='appointments_as_doctor')


class MedicalRecord(db.Model):
    """电子病历模型"""
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    diagnosis = db.Column(db.Text, nullable=False)  # 诊断结果
    prescription = db.Column(db.Text)  # 处方
    notes = db.Column(db.Text)  # 备注
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    patient = db.relationship('User', foreign_keys=[patient_id])
    doctor = db.relationship('User', foreign_keys=[doctor_id])
    appointment = db.relationship('Appointment')


class Drug(db.Model):
    """药品模型"""
    __tablename__ = 'drugs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    specification = db.Column(db.String(200))  # 规格
    manufacturer = db.Column(db.String(200))  # 生产厂家
    price = db.Column(db.Float, nullable=False)  # 价格
    stock = db.Column(db.Integer, nullable=False, default=0)  # 库存
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Schedule(db.Model):
    """医生排班模型"""
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    work_date = db.Column(db.Date, nullable=False, index=True)
    time_slot = db.Column(db.String(20), nullable=False)  # 上午/下午
    max_patients = db.Column(db.Integer, default=20)  # 最大接诊人数
    current_count = db.Column(db.Integer, default=0)  # 当前已预约人数
    
    doctor = db.relationship('User', backref='schedules')


# ==================== 装饰器 ====================

def role_required(*roles):
    """
    权限控制装饰器
    用法: @role_required('admin', 'doctor')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.role not in roles:
                flash("您没有权限访问此页面", "danger")
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ============================================================
# 首页路由
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'doctor':
        return redirect(url_for('doctor_dashboard'))
    else:
        return redirect(url_for('patient_dashboard'))


# ============================================================
# 登录/注册/退出
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if role and user.role != role:
                flash('该用户不是此角色，请检查角色选择', 'danger')
                return render_template('login.html')
            
            login_user(user)
            flash(f'欢迎回来，{user.name}！', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        name = request.form.get('name')
        role = request.form.get('role')
        phone = request.form.get('phone')
        
        if password != confirm_password:
            flash('两次输入的密码不一致', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'danger')
            return render_template('register.html')
        
        user = User(username=username, name=name, role=role, phone=phone)
        user.set_password(password)
        
        if role == 'patient':
            user.gender = request.form.get('gender')
            user.age = request.form.get('age', type=int)
            user.address = request.form.get('address')
        
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功，请登录', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('index'))


# ============================================================
# 管理员功能
# ============================================================

@app.route('/admin/dashboard')
@login_required
@role_required('admin')
# TODO: 后续可以加图表统计
# 管理员首页 - 显示系统概览
def admin_dashboard():
    total_doctors = User.query.filter_by(role='doctor').count()
    total_patients = User.query.filter_by(role='patient').count()
    total_appointments = Appointment.query.count()
    today_appointments = Appointment.query.filter_by(appointment_date=date.today()).count()
    low_stock_drugs = Drug.query.filter(Drug.stock < 50).count()
    
    # 最近预约
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(10).all()
    
    # 各科室医生数量
    departments = db.session.query(User.department, db.func.count(User.id)).filter(
        User.role == 'doctor', User.department.isnot(None)
    ).group_by(User.department).all()
    
    return render_template('admin/dashboard.html', 
                         total_doctors=total_doctors,
                         total_patients=total_patients,
                         total_appointments=total_appointments,
                         today_appointments=today_appointments,
                         low_stock_drugs=low_stock_drugs,
                         recent_appointments=recent_appointments,
                         departments=departments)


@app.route('/admin/doctors')
@login_required
@role_required('admin')
def admin_doctors():
    page = request.args.get('page', 1, type=int)
    doctors = User.query.filter_by(role='doctor').paginate(page=page, per_page=10)
    departments = Department.query.all()
    return render_template('admin/doctors.html', doctors=doctors, departments=departments)


@app.route('/admin/doctor/add', methods=['POST'])
@login_required
@role_required('admin')
def admin_add_doctor():
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    department = request.form.get('department')
    title = request.form.get('title')
    phone = request.form.get('phone')
    email = request.form.get('email')
    description = request.form.get('description')
    
    if User.query.filter_by(username=username).first():
        flash('用户名已存在', 'danger')
        return redirect(url_for('admin_doctors'))
    
    doctor = User(username=username, name=name, role='doctor',
                  department=department, title=title,
                  phone=phone, email=email, description=description)
    doctor.set_password(password)
    
    db.session.add(doctor)
    db.session.commit()
    flash('医生添加成功', 'success')
    return redirect(url_for('admin_doctors'))


@app.route('/admin/doctor/edit/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_edit_doctor(id):
    doctor = User.query.get_or_404(id)
    doctor.name = request.form.get('name')
    doctor.department = request.form.get('department')
    doctor.title = request.form.get('title')
    doctor.phone = request.form.get('phone')
    doctor.email = request.form.get('email')
    doctor.description = request.form.get('description')
    
    if request.form.get('password'):
        doctor.set_password(request.form.get('password'))
    
    db.session.commit()
    flash('医生信息更新成功', 'success')
    return redirect(url_for('admin_doctors'))


@app.route('/admin/doctor/delete/<int:id>')
@login_required
@role_required('admin')
def admin_delete_doctor(id):
    doctor = User.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    flash('医生已删除', 'success')
    return redirect(url_for('admin_doctors'))


@app.route('/admin/patients')
@login_required
@role_required('admin')
def admin_patients():
    page = request.args.get('page', 1, type=int)
    patients = User.query.filter_by(role='patient').paginate(page=page, per_page=10)
    return render_template('admin/patients.html', patients=patients)


@app.route('/admin/appointments')
@login_required
@role_required('admin')
def admin_appointments():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    query = Appointment.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    appointments = query.order_by(Appointment.appointment_date.desc()).paginate(page=page, per_page=15)
    return render_template('admin/appointments.html', appointments=appointments, status_filter=status_filter)


@app.route('/admin/appointment/status/<int:id>/<status>')
@login_required
@role_required('admin')
def admin_update_appointment_status(id, status):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = status
    db.session.commit()
    flash('预约状态已更新', 'success')
    return redirect(url_for('admin_appointments'))


@app.route('/admin/drugs')
@login_required
@role_required('admin')
def admin_drugs():
    page = request.args.get('page', 1, type=int)
    drugs = Drug.query.order_by(Drug.name).paginate(page=page, per_page=10)
    return render_template('admin/drugs.html', drugs=drugs)


@app.route('/admin/drug/add', methods=['POST'])
@login_required
@role_required('admin')
def admin_add_drug():
    drug = Drug(
        name=request.form.get('name'),
        specification=request.form.get('specification'),
        manufacturer=request.form.get('manufacturer'),
        price=request.form.get('price', type=float),
        stock=request.form.get('stock', type=int),
        description=request.form.get('description')
    )
    db.session.add(drug)
    db.session.commit()
    flash('药品添加成功', 'success')
    return redirect(url_for('admin_drugs'))


@app.route('/admin/drug/edit/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_edit_drug(id):
    drug = Drug.query.get_or_404(id)
    drug.name = request.form.get('name')
    drug.specification = request.form.get('specification')
    drug.manufacturer = request.form.get('manufacturer')
    drug.price = request.form.get('price', type=float)
    drug.stock = request.form.get('stock', type=int)
    drug.description = request.form.get('description')
    db.session.commit()
    flash('药品信息更新成功', 'success')
    return redirect(url_for('admin_drugs'))


@app.route('/admin/drug/delete/<int:id>')
@login_required
@role_required('admin')
def admin_delete_drug(id):
    drug = Drug.query.get_or_404(id)
    db.session.delete(drug)
    db.session.commit()
    flash('药品已删除', 'success')
    return redirect(url_for('admin_drugs'))


@app.route('/admin/departments')
@login_required
@role_required('admin')
def admin_departments():
    departments = Department.query.all()
    return render_template('admin/departments.html', departments=departments)


@app.route('/admin/department/add', methods=['POST'])
@login_required
@role_required('admin')
def admin_add_department():
    dept = Department(
        name=request.form.get('name'),
        description=request.form.get('description'),
        location=request.form.get('location')
    )
    db.session.add(dept)
    db.session.commit()
    flash('科室添加成功', 'success')
    return redirect(url_for('admin_departments'))


@app.route('/admin/department/delete/<int:id>')
@login_required
@role_required('admin')
def admin_delete_department(id):
    dept = Department.query.get_or_404(id)
    db.session.delete(dept)
    db.session.commit()
    flash('科室已删除', 'success')
    return redirect(url_for('admin_departments'))


@app.route('/admin/schedules')
@login_required
@role_required('admin')
def admin_schedules():
    doctors = User.query.filter_by(role='doctor').all()
    schedules = Schedule.query.order_by(Schedule.work_date.desc()).limit(50).all()
    return render_template('admin/schedules.html', doctors=doctors, schedules=schedules)


@app.route('/admin/schedule/add', methods=['POST'])
@login_required
@role_required('admin')
def admin_add_schedule():
    schedule = Schedule(
        doctor_id=request.form.get('doctor_id', type=int),
        work_date=datetime.strptime(request.form.get('work_date'), '%Y-%m-%d').date(),
        time_slot=request.form.get('time_slot'),
        max_patients=request.form.get('max_patients', type=int)
    )
    db.session.add(schedule)
    db.session.commit()
    flash('排班添加成功', 'success')
    return redirect(url_for('admin_schedules'))


@app.route('/admin/schedule/delete/<int:id>')
@login_required
@role_required('admin')
def admin_delete_schedule(id):
    schedule = Schedule.query.get_or_404(id)
    db.session.delete(schedule)
    db.session.commit()
    flash('排班已删除', 'success')
    return redirect(url_for('admin_schedules'))


@app.route('/admin/medical-records')
@login_required
@role_required('admin')
def admin_medical_records():
    page = request.args.get('page', 1, type=int)
    records = MedicalRecord.query.order_by(MedicalRecord.created_at.desc()).paginate(page=page, per_page=15)
    return render_template('admin/medical_records.html', records=records)


@app.route('/admin/export/appointments')
@login_required
@role_required('admin')
def admin_export_appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['编号', '病人', '医生', '日期', '时段', '状态', '创建时间'])
    
    for a in appointments:
        writer.writerow([
            a.id,
            a.patient.name if a.patient else '未知',
            a.doctor.name if a.doctor else '未知',
            a.appointment_date,
            a.time_slot,
            a.status,
            a.created_at
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'appointments_{date.today()}.csv'
    )


@app.route('/admin/export/drugs')
@login_required
@role_required('admin')
def admin_export_drugs():
    drugs = Drug.query.order_by(Drug.name).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['编号', '药品名称', '规格', '生产厂家', '价格', '库存'])
    
    for drug in drugs:
        writer.writerow([drug.id, drug.name, drug.specification, drug.manufacturer, drug.price, drug.stock])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'drugs_{date.today()}.csv'
    )


# ============================================================
# 医生功能
# ============================================================

@app.route('/doctor/dashboard')
@login_required
@role_required('doctor')
def doctor_dashboard():
    today = date.today()
    
    # 今日预约
    today_appointments = Appointment.query.filter_by(
        doctor_id=current_user.id,
        appointment_date=today
    ).order_by(Appointment.time_slot).all()
    
    # 待处理预约
    pending_appointments = Appointment.query.filter_by(
        doctor_id=current_user.id,
        status='pending'
    ).count()
    
    # 已完成病历数
    completed_records = MedicalRecord.query.filter_by(
        doctor_id=current_user.id
    ).count()
    
    # 本周排班
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    week_schedules = Schedule.query.filter(
        Schedule.doctor_id == current_user.id,
        Schedule.work_date.between(week_start, week_end)
    ).order_by(Schedule.work_date).all()
    
    return render_template('doctor/dashboard.html',
                         today_appointments=today_appointments,
                         pending_appointments=pending_appointments,
                         completed_records=completed_records,
                         week_schedules=week_schedules)


@app.route('/doctor/appointments')
@login_required
@role_required('doctor')
def doctor_appointments():
    status = request.args.get('status', '')
    page = request.args.get('page', 1, type=int)
    
    query = Appointment.query.filter_by(doctor_id=current_user.id)
    if status:
        query = query.filter_by(status=status)
    
    appointments = query.order_by(Appointment.appointment_date.desc()).paginate(page=page, per_page=10)
    return render_template('doctor/appointments.html', appointments=appointments, status_filter=status)


@app.route('/doctor/appointment/confirm/<int:id>')
@login_required
@role_required('doctor')
def doctor_confirm_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.doctor_id != current_user.id:
        flash('您没有权限操作此预约', 'danger')
        return redirect(url_for('doctor_appointments'))
    
    appointment.status = 'confirmed'
    db.session.commit()
    flash('预约已确认', 'success')
    return redirect(url_for('doctor_appointments'))


@app.route('/doctor/appointment/complete/<int:id>')
@login_required
@role_required('doctor')
def doctor_complete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.doctor_id != current_user.id:
        flash('您没有权限操作此预约', 'danger')
        return redirect(url_for('doctor_appointments'))
    
    appointment.status = 'completed'
    db.session.commit()
    flash('就诊已完成，请填写病历', 'success')
    return redirect(url_for('doctor_add_record', appointment_id=id))


@app.route('/doctor/records')
@login_required
@role_required('doctor')
def doctor_records():
    page = request.args.get('page', 1, type=int)
    records = MedicalRecord.query.filter_by(
        doctor_id=current_user.id
    ).order_by(MedicalRecord.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('doctor/records.html', records=records)


@app.route('/doctor/record/add', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def doctor_add_record():
    appointment_id = request.args.get('appointment_id', type=int)
    appointment = Appointment.query.get_or_404(appointment_id) if appointment_id else None
    
    if request.method == 'POST':
        record = MedicalRecord(
            patient_id=request.form.get('patient_id', type=int),
            doctor_id=current_user.id,
            appointment_id=request.form.get('appointment_id', type=int),
            diagnosis=request.form.get('diagnosis'),
            prescription=request.form.get('prescription'),
            notes=request.form.get('notes')
        )
        db.session.add(record)
        
        # 更新预约状态
        if record.appointment_id:
            apt = Appointment.query.get(record.appointment_id)
            if apt:
                apt.status = 'completed'
        
        db.session.commit()
        flash('病历已创建', 'success')
        return redirect(url_for('doctor_records'))
    
    patients = User.query.filter_by(role='patient').all()
    return render_template('doctor/add_record.html', appointment=appointment, patients=patients)


@app.route('/doctor/record/view/<int:id>')
@login_required
@role_required('doctor')
def doctor_view_record(id):
    record = MedicalRecord.query.get_or_404(id)
    return render_template('doctor/view_record.html', record=record)


@app.route('/doctor/schedule')
@login_required
@role_required('doctor')
def doctor_schedule():
    schedules = Schedule.query.filter_by(
        doctor_id=current_user.id
    ).order_by(Schedule.work_date).all()
    return render_template('doctor/schedule.html', schedules=schedules)


# ============================================================
# 病人功能
# ============================================================

@app.route('/patient/dashboard')
@login_required
@role_required('patient')
def patient_dashboard():
    # 我的预约
    my_appointments = Appointment.query.filter_by(
        patient_id=current_user.id
    ).order_by(Appointment.appointment_date.desc()).limit(5).all()
    
    # 我的病历
    my_records = MedicalRecord.query.filter_by(
        patient_id=current_user.id
    ).order_by(MedicalRecord.created_at.desc()).limit(5).all()
    
    return render_template('patient/dashboard.html',
                         my_appointments=my_appointments,
                         my_records=my_records)


@app.route('/patient/appointments')
@login_required
@role_required('patient')
def patient_appointments():
    page = request.args.get('page', 1, type=int)
    appointments = Appointment.query.filter_by(
        patient_id=current_user.id
    ).order_by(Appointment.appointment_date.desc()).paginate(page=page, per_page=10)
    return render_template('patient/appointments.html', appointments=appointments)


@app.route('/patient/appointment/book', methods=['GET', 'POST'])
@login_required
@role_required('patient')
# 预约挂号 - 病人端
def patient_book_appointment():
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id', type=int)
        appointment_date = datetime.strptime(request.form.get('appointment_date'), '%Y-%m-%d').date()
        time_slot = request.form.get('time_slot')
        symptom = request.form.get('symptom')
        
        # 检查排班
        schedule = Schedule.query.filter_by(
            doctor_id=doctor_id,
            work_date=appointment_date,
            time_slot=time_slot
        ).first()
        
        if schedule and schedule.current_count >= schedule.max_patients:
            flash('该时段预约已满，请选择其他时间', 'danger')
            return redirect(url_for('patient_book_appointment'))
        
        # 检查是否已预约
        existing = Appointment.query.filter_by(
            patient_id=current_user.id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            time_slot=time_slot
        ).first()
        
        if existing:
            flash('您已预约该时段，请勿重复预约', 'danger')
            return redirect(url_for('patient_book_appointment'))
        
        appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            time_slot=time_slot,
            symptom=symptom
        )
        db.session.add(appointment)
        
        # 更新排班计数
        if schedule:
            schedule.current_count += 1
        
        db.session.commit()
        flash('预约成功！请按时就诊', 'success')
        return redirect(url_for('patient_appointments'))
    
    departments = Department.query.all()
    doctors = User.query.filter_by(role='doctor').all()
    return render_template('patient/book_appointment.html', departments=departments, doctors=doctors)


@app.route('/patient/appointment/cancel/<int:id>')
@login_required
@role_required('patient')
def patient_cancel_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.patient_id != current_user.id:
        flash('您没有权限操作此预约', 'danger')
        return redirect(url_for('patient_appointments'))
    
    if appointment.status in ['completed', 'cancelled']:
        flash('该预约无法取消', 'danger')
        return redirect(url_for('patient_appointments'))
    
    appointment.status = 'cancelled'
    
    # 更新排班计数
    schedule = Schedule.query.filter_by(
        doctor_id=appointment.doctor_id,
        work_date=appointment.appointment_date,
        time_slot=appointment.time_slot
    ).first()
    if schedule and schedule.current_count > 0:
        schedule.current_count -= 1
    
    db.session.commit()
    flash('预约已取消', 'success')
    return redirect(url_for('patient_appointments'))


@app.route('/patient/records')
@login_required
@role_required('patient')
def patient_records():
    page = request.args.get('page', 1, type=int)
    records = MedicalRecord.query.filter_by(
        patient_id=current_user.id
    ).order_by(MedicalRecord.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('patient/records.html', records=records)


@app.route('/patient/record/view/<int:id>')
@login_required
@role_required('patient')
def patient_view_record(id):
    record = MedicalRecord.query.get_or_404(id)
    if record.patient_id != current_user.id:
        flash('您没有权限查看此病历', 'danger')
        return redirect(url_for('patient_records'))
    return render_template('patient/view_record.html', record=record)


@app.route('/patient/doctors')
@login_required
@role_required('patient')
def patient_doctors():
    department = request.args.get('department', '')
    query = User.query.filter_by(role='doctor')
    if department:
        query = query.filter_by(department=department)
    doctors = query.all()
    departments = Department.query.all()
    return render_template('patient/doctors.html', doctors=doctors, departments=departments)


@app.route('/api/doctors')
def api_doctors():
    department = request.args.get('department', '')
    doctor_id = request.args.get('id', type=int)
    query = User.query.filter_by(role='doctor')
    if department:
        query = query.filter_by(department=department)
    if doctor_id:
        query = query.filter_by(id=doctor_id)
    doctors = query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'department': d.department,
        'title': d.title,
        'phone': d.phone,
        'email': d.email,
        'description': d.description
    } for d in doctors])


@app.route('/api/schedules')
def api_schedules():
    doctor_id = request.args.get('doctor_id', type=int)
    date_str = request.args.get('date', '')
    
    if not doctor_id or not date_str:
        return jsonify([])
    
    query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    schedules = Schedule.query.filter_by(
        doctor_id=doctor_id,
        work_date=query_date
    ).all()
    
    return jsonify([{
        'id': s.id,
        'time_slot': s.time_slot,
        'max_patients': s.max_patients,
        'current_count': s.current_count,
        'available': s.current_count < s.max_patients
    } for s in schedules])


@app.route('/api/drugs')
def api_drugs():
    drug_id = request.args.get('id', type=int)
    query = Drug.query
    if drug_id:
        query = query.filter_by(id=drug_id)
    drugs = query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'specification': d.specification,
        'manufacturer': d.manufacturer,
        'price': d.price,
        'stock': d.stock,
        'description': d.description
    } for d in drugs])


# ============================================================
# 数据库初始化
# ============================================================

def init_db():
    """初始化数据库，创建默认账号和数据"""
    """初始化数据库并创建默认数据"""
    with app.app_context():
        db.create_all()
        
        # 创建默认管理员
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                name='系统管理员',
                role='admin',
                phone='13800000000',
                email='admin@hospital.com'
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # 创建默认科室
        default_departments = [
            {'name': '内科', 'description': '内科疾病诊治', 'location': '门诊楼2层'},
            {'name': '外科', 'description': '外科疾病诊治', 'location': '门诊楼3层'},
            {'name': '儿科', 'description': '儿童疾病诊治', 'location': '门诊楼1层'},
            {'name': '妇产科', 'description': '妇科及产科疾病诊治', 'location': '门诊楼4层'},
            {'name': '眼科', 'description': '眼科疾病诊治', 'location': '门诊楼5层'},
            {'name': '口腔科', 'description': '口腔疾病诊治', 'location': '门诊楼5层'},
            {'name': '皮肤科', 'description': '皮肤疾病诊治', 'location': '门诊楼4层'},
            {'name': '中医科', 'description': '中医诊治与调理', 'location': '门诊楼6层'},
        ]
        
        for dept_data in default_departments:
            if not Department.query.filter_by(name=dept_data['name']).first():
                dept = Department(**dept_data)
                db.session.add(dept)
        
        # 创建默认医生
        default_doctors = [
            {'username': 'doctor1', 'name': '张医生', 'department': '内科', 'title': '主任医师', 'phone': '13800000001'},
            {'username': 'doctor2', 'name': '李医生', 'department': '外科', 'title': '副主任医师', 'phone': '13800000002'},
            {'username': 'doctor3', 'name': '王医生', 'department': '儿科', 'title': '主治医师', 'phone': '13800000003'},
            {'username': 'doctor4', 'name': '赵医生', 'department': '妇产科', 'title': '主任医师', 'phone': '13800000004'},
            {'username': 'doctor5', 'name': '刘医生', 'department': '眼科', 'title': '主治医师', 'phone': '13800000005'},
        ]
        
        for doc_data in default_doctors:
            if not User.query.filter_by(username=doc_data['username']).first():
                doctor = User(
                    username=doc_data['username'],
                    name=doc_data['name'],
                    role='doctor',
                    department=doc_data['department'],
                    title=doc_data['title'],
                    phone=doc_data['phone']
                )
                doctor.set_password('123456')
                db.session.add(doctor)
        
        # 创建默认药品
        default_drugs = [
            {'name': '阿莫西林胶囊', 'specification': '0.5g*24粒', 'manufacturer': '华北制药', 'price': 12.50, 'stock': 500},
            {'name': '布洛芬缓释胶囊', 'specification': '0.3g*20粒', 'manufacturer': '中美史克', 'price': 25.00, 'stock': 300},
            {'name': '头孢克肟片', 'specification': '50mg*12片', 'manufacturer': '广州白云山', 'price': 18.00, 'stock': 200},
            {'name': '感冒灵颗粒', 'specification': '10g*9袋', 'manufacturer': '三九医药', 'price': 15.80, 'stock': 400},
            {'name': '维生素C片', 'specification': '100mg*100片', 'manufacturer': '东北制药', 'price': 5.00, 'stock': 1000},
            {'name': '硝苯地平片', 'specification': '10mg*30片', 'manufacturer': '上海医药', 'price': 8.50, 'stock': 600},
            {'name': '阿司匹林肠溶片', 'specification':'100mg*30片', 'manufacturer': '拜耳医药', 'price': 15.00, 'stock': 800},
            {'name': '盐酸二甲双胍片', 'specification': '0.5g*20片', 'manufacturer': '中美上海施贵宝', 'price': 22.00, 'stock': 350},
            {'name': '氯雷他定片', 'specification': '10mg*6片', 'manufacturer': '西安杨森', 'price': 28.00, 'stock': 250},
        ]
        
        for drug_data in default_drugs:
            if not Drug.query.filter_by(name=drug_data['name']).first():
                drug = Drug(**drug_data)
                db.session.add(drug)
        
        db.session.commit()
        print('数据库初始化完成！')


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
