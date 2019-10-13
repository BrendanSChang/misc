const express = require('express')
const router = express.Router()

const asyncWrap = require('../utils/asyncWrap').asyncWrap
const userController = require('../controllers/user.controller')

router.post('/', asyncWrap(userController.createUser))
router.get('/', asyncWrap(userController.getUsers))
router.get('/:handle', asyncWrap(userController.getUser))
router.put('/:handle', asyncWrap(userController.updateUser))
router.delete('/:handle', asyncWrap(userController.deleteUser))

module.exports = router

