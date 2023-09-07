const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const port = 3000;

app.use(bodyParser.json());

async function sendToDiscordWebhook(serverName, message) {
  try {
    const webhookUrl = 'YOUR_DISCORD_WEBHOOK_URL'; // Discord WebhookのURLに置き換える
    const payload = {
      username: '名前と武器割り当てくん',
      content: `**${serverName}**\n${message}`,
    };
    await axios.post(webhookUrl, payload);
    console.log('Message sent to Discord successfully');
  } catch (error) {
    console.error('Error sending message to Discord:', error);
    throw new Error('Failed to send message to Discord');
  }
}

app.post('/sendDataToDiscord', (req, res) => {
  const data = req.body;
  const { serverName, weapons } = data;

  let message = '';
  for (const { name, weapon } of weapons) {
    message += `${name}さん：「${weapon.name}」\n`;
  }

  sendToDiscordWebhook(serverName, message)
    .then(() => {
      res.json({ message: 'Data sent to Discord successfully' });
    })
    .catch((error) => {
      console.error('Error sending data to server:', error);
      res.status(500).json({ error: 'Failed to send data to Discord' });
    });
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});