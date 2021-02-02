# Ansible Tower

This playbook generates an inventory based off of a list of `engagement_users` found in the `engagement.json` file. It parses out the users into the expected structure found [here](https://github.com/redhat-cop/infra-ansible).

# Variables

Some additional variables are required to be passed in from a private config file

| name      | description                                           | required | default |
|-----------|-------------------------------------------------------|----------|---------|
| directory | The directory path to create the appropriate files in | y        | NA      |
| company_name | Company Name | y | NA |
| organization | Tower Org | y | NA |
| scm_credential_name | Credential name for checking out repos | y | NA |
| ansible_tower_url | Tower URL | y | NA |
| ansible_tower_admin_password | Tower Admin Password | y | NA |
