const express = require('express');
const app = express();
const Discord = require('discord.js');
const client = new Discord.Client();
const characters = [
    // キャラクター情報をここに記述
];

// Discordのボットトークンを設定
const token = 'YOUR_DISCORD_BOT_TOKEN';
const channelID = 'YOUR_DISCORD_CHANNEL_ID'; // 送信先のチャンネルID

// Discordのボットがログインした際の処理
client.once('ready', () => {
    console.log('Bot is ready!');
});

// サーバーサイドからのAPIエンドポイント
app.post('/sendResult', express.json(), (req, res) => {
    const { name1, name2, name3, selectedCategory } = req.body;

    const selectedCharacters = getRandomCharacters(selectedCategory);

    const resultMessage = `
        ${name1}さんのキャラクターは「${selectedCharacters[0].name}」です。
        ${name2}さんのキャラクターは「${selectedCharacters[1].name}」です。
        ${name3}さんのキャラクターは「${selectedCharacters[2].name}」です。
    `;

    // Discordのチャンネルにメッセージを送信
    const channel = client.channels.cache.get(channelID);
    channel.send(resultMessage);

    res.json({ message: '選択結果を送信しました。' });
});

function getRandomCharacters(selectedCategory) {
    // カテゴリーに応じてキャラクターをフィルタリングしてランダムに3つ選択するロジックを実装
}

// Discordのボットをログイン
client.login(token);

// サーバーを起動
const port = 3000;
app.listen(port, () => {
    console.log(`サーバーが http://localhost:${port} で起動しました。`);
});