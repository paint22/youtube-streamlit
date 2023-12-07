from flask import Flask, request, jsonify, render_template, send_file, Blueprint
from werkzeug.utils import secure_filename
from PIL import Image
import mysql.connector
import os
import qrcode
import uuid
import io
from PIL import ImageOps

app = Flask(__name__)

# アップロードフォルダの設定
UPLOAD_FOLDER = 'c:\\Users\\kudosyo\\Desktop\\プロジェクト1\\my-goods-app\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# QRコードの保存場所を設定
QR_CODE_FOLDER = 'c:\\Users\\kudosyo\\Desktop\\プロジェクト1\\my-goods-app\\qrcodes'
app.config['QR_CODE_FOLDER'] = QR_CODE_FOLDER

# MySQL接続情報
mysql_config = {
    'user': 'root',
    'password': 'Kudosyo76508321',
    'host': '127.0.0.1',
    'database': '物品',
    'raise_on_warnings': True,
    'pool_size': 5
}

# MySQL接続プール
conn_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", **mysql_config)

def get_connection():
    return conn_pool.get_connection()

def save_loaded_file(file, upload_folder):
    try:
        if file and file.filename:
            # ファイル名の生成
            filename = secure_filename(file.filename)
            filename = str(uuid.uuid4()) + '_' + filename
            file_path = os.path.join(upload_folder, filename)

            # 拡張子によって処理を分岐
            if filename.lower().endswith(('.webp', '.png', '.jpg', '.jpeg', '.gif')):
                # WebP、PNG、JPG、JPEG、GIFのいずれかの場合
                # ファイル内容をメモリに読み込む
                file_data = file.read()

                # WebPをJPEGに変換（WebP以外はそのまま保存）
                if filename.lower().endswith('.webp'):
                    image = Image.open(io.BytesIO(file_data))
                    jpeg_file = file_path.rsplit('.', 1)[0] + '.jpg'
                    image = ImageOps.exif_transpose(image)  # 画像の向きを修正
                    image.convert("RGB").save(jpeg_file, "JPEG")
                    file_path = jpeg_file
                else:
                    with open(file_path, 'wb') as f:
                        f.write(file_data)

                return file_path
            else:
                print('サポートされていないファイル形式です:', filename)
    except Exception as e:
        print(f'ファイルの保存に失敗しました: {e}')
    return None

def generate_qr_code(qr_data, output_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(output_path)

@app.route('/')
def home():
    return render_template('物品登録.html')

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

        # カメラで撮影した写真をJPEG形式で保存
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and photo.filename:
                # 画像の保存処理
                jpeg_file_path = save_loaded_file(photo, app.config['UPLOAD_FOLDER'])
            else:
                jpeg_file_path = None
        else:
            jpeg_file_path = None

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
        app.logger.error('エラーが発生しました: %s', str(e))
        return jsonify({'error': 'アイテムの追加中にエラーが発生しました.'}), 500

@app.route('/api/get_qrcode/<int:item_id>', methods=['GET'])
def get_qrcode(item_id):
    # データベースからQRコードファイルのパスを取得
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT QRコード FROM goods WHERE ID = %s"
        cursor.execute(query, (item_id,))
        qr_code_path = cursor.fetchone()[0]
        conn.close()

        if qr_code_path:
            return send_file(qr_code_path, mimetype='image/png')
        else:
            return 'QRコードが見つかりません', 404
    except Exception as e:
        app.logger.error('エラーが発生しました: %s', str(e))
        return 'QRコードの取得中にエラーが発生しました', 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(QR_CODE_FOLDER):
        os.makedirs(QR_CODE_FOLDER)
    # ローカルネットワーク上でアクセス可能にするために host を '0.0.0.0' に設定
    app.run(host='0.0.0.0', port=5000, debug=True)
