![](https://cloud.githubusercontent.com/assets/109988/10830648/215db03c-7e57-11e5-9a46-ca90186dd8af.png)

## Bootstrapping
our environment and install requirements.
```
mkvirtualenv nyt-elections-admin
git clone git@github.com:newsdev/nyt-elections-admin.git && cd nyt-elections-admin
pip install -r requirements.txt
add2virtualenv .
export DJANGO_SETTINGS_MODULE=config.dev.settings
```

* Before you can load data, you need to have a Postgres database called `elex` and a user `elex` that can insert/update/delete but also create indexes. Since it's local development, we recommend making this user a superuser.
```
createdb elex
createuser elex
psql elex
alter user elex with superuser;
```

* Now you can load data.
```
django-admin load_election
```