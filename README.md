IHC class project

#### How to use in linux:
```
cd ihc-app
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
FLASK_APP=webapp.py flask run
```
#### How to use in Windows :
```
cd ihc-app
python3 -m venv venv
venv/bin/activate.bat
pip3 install -r requirements.txt
set FLASK_APP=webapp.py
flask run
```
#### How to create the database:
```
FLASK_APP=webapp.py flask shell
```
###### Within the shell, type the following commands:
```
db.create_all()
Role.insert_roles()
quit()
```
#### How to run the tests:
```
FLASK_APP=webapp.py flask test
```

#### how to build and run docker image:
##### First edit the Dockerfile and change the environment variables values
MAIL_DEFAULT_SENDER
MAIL_USERNAME  (only gmail for now)
MAIL_PASSWORD
ADMIN_EMAIL

##### Lastly execute these commands:
```
docker build -t ihcapp .
docker run -d -p 8080:5000 ihcapp
```
