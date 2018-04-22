from flask import Blueprint,render_template,request,current_app, flash,redirect, url_for
from simpledu.decorators import admin_required
from flask_login import login_required
from simpledu.models import Course,db,User
from simpledu.forms import CourseForm,UserForm
admin = Blueprint('admin',__name__,url_prefix='/admin')

@admin.route('/')
@login_required
def admin_index():
    return render_template('admin/index.html')

@admin.route('/courses')
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False
    )
    return render_template('admin/courses.html', pagination=pagination)

@admin.route('/courses/create', methods=['GET','POST'])
@admin_required
def create_course():
    form = CourseForm()
    print(form)
    if form.validate_on_submit():
        form.create_course()
        flash('课程创建成功','success')
        return redirect(url_for('admin.courses'))
    else:
        return render_template('admin/create_course.html', form=form)

@admin.route('/courses/<int:course_id>/edit', methods=['GET','POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('课程更新成功', 'success')
        return redirect(url_for('admin.courses'))
    else:
        return render_template('admin/edit_course.html', form=form, course= course)

@admin.route('/courses/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('课程删除成功', 'success')
    return redirect(url_for('admin.courses'))

@admin.route('/users')
@admin_required
def users():
    pagination = User.query.paginate(
        page = request.args.get('page',default=1,type=int),
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = True
    )
    return render_template('admin/users.html',pagination=pagination)

@admin.route('/users/add_user', methods=['GET','POST'])
@admin_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        form.add_user()
        flash('添加成功', 'success')
        return redirect(url_for('admin.users'))
    else:
        return render_template('admin/add_user.html',form=form)

@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('课程更新成功','success')
        return redirect(url_for('admin.users'))
    else:
        return render_template('admin/edit_user.html',form=form,user=user)

@admin.route('/users/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.users'))