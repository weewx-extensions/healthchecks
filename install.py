#
#    Copyright (c) 2020-2023 Rich Bell <bellrichm@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
""" Installer for MTTQSubscribe driver and service. """

from io import StringIO

import configobj

from weecfg.extension import ExtensionInstaller

VERSION = '0.2.0'

HEALTHCHECKS_CONFIG = """
[StdReport]
    [[Healthchecks]]
        # Turn the service on and off.
        # Default is: true
        # Only used by the service.
        enable = false
        
        skin = healthchecks
        
        # The host to 'ping'
        # Default is hc-ping.com
        # host = hc-ping.com
        
        # The http request timeout
        # The default is 10
        # timeout = 10
        
        # The HealthChecks uuid
        uuid = REPLACE_ME
"""


def loader():
    """ Load and return the extension installer. """
    return HealthchecksInstaller()

class HealthchecksInstaller(ExtensionInstaller):
    """ The extension installer. """
    def __init__(self):
        install_dict = {
            'version': VERSION,
            'name': 'Healthchecks',
            'description': 'Monitor WeeWX using Healthchecks.io.',
            'author': "Rich Bell",
            'author_email': "bellrichm@gmail.com",
            'files': [
                ('bin/user', ['bin/user/healthchecks.py']),
                ('skins/healthchecks',['skins/healthchecks/skin.conf']),             
            ]
        }

        healthchecks_dict = configobj.ConfigObj(HEALTHCHECKS_CONFIG)
        install_dict['config'] = healthchecks_dict
        install_dict['prep_services'] = 'user.healthchecks.Healthchecks'

        super().__init__(install_dict)
