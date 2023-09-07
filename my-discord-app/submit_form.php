<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $name = $_POST["name"];
    $email = $_POST["email"];
    $message = $_POST["message"];

    // ここで受け取った情報を処理する（例：データベースに保存、メール送信など）。
    // この例ではただフォームの内容を表示するだけです。
    echo "<h2>お問い合わせ内容:</h2>";
    echo "<p><strong>名前:</strong> " . $name . "</p>";
    echo "<p><strong>Eメール:</strong> " . $email . "</p>";
    echo "<p><strong>メッセージ:</strong> " . $message . "</p>";
}
?>