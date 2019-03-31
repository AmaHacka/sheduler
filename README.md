# Sheduler

Employee schedule management system. 
### Features:
1. You can split day by odd end even week
2. Automatic odd/even week detection
3. One command to deploy

###Stack:
* Python 3.7
* Django 2.1.7
* SqLite (or something for Django if you want)

###How to run:
0. Create superuser by: ptython manage.py createsuperuser
1. docker build . -t sheduler
2. docker run -p 80:80 sheduler

### Examples:

![alt text](https://raw.githubusercontent.com/AmaHacka/sheduler/blob/master/screenshots/index.png)
![alt text](https://raw.githubusercontent.com/AmaHacka/sheduler/blob/master/screenshots/worker.png)
![alt text](https://raw.githubusercontent.com/AmaHacka/sheduler/blob/master/screenshots/admin.png)
