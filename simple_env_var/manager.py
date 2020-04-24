"""
   Copyright 2020 Yann Dumont

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


__all__ = ('configuration', 'section', 'loadConfig')


from os import getenv
from logging import getLogger
from inspect import isclass


_root_logger = getLogger('simple-env-var')
_root_logger.propagate = False


class Singleton(type):
    __instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


class Configuration(metaclass=Singleton):
    def __init__(self, load: bool = True):
        if not isinstance(load, bool):
            raise TypeError
        self.__logger = _root_logger.getChild(self.__class__.__name__)
        self.__initiated = False
        if load:
            self.__loadConfig()

    def __loadConfig(self):
        if not self.__initiated:
            sections = {item.__name__: item() for item in self.__class__.__dict__.values() if isclass(item) and issubclass(item, Section)}
            self.__dict__ = {**self.__dict__, **sections}
            self.__logger.debug("Checking environment variables ...")
            for section in sections:
                for key in sections[section].__dict__:
                    env_data = self.__getEnvData(section, key)
                    if env_data:
                        self.__logger.info(
                            "Setting value for key '{}' in section '{}' from environment variable".format(key, section)
                        )
                        sections[section].__dict__[key] = env_data
                    else:
                        if sections[section].__dict__[key] or type(sections[section].__dict__[key]) is bool:
                            self.__logger.info("Using default value for key '{}' in section '{}'".format(key, section))
                        else:
                            self.__logger.warning("Key '{}' in section '{}' not set".format(key, section))
            self.__initiated = True

    def __getEnvData(self, section: str, key: str):
        env_data = getenv("{}_{}_{}".format(self.__class__.__name__, section, key).upper())
        if env_data:
            self.__logger.debug("Found environment variable for key '{}' in section '{}'".format(key, section))
            return self.__loadValue(env_data)

    def __loadValue(self, value: str):
        if len(value) == 0:
            return None
        elif value.isalpha():
            if value in 'True':
                return True
            elif value in 'False':
                return False
            else:
                return value
        else:
            try:
                return int(value)
            except ValueError:
                pass
            try:
                return float(value)
            except ValueError:
                pass
            try:
                return complex(value)
            except ValueError:
                pass
            return value


def configuration(cls):
    attr_dict = cls.__dict__.copy()
    del attr_dict['__dict__']
    del attr_dict['__weakref__']
    sub_cls = type(cls.__name__, (Configuration,), attr_dict)
    sub_cls.__qualname__ = cls.__qualname__
    return sub_cls


def loadConfig(config: object):
    if not isinstance(config, Configuration):
        raise TypeError(type(config))
    config._Configuration__loadConfig()


class Section:
    def __init__(self):
        for key, value in self.__class__.__dict__.items():
            if not key.startswith('_'):
                self.__dict__[key] = value

    def __setattr__(self, key, value):
        err_msg = "value assignment for '{}.{}' not allowed".format(self.__class__.__qualname__, key)
        raise AttributeError(err_msg)


def section(cls):
    attr_dict = cls.__dict__.copy()
    del attr_dict['__dict__']
    del attr_dict['__weakref__']
    sub_cls = type(cls.__name__, (Section,), attr_dict)
    sub_cls.__qualname__ = cls.__qualname__
    return sub_cls
