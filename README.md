
# TWEB - GitHub Analytics 

## Introduction 

Welcome to the Github page dedicated to the first TWEB project of the year, using Github's API !

The idea of the project is to be able to create a image based on smaller images coming from the avatars of all contrbutors in a repository.

This program could be uselfull, for example, to recreate the logo of a buisness with the persons working on a certain project !


## The Client

The client is the graphical interface you interact with. Basically, you can do two things : looking at some photo mosaic that were already made or create your own picture. You need to add three things.
Note that we did not make checks so the inputs must be correct : 

- URL of a Githug repository

The URL __must__ respect the following format : https://github.com/owner/repo

<aside class="notice">
The number of contributors in a given repository must not be shown as infinite. In such a case, our program won't be able to create the image because of the limitations of the Github's API.
</aside>

- your e-mail address

The new picture will be sent to this address. If you don't receive any message, you should check in your spam box.

- URL of an image

This image will be the template for the mosaic picture. You need to provide a valid URL from internet.

When you did all these things, you can go check your Facebook for a while :)


## The Server 

The server, on its side, make a POST request. Whenever it gots an answer, it does the following thing :

He takes the URL from the repo and make a Github API request to collect the avatars URL from the collaborators. With these URL and the URL of the image, it builds a mosaic picture. 

The picture is available on the website too. 

__Known Bug__ : on Docker, it works fine but on Heroku, there is a little bug : sometime the image in not loaded on the web page. He could be due to the fact that heroku ereases files when the dyno dies. This should be fixed in the future. 

Its last action is to send the picture by e-mail to the address he got within the POST request. 


## Technologies used 

We searched for a script that made photo mosaic. We found one on this github repo ('https://github.com/codebox/mosaic/blob/master/mosaic.py'). The code is written in Python 2. We wanted to change it so it could work with Python 3. Unfortunately, it uses some libraries that were deprecated in Python 3. Our knowleges in Python are limited, so we did not instist. We took this code and adapted it with our needs. <br>Here are the changes we made : 
  - The intial code is supposed to take a picture and a directory, containing all the tiles. We replaced that so that the code would work with url. 
  - We added a variable to stock the final image. Instead of writting it on a directory and then have to read it again, we simply kept it this variable.

Because we chose this script, the server had to be in Python too. So we deployed the server on Heroku with Flask. We started with this git repo ('https://github.com/datademofun/heroku-basic-flask') to undersand how it worked. 

Finally, to send an e-mail, we chose to connect to a gmail server. Because of this, we had to create an account and give credentials in the code. A good thing would be to make those credentials private. 

We found an equivalent to ESLint for Python. It is called pylama. We added a line in the Dockerfile so pylama would check all .py files. 


## Heroku Limitation 

Heroku has set a default timeout. If the request take more than 30 seconds, Heroku shuts down the connexion. 
It is said in offical documentation (https://devcenter.heroku.com/articles/request-timeout) that if th application is doing a long-running task, such as image processing or sending an e-mail (which is exactly what we do), we should move our work to a background task. We invastigated this possiblity. There are some frameworks, like celery, that makes background job. But unfortunately, we did not have enough time left to learn how to use it and to implement it in our code. So we decided to reduce the number of tiles and the quality of them, so the request would take less than 30 seconds. The result is a bit less nice than it used to be, but it gives us what we wanted. <br>In the future, an amelioration would be to implements theses background jobs to have better pictures. <br>Note that if you run the application locally, you will get a better image :)


## Set Up 

# Github Credentials 

In order to make requests to the Github API, we inserted our github credentials into the code. Since it is servers side, it has little risk to be read by the client.

# SMTP Server

We used a G-mail server to send the e-mail. G-mail want the person who send the e-mail to be authentificated. We created a special account for this lab (tweb.is.fun@gmail.com). The username and the password are available in a file (smtp-crendentials.json). This is cleary not a good practice, and we should have done the same thing as for the github credentials.


# Run locally 

Procedure : 

```
git clone repo
cd repo
docker-compose up --build
```

Port number is : 

Note that if you run locally the application, you can test a repo with a large number of collaborators. But do not take a repo with infinite number of collaborators, the app would crash because of Github API that does not support that kind of requests (Error : 'The history or contributor list is too large to list contributors for this repo').


# Run with Heroku 

```
git clone
cd 
heroku open  
```

Host name : https://calm-lake-26914.herokuapp.com/


Please choose a repository with a small number of contributors (we tested until 100 people) because the app will not get enough time to perform all the commands and it will crash. 
