const express = require("express");
const app = express();
const port = 3000;

// POSTリクエストを処理するエンドポイント
app.post("/send-to-discord", (req, res) => {
  // Discordへのリクエスト処理をここに書く
  // 例えば、sendToDiscord関数を呼び出すなど
});

app.listen(port, () => {
  console.log(`サーバーがポート${port}で起動しました。`);
});


