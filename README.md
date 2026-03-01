# Cloud Infrastructure Drift Analysis Tool

## Overview
Compares Cloud resources against Infrastructure-as-Code (IaC) definitions to detect drift.

## States

- Match → No differences. ChangeLog is empty.
- Modified → Differences detected. ChangeLog contains entries.
- Missing → Cloud resource not defined in IaC. ChangeLog is empty.

## Run the Tool Locally

Default:
pip install -r requirements.txt
python3 main.py

Custom paths:
python3 main.py --cloud path/to/cloud.json --iac path/to/iac.json

## Run the via Docker 

docker build -t cloud-iac-analyzer .
docker run cloud-iac-analyzer   
## Run Tests

pip install -r requirements.txt
pytest