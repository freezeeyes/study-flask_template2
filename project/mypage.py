from flask import Blueprint, render_template, redirect, url_for, session


mypage = Blueprint('mypage', __name__)


# マイページ - http://localhost:5000/profile
@mypage.route('/profile')
def profile():
    if 'uid' in session:
        return render_template('profile.html')
    return redirect(url_for('auth.login'))
