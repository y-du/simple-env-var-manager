"""
   Copyright 2022 Yann Dumont

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

import unittest
import os
import sevm


test_str = "test"


class Section(sevm.Config):
    var_c = None
    var_d = test_str


class Config(sevm.Config):
    var_a = None
    var_b = test_str
    section = Section


class TestConfig(unittest.TestCase):
    def test_default_value(self):
        config = Config()
        self.assertEqual(config.var_b, test_str)

    def test_override_value_str(self):
        os.environ["VAR_A"] = test_str
        config = Config()
        self.assertEqual(config.var_a, test_str)

    def test_override_value_empty_str(self):
        os.environ["VAR_A"] = ""
        config = Config()
        self.assertEqual(config.var_a, "")

    def test_override_value_int(self):
        os.environ["VAR_A"] = "0"
        config = Config()
        self.assertEqual(config.var_a, 0)

    def test_override_value_negative_int(self):
        os.environ["VAR_A"] = "-1"
        config = Config()
        self.assertEqual(config.var_a, -1)

    def test_override_value_float(self):
        os.environ["VAR_A"] = "0.0"
        config = Config()
        self.assertEqual(config.var_a, 0.0)

    def test_override_value_negative_float(self):
        os.environ["VAR_A"] = "-1.0"
        config = Config()
        self.assertEqual(config.var_a, -1.0)

    def test_override_value_complex(self):
        os.environ["VAR_A"] = "3+5j"
        config = Config()
        self.assertEqual(config.var_a, (3+5j))

    def test_override_value_true(self):
        os.environ["VAR_A"] = "true"
        config = Config()
        self.assertEqual(config.var_a, True)

    def test_override_value_false(self):
        os.environ["VAR_A"] = "false"
        config = Config()
        self.assertEqual(config.var_a, False)

    def test_section_default_value(self):
        config = Config()
        self.assertEqual(config.section.var_d, test_str)

    def test_section_override_value_str(self):
        os.environ["SECTION_VAR_C"] = test_str
        config = Config()
        self.assertEqual(config.section.var_c, test_str)

    def test_lower_case_keys(self):
        os.environ["var_a"] = test_str
        config = Config(upper_keys=False)
        self.assertEqual(config.var_a, test_str)

    def test_section_lower_case_keys(self):
        os.environ["section_var_c"] = test_str
        config = Config(upper_keys=False)
        self.assertEqual(config.section.var_c, test_str)

    def test_prefix_override_value_str(self):
        os.environ["TEST_VAR_A"] = test_str
        config = Config(prefix="test")
        self.assertEqual(config.var_a, test_str)

    def test_prefix_section_override_value_str(self):
        os.environ["TEST_SECTION_VAR_C"] = test_str
        config = Config(prefix="test")
        self.assertEqual(config.section.var_c, test_str)

    def test_prefix_no_sub_prefix_override_value_str(self):
        os.environ["TEST_VAR_C"] = test_str
        config = Config(prefix="test", sub_prefix=False)
        self.assertEqual(config.section.var_c, test_str)

    def test_no_sub_prefix_override_value_str(self):
        os.environ["VAR_C"] = test_str
        config = Config(sub_prefix=False)
        self.assertEqual(config.section.var_c, test_str)

    def test_require_value(self):
        try:
            Config(require_value=True)
        except Exception as ex:
            self.assertIsInstance(ex, sevm.NoValueError)


if __name__ == '__main__':
    unittest.main()
