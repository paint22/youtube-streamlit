import mysql.connector

# データベースに接続
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Kudosyo76508321",
    database="sotuken"
)

# データベースの文字エンコーディング情報を取得
cursor = connection.cursor()
cursor.execute("SELECT @@character_set_database, @@collation_database")
encoding_info = cursor.fetchone()

# 結果を表示
print("データベースの文字エンコーディング:", encoding_info[0])
print("データベースの照合順序:", encoding_info[1])

# 接続を閉じる
cursor.close()
connection.close()