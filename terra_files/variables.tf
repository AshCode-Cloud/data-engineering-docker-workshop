variable "project" {
  description = "Project"
  default     = "kestra-sandbox-demo-496308"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "us-central1"
}


variable "bq_dataset_name" {
  description = "my BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "my Storage Bucket Name"
  default     = "kestra-sandbox-demo-496308-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}