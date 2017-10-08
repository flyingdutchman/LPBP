function $$getPage(pageNumber) {
  if (pageNumber < 1 || pageNumber > this.numOfPages) {
    return {
      header: {
        error: 'page does not exist',
      },
    };
  }
  const hasNextPage = pageNumber < this.numOfPages;
  return {
    header: {
      pageNumber,
      hasNextPage,
    },
    data: {
    },
  };
}

class Client {
  constructor(numOfPages) {
    this.numOfPages = numOfPages;
  }

  getPage(pageNumber, pageIsAvailable) {
    const delay = Math.random() * 1000;
    setTimeout(() => {
      pageIsAvailable($$getPage.bind(this)(pageNumber));
    }, delay);
  }
}

module.exports = Client;

