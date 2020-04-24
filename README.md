simple-env-var-manager
=======

Define configuration structures, read config values from environment and access your configuration via an object tree that plays well with IDE code completion.

---

+ [Description](#description)
+ [Quick start](#quick-start)
+ [Requirements](#requirements)
+ [Installation](#installation)
+ [Usage](#usage)
    + [Defining configurations](#defining-configurations)
    + [Initializing configurations](#initializing-configurations)
    + [Setting and getting values](#setting-and-getting-values)
    + [Overriding values via environment variables](#overriding-values-via-environment-variables)
    + [Logging](#logging)

---

Description
---

With `simple-env-var-manager` the configuration is defined as a "structure" in your code and is accessible by IDE code completion mechanisms, thus ruling out having to guess config keys during implementation.
Configurations are stored as object trees during runtime and values reside in attributes.
See [Usage](#usage) for more information.


Quick start
---

    from simple_env_var import configuration, section
    
    @configuration
    class MyConf:

        @section
        class MySection:
            val_1 = 123
            val_2 = "test"
            val_3 = True

    conf = MyConf()


Requirements
----

Python 3.5 or later.


Installation
----

Install the `simple-env-var-manager` package via pip by issuing the following command with the desired release `X.X.X`: 

- `pip install git+https://github.com/y-du/simple-env-var-manager.git@X.X.X` 

Upgrade to new version: 

- `pip install --upgrade git+https://github.com/y-du/simple-env-var-manager.git@X.X.X`

Uninstall: 

- `pip uninstall simple-env-var-manager`


Usage
----

#### Defining configurations

To create a configuration create a `class` and decorate it with `@configuration`.
Within this class you add sections to your configuration by creating further classes and decorating them with `@section`.
Sections house the keys and default values in the form of class attributes.
There's no limit to how many configurations you create.

    from simple_conf import configuration, section
    
    @configuration
    class MyConf:

        @section
        class MySection:
            key = "value"


#### Initializing configurations

To use your configuration you must instantiate it first. 
Multiple instantiations of the same configuration will always yield the same instance. 
By using the `@configuration` decorator the init signature changes:

    conf = MyConf(load=True)

- `load` if set to `False` loading from the environment can be deferred and triggered manually with the provided `loadConfig` function at a later point in time.
    
        my_conf = MyConf(load=False)
        
        # do something
        # my_conf will access the default values of MyConf during this time
        
        loadConfig(my_conf)


#### Setting and getting values

During runtime values are stored in attributes housed in objects representing the respective sections.
Getting values is straightforward:
 
    print(configuration.section.key) -> "value"


Possible types are: `str`, `int`, `float`, `complex`, `bool`, `NoneType`. Other types will be treated as strings.


#### Logging

If your project uses the python `logging` facility you can combine the output produced by `simple-env-var-manager` with your log output.

Retrieve the "simple-env-var" logger via:

    logger = logging.getLogger("simple-env-var")

Add your handler to the logger and optionally set the desired level:

    logger.addHandler(your_handler)
    logger.setLevel(logging.INFO)   # optional
