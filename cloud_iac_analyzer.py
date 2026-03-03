import json
from typing import Any, TypedDict, cast


class Resource(TypedDict):
    id: str
    type: str
    properties: dict[str, Any]


class DriftEntry(TypedDict):
    KeyName: str
    CloudValue: Any
    IacValue: Any


class AnalysisResult(TypedDict):
    CloudResourceItem: Resource
    IacResourceItem: Resource
    State: str
    ChangeLog: list[DriftEntry]


def load_json_file(file_path: str) -> list[Resource]:
    """
    Loads and validates a JSON file containing a list of resources.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError as exc:
        raise FileNotFoundError(f"{file_path} not found.") from exc

    except json.JSONDecodeError as exc:
        raise ValueError(f"{file_path} contains invalid JSON.") from exc

    if not isinstance(data, list):
        raise ValueError("Input file must contain a JSON array.")

    validated_resources: list[Resource] = []

    for item in data:
        if (
            isinstance(item, dict)
            and isinstance(item.get("id"), str)
            and isinstance(item.get("type"), str)
            and isinstance(item.get("properties"), dict)
        ):
            validated_resources.append(cast(Resource, item))
        else:
            raise ValueError("Invalid resource structure detected.")

    return validated_resources


def detect_property_drift(
    cloud_value: Any,
    iac_value: Any,
    parent_key: str = ""
) -> list[DriftEntry]:
    """
    Recursively detects differences between Cloud and IaC properties.
    Supports nested dictionaries and arrays.
    """

    change_log: list[DriftEntry] = []

    if isinstance(cloud_value, dict) and isinstance(iac_value, dict):
        all_keys = set(cloud_value.keys()) | set(iac_value.keys())
        for key in all_keys:
            new_key = f"{parent_key}.{key}" if parent_key else key
            change_log.extend(
                detect_property_drift(
                    cloud_value.get(key),
                    iac_value.get(key),
                    new_key
                )
            )

    elif isinstance(cloud_value, list) and isinstance(iac_value, list):
        if len(cloud_value) != len(iac_value):
            change_log.append({
                "KeyName": parent_key,
                "CloudValue": len(cloud_value),
                "IacValue": len(iac_value),
            })

        for index, (c_item, i_item) in enumerate(zip(cloud_value, iac_value)):
            new_key = f"{parent_key}[{index}]"
            change_log.extend(detect_property_drift(c_item, i_item, new_key))

    else:
        if cloud_value != iac_value:
            change_log.append({
                "KeyName": parent_key,
                "CloudValue": cloud_value,
                "IacValue": iac_value,
            })

    return change_log



def build_index(resources: list[Resource]) -> dict[str, Resource]:
    """
    Builds a resource index keyed by resource ID.
    """
    index: dict[str, Resource] = {}
    for resource in resources:
        index[resource["id"]] = resource
    return index


def analyze_resources(
    cloud_resources: list[Resource],
    iac_resources: list[Resource]
) -> list[AnalysisResult]:
    """
    Compares Cloud resources against IaC resources
    and returns structured drift analysis.
    """

    if not cloud_resources:
        return []

    report: list[AnalysisResult] = []
    iac_index = build_index(iac_resources)

    for cloud_resource in cloud_resources:
        resource_id = cloud_resource["id"]
        matching_iac = iac_index.get(resource_id)

        if matching_iac is None:
            
            report.append({
                "CloudResourceItem": cloud_resource,
                "IacResourceItem": {
                    "id": resource_id,
                    "type": "",
                    "properties": {}
                },
                "State": "Missing",
                "ChangeLog": [],
            })
            continue

        change_log = detect_property_drift(
            cloud_resource.get("properties", {}),
            matching_iac.get("properties", {})
        )

        state = "Match" if not change_log else "Modified"

        report.append({
            "CloudResourceItem": cloud_resource,
            "IacResourceItem": matching_iac,
            "State": state,
            "ChangeLog": change_log,
        })

    return report