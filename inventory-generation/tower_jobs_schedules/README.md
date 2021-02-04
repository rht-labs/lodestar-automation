# Ansible Tower

This playbook generates an inventory of scheduled notifications combining email templates, email credentails, and data found in the `engagement.json` file. The stages are:

1) Build tower_jobs_schedules inventory from resource-dispatcher
2) Launch configure-ansible-tower from your Tower instance with the new inventory from the first stage of deployment
3) Schedules in Tower trigger notification jobs at the desired time sending email to selected engagement users with updates about engagement onboarding and offboarding

# Variables

Some additional variables are required to be passed in from a private config file

| name      | description                                           | required | default |
|-----------|-------------------------------------------------------|----------|---------|
| directory | The directory path to create the appropriate files in | y        | NA      |
| company_name | Company Name | y | NA |
| organization | Tower Org | y | NA |
| scm_credential_name | Credential name for checking out repos | y | NA |
| ansible_tower_url | Tower URL | y | NA |
| ansible_tower_admin_username | Tower Admin Username | no | admin |
| ansible_tower_admin_password | Tower Admin Password | y | NA |
| mail_host_source_project | Project name for mail-host credentials | y | NA |
