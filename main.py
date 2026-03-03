import argparse
import json
import os
from cloud_iac_analyzer import load_json_file, analyze_resources
from s3_uploader import upload_report_to_s3


def parse_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cloud Infrastructure Drift Analyzer"
    )
    parser.add_argument(
        "--cloud",
        default="data/cloud.json",
        help="Path to the current cloud state JSON file"
    )
    parser.add_argument(
        "--iac",
        default="data/iac.json",
        help="Path to the IaC definition JSON file"
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload the report to S3 (LocalStack or AWS)"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_cli_arguments()

    # Load JSON resources
    cloud_resources = load_json_file(args.cloud)
    iac_resources = load_json_file(args.iac)

    # Analyze resources
    analysis_result = analyze_resources(cloud_resources, iac_resources)

    # Save report locally
    report_path = "report.json"
    with open(report_path, "w") as file:
        json.dump(analysis_result, file, indent=4)

    print(f"Analysis report saved to {report_path}")

    # Upload to S3 if requested
    if args.upload:
        try:
            upload_report_to_s3(report_path)
            print(f"Report successfully uploaded to S3")
        except Exception as e:
            print(f"Failed to upload report to S3: {e}")


if __name__ == "__main__":
    # Ensure S3_ENDPOINT is set for LocalStack or AWS
    if "S3_ENDPOINT" not in os.environ:
        os.environ["S3_ENDPOINT"] = "http://localstack:4566"
    main()