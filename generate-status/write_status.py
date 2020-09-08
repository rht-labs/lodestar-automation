import json
import datetime
from os import path

subject = context["repositories"]

status = {
  "overall_status": "",
  "messages": [],
  "subsystems": []
}
ocp_subsystem = {
  "name": "OpenShift",
  "status": "",
  "state": "",
  "info": "",
  "updated": "",
  "access_urls": [],
  "messages": []
}

with open(f"../../{subject['directory']}/engagement.json", "r") as read_file:
  engagement = json.load(read_file)

if path.exists(f"../../{subject['directory']}/status.json"):
  with open(f"../../{subject['directory']}/status.json", "r") as read_file:
    existing_status = json.load(read_file)
else:
  existing_status = False

if "current_state" not in subject["anarchy_subject"]["spec"]["vars"] or "desired_state" not in subject["anarchy_subject"]["spec"]["vars"]:
  print(f"Skipping {subject['directory']} - state information not found in the Anarchy subject")
  return

if existing_status:
  existing_ocp_subsystem = [subsystem for subsystem in existing_status["subsystems"] if subsystem["name"] == "OpenShift"]
  if len(existing_ocp_subsystem) > 0:
    if subject["anarchy_subject"]["spec"]["vars"]["current_state"] == existing_ocp_subsystem[0]["state"]:
      print(f"Skipping {subject['directory']} - state has not changed since last update")
      return

current_state = subject["anarchy_subject"]["spec"]["vars"]["current_state"]
desired_state = subject["anarchy_subject"]["spec"]["vars"]["desired_state"]

region = engagement["engagement_region"].lower() if "engagement_region" in engagement else "na"
region_url = f"{region}-1"

ocp_subsystem["state"] = current_state
ocp_subsystem["updated"] = str(datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0).isoformat())
ocp_subsystem["access_urls"] = [
  {
    "title": "Web Console",
    "url": f"https://console-openshift-console.apps.{engagement['ocp_sub_domain']}.{region_url}.{context['ocp_base_url']}"
  },
  {
    "title": "API",
    "url": f"https://api.{engagement['ocp_sub_domain']}.{region_url}.{context['ocp_base_url']}:6443"
  }
]

if current_state == "provisioning":
  ocp_subsystem["status"] = "yellow"
  ocp_subsystem["info"] = "Building Cluster. This normally takes about ~45 min from launch. Please check back later for an updated status."
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
