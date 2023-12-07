from flask import Flask, request, jsonify, render_template, send_file, redirect, send_from_directory, make_response
from werkzeug.utils import secure_filename
import mysql.connector
import os
from io import BytesIO
import base64
import logging
import qrcode
import uuid

app = Flask(__name__, template_folder='templates')
app.logger.setLevel(logging.DEBUG)

# アップロードフォルダの設定
UPLOAD_FOLDER = 'c:\\Users\\kudosyo\\Desktop\\プロジェクト1\\my-goods-app\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# QRコードの保存場所を設定
QR_CODE_FOLDER = 'c:\\Users\\kudosyo\\Desktop\\プロジェクト1\\my-goods-app\\qrcodes'
app.config['QR_CODE_FOLDER'] = QR_CODE_FOLDER

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

mysql_config = {
    'user': 'root',
    'password': 'Kudosyo76508321',
    'host': '127.0.0.1',
    'database': '物品',
    'raise_on_warnings': True,
    'pool_size': 5
}

conn_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", **mysql_config)


def get_connection():
    return conn_pool.get_connection()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_loaded_file(file, upload_folder):
    if file and file.filename:
        # ファイル名の生成
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    return None


def generate_qr_code(data, path_to_save):
    # QR コードオブジェクトの生成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # QR コードイメージの生成
    img = qr.make_image(fill='black', back_color='white')

    # QR コードイメージの保存
    img.save(path_to_save)

@app.route('/')
def home():
    return render_template('物品管理.html')


