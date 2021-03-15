import MySQLdb


# データベースの接続情報
DB_USERNAME = ''
DB_PASSWORD = ''
DB_HOSTNAME = ''
DB_DATABASE = ''


def get_connect():
    return MySQLdb.connect(user=DB_USERNAME, passwd=DB_PASSWORD, host=DB_HOSTNAME, db=DB_DATABASE)


def disconnect(connect, cursor):
    cursor.close()
    connect.close()


if __name__ == '__main__':
    # TODO: データベースにテーブルを作成する

    import hashlib
    from datetime import datetime

    # 現在の日時を取得する
    now = datetime.now()

    # データベースに接続してカーソルを取得する
    connect = get_connect()
    cursor = connect.cursor()

    # usersテーブルの削除
    cursor.execute('DROP TABLE IF EXISTS users;')

    # usersテーブルの作成
    stmt = '''
    CREATE TABLE users (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(100) NOT NULL,
        password VARCHAR(100) NOT NULL,
        username VARCHAR(100) NOT NULL,
        created_at datetime DEFAULT NULL,
        updated_at datetime DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    '''
    cursor.execute(stmt)

    # 仮ユーザの追加
    hashpass = hashlib.sha256('hogehoge'.encode('utf-8')).hexdigest()
    stmt = 'INSERT INTO users(email,password,username,created_at,updated_at) VALUES(%s,%s,%s,%s,%s);'
    cursor.executemany(
        stmt,
        [
            ('ito@g.com', hashpass, 'ito', now, now),
            ('kato@g.com', hashpass, 'kato', now, now),
            ('sato@g.com', hashpass, 'sato', now, now),
        ]
    )
    connect.commit()

    # カーソルとデータベースの接続を切断する
    disconnect(connect, cursor)
