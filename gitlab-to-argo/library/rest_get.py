#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import requests

"""
An ansible module to wrap the calls to Ansible Tower REST API (and potentially others).
Main purpose is to better handle REST pagination
"""

# pylint: disable=redefined-builtin,wildcard-import,unused-wildcard-import
from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: rest_get
short_description: Perform REST Calls to get data and to better handle REST pagination
author: Øystein Bedin & Jacob See
requirements: [ ]
'''
EXAMPLES = '''
- rest_get:
    host_url: "https://tower.example.com"
    api_uri: "/api/v2/projects/"
    rest_user: "user"
    rest_password: "passwd"
'''


def main():
    module = AnsibleModule(
        argument_spec=dict(
            url=dict(required=True),
            headers=dict(required=False),
        ),
        supports_check_mode=True,
    )

    # Retrieve the parameters passed in
    url         = module.params['url']
    headers     = module.params['headers']

    # Initialize the output to empty list or dict
    # if re.match('/api/v[12]/settings', api_uri):
    #     rest_output = {}
    # else:
    rest_output = []

    next_call = url

    # Loop till the 'next' element contains Null/None
    while next_call is not None:
        r = requests.get(
            next_call,
            headers=headers,
            verify=False
        )

        # Fetch the next URI returned by the REST call
        # TODO: better error handling when REST service returns non-200 OK
        if "Link" in r.headers:
            next_call = r.headers["Link"]
        else:
            next_call = None

        # Merge the results json to the output list of items
        rest_output = rest_output + r.json()

    module.exit_json(
      changed=False,
      rest_output=rest_output
    )


if __name__ == '__main__':
    main()
