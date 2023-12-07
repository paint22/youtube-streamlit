import qrcode

# UTF-8エンコードされたテキストデータ
utf8_text = "北海道の拠点"

# QRコードを生成
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(utf8_text.encode('utf-8'))  # UTF-8にエンコード
qr.make(fit=True)

# QRコードを画像として保存
img = qr.make_image(fill_color="black", back_color="white")
img.save("utf8mb4_qrcode.png")

