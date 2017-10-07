const request = require('superagent');
const { username, token } = require('../github-credentials.json');
const fs = require('fs');

function downloadContributorsAvatars(originalUrl) {
  // TODO Url doit être sous la forme https://github.com/"user"/"repo"
  // Url donné : https://github.com/flyingdutchman/LPBP
  // const url = `https://api.github.com/repos/${owner}/${repo}/contributors`;

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
    });
}

module.exports = {
  downloadContributorsAvatars,
};
