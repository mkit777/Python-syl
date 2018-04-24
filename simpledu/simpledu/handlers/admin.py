from flask import Blueprint,render_template,request,current_app, flash,redirect, url_for
from simpledu.decorators import admin_required
from flask_login import login_required
from simpledu.models import Course,db,User,Live
from simpledu.forms import CourseForm,UserForm,LiveForm,MessageForm
from simpledu.handlers.ws import redis
import json
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

@admin.route('/lives')
@admin_required
def lives():
    page = request.args.get('page',default=0,type=int)
    pagination = Live.query.paginate(page=page, per_page=10,error_out=False)
    return render_template('admin/lives.html',pagination=pagination)

@admin.route('/lives/add',methods=['GET','POST'])
@admin_required
def create_live():
    form = LiveForm()
    if form.validate_on_submit():
        form.create_live()
        flash('add live successfully','success')
        return redirect(url_for('admin.lives'))
    return render_template('admin/add_live.html',form=form)

@admin.route('/lives/<int:live_id>/edit', methods=['GET','POST'])
@admin_required
def edit_live(live_id):
    live = Live.query.get_or_404(live_id)
    form = LiveForm(obj=live)
    form.liver_name.data = live.liver.username
    if form.is_submitted():
        form.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        flash('edit live sunccessfully','success')
        return redirect(url_for('admin.lives'))
    else:
        return render_template('admin/edit_live.html',form=form)


@admin.route('/lives/<int:live_id>/delet')
@admin_required
def delete_live(live_id):
    live = Live.query.get_or_404(live_id)
    db.session.delete(live)
    db.session.commit()
    flash('删除成功','sunccess')
    return redirect(url_for('admin.lives'))

@admin.route('/message',methods=['GET','POST'])
@admin_required
def message():
    form = MessageForm()
    if form.validate_on_submit():
        redis.publish('chat',json.dumps({'username':'System','text':form.text.data}))
        flash('发送成功','success')
        return redirect(url_for('admin.message'))
    return render_template('admin/message.html',form=form)


