const chai = require('chai');
const dirty = require('dirty-chai');
const request = require('superagent');
const { username, token } = require('../github-credentials.json');

const should = chai.should();
chai.use(dirty);

describe('Github API', () => {
  it('gets me the avatar of a user', (done) => {
    const owner = 'LuanaMartelli';
    const url = `https://api.github.com/users/${owner}`;
    request.get(url).auth(username, token).set('Accept', 'application/vnd.github.v3+json').end((err, res) => {
      should.not.exist(err);
      should.exist(res);
      done();
    });
  });
});

