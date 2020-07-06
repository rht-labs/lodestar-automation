import json
import datetime

subject = context["repositories"]

status = {
  "overall_status": "",
  "messages": [],
  "subsystems": []
}
ocp_subsystem = {
  "name": "openshift",
  "status": "",
  "state": "",
  "info": "",
  "updated": "",
  "access_urls": [],
  "messages": []
}

with open(f"../../{subject['directory']}/engagement.json", "r") as read_file:
  engagement = json.load(read_file)

current_state = subject["anarchy_subject"]["spec"]["vars"]["current_state"]
desired_state = subject["anarchy_subject"]["spec"]["vars"]["desired_state"]

ocp_subsystem["state"] = current_state
ocp_subsystem["updated"] = str(datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0).isoformat())
ocp_subsystem["access_urls"] = [
  {
    "title": "Web Console",
    "url": f"https://console-openshift-console.apps.{engagement['ocp_sub_domain']}.{context['ocp_base_url']}"
  },
  {
    "title": "API",
    "url": f"https://api.{engagement['ocp_sub_domain']}.{context['ocp_base_url']}:6443"
  }
]

if current_state == "provisioning":
  ocp_subsystem["status"] = "yellow"
  ocp_subsystem["info"] = "Building cluster"
elif current_state == desired_state :
  ocp_subsystem["status"] = "green"
  ocp_subsystem["info"] = "Working as expected"
else:
  ocp_subsystem["status"] = "yellow"
  ocp_subsystem["info"] = "Contact SRE team"

status["overall_status"] = ocp_subsystem["status"]
status["subsystems"].append(ocp_subsystem)

with open(f"../../{subject['directory']}/status.json", 'w') as fp:
  json.dump(status, fp)
