#    Copyright (c) 2025-2026 Rich Bell <bellrichm@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#

import configobj
import logging

import unittest
import mock

import helpers

import user.healthchecks

class TestHealthChecksService(unittest.TestCase):
    def test_init(self):
        print("start")

        mock_engine = mock.Mock()
        host = helpers.random_string()
        uuid = helpers.random_string()

        config_dict = {
            'StdReport': {
                'HealthChecks': {
                    'host': host,
                    'uuid': uuid
                }
            }
        }
        config = configobj.ConfigObj(config_dict)

        with mock.patch('user.healthchecks.urlopen') as mock_urlopen:

            user.healthchecks.HealthChecksService(mock_engine, config)

            mock_urlopen.assert_called_once_with(f"https://{host}/{uuid}/start", timeout=10)

        print("end")

    def test_init_enable_is_false(self):
        print("start")

        mock_engine = mock.Mock()
        config_dict = {
            'StdReport': {
                'HealthChecks': {
                    'enable': False
                }
            }
        }
        config = configobj.ConfigObj(config_dict)

        logger = logging.getLogger('user.healthchecks')
        with mock.patch('user.healthchecks.threading') as mock_threading:
            with mock.patch.object(logger, 'info') as mock_info:
                thread_id = helpers.random_string()
                mock_threading.get_native_id.return_value = thread_id

                user.healthchecks.HealthChecksService(mock_engine, config)

                mock_info.assert_called_once_with("%s %s", thread_id, "Not enabled, exiting.")

        print("end")

if __name__ == '__main__':
    helpers.run_tests()
