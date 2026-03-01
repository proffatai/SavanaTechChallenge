import pytest
from cloud_iac_analyzer import (
    find_matching_iac_resource,
    compare_properties,
    analyze_resources
)


def test_find_matching_resource():
    cloud = {"id": "res-1"}
    iac = [{"id": "res-1"}]

    result = find_matching_iac_resource(cloud, iac)

    assert result is not None
    assert result["id"] == "res-1"

def test_missing_resource():
    cloud_resources = [{"id": "res-1", "properties": {}}]
    iac_resources = []

    result = analyze_resources(cloud_resources, iac_resources)

    assert result[0]["State"] == "Missing"


def test_property_difference():
    cloud_props = {"size": "10kb"}
    iac_props = {"size": "20kb"}

    changes = compare_properties(cloud_props, iac_props)

    assert len(changes) == 1
    assert changes[0]["KeyName"] == "size"


def test_property_match():
    cloud_props = {"size": "10kb"}
    iac_props = {"size": "10kb"}

    changes = compare_properties(cloud_props, iac_props)

    assert len(changes) == 0