const userService = require('../services/user.service');

exports.createUser = async (req, res, next) => {
    res.send(await userService.createUser(req.body));
};

exports.getUsers = async (req, res, next) => {
    res.send(await userService.getUsers());
};

exports.getUser = async (req, res, next) => {
    res.send(await userService.getUser(req.params.handle));
};

exports.updateUser = async (req, res, next) => {
    res.send(await userService.updateUser(req.params.handle, req.body));
};

exports.deleteUser = async (req, res, next) => {
    res.send(await userService.deleteUser(req.params.handle));
};

