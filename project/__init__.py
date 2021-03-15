from flask import Flask
import secrets


# 初期設定
# **********************************************************************

app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)


# 非認証ルートの読み込み
# **********************************************************************

# 主要サービスのルートを読み込む
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

# アカウントページのルートを読み込む
from .mypage import mypage as mypage_blueprint
app.register_blueprint(mypage_blueprint)


# 認証ルートの読み込み
# **********************************************************************

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)
