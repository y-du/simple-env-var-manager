simple-env-var-manager
=======

Define configurations, read config values from environment and access your configuration via an object tree that plays well with IDE code completion.

---

+ [Description](#description)
+ [Installation](#installation)

---

Description
---

With `simple-env-var-manager` the configuration is defined as a class in your code and is accessible by IDE code completion mechanisms, thus ruling out having to guess config keys during implementation.
Configurations are stored as object trees during runtime and values reside in attributes.

Installation
----

Install the `simple-env-var-manager` package via pip by issuing the following command with the desired release `X.X.X`: 

- `pip install git+https://github.com/y-du/simple-env-var-manager.git@X.X.X` 

Upgrade to new version: 

- `pip install --upgrade git+https://github.com/y-du/simple-env-var-manager.git@X.X.X`

Uninstall: 

- `pip uninstall simple-env-var-manager`
