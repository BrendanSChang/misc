const chai = require('chai');
const should = chai.should();

const chaiHttp = require('chai-http');
chai.use(chaiHttp);

const server = require('../server');
const userCollection = require('../models/user.model').get();

describe('user', () => {
    describe('create new user', () => {
        before(async () => {
            await (await userCollection).deleteMany({});
        });
        it('should create a new user', async () => {
            chai.request(server)
                .post('/users')
                .send({'handle': 'user'})
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('insertedCount').eql(1);
                });
        });
        it('should find the new user', async () => {
            chai.request(server)
                .get('/users/user')
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('handle').eql('user');
                });
        });
    });

    describe('get all users', () => {
        before(async () => {
            await (await userCollection).deleteMany({});
        });
        it('should have no users', async () => {
            chai.request(server)
                .get('/users')
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('array');
                    res.body.length.should.be.eql(0);
                });
        });
        it('should create a new user', async () => {
            chai.request(server)
                .post('/users')
                .send({'handle': 'user'})
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('insertedCount').eql(1);
                });
        });
        it('should have one user', async () => {
            chai.request(server)
                .get('/users')
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('array');
                    res.body.length.should.be.eql(1);
                    res.body[0].should.have.property('handle').eql('user');
                });
        });
    });

    describe('get a user', () => {
        before(async () => {
            await (await userCollection).deleteMany({});
        });
        it('should not get a nonexistent user', async () => {
            chai.request(server)
                .get('/users')
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('array');
                    res.body.length.should.be.eql(0);
                });
        });
        it('should create a new user', async () => {
            chai.request(server)
                .post('/users')
                .send({'handle': 'user'})
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('insertedCount').eql(1);
                });
        });
        it('should get the new user', async () => {
            chai.request(server)
                .get('/users/user')
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('handle').eql('user');
                });
        });
    });

    describe('update a user', () => {
        before(async () => {
            await (await userCollection).deleteMany({});
        });
        it('should not update a nonexistent user', async () => {
            chai.request(server)
                .put('/users/user1')
                .send({'handle': 'user2'})
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('modifiedCount').eql(0);
                });
        });
        it('should create a new user user1', async () => {
            chai.request(server)
                .post('/users')
                .send({'handle': 'user1'})
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('insertedCount').eql(1);
                });
        });
        it('should update user1 to user2', async () => {
            chai.request(server)
                .put('/users/user1')
                .send({'handle': 'user2'})
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('modifiedCount').eql(1);
                });
        });
        it('should not get user1', async () => {
            chai.request(server)
                .get('/users/user1')
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.be.empty;
                });
        });
        it('should get user2', async () => {
            chai.request(server)
                .get('/users/user2')
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('handle').eql('user2');
                });
        });
    });

    describe('delete a user', () => {
        before(async () => {
            await (await userCollection).deleteMany({});
        });
        it('should not delete a nonexistent user', async () => {
            chai.request(server)
                .delete('/users/user1')
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('deletedCount').eql(0);
                });
        });
        it('should create a new user', async () => {
            chai.request(server)
                .post('/users')
                .send({'handle': 'user'})
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('insertedCount').eql(1);
                });
        });
        it('should delete the new user', async () => {
            chai.request(server)
                .delete('/users/user')
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('deletedCount').eql(1);
                });
        });
        it('should have no users', async () => {
            chai.request(server)
                .get('/users')
                .end((err, res) => {
                    should.not.exist(err);
                    res.should.have.status(200);
                    res.body.should.be.a('array');
                    res.body.length.should.be.eql(0);
                });
        });
    });
});