@app.route('/api/get_items', methods=['GET'])
def get_items():
    field = request.args.get('field')
    text = request.args.get('text')
    valid_fields = ['物品名', '保管場所', '状態', '管理責任者', '整理番号', '規格', '製造番号', '製造元', '購入先', '所属']
    if field and field not in valid_fields:
        return jsonify({'error': '無効な検索フィールド'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if field and text:
            select_query = f"SELECT * FROM goods WHERE {field} LIKE %s"
            cursor.execute(select_query, (f"%{text}%",))
        else:
            select_query = "SELECT * FROM goods"
            cursor.execute(select_query)

        items = cursor.fetchall()
        cursor.close()
        conn.close()

        formatted_items = []
        for item in items:
            formatted_item = {
                'ID': item['ID'],
                '購入日': item['購入日'],
                'コード': item['コード'],
                '整理番号': item['整理番号'],
                'ST数量': item['ST数量'],
                '物品名': item['物品名'],
                '規格': item['規格'],
                '製造番号': item['製造番号'],
                '製造先': item['製造先'],
                '保管場所': item['保管場所'],
                '単価': item['単価'],
                '金額': item['金額'],
                '納入日': item['納入日'],
                '支払日': item['支払日'],
                '購入先': item['購入先'],
                '所属': item['所属'],
                '前所属': item['前所属'],
                '管理責任者': item['管理責任者'],
                '前任者': item['前任者'],
                '状態': item['状態'],
                '写真': os.path.basename(item['写真']) if item.get('写真') else None,
                'QRコード': os.path.basename(item['QRコード']) if item.get('QRコード') else None
            }
            formatted_items.append(formatted_item)

        return jsonify(formatted_items)

    except Exception as e:
        app.logger.error(f'エラーが発生しました: {str(e)}')
        return jsonify({'error': 'データの取得中にエラーが発生しました.'}), 500




@app.route('/api/edit_item/<int:item_id>', methods=['POST'])
def edit_item(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        data = request.form

        def convert_int(value):
            try:
                return int(value) if value else None
            except ValueError:
                return None

        # データの取得と変換
        購入日 = data.get('購入日') or None
        コード = data.get('コード')
        整理番号 = convert_int(data.get('整理番号'))
        ST数量 = data.get('ST数量')
        物品名 = data.get('物品名')
        規格 = data.get('規格')
        製造番号 = convert_int(data.get('製造番号'))
        製造先 = convert_int(data.get('製造先'))
        保管場所 = convert_int(data.get('保管場所'))
        単価 = convert_int(data.get('単価'))
        金額 = data.get('金額')
        納入日 = data.get('納入日') or None
        支払日 = data.get('支払日') or None
        購入先 = data.get('購入先')
        所属 = data.get('所属')
        前所属 = data.get('前所属')
        管理責任者 = convert_int(data.get('管理責任者'))
        前任者 = convert_int(data.get('前任者'))
        状態 = data.get('状態')

        # 更新クエリ
        update_query = """
            UPDATE goods 
            SET 
                購入日 = COALESCE(%s, 購入日), 
                コード = %s, 
                整理番号 = %s, 
                ST数量 = %s, 
                物品名 = %s, 
                規格 = %s, 
                製造番号 = %s, 
                製造先 = %s, 
                保管場所 = %s, 
                単価 = %s, 
                金額 = %s, 
                納入日 = COALESCE(%s, 納入日), 
                支払日 = COALESCE(%s, 支払日), 
                購入先 = %s, 
                所属 = %s, 
                前所属 = %s, 
                管理責任者 = %s, 
                前任者 = %s, 
                状態 = %s 
            WHERE ID = %s
        """
        cursor.execute(update_query, (
            購入日, コード, 整理番号, ST数量, 物品名, 規格, 製造番号, 製造先, 保管場所, 単価, 金額, 納入日, 支払日, 購入先, 所属, 前所属, 管理責任者, 前任者, 状態, item_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': '物品が正常に編集されました。'})

    except Exception as e:
        app.logger.error(f'エラーが発生しました: {str(e)}')
        return jsonify({'error': '変更の保存中にエラーが発生しました: ' + str(e)}), 500


# アイテムの写真を取得するエンドポイント
@app.route('/api/get_photo/<int:item_id>', methods=['GET'])
def get_photo(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        select_query = "SELECT 写真 FROM goods WHERE ID = %s"
        cursor.execute(select_query, (item_id,))
        item = cursor.fetchone()

        cursor.close()
        conn.close()

        if item and item['写真']:
            # 写真ファイルのパスを取得
            photo_path = item['写真']

            # 写真ファイルを直接クライアントに返す
            return send_file(photo_path, as_attachment=False)

        else:
            return jsonify({'error': '写真が見つかりません。'}), 404
    except Exception as e:
        app.logger.error('エラーが発生しました: %s', str(e))
        return jsonify({'error': '写真の取得中にエラーが発生しました。'}), 500

@app.route('/api/get_qrcode/<int:item_id>', methods=['GET'])
def get_qrcode(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        select_query = "SELECT QRコード FROM goods WHERE ID = %s"
        cursor.execute(select_query, (item_id,))
        item = cursor.fetchone()

        cursor.close()
        conn.close()

        if item and item['QRコード']:
            qr_full_path = item['QRコード']
            app.logger.debug(f'QR Code path: {qr_full_path}')  # パスをログに出力
            return send_file(qr_full_path, as_attachment=False)
        else:
            return jsonify({'error': 'QRコードが見つかりません。'}), 404
    except Exception as e:
        app.logger.error('エラーが発生しました: %s', str(e))
        return jsonify({'error': 'QRコードの取得中にエラーが発生しました。'}), 500
    
@app.route('/upload_photo/<int:item_id>', methods=['POST'])
def upload_photo(item_id):
    try:
        photo_file = request.files['photo']
        if photo_file and allowed_file(photo_file.filename):
            filename = secure_filename(photo_file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            photo_file.save(file_path)

            conn = get_connection()
            cursor = conn.cursor()
            update_query = "UPDATE goods SET 写真 = %s WHERE ID = %s"
            cursor.execute(update_query, (file_path, item_id))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/')
        else:
            return jsonify({'error': '無効なファイル形式です。'}), 400
    except Exception as e:
        app.logger.error(f'エラーが発生しました: {str(e)}')
        return jsonify({'error': 'ファイルのアップロード中にエラーが発生しました。'}), 500
    #物品登録
@app.route('/api/add_item', methods=['POST'])
def add_item():
    try:
        # フォームからデータを取得
        物品名 = request.form['物品名']
        コード = request.form['コード']
        保管場所 = int(request.form['保管場所']) if request.form['保管場所'] else None
        数量 = int(request.form['数量']) if '数量' in request.form and request.form['数量'] else 0
        購入日 = request.form['購入日'] or None  # 空白の場合は None に設定
        状態 = request.form['状態']
        管理責任者 = int(request.form['管理責任者']) if request.form['管理責任者'] else None
        規格 = request.form['規格']
        製造番号 = int(request.form['製造番号']) if request.form['製造番号'] else None
        製造先 = int(request.form['製造先']) if request.form['製造先'] else None
        単価 = int(request.form['単価']) if request.form['単価'] else None
        金額 = request.form['金額']
        納入日 = request.form['納入日'] or None  # 空白の場合は None に設定
        支払日 = request.form['支払日'] or None  # 空白の場合は None に設定
        購入先 = request.form['購入先']
        所属 = request.form['所属']
        前所属 = request.form['前所属']
        前任者 = int(request.form['前任者']) if request.form['前任者'] else None
        整理番号 = int(request.form['整理番号']) if request.form['整理番号'] else None

       # 写真の処理
        photo_file = request.files.get('photo')
        jpeg_file_path = save_loaded_file(photo_file, app.config['UPLOAD_FOLDER']) if photo_file else None
        # 数量分のデータをデータベースに挿入
        for i in range(1, 数量 + 1):
            # ST数量を生成 (例: 2-1, 2-2, ...)
            st_quantity = f"{数量}-{i}"

            # QRコードデータを作成
            qr_data = f"購入日: {購入日}, コード: {コード}, 整理番号: {整理番号}, ST数量: {st_quantity}, 管理責任者: {管理責任者}"

            # QRコードの保存パス
            qr_filename = f"{コード}_{整理番号}_{管理責任者}_{st_quantity}.png"
            qr_full_path = os.path.join(app.config['QR_CODE_FOLDER'], qr_filename)

            # QRコードを生成して保存
            generate_qr_code(qr_data, qr_full_path)
        # SQLクエリの作成
            insert_query = """
            INSERT INTO goods (物品名, コード, 保管場所, 購入日, 状態, 管理責任者, 規格, 製造番号, 製造先, 単価, 金額, 納入日, 支払日, 購入先, 所属, 前所属, 前任者, 整理番号, ST数量, 写真, QRコード)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # パラメータの作成
            data = (物品名, コード, 保管場所, 購入日, 状態, 管理責任者, 規格, 製造番号, 製造先, 単価, 金額, 納入日, 支払日, 購入先, 所属, 前所属, 前任者, 整理番号, st_quantity, jpeg_file_path, qr_full_path)

            # データベースへの接続を取得
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(insert_query, data)
            conn.commit()

            # 接続を閉じる
            cursor.close()
            conn.close()

        return jsonify({'message': 'アイテムが正常に追加されました.'})

    except Exception as e:
        app.logger.error(f'アイテム追加中のエラー: {e}')
        return jsonify({'error': 'アイテムの追加中にエラーが発生しました.'}), 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(QR_CODE_FOLDER):
        os.makedirs(QR_CODE_FOLDER)
    app.run(debug=True)



    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)