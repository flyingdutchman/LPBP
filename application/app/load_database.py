import bs4
import random
import string
import os

basedir = os.path.abspath(os.path.dirname(__file__))


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def html(name):
    # load the file
    with open(os.path.join(basedir, 'templates/index.html')) as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt)

    string = "<div class='col-md-4 col-sm-6 portfolio-item'> \
                  <div class='portfolio-hover'> \
                    <div class='portfolio-hover-content'> \
                    </div> \
                  </div> \
                  <img class='img-fluid' src='../static/img/portfolio/" + name + ".jpeg' alt=''> \
                <div class='portfolio-caption'> \
                  <h4>" + name + "</h4> \
                  <p class='text-muted'>Nice</p> \
                </div> \
              </div>"

    result = bs4.BeautifulSoup(string)
    res = soup.find(id="dbImages")
    res.append(result)

    with open(os.path.join(basedir, 'templates/index.html'), "w") as outf:
        outf.write(str(soup))
