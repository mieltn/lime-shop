## How to run
1. `git clone https://github.com/mieltn/limeshop.git -b develop` to clone develop branch and `cd limeshop`
2. `python3 -m venv venv` to create virtual env and `source venv/bin/activate` to activate
3. `pip install -r requirements.txt`
4. `python manage.py makemigrations` then `python manage.py migrate` to set up db
5. `python manage.py createsuperuser` to create admin and be able to access admin panel to add input data
6. `python manage.py runserver`