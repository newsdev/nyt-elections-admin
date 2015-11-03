![](https://cloud.githubusercontent.com/assets/109988/10830648/215db03c-7e57-11e5-9a46-ca90186dd8af.png)

A really, really simple Django-based admin interface for our elections loader.

**NOTE**: This is substantially broken and will be in active development leading up to the November 3rd, 2015, general election. Use at your own risk.

## Bootstrapping
Our environment and install requirements.

### Database
```
createdb elex
createuser elex
psql elex
alter user elex with superuser;
```

### Python environment
```
mkvirtualenv nyt-elections-admin
git clone git@github.com:newsdev/nyt-elections-admin.git && cd nyt-elections-admin
pip install -r requirements.txt
add2virtualenv .
export DJANGO_SETTINGS_MODULE=config.dev.settings
```

### Secrets / configuration
```
AP_API_KEY              # Your AP API key
ELEX_RECORDING=         # mongodb or flat
ELEX_LOGGING_URL=       # Your syslog URL, e.g., 127.0.0.1 or logs.papertrail.com
ELEX_LOGGING_PORT=      # Your syslog port, e.g., 514 or 1111
```

### Load data

#### Initial data
Initial data is only candidates, ballot positions and races. Does not run aggregates.
```
django-admin load_initial --date=2015-11-03
```

#### Global data
Global data loads the entire state of all races for this election. Does run aggregates. Will blow away edits to candidates and ballot positions.
```
django-admin load_initial --date=2015-11-03
```

### Updates
Updates refreshes races, candidate results and reporting units. Does run aggregates. Will not blow away edits to candidates or ballot positions.
```
django-admin load_updates --date=2015-11-03
```