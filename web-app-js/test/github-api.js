const chai = require('chai');
const dirty = require('dirty-chai');
const request = require('superagent');
const { username, token } = require('../github-credentials.json');

const should = chai.should();
chai.use(dirty);

describe('Github API', () => {
  it('Gets me the avatar (image data) of a given user', (done) => {
    const owner = 'LuanaMartelli';
    const url = `https://api.github.com/users/${owner}`;
    request.get(url).auth(username, token).set('Accept', 'application/vnd.github.v3+json').end((err, res) => {
      should.not.exist(err);
      should.exist(res);
      const avatar = res.body.avatar_url;
      request.get(avatar).auth(username, token).set('Accept', 'image/*').end((err2, res2) => {
        should.not.exist(err2);
        should.exist(res2);
        done();
      });
    });
  });
  it('gets me list of contributors for a repo', (done) => {
    const repo = 'LPBP';
    const owner = 'flyingdutchman';
    const url = `https://api.github.com/repos/${owner}/${repo}/contributors`;
    request.get(url).auth(username, token).set('Accept', 'application/vnd.github.v3+json').end((err, res) => {
      should.not.exist(err);
      should.exist(res);
      done();
    });
  });
});
