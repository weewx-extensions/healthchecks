#    Copyright (c) 2026 Rich Bell <bellrichm@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#

import unittest
import mock

import helpers

import user.healthchecks

class TestHealthChecksServiceThread(unittest.TestCase):
    def test_run(self):
        with mock.patch('user.healthchecks.threading'):
            with mock.patch('user.healthchecks.urlopen'):
                SUT = user.healthchecks.HealthChecksServiceThread(None, None, None)

                with mock.patch.object(user.healthchecks.HealthChecksServiceThread, 'running', new_callable=mock.PropertyMock) as mock_running:
                    # ToDo: Why does the first item 'disappear'?
                    # I really only want 'True, False' so that the loop being tested runs once.
                    # But, I need the extra 'True' for some reason
                    mock_running.side_effect = [True, True, False]

                    SUT.run()
                    print("done 1")

        print("done  2")

if __name__ == '__main__':
    helpers.run_tests()
