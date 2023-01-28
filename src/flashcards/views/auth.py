from flask import Blueprint, render_template

auth_blueprint = Blueprint('auth', __name__,
                           template_folder='templates')


@auth_blueprint.route('/auth')
def auth():
    return render_template('auth.html')
