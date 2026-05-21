# Data Engineering Pipeline Workshop 🚀

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![Terraform](https://img.shields.io/badge/Terraform-Enabled-7B42BC.svg)
![GCP](https://img.shields.io/badge/GCP-Cloud-4285F4.svg)

## 📌 Project Overview
This repository contains a containerized, end-to-end data engineering pipeline. It is designed to automatically ingest, process, and load large datasets (such as the NYC Taxi Trip Data in `.parquet` and `.csv.gz` formats) into a cloud data warehouse using modern data engineering practices.

## 🛠️ Tech Stack & Architecture
* **Python**: Core logic for data ingestion and processing (`main.py`, `ingest_data.py`).
* **Docker & Docker Compose**: Containerization for reproducible environments and easy service orchestration (`docker-compose.yaml`).
* **Terraform**: Infrastructure as Code (IaC) to provision cloud resources dynamically on Google Cloud Platform (GCP).
* **Git**: Version control with strict rules to prevent credential leaks and large binary blobs.

## 📂 Project Structure
```text
.
├── docker-compose.yaml    # Container orchestration for database and related services
├── main.py                # Main execution script for the pipeline
├── ingest_data.py         # Data extraction and loading logic
├── terra_files/           # Terraform configurations for GCP infrastructure
├── .gitignore             # Security rules to exclude credentials and large binaries
└── README.md              # Project documentation
