const express = require('express');
const app = express();
const port = 8080;

const weapons = [
    // ここに武器のデータを追加してください
];

app.get('/getRandomWeapon', (req, res) => {
    const category = req.query.category;
    const filteredWeapons = category === 'all' ? weapons : weapons.filter(w => w.category === category);

    if (filteredWeapons.length === 0) {
        return res.status(404).json({ error: 'Not found' });
    }

    const randomWeapon = filteredWeapons[Math.floor(Math.random() * filteredWeapons.length)];
    res.json({ weapon: randomWeapon });
});

app.listen(port, () => {
    console.log(`サーバーがポート${port}で起動しました`);
});
