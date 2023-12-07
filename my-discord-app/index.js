const express = require('express');
const app = express();
const fetch = require('node-fetch');

app.use(express.json());

let webhookUrl = null;

app.post('/sendToDiscord', (req, res) => {
  if (!webhookUrl) {
    res.status(400).json({ error: 'Discord Webhook URLが設定されていません' });
    return;
  }

  const payload = {
    username: '割り当てボット',
    avatar_url: '',
    content: `【結果一覧】\n${req.body.result}`,
  };

  fetch(webhookUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    res.json({ success: true });
  })
  .catch(error => {
    console.error('Error sending message to Discord:', error);
    res.status(500).json({ error: 'Failed to send message to Discord' });
  });
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
