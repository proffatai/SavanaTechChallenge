from cloud_iac_analyzer import analyze_resources, Resource


def test_missing_resource() -> None:
    cloud: list[Resource] = [{"id": "res-1", "type": "compute", "properties": {}}]
    iac: list[Resource] = []

    result = analyze_resources(cloud, iac)

    assert result[0]["State"] == "Missing"
    assert result[0]["ChangeLog"] == []


def test_match_resource() -> None:
    cloud: list[Resource] = [{"id": "res-1", "type": "compute", "properties": {"size": "10kb"}}]
    iac: list[Resource] = [{"id": "res-1", "type": "compute", "properties": {"size": "10kb"}}]

    result = analyze_resources(cloud, iac)

    assert result[0]["State"] == "Match"
    assert result[0]["ChangeLog"] == []


def test_modified_nested_properties() -> None:
    cloud: list[Resource] = [
        {
            "id": "res-1",
            "type": "storage",
            "properties": {
                "size": "17kb",
                "tags": {
                    "totalAmount": "17kb"
                }
            }
        }
    ]

    iac: list[Resource] = [
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

    result = analyze_resources(cloud, iac)

    assert result[0]["State"] == "Modified"
    assert len(result[0]["ChangeLog"]) == 2

    keys = {c["KeyName"] for c in result[0]["ChangeLog"]}
    assert "size" in keys
    assert "tags.totalAmount" in keys


def test_resource_without_properties() -> None:
    cloud: list[Resource] = [{"id": "res-1", "type": "compute", "properties": {}}]
    iac: list[Resource] = [{"id": "res-1", "type": "compute", "properties": {}}]

    result = analyze_resources(cloud, iac)

    assert result[0]["State"] == "Match"
    assert result[0]["ChangeLog"] == []


def test_array_comparison() -> None:
    """
    Tests that array differences are detected correctly.
    """
    cloud: list[Resource] = [{
        "id": "res-1",
        "type": "security-group",
        "properties": {
            "rules": [
                {"port": 80},
                {"port": 443}
            ]
        }
    }]

    iac: list[Resource] = [{
        "id": "res-1",
        "type": "security-group",
        "properties": {
            "rules": [
                {"port": 80},
                {"port": 8080}
            ]
        }
    }]

    result = analyze_resources(cloud, iac)

    assert result[0]["State"] == "Modified"

    keys = {c["KeyName"] for c in result[0]["ChangeLog"]}
    assert "rules[1].port" in keys