
# webshop in django 🪐

built in Django using some JavaScript(AJAX). \


the admin panel is designed for very little user-admin effort and is quite intuitive for anyone to use. to make an order you gotta be loged in. 

to get pass to see panel admin on heroku, dm 📩




## look at the demo

https://webshop-django-app.herokuapp.com/
## get SECRET_KEY

to run this project, you will need to add `SECRET_KEY`
to your .env file in webshop directory:

to get `SECRET_KEY` use the code below:

```bash
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
```

 


## install locally

follow these steps:

✔️ create virtualenv and install requirements:
```bash
  pip install -r requirements.txt
```

✔️ do migrations
```bash
  python manage.py migrate
```
✔️ create admin user
```bash
  python manage.py createsuperuser
```
✔️ runserver!

```bash
  python manage.py runserver
```

## created by
[@kkaarroollm](https://www.github.com/kkaarroollm)

