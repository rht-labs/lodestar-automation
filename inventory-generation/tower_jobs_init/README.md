# Ansible Tower

This playbook is used to inform Ansible Tower of new inventories created by lodestar-automation. When a new inventory is created, it will generate the necessary projects, job templates, inventories, and inventory sources to kick off the [Configure Ansible Tower](https://github.com/redhat-cop/infra-ansible/blob/master/playbooks/ansible/tower/configure-ansible-tower.yml) and report back the relevant job ID.

# Variables

Some additional variables are required to be passed in from a private config file

| name      | description                                           | required | default |
|-----------|-------------------------------------------------------|----------|---------|
| directory | The directory path to create the appropriate files in | y        | NA      |
| organization | Tower Org | y | NA |
| ansible_tower_url | Tower URL | y | NA |
| ansible_tower_admin_password | Tower Admin Password | y | NA |
| ansible_tower_username | Tower User Name | y | NA |
| scm_credential_name | Name of the existing Source Credential in Tower | y | NA |
