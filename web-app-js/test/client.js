const chai = require('chai');
const dirty = require('dirty-chai');

chai.should();
chai.use(dirty);

const Client = require('../src/client.js');

describe('Client', () => {
  const numPages = 2;
  const client = new Client(numPages);

  describe('getPage', () => {
    it('should allow me to get a page', (done) => {
      client.getPage(1, (res) => {
        res.header.should.have.property('pageNumber', 1);
        res.header.should.have.property('hasNextPage', true);
        done();
      });
    });

    it('should tell me when I am on the last page', (done) => {
      client.getPage(2, (res) => {
        res.header.should.have.property('pageNumber', 2);
        res.header.should.have.property('hasNextPage', false);
        done();
      });
    });

    it('should return an error if the page does not exists', (done) => {
      let numOfFunctions = 0;
      function notify() {
        numOfFunctions += 1;
        if (numOfFunctions === 3) {
          done();
        }
      }
      client.getPage(-1, (res) => {
        res.header.should.have.property('error', 'page does not exist');
        notify();
      });
      client.getPage(0, (res) => {
        res.header.should.have.property('error', 'page does not exist');
        notify();
      });
      client.getPage(numPages + 1, (res) => {
        res.header.should.have.property('error', 'page does not exist');
        notify();
      });
    });
  });
});
