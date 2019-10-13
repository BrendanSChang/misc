const express = require('express');
const bodyParser = require('body-parser');
const db = require('./utils/db');
const user = require('./routes/user.route');

const port = 3000;

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(function (err, req, res, next) {
    if (res.headersSent) {
        return next(err);
    }
    res.status(500).send('Request failed!');
});

app.use('/users', user);

app.get('/', (req, res) => {
    res.send('Hello World!');
});

app.listen(port, () => {
    console.log(`Example app listening on port ${port}!`);
});

process.on('SIGTERM', () => {
    db.close((err) => {
        if (err) throw err;
    });
});

// For testing.
module.exports = app;

