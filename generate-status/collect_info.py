from kubernetes import client, config
import gitlab

g = gitlab.Gitlab(context["gitlab_url"],
                  private_token=context["gitlab_private_key"])
gitlab_group = g.groups.get(context["gitlab_group"])

config.load_incluster_config()
custom_object_api = client.CustomObjectsApi()
anarchy_subject_list = custom_object_api.list_namespaced_custom_object(
    group="anarchy.gpte.redhat.com",
    version="v1",
    namespace=context["babylon_namespace"],
    plural="anarchysubjects",
)


def getOCPAnarchySubject(project_id):
    subject = list(filter(lambda x: 'ocp4' in x["metadata"]["annotations"]["poolboy.gpte.redhat.com/resource-claim-name"]
                          and project_id in x["metadata"]["annotations"]["poolboy.gpte.redhat.com/resource-claim-name"], anarchy_subject_list["items"]))
    if len(subject) > 0:
        return subject[0]
    else:
        return None


context["repositories"] = [
    {
        "url": project.ssh_url_to_repo,
        "directory": str(project.id),
        "ocp_anarchy_subject": getOCPAnarchySubject(str(project.id))
    }
    for project in gitlab_group.projects.list(all=True, include_subgroups=True)]

context["repositories"] = list(
    filter(lambda x: x["ocp_anarchy_subject"] is not None, context["repositories"]))

need_to_process = [element["directory"] for element in context["repositories"]]

print(f"Will update status for repositories: {need_to_process}")
