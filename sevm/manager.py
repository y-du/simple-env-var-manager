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

__all__ = ("Config", "NoValueError")

import os


def format_key(key: str, upper: bool, prefix=None) -> str:
    if prefix:
        key = prefix + key
    if upper:
        key = key.upper()
    return key


def detect_type(value: str):
    if value.isalpha():
        if value == "true":
            return True
        elif value == "false":
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


class ConfigError(Exception):
    pass


class SetAttributeError(ConfigError):
    def __init__(self, arg):
        super().__init__(f"'{arg}' is immutable")


class NoValueError(ConfigError):
    def __init__(self, arg):
        super().__init__(f"no value for '{arg}'")


class Config:
    def __init__(self, prefix: str = None, sub_prefix: bool = True, upper_keys: bool = True, require_value: bool = False):
        environment = os.environ
        if prefix and not prefix.endswith("_"):
            prefix = prefix + "_"
        for key in self.__class__.__dict__:
            if not key.startswith("_"):
                value = self.__class__.__dict__[key]
                if self.__is_config(value):
                    _prefix = None
                    if prefix and sub_prefix:
                        _prefix = f"{prefix}{format_key(key=key, upper=upper_keys)}_"
                    elif sub_prefix:
                        _prefix = f"{format_key(key=key, upper=upper_keys)}_"
                    self.__dict__[key] = value(prefix=_prefix or prefix, sub_prefix=sub_prefix, upper_keys=upper_keys)
                elif format_key(key=key, prefix=prefix, upper=upper_keys) in environment:
                    self.__dict__[key] = detect_type(environment[format_key(key=key, prefix=prefix, upper=upper_keys)])
                else:
                    if value is None and require_value:
                        raise NoValueError(key)
                    self.__dict__[key] = value

    def __setattr__(self, key, value):
        raise SetAttributeError(key)

    @staticmethod
    def __is_config(cls):
        try:
            return issubclass(cls, Config)
        except TypeError:
            return False
