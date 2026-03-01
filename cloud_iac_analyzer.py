import json


def load_json_file(file_path: str):
    with open(file_path, "r") as file:
        return json.load(file)


def detect_property_drift(cloud_props,iac_props,parent_key=""):

    change_log = []
    all_keys = set(cloud_props.keys()) | set(iac_props.keys())

    for key in all_keys:
        cloud_value = cloud_props.get(key)
        iac_value = iac_props.get(key)

        full_key = f"{parent_key}.{key}" if parent_key else key

        if isinstance(cloud_value, dict) and isinstance(iac_value, dict):
            change_log.extend(
                detect_property_drift(cloud_value, iac_value, full_key)
            )
        elif cloud_value != iac_value:
            change_log.append({
                "KeyName": full_key,
                "CloudValue": cloud_value,
                "IacValue": iac_value
            })

    return change_log


def analyze_resources(cloud_resources,iac_resources) :

    report = []

    iac_index = {r["id"]: r for r in iac_resources}

    for cloud_resource in cloud_resources:
        resource_id = cloud_resource.get("id")

        matching_iac = iac_index.get(resource_id)

        cloud_props = cloud_resource.get("properties", {})
        iac_props = matching_iac.get("properties", {}) if matching_iac else {}

        if matching_iac is None:
            state = "Missing"
            change_log = []
        else:
            change_log = detect_property_drift(cloud_props, iac_props)
            state = "Match" if not change_log else "Modified"

        report.append({
            "CloudResourceItem": cloud_resource,
            "IacResourceItem": matching_iac,
            "State": state,
            "ChangeLog": change_log
        })

    return report