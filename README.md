# ytdjango
Put Youtube video url in ytdjango web application and magically enjoy mp3 file in your phone. 

#Issues/TODO
  - Only available language: Polish


#Set up application

###1. Set mp3 files dir
in file: ytdjango/ytdjango/setting.py
  - MAIN_MP3_DIR="path"

###2. Configure RabbitMQ
in file: ytdjango/ytdjango/setting.py
  - BROKER_HOST = "127.0.0.1"
  - BROKER_PORT = 5672
  - BROKER_VHOST = "/"
  - BROKER_USER = "guest"
  - BROKER_PASSWORD = "guest"

###3. Create database
  - cd ydjango
  - python manage.py migrate

###4. Install python dependencies
  - sudo pip install -r requierments.txt

###5.Test. 
####Change ip address in RunDevServ.sh if you want to
  - python manage.py  createsuperuser
  - ./RunCelery.sh
  - ./RunDevServ.sh
  - Point your browser to http://127.0.0.1:8000/
