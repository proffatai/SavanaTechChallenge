import argparse
import json
from cloud_iac_analyzer import load_json_file, analyze_resources


def parse_cli_arguments():
    parser = argparse.ArgumentParser(
        description="Cloud Infrastructure Drift Analyzer"
    )
    parser.add_argument(
        "--cloud",
        default="data/cloud.json",
        help="Path to Cloud resources JSON file"
    )
    parser.add_argument(
        "--iac",
        default="data/iac.json",
        help="Path to IaC resources JSON file"
    )
    return parser.parse_args()


def main():
    args = parse_cli_arguments()

    cloud_resources = load_json_file(args.cloud)
    iac_resources = load_json_file(args.iac)

    analysis_result = analyze_resources(
        cloud_resources,
        iac_resources
    )

    print(json.dumps(analysis_result, indent=4))


if __name__ == "__main__":
    main()