import json


def load_json_file(file_path: str) -> list:
    with open(file_path, "r") as file:
        return json.load(file)


def find_matching_iac_resource(cloud_resource: dict, iac_resources: list):
    return next(
        (iac for iac in iac_resources if iac["id"] == cloud_resource["id"]),
        None
    )


def compare_properties(cloud_props: dict, iac_props: dict, parent_key=""):
    change_log = []
    all_keys = set(cloud_props.keys()) | set(iac_props.keys())

    for key in all_keys:
        cloud_value = cloud_props.get(key)
        iac_value = iac_props.get(key)

        full_key = f"{parent_key}.{key}" if parent_key else key

        if isinstance(cloud_value, dict) and isinstance(iac_value, dict):
            change_log.extend(
                compare_properties(cloud_value, iac_value, full_key)
            )
        elif cloud_value != iac_value:
            change_log.append({
                "KeyName": full_key,
                "CloudValue": cloud_value,
                "IacValue": iac_value
            })

    return change_log


def analyze_resources(cloud_resources: list, iac_resources: list) -> list:
    report = []

    for cloud_resource in cloud_resources:
        matching_iac = find_matching_iac_resource(
            cloud_resource, iac_resources
        )

        if matching_iac is None:
            state = "Missing"
            change_log = []
        else:
            change_log = compare_properties(
                cloud_resource["properties"],
                matching_iac["properties"]
            )
            state = "Match" if not change_log else "Modified"

        report.append({
            "CloudResourceItem": cloud_resource,
            "IacResourceItem": matching_iac,
            "State": state,
            "ChangeLog": change_log
        })

    return report