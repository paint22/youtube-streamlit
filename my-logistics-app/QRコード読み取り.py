import cv2
from pyzbar.pyzbar import decode
import mysql.connector

# データベースに接続
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Kudosyo76508321",
    database="sotuken",
    charset="utf8mb4"  # 文字エンコーディングをUTF8MB4に設定
)

# データベースカーソルを作成
cursor = connection.cursor()

# カメラを開く
cap = cv2.VideoCapture(0)

# 既に読み取ったQRコードをトラッキングするためのセット
read_qr_codes = set()

# 出発地点のQRコードを読み取るフラグ
read_departure = False

while True:
    # カメラからフレームをキャプチャ
    ret, frame = cap.read()

    # QRコードをデコード
    decoded_objects = decode(frame)

    for obj in decoded_objects:
        qr_code_data = obj.data.decode("utf-8")
        
        # 既に読み取ったQRコードでないことを確認
        if qr_code_data not in read_qr_codes:
            print("QRコードのデータ:", qr_code_data)
            
            if not read_departure:
                # 出庫確認
                data_elements = qr_code_data.split(",")
                if len(data_elements) == 3:
                    material_code, material_name, quantity = data_elements
                    cursor.execute("UPDATE sotuken_table SET 出庫確認 = %s WHERE 商品コード = %s AND 商品名 = %s AND 数量 = %s", ("◯", material_code, material_name, quantity))
                    print("出庫確認が更新されました。")
                    read_qr_codes.add(qr_code_data)
                else:
                    print("QRコードのデータが正しくありません:", qr_code_data)
            else:
                # 出発地点のQRコードをすべての行に書き込む
                cursor.execute("UPDATE sotuken_table SET 出発地点 = %s", (qr_code_data,))
                print("出発地点が更新されました。")
                read_qr_codes.add(qr_code_data)
                read_departure = False  # 出発地点の読み取りが完了
    
    # トランザクションのコミット
    connection.commit()

    # フレームを表示
    cv2.imshow("QR Code Scanner", frame)

    # 'd'キーが押されたら出発地点読み取りフラグを有効化
    if cv2.waitKey(1) & 0xFF == ord('d'):
        read_departure = True

    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# データベース接続を閉じる
cursor.close()
connection.close()

# カメラを解放
cap.release()

# OpenCVのウィンドウを閉じる
cv2.destroyAllWindows()
