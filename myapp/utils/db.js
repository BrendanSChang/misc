const MongoClient = require('mongodb').MongoClient;

const {
    MONGO_USERNAME,
    MONGO_PASSWORD,
    MONGO_HOSTNAME,
    MONGO_PORT,
    MONGO_DB
} = process.env;

const url = `mongodb://${MONGO_USERNAME}:${MONGO_PASSWORD}@${MONGO_HOSTNAME}:${MONGO_PORT}/${MONGO_DB}?authSource=admin`;

let db = null;

async function connect() {
    if (db) return
    let conn = await MongoClient.connect(url, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    });
    db = conn.db(`${MONGO_DB}`);
};
exports.connect = connect;

exports.get = async () => {
    if (!db) await connect();
    return db;
};

exports.close = (done) => {
    if (db) {
        db.close(function(err, result) {
            db = null;
            done(err);
        })
    }
};

