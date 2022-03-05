"""
   Copyright 2019 Yann Dumont

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

__version__ = "2.1.0"
__title__ = "simple-env-var-manager"
__description__ = "Define configurations, read configurations from environemnt and access your variables via an object tree that plays well with IDE code completion."
__url__ = "https://github.com/y-du/env-var-manager"
__author__ = "Yann Dumont"
__license__ = "Apache License 2.0"
__copyright__ = "Copyright (c) 2019 Yann Dumont"


from .manager import *

__all__ = (
    manager.__all__
)
