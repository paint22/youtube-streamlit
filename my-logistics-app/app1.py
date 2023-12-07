from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Kudosyo76508321@127.0.0.1/sotuken'
db = SQLAlchemy(app)

# データベースモデルの定義
class sotukentable(db.Model):
    __tablename__ = 'sotuken_table'
    商品コード = db.Column(db.Integer, primary_key=True)  # カラム名を変更
    商品名 = db.Column(db.String(45), nullable=False)     # カラム名を変更
    数量 = db.Column(db.Integer, nullable=False)           # カラム名を変更
    発注日 = db.Column(db.String(45), nullable=False)      # カラム名を変更
    結果 = db.Column(db.String(45))                        # カラム名を変更

# 物流管理システムのルートURLにテーブル情報を表示するためのルートを追加
@app.route('/')
def index():
    # データベースからテーブル情報を取得
    orders = sotukentable.query.all()
    
    # テーブル情報をHTMLテンプレートに渡して表示
    return render_template('index2.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)