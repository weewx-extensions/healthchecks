#    Copyright (c) 2026 Rich Bell <bellrichm@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#

import unittest
import mock

import configobj

import helpers

import user.healthchecks

class TestHealthChecksServiceThread(unittest.TestCase):
    def test_run(self):
        host = helpers.random_string()
        uuid = helpers.random_string()

        skin_dict = {
            'host': host,
            'uuid': uuid
        }

        skin_config = configobj.ConfigObj(skin_dict)
        with mock.patch('user.healthchecks.weewx.reportengine'):
            with mock.patch('user.healthchecks.urlopen') as mock_urlopen:
                SUT = user.healthchecks.HealthChecksGenerator(None, skin_config)

                SUT.run()

                mock_urlopen.assert_called_once_with(f"https://{host}/{uuid}", timeout=10)

if __name__ == '__main__':
    helpers.run_tests()
