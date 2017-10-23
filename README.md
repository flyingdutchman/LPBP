# TWEB - GitHub Analytics 

## Introduction 

Welcome to the Github page dedicated to the first TWEB project of the year, using Github's API !

The idea of the project is to be able to create a image based on smaller images coming from the avatars of all contrbutors in a repository.

This program could be usefull, for example, to recreate the logo of a buisness with the avatars of people working on a project !

## The Client

The client is the graphical interface you interact with. Basically, you can do two things : looking at some photo mosaic that were already made or create your own picture.
In order to make your own mosaic you need to fill out a form :

:information_source: Please take note that the input are not parsed, wrong input will cause the app to crash 

- *URL of a Githug repository*

The URL **must** respect the following format : `https://github.com/owner/repo`

:warning: The number of contributors in a given repository must not be shown as infinite. In such a case, our program won't be able to create the image because of the limitations of the Github's API. (Error : 'The history or contributor list is too large to list contributors for this repo').

- *Your Email address*

	The new picture will be sent to this address. If you don't receive any message, you should check in your spam box.

- *URL of an image*

	This image will be the template for the mosaic picture. You need to provide a valid URL from internet.

When you did all these things, you can go check your Facebook for a while :grin:

## The Server 

The server, on its side, waits for a POST from the client. When he recives it, the server do the following things :

He takes the URL from the repo and make a Github API request to collect the avatars URL from all non-anonymous collaborators. Then the server will proceed to build the given image with the avatars it just downloaded.

Once the image has been generated, a Email is sent to with the new image attached to it. Also, the image is saved and shown as an example on the website.

**Known Bug** : On Docker, the program works fine but on Heroku, there is a bug : sometime the image is not loaded on the web page. It could be because heroku ereases files when the dyno dies. This should be fixed in the future. 

Its last action is to send the picture by e-mail to the address he got within the POST request. 

## Technologies used 

We searched for a script that made photo mosaic. We found one on this github repo (https://github.com/codebox/mosaic/blob/master/mosaic.py). The code is written in Python 2. We wanted to change it so it could work with Python 3. Unfortunately, it uses some libraries that were deprecated in Python 3. Our knowleges in Python are limited, so we did not insisted. We took this code and adapted it with our needs.
Here are the changes we made : 
- The intial code is supposed to take a picture and a directory, containing all the tiles. We replaced that so that the code would work with url. 
- We added a variable to stock the final image. Instead of writting it on a directory and then have to read it again, we simply kept it.

Because we chose this script, the server had to be in Python too. So we deployed the server on Heroku with Flask. We started with this git repo (https://github.com/datademofun/heroku-basic-flask) to undersand how it worked. 

Finally, to send an e-mail, we chose to connect to a gmail server. Because of this, we had to create an account and give credentials in the code. A good thing would be to make those credentials private. 

We found an equivalent to ESLint for Python. It is called Pylama. We added a line in the Dockerfile so pylama would check all .py files. 


## Heroku Limitation 

Heroku has set a default timeout. If the request take more than 30 seconds, Heroku shuts down the connexion. 
It is said in offical documentation (https://devcenter.heroku.com/articles/request-timeout) that if th application is doing a long-running task, such as image processing or sending an e-mail (which is exactly what we do), we should move our work to a background task. We invastigated this possiblity. There are some frameworks, like celery, that makes background job. But unfortunately, we did not have enough time left to learn how to use it and to implement it in our code. So we decided to reduce the number of tiles and the quality of them, so the request would take less than 30 seconds. The result is a bit less nice than it used to be, but it gives us what we wanted. <br>In the future, an amelioration would be to implements theses background jobs to have better pictures. <br>Note that if you run the application locally, you will get a better image :)


## Set Up 

### Github and SMTP Credentials 

In order to make requests to the Github API, we created a file `github-credentials.json` that we access in our code.
Same goes for the `smtp-credentials.json` file: it has been created to be able to send a mail message. 
We used a G-mail server to send the e-mail. G-mail want the person who send the e-mail to be authentificated and so we created a special account for this lab (tweb.is.fun@gmail.com).

### Run locally (Docker)

To run the program locally you need to have Docker installed on your machine. (https://www.docker.com)

Procedure : 

```
git clone https://github.com/flyingdutchman/LPBP.git
cd LPBP
docker-compose up --build
```

:information_source:  You might need to `sudo` in order to build the container.

Then, to access the webpage run the command `docker ps` and note down the ID and port of the container.
Once it has been done, you can get the IP adress thanks to
`docker inspect CONTAINER_ID | grep "IP"`

And there you have it ! Just access the website by typing the found IP adress and port (i.e. 172.18.0.2:7070)

### Run with Heroku 

You can already visit our funciton version on https://little-pics-in-big-pics.herokuapp.com but if you wish to create your own Heroku app, just follow the next instructions :

```
git clone https://github.com/flyingdutchman/LPBP.git
cd LPBP
heroku login
heroku create
git add .
git commit -m "Init"
git push heroku master
heroku open
```

You will be then able to access the website at https://APPNAME.herokuapp.com/

## Trivia

Il y a un dossier nommé "js testing" qui n'est pas utilisé dans le code mais que nous avons souhaité laisser.
Il montre en effet les premières démarches que nous avions fair en début de projet pour effectuer le retrait des URL avatars du côté client.
Cela a été changé pour être fait du côté serveur en Python grâce à la librairie [PyGithub](http://pygithub.readthedocs.io/en/latest/index.html).