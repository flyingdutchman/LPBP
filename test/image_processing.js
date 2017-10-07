const chai = require('chai');
const dirty = require('dirty-chai');
const Image = require('../src/image_processing');

const request = require('superagent');
const { username, token } = require('../github-credentials.json');
const fs = require('fs');

chai.should();
chai.use(dirty);

describe('Test Functions', () => {
  it('Gets me the avatar (image data) of a given user', (done) => {
    // Image.downloadContributorsAvatars('https://github.com/flyingdutchman/LPBP');
    const originalUrl = 'https://github.com/flyingdutchman/LPBP';
    const newUrl = originalUrl.replace('github.com', 'api.github.com/repos').concat('/contributors');
    request
      .get(newUrl)
      .auth(username, token)
      .set('Accept', 'application/vnd.github.v3+json')
      .end((err, res) => {
      /* if (err != null) {
        throw err;
        // TODO
      } */
        const directoryName = 'tmp_images';
        if (!fs.exists(directoryName)) {
          fs.mkdir('tmp_images');
        }
        const contributors = res.body;
        for (let i = 0; i < contributors.length; i++) {
          const avatar = contributors[i].avatar_url;
        }
        /* Must be here. If put after it(), done is launch before end of method */
        done();
      });
  });
});
