# Sheduler

Employee schedule management system. 
### Features:
1. You can split day by odd end even week
2. Automatic odd/even week detection
3. One command to deploy

### Stack:
* Python 3.7
* Django 2.1.7
* Bootstrap 4
* SqLite (or something for Django if you want)

### How to run:
0. Create superuser by: python manage.py createsuperuser
1. docker build . -t sheduler
2. docker run -p 80:80 sheduler

Disable debug in settings and configure allowed hosts.

WARNING: You shouldn't use this service with build-in http server. There just code and brief example how
to run in quickly. Configure web-server and database.  

### Examples:
Index page
![index](https://raw.githubusercontent.com/AmaHacka/sheduler/master/screenshots/index.png)
Worker details
![worker](https://raw.githubusercontent.com/AmaHacka/sheduler/master/screenshots/worker.png)
Worker config in admin panel
![admin](https://raw.githubusercontent.com/AmaHacka/sheduler/master/screenshots/admin.png)
