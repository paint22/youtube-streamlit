from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Kudosyo76508321@127.0.0.1/sotuken'
db = SQLAlchemy(app)

# データベースモデルの定義
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_code = db.Column(db.String(50), nullable=False)
    material_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# 発注をデータベースに追加するエンドポイント
@app.route('/add_order', methods=['POST'])
def add_order():
    data = request.get_json()
    material_code = data['material_code']
    material_name = data['material_name']
    quantity = data['quantity']

    order = Order(material_code=material_code, material_name=material_name, quantity=quantity)
    db.session.add(order)
    db.session.commit()

    return jsonify(message="発注が追加されました")

# 物流管理システムから発注情報を取得するエンドポイント
@app.route('/get_orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    order_list = []
    for order in orders:
        order_data = {
            'material_code': order.material_code,
            'material_name': order.material_name,
            'quantity': order.quantity
        }
        order_list.append(order_data)

    return jsonify(orders=order_list)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)