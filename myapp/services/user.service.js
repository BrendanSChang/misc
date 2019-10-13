const userCollection = require('../models/user.model').get();

exports.createUser = async (body) => {
    return (await userCollection).insertOne(body);
};

exports.getUsers = async (handle) => {
    return (await userCollection).find().toArray();
};

exports.getUser = async (handle) =>  {
    return (await userCollection).findOne({handle: handle});
};

exports.updateUser = async (handle, body) => {
    return (await userCollection).updateOne({handle: handle}, {$set: body});
};

exports.deleteUser = async (handle) => {
    return (await userCollection).deleteOne({handle: handle});
};

