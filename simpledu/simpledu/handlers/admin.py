from flask import Blueprint,render_template
from simpledu.decorators import admin_required
admin = Blueprint('admin',__name__,url_prefix='/admin')

@admin.route('/')
@admin_required
def admin_index():
    return  render_template('admin/index.html')