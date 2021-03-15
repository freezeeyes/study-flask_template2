from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from project import db_mysql
import hashlib
from datetime import datetime


auth = Blueprint('auth', __name__)


# サインアップページ - http://localhost:5000/signup
@auth.route('/signup')
def signup():
    if 'uid' in session:
        return redirect(url_for('mypage.profile'))
    return render_template('signup.html')


# ログインページ - http://localhost:5000/login
@auth.route('/login')
def login():
    if 'uid' in session:
        return redirect(url_for('mypage.profile'))
    return render_template('login.html')


# サインアップ処理 - http://localhost:5000/signup
@auth.route('/signup', methods=['POST'])
def signup_post():
    # サインアップページの入力フォームの値を取得する
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    # データベースに接続してカーソルを取得する
    connect = db_mysql.get_connect()
    cursor = connect.cursor()

    # usersテーブルからアカウント情報を取得する
    stmt = 'SELECT * FROM users WHERE email=%s;'
    cursor.execute(stmt, (email,))
    row = cursor.fetchone()

    if row == None:
        # 現在の日時を取得する
        dt = datetime.now()
        # usersテーブルにアカウントを挿入する
        stmt = 'INSERT INTO users(email,password,username,created_at,updated_at) VALUES(%s,%s,%s,%s,%s);'
        # args = (email, hashlib.sha256((str(password)+str(email)).encode('utf-8')).hexdigest(), name, dt, dt)
        args = (email, hashlib.sha256('hogehoge'.encode('utf-8')).hexdigest(), name, dt, dt)
        cursor.execute(stmt, args)
        connect.commit()
    else:
        flash('既にメールアドレスが登録されています。')
        return redirect(url_for('auth.signup'))

    # カーソルとデータベースの接続を切断する
    db_mysql.disconnect(connect, cursor)
    
    return redirect(url_for('auth.login'))


# ログイン処理 - http://localhost:5000/login
@auth.route('/login', methods=['POST'])
def login_post():
    # ログインページの入力フォームの値を取得する
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember')
    print(remember)

    # データベースに接続してカーソルを取得する
    connect = db_mysql.get_connect()
    cursor = connect.cursor()

    # usersテーブルからアカウント情報を取得する
    stmt = 'SELECT * FROM users WHERE email=%s;'
    cursor.execute(stmt, (email,))
    row = cursor.fetchone()

    if row == None:
        # カーソルとデータベースの接続を切断する
        db_mysql.disconnect(connect, cursor)

        flash('アカウントが登録されていません')
        return redirect(url_for('auth.login'))

    # elif row[2] == hashlib.sha256((str(password)+str(email)).encode('utf-8')).hexdigest():
    elif row[2] == hashlib.sha256(str(password).encode('utf-8')).hexdigest():
        # セッションを保存する
        session['uid'] = row[0]
        session['name'] = row[3]
        session['remember'] = True if remember else False

        # カーソルとデータベースの接続を切断する
        db_mysql.disconnect(connect, cursor)
    
        return redirect(url_for('mypage.profile'))

    else:
        # カーソルとデータベースの接続を切断する
        db_mysql.disconnect(connect, cursor)

        flash('メールアドレスまたはパスワードが間違っています。')
        return redirect(url_for('auth.login'))


# ログアウト処理 - http://localhost:5000/logout
@auth.route('/logout')
def logout():
    # セッションを削除する
    session.pop('uid', None)
    session.pop('name', None)
    session.pop('remember', None)
    return redirect(url_for('main.index'))
