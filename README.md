# covid-whatsapp-bot project

covid-whatsapp-bot is a django RESTful api for retrieving the covid data from database.
check the [link](https://covidbot-durian.herokuapp.com/) deployed on heroku.

## setup venv

```sh
python3 -m venv venv
source venv/bin/activate
```

## install requirements

```bash
pip install -r requirements.txt

```

## running django management commands & usage

```sh
source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=movieswiki.settings
python manage.py makemigrations
python manage.py migrate
python manage.py fill_countries
python manage.py fill_covid_reports
python manage.py runserver
```

# api endpoints

### List of countries

/api/countries/ (GET)

### Country covid detail

/api/country/<country-name>/ (GET)