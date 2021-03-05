# CMPUT404_PROJECT

CMPUT404-project-socialdistribution
===================================

CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

## Running the Program Locally

Konnection has two components, a client and a server. 
### Running the Server
⚠️ **Note**: Make sure to have python3 and postgreSQL installed. Reference to 
Please refer to our [konnection101](https://github.com/C404TEAMW21/CMPUT404_PROJECT/wiki/Konnection101) 
to learn more about installing and setting up the database. 
Go into a terminal window in the root directory of this repository and run
```
python3 -m venv venv
source venv/bin/activate
cd server
pip install -r requirements.txt
python3 manage.py runserver --settings konnection.settings.local
```
Please contact any of the project member to get the `.env` file
### Running the Client
⚠️ **Note**: Make sure you have npm installed. If server is not running, the webpage will throw an error.
Go into a terminal window in the root directory of this repository and run
```
cd client
npm install
npm run dev
``` 
## Running the Test Locally
⚠️ **Note**: Make sure to have python3 and postgreSQL installed. Reference to 
Please refer to our [konnection101](https://github.com/C404TEAMW21/CMPUT404_PROJECT/wiki/Konnection101) 
to learn more about installing and setting up the database. 
Go into a terminal window in the root directory of this repository and run
```
python3 -m venv venv
source venv/bin/activate
cd server
pip install -r requirements.txt
python3 manage.py test --settings konnection.settings.local
```
### Need More Helpful Commands? 
Please refer to our [konnection101](https://github.com/C404TEAMW21/CMPUT404_PROJECT/wiki/Konnection101) if 
you need more info with how to set up the database, installing backend command, etc. 

### Frontend and Backend Host
For more infromation about deployment, refer to [Deployment Strategy](https://github.com/C404TEAMW21/CMPUT404_PROJECT/wiki/Deployment-Strategy)

- **Frontend host URL (Client)**: [https://konnection-client.herokuapp.com/login](https://konnection-client.herokuapp.com/login)

- **Backend host URL (Server)**: [https://konnection-server.herokuapp.com/](https://konnection-server.herokuapp.com/)

Repo Contributors / Licensing
=============================

Team Members:

    Kean Weng Yap
    Monica Bui
    Ian Seng Wok
    Amy Xiang
    Hailan Xu

Project Creation Contributors / Licensing
========================

LICENSE, README.md and project.org files are inherited [Professor Abram Hindle's repo](https://github.com/abramhindle/CMPUT404-project-socialdistribution).

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

Contributors:

    Karim Baaba
    Ali Sajedi
    Kyle Richelhoff
    Chris Pavlicek
    Derek Dowling
    Olexiy Berjanskii
    Erin Torbiak
    Abram Hindle
    Braedy Kuzma


References
=============================
Connecting PostgreSQL to Django
* From [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)
* From [Justin Ellingwood](https://www.digitalocean.com/community/users/jellingwood)
* Accessed Feb 9 2021

Adding secrets to env file
* From [StackOverflow](https://stackoverflow.com/a/61437799)
* From [Zack Plauché](https://stackoverflow.com/users/10415970/zack-plauch%c3%a9)
* Accessed Feb 9 2021

Adding PostgreSQL to GitHub Actions Job
* From [HackSoft](https://hacksoft.io/github-actions-in-action-setting-up-django-and-postgres/)
* From [Radoslav Georgiev](https://hacksoft.io/author/radoslav-georgiev/)
* Accessed Feb 9 2021

UUID Django Model Field Type
* From [Django Docs](https://docs.djangoproject.com/en/3.1/ref/models/fields/#uuidfield)
* Accessed Feb 13 2021

Choices Django Model Field Option
* From [Django Docs](https://docs.djangoproject.com/en/3.1/ref/models/fields/#choices)
* Accessed Feb 14 2021

Django Settings
* From [Django Docs](https://docs.djangoproject.com/en/3.1/topics/settings/)
* Accessed Feb 14 2021

AssertRegex
* From [StackOverflow](https://stackoverflow.com/a/64192098)
* From [mrts](https://stackoverflow.com/users/258772/mrts)
* Accessed Feb 14 2021

CORS
* From [zaidfazil](https://stackoverflow.com/questions/44037474/cors-error-while-consuming-calling-rest-api-with-react/44037631#44037631)
* Accessed Feb 16 2021

Django Restframework
* From [Medium](https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c)
* From [Bennett Garner](https://bennettgarner.medium.com)
* Accessed Feb 15 2021

Fix Django Authenticate Token issue 
* From [StackOverflow](https://stackoverflow.com/questions/35601130/django-rest-framework-using-tokenauthentication-with-browsable-api)
* From [ilse2005](https://stackoverflow.com/users/1762988/ilse2005)
* Accessed Feb 16 2021

Django Restframework Generic Views 
* From [Django REST framework Docs](https://www.django-rest-framework.org/api-guide/generic-views/)
* Accessed Feb 16 2021

Concrete View Classes
* From [Django REST Framework](https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes)
* Accessed Feb 16 2021

Get Object of 404
* From [Django Docs](https://docs.djangoproject.com/en/3.1/topics/http/shortcuts/#get-object-or-404)
* Accessed Feb 16 2021

PUT Partial Updates using Generics
* From [StackOverflow](https://stackoverflow.com/a/29761525)
* From [soooooot](https://stackoverflow.com/users/1889075/soooooot)
* Accessed Feb 16 2021

Serializers Partial Updates
* From [Django REST Framework](https://www.django-rest-framework.org/api-guide/serializers/#partial-updates)
* Accessed Feb 16 2021

Put as Create
* From [GitHub](https://gist.github.com/tomchristie/a2ace4577eff2c603b1b#gistcomment-2588991)
* From [mightyroser](https://github.com/mightyroser)
* Accessed Feb 16 2021

Django Update user profile 
* From [Medium](https://medium.com/django-rest/django-rest-framework-change-password-and-update-profile-1db0c144c0a3)
* From [Yunus Emre Cevik](https://yunusemrecevik.medium.com/)
* Accessed Feb 17 2021

Get User Info in Serializer
* From [StackOverflow](https://stackoverflow.com/a/29934446)
* From [soooooot](https://stackoverflow.com/users/1889075/soooooot)
* Accessed Feb 17 2021 

Serializer Method Field
* From [StackOverflow](https://stackoverflow.com/a/52935481)
* From [ocobacho](https://stackoverflow.com/users/10297128/ocobacho)
* Accessed Feb 18 2021

Serialize Model Instance
* From [StackOverflow](https://stackoverflow.com/a/3289057)
* From [xaralis](https://stackoverflow.com/users/303184/xaralis)
* Accessed Feb 23 2021

Paginate Nested Object
* From [StackOverflow](https://stackoverflow.com/a/49677960)
* From [Abdelrahmen Ayman](https://stackoverflow.com/users/7469841/abdelrahmen-ayman)
* Accessed Feb 24 2021

Django Anti-Patterns: Signals
* From [lincoln loop](https://lincolnloop.com/blog/django-anti-patterns-signals/)
* From [Peter Baumgartner](https://lincolnloop.com/about/peter-baumgartner/)
* Accessed Feb 28 2021

Follower 
* From [StackOverflow](https://stackoverflow.com/questions/62060573/django-rest-framework-getting-followers-using-related-name-of-manytomanyfield)
* Accessed Feb 28 2021

Aceess Many to Many object
* From [StackOverflow](https://stackoverflow.com/questions/31876213/how-to-use-limit-in-django-rest-framework-generics-retrieveapiview)
* Accessed Mar 1 2021

Unique Together
* From [StackOverflow](https://stackoverflow.com/a/2201687)
* Accessed Mar 2 2021

Deploying Django to Heroku: Connecting Heroku Postgres
* From [Bennett Garner](https://bennettgarner.medium.com)
* From [Noteworthy](https://blog.usejournal.com/deploying-django-to-heroku-connecting-heroku-postgres-fcc960d290d1)
* Accessed Mar 3 2021

How to Structure the Django Settings for Different Environments
* From [Max Goodridge](https://www.youtube.com/channel/UCAx4nmhI7S1RcPiaG-Uw0tg)
* From [Youtube](https://www.youtube.com/watch?v=zPVLRvpzOOU)
* Accessed Mar 3 2021

Heroku - Django app
* From [Heroku doc](https://devcenter.heroku.com/articles/django-app-configuration)
* Accessed Mar 3 2021

How to Deploy Your React App to Heroku
* From [Daniel Stoica](https://medium.com/@dldanielstoica)
* From [Better Programming](https://betterprogramming.pub/how-to-deploy-your-react-app-to-heroku-aedc28b218ae)
* Accessed Mar 4 2021

How to Deploy Your React App to Heroku
* From [dahlbyk](https://stackoverflow.com/users/54249/dahlbyk)
* From [Andy_D](https://stackoverflow.com/users/3394347/andy-d)
* From [StackOverflow](https://stackoverflow.com/questions/42458434/how-to-set-build-env-variables-when-running-create-react-app-build-script)
* Accessed Mar 4 2021

Deploy to Heroku
* From [GitHub Action Doc-heroku-deploy](https://github.com/marketplace/actions/deploy-to-heroku)
* Accessed Mar 4 2021


