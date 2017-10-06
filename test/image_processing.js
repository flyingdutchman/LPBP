const chai = require('chai');
const dirty = require('dirty-chai');
const Image = require('../src/image_processing');

const should = chai.should();
chai.use(dirty);

describe('Test Functions', () => {
  it('Gets me the avatar (image data) of a given user', (done) => {
    Image.downloadContributorsAvatars('https://github.com/flyingdutchman/LPBP');
    done();
  });
});
