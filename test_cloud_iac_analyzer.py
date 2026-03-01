from cloud_iac_analyzer import analyze_resources


def test_missing_resource():
    cloud = [{"id": "res-1", "properties": {}}]
    iac = []

    result = analyze_resources(cloud, iac)

    assert result[0]["State"] == "Missing"
    assert result[0]["ChangeLog"] == []


def test_match_resource():
    cloud = [{"id": "res-1", "properties": {"size": "10kb"}}]
    iac = [{"id": "res-1", "properties": {"size": "10kb"}}]

    result = analyze_resources(cloud, iac)

    assert result[0]["State"] == "Match"
    assert result[0]["ChangeLog"] == []


def test_modified_nested_properties():
    cloud = [
        {
            "id": "res-1",
            "properties": {
                "size": "17kb",
                "tags": {
                    "totalAmount": "17kb"
                }
            }
        }
    ]

    iac = [
        {
            "id": "res-1",
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


def test_resource_without_properties():
    cloud = [{"id": "res-1"}]
    iac = [{"id": "res-1"}]

    result = analyze_resources(cloud, iac)

    assert result[0]["State"] == "Match"
    assert result[0]["ChangeLog"] == []