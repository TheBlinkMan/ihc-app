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
