import json

cloud_resources = [
    {
        "id": "res-1",
        "type": "storage",
        "properties": {
            "size": "17kb",
            "tags": {
                "totalAmount": "17kb"
            }
        }
    },
    {
        "id": "res-2",
        "type": "compute",
        "properties": {
            "instanceType": "t2.micro"
        }
    }
]


iac_resources = [
    {
        "id": "res-1",
        "type": "storage",
        "properties": {
            "size": "22kb",
            "tags": {
                "totalAmount": "22kb"
            }
        }
    }
]



def find_matching_iac_resource(cloud_resource, iac_resources):
    for iac_resource in iac_resources:
        if iac_resource["id"] == cloud_resource["id"]:
            return iac_resource
    return None

def compare_properties(cloud_props, iac_props, parent_key=""):
    change_log = []
    all_keys = set(cloud_props.keys()) | set(iac_props.keys())

    for key in all_keys:
        cloud_value = cloud_props.get(key)
        iac_value = iac_props.get(key)

        if parent_key == "":
            full_key = key
        else:
            full_key = parent_key + "." + key


        if isinstance(cloud_value, dict) and isinstance(iac_value, dict):
            nested_changes = compare_properties(cloud_value, iac_value, full_key)
            change_log.extend(nested_changes)

    
        elif cloud_value != iac_value:
            change_log.append({
                "KeyName": full_key,
                "CloudValue": cloud_value,
                "IacValue": iac_value
            })

    return change_log



def analyze_resources(cloud_resources, iac_resources):

    report = []

    for cloud_resource in cloud_resources:

        matching_iac = find_matching_iac_resource(cloud_resource, iac_resources)

      
        if matching_iac is None:
            state = "Missing"
            change_log = []

        else:
            change_log = compare_properties(
                cloud_resource["properties"],
                matching_iac["properties"]
            )

            if len(change_log) == 0:
                state = "Match"
            else:
                state = "Modified"

        result = {
            "CloudResourceItem": cloud_resource,
            "IacResourceItem": matching_iac,
            "State": state,
            "ChangeLog": change_log
        }

        report.append(result)

    return report


analysis_result = analyze_resources(cloud_resources, iac_resources)

print(json.dumps(analysis_result, indent=4))