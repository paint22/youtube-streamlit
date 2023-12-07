const express = require('express');
const app = express();
const port = 3000; // 使用するポート番号を指定

// ミドルウェアを設定
app.use(express.json());

// '/set-webhook-url' エンドポイントへのPOSTリクエストを処理
app.post('/set-webhook-url', (req, res) => {
  const { webhookUrl } = req.body;
  setWebhookUrl(webhookUrl); // ウェブフックのURLを設定する
  res.send("ウェブフックのURLを設定しました。");
});

// '/send-to-discord' エンドポイントへのPOSTリクエストを処理
app.post('/send-to-discord', (req, res) => {
  const { assignedWeapons } = req.body;

  // Discordに送信するリクエストを作成
  const payload = {
    username: "割り当てボット",
    avatar_url: "",
    content: `&#8203;``oaicite:{"number":1,"invalid_reason":"Malformed citation 【結果一覧】"}``&#8203;\n${assignedWeapons.map(({ name, weapon }) => `${name}さん：「${weapon.name}」`).join("\n")}`,
  };

  fetch(webhookUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    res.send("結果をDiscordに送信しました！");
  })
  .catch(error => {
    console.error("Error sending message to Discord:", error);
    res.status(500).send("Discordへの送信中にエラーが発生しました。");
  });
});

// サーバーを起動
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});

let webhookUrl = null;

function setWebhookUrl(url) {
  webhookUrl = url;
  console.log(`Webhook URLが設定されました: ${webhookUrl}`);
}
