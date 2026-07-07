#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Your Name <your.email@example.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Module for creating a file with custom content

version_added: "1.0.0"

description:
    - This module creates a text file on the remote host at the specified path
    - with the specified content.

options:
    path:
        description:
            - The path where the file should be created.
        required: true
        type: str
    content:
        description:
            - The content to write to the file.
        required: true
        type: str
    state:
        description:
            - Whether the file should exist or not.
        choices: ['present', 'absent']
        default: present
        type: str

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
- name: Create a file with content
  my_own_collection.my_own_module:
    path: /tmp/test.txt
    content: "Hello, Ansible!"

- name: Remove a file
  my_own_collection.my_own_module:
    path: /tmp/test.txt
    state: absent
'''

RETURN = r'''
path:
    description: The path to the file
    type: str
    returned: success
    sample: /tmp/test.txt
content:
    description: The content written to the file
    type: str
    returned: success
    sample: "Hello, Ansible!"
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    # Define arguments
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )

    result = dict(
        changed=False,
        path='',
        content='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    state = module.params['state']

    # Check mode
    if module.check_mode:
        if state == 'present':
            if not os.path.exists(path):
                result['changed'] = True
                result['message'] = f"File {path} would be created"
            else:
                with open(path, 'r') as f:
                    existing_content = f.read()
                if existing_content != content:
                    result['changed'] = True
                    result['message'] = f"File {path} would be updated"
        else:
            if os.path.exists(path):
                result['changed'] = True
                result['message'] = f"File {path} would be removed"
        module.exit_json(**result)

    try:
        if state == 'present':
            if not os.path.exists(path):
                # Create directory if not exists
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as f:
                    f.write(content)
                result['changed'] = True
                result['message'] = f"File {path} created"
            else:
                with open(path, 'r') as f:
                    existing_content = f.read()
                if existing_content != content:
                    with open(path, 'w') as f:
                        f.write(content)
                    result['changed'] = True
                    result['message'] = f"File {path} updated"
                else:
                    result['message'] = f"File {path} already exists with correct content"
        else:  # state == 'absent'
            if os.path.exists(path):
                os.remove(path)
                result['changed'] = True
                result['message'] = f"File {path} removed"
            else:
                result['message'] = f"File {path} does not exist"

        result['path'] = path
        result['content'] = content
        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=f"An error occurred: {str(e)}", **result)

def main():
    run_module()

if __name__ == '__main__':
    main()
