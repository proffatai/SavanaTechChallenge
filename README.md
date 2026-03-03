# Cloud Infrastructure Drift Analysis Tool

## Overview
This tool compares **Cloud resources** against **Infrastructure-as-Code (IaC)** definitions to detect drift. It identifies missing resources, modified properties, and matches. It can also upload the analysis report to a local S3 bucket via **LocalStack**.

## Drift States

- **Match** → No differences. `ChangeLog` is empty.  
- **Modified** → Differences detected. `ChangeLog` contains entries.  
- **Missing** → Cloud resource not defined in IaC. `ChangeLog` is empty.  


## 1. Install dependencies
```bash
1. pip install -r requirements.txt

2. Run with default JSON files

Uses:
	•	data/cloud.json
	•	data/iac.json
    
`python3 main.py`

3. Run with custom JSON paths
`python3 main.py --cloud path/to/cloud.json --iac path/to/iac.json`

4. Run with S3 upload (requires LocalStack)
python3 main.py --upload


 ## Docker

 `docker build -t cloud-iac-analyzer .` #Build docker image
 `docker run cloud-iac-analyzer` #Run container

## LocalStack + S3 Upload
1. Start LocalStack with Docker Compose

`docker compose up --build`

	•	LocalStack service
	•	S3 bucket: analyzer-reports

2. Run analyzer and upload report
`python3 main.py --upload`

## Run Tests in virtual environment
python3 -m venv venv                    
source venv/bin/activate
pip install -r requirements.txt
pytest

Tests include:
	•	Missing resources detection
	•	Matching resources
	•	Modified properties (nested & arrays)
	•	Array differences detection with bracket notation (rules[1].port)
