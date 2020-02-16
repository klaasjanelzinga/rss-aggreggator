#!/usr/bin/env bash

echo "Log on to console and create a new project."
gcloud components update
gcloud config set run/platform managed
gcloud config set run/region europe-west4
gcloud auth configure-docker
gcloud components install docker-credential-gcr

# Enable cloud scheduler, service account with permissions on cron service.
gcloud services enable cloudscheduler.googleapis.com
gcloud iam service-accounts create rss-aggregator-scheduler --display-name "RSS Aggregator scheduler"
gcloud run services add-iam-policy-binding cron \
   --member=serviceAccount:rss-aggregator-scheduler@PROJECT-ID.iam.gserviceaccount.com \
   --role=roles/run.invoker