import os
import tempfile
import unittest

from mercury206 import config


class TestCreateSampleConfig(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='rt')

    def tearDown(self):
        self.temp_file.close()
        os.unlink(self.temp_file.name)

    def test_create_sample_config(self):
        config.create_sample_config(self.temp_file.name)
        self.assertEqual("""[serial]
device = 

[mercury]
address = 123456

""",
            self.temp_file.read())


class TestLoadConfig(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_config_path = os.path.join(current_dir, 'test_config.ini')

    def test_settings_from_config(self):
        settings = config.settings_from_config(self.test_config_path)
        self.assertEqual(
            {'address': 123456, 'device': '/dev/serial'},
            settings)
