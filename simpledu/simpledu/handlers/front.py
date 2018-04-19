from flask import Blueprint,render_template,redirect,flash,url_for,request
from simpledu.models import User,Course
from simpledu.forms import LoginForm, RegisterForm
from flask_login import login_user,logout_user,login_required
from flask import request, current_app

front = Blueprint('front',__name__)

@front.route('/')
def index():
    page = request.args.get('page',default=1,type=int)
    pagination = Course.query.paginate(
        page=page,
        per_page = current_app.config['INDEX_PER_PAGE'],
        error_out=True
    )
    return render_template('index.html',pagination=pagination)

@front.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.username.data.isalnum())
        if not form.username.data.isalnum():
            flash('username not all number',category='danger')
        else:
            form.create_user()
            flash('注册成功，请登录！','success')
            return redirect(url_for('.login'))
    return render_template('register.html',form=form)


@front.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user,form.remember_me)
        return redirect(url_for('.index'))
    else:
        return render_template('login.html',form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录','success')
    return redirect(url_for('.index'))
