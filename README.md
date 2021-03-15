# study-flask_template2

Flask学習用のテンプレートプロジェクトです。

ユーザ機能は実装済みで、必要に応じてusersテーブルを修正してください。

データベースはMySQLを使用しています。

※現時点では、セッションが弱い設定になっているため注意が必要です。

## データベースの構築

以下のファイルに、MySQLの接続に必要な設定を記述してください。

データベースのテーブル作成は、直接作成するか、ファイル末尾のif文内に記述してpythonファイルを実行するかしてください。

`project/db_mysql.py`

```project/db_mysql.py
# データベースの接続情報
DB_USERNAME = ''
DB_PASSWORD = ''
DB_HOSTNAME = ''
DB_DATABASE = ''
```
