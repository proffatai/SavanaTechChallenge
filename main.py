import json
from cloud_iac_analyzer import load_json_file, analyze_resources

def main():
    cloud_resources = load_json_file("data/cloud.json")
    iac_resources = load_json_file("data/iac.json")

    analysis_result = analyze_resources(cloud_resources, iac_resources)

    print(json.dumps(analysis_result, indent=4))
   
if __name__ == "__main__":
    main()