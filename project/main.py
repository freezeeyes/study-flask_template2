from flask import Blueprint, render_template


main = Blueprint('main', __name__)


# トップページ - http://localhost:5000/
@main.route('/')
def index():
    return render_template('index.html')
