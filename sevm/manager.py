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

__all__ = ("Configuration", )

import os


def format_key(key: str, upper: bool) -> str:
    if upper:
        return key.upper()
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


class SetAttributeError(Exception):
    def __init__(self, arg):
        super().__init__(f"'{arg}' is immutable")


class Configuration:
    def __init__(self, upper_keys: bool = True):
        environment = os.environ
        for key in self.__class__.__dict__:
            if not key.startswith("_"):
                value = self.__class__.__dict__[key]
                if self.__is_config(value):
                    self.__dict__[key] = value(upper_keys=upper_keys)
                elif format_key(key, upper_keys) in environment:
                    self.__dict__[key] = detect_type(environment[format_key(key, upper_keys)])
                else:
                    self.__dict__[key] = value

    def __setattr__(self, key, value):
        raise SetAttributeError(key)

    @staticmethod
    def __is_config(cls):
        try:
            return issubclass(cls, Configuration)
        except TypeError:
            return False
