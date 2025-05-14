# IMPORTANT FOR EVERYONE
The order of execution of commands:

1. **Create venv**:
~~~bash
python -m venv venv
~~~
---
2. **Activate venv**:
~~~bash
venv\Scripts\activate
~~~
---
3. **Install packages**:
~~~bash
pip install -r requirements.txt
~~~
---
4. **Migrates**:
~~~bash
python src\manage.py makemigrations
~~~
~~~bash
python src\manage.py migrate
~~~
---
5. **Load data-file**:
~~~bash
python src\manage.py loaddata moviesApp/fixtures/countries.json
~~~

### Working!
