from flask import Flask, request, render_template
from mail import send_mail
from mosaic import mosaic
from load_database import html, randomword
from github import Github
import os
import json


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))


@app.route('/')
def index():
    return render_template('index.html')


def get_avatars(repository_url):

    start = repository_url.find(".com/") + 5
    repo_url = repository_url[start:]

    with open(os.path.join(basedir, 'github-credentials.json')) as data_file:
        data = json.load(data_file)
    g = Github(login_or_token=data['token'])

    repo = g.get_repo(repo_url)

    urls = []
    for user in repo.get_contributors():
        urls.append(user.avatar_url)

    return urls


@app.route('/', methods=['POST'])
def contact():
    if request.method == 'POST':
        pic = request.form['URL_Image']
        mail = request.form['email']
        print "Getting avatars url of contributors..."
        tiles_url = get_avatars(request.form['repo_git'])
        print "... Success !"
        print "Mosaic Generation ..."
        img = mosaic(pic, tiles_url)
        name = randomword(5)
        path = os.path.join(basedir, 'static/img/portfolio/' + name + '.jpeg')
        img.save(path)
        html(name)

        print "Sending mail..."
        send_mail(mail, img)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True, port=7036)
