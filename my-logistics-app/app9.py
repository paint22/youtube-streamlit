from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__, static_folder='static')

# データベースに接続
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Kudosyo76508321",
    database="sotuken"
)

# データベースカーソルを作成
cursor = connection.cursor()

# ホームページ用のルート
@app.route('/')
def home():
    # データベースからデータを取得
    cursor.execute("SELECT * FROM sotuken_table")
    orders = cursor.fetchall()

    # テンプレートにデータを渡してレンダリング
    return render_template('index2.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)