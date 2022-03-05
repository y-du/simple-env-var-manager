simple-env-var-manager
=======

Define configurations, read config values from environment and access your configuration via an object tree that plays well with IDE code completion.

---

+ [Description](#description)
+ [Quickstart](#quickstart)
+ [Installation](#installation)

---

Description
---

With `simple-env-var-manager` the configuration is defined as a class in your code and is accessible by IDE code completion mechanisms, thus ruling out having to guess config keys during implementation.
Configurations are stored as object trees during runtime and values reside in attributes.
See [Usage](#usage) for more information.


Quickstart
---

Declare environment variables:

```shell
export APP_ID="0c19d322-bc6f-43ea-8956-a853f4db9c06"
export DATABASE_HOST="localhost"
export DATABASE_PORT="5034"
export ALLOW_RETRY="true"
export LOG_LEVEL="info"
```

Implement configs by subclassing `sevm.Config` in your application:

```python
import sevm


# declare config
class DatabaseConfig(sevm.Config):
  host = None
  port = None


# declare config
class Config(sevm.Config):
  app_id = None

  # declare default values
  retry_delay = 5
  allow_retry = False
  log_level = "warning"

  # use a config as a subsection
  database = DatabaseConfig


# initialize config
config = Config()

# automatic boolean string interpretation
if config.allow_retry:
  while not db.connected():
    try:
      # automatic type conversion
      db.connect(config.database.host, config.database.port)
    except ConnectionError:
      logger.warning("connecting to database failed")
      time.sleep(config.retry_delay)
    logger.info("connected to database")
else:
  ...
```

Installation
----

Install the `simple-env-var-manager` package via pip by issuing the following command with the desired release `X.X.X`: 

- `pip install git+https://github.com/y-du/simple-env-var-manager.git@X.X.X` 

Upgrade to new version: 

- `pip install --upgrade git+https://github.com/y-du/simple-env-var-manager.git@X.X.X`

Uninstall: 

- `pip uninstall simple-env-var-manager`
