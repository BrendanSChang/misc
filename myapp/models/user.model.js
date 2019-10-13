const db = require('../utils/db').get()

let users = null

exports.get = async () => {
    if (!users) {
        users = (await db).collection('users');
    }
    return users;
};

