#    Copyright (c) 2025 Rich Bell <bellrichm@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#

import configobj
import logging

import unittest
import mock

import user.healthchecks

class TestConfiguration(unittest.TestCase):
    def test_enable_is_false(self):
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
        with mock.patch.object(logger, 'info') as mock_info:
            user.healthchecks.HealthChecksService(mock_engine, config)
            mock_info.assert_called_once_with(
                "Not enabled, exiting.")

        print("end")

if __name__ == '__main__':
    test_suite = unittest.TestSuite()                                                    # noqa: E265
    test_suite.addTest(TestConfiguration('test_enable_is_false'))  # noqa: E265
    unittest.TextTestRunner().run(test_suite)                                            # noqa: E265

    #unittest.main(exit=False)                                                           # noqa: E265
