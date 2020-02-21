#!/usr/bin/env bash

echo "Log on to console and create a new project."

PROJECT_ID=??
CRON_FETCH_DATA_URL=https://cron-ntapdiwuga-ez.a.run.app/cron/fetch-data
CRON_CLEANUP_URL=https://cron-ntapdiwuga-ez.a.run.app/cron/cleanup

gcloud components update
gcloud config set run/platform managed
gcloud config set run/region europe-west4
gcloud auth configure-docker
gcloud components install docker-credential-gcr

# Enable cloud scheduler, service account with permissions on cron service.
gcloud services enable cloudscheduler.googleapis.com
gcloud iam service-accounts create rss-aggregator-scheduler --display-name "RSS Aggregator scheduler"
gcloud run services add-iam-policy-binding cron \
   --member=serviceAccount:rss-aggregator-scheduler@${PROJECT_ID}.iam.gserviceaccount.com \
   --role=roles/run.invoker

# Schedule two jobs.
gcloud beta scheduler jobs create http test-job --schedule "every 7 hours" \
   --http-method=GET \
   --uri=${CRON_FETCH_DATA_URL} \
   --oidc-service-account-email=rss-aggregator-scheduler@${PROJECT_ID}.iam.gserviceaccount.com   \
   --oidc-token-audience=${CRON_FETCH_DATA_URL}
gcloud beta scheduler jobs create http test-job --schedule "every 7 hours" \
   --http-method=GET \
   --uri=${CRON_CLEANUP_URL} \
   --oidc-service-account-email=rss-aggregator-scheduler@${PROJECT_ID}.iam.gserviceaccount.com   \
   --oidc-token-audience=${CRON_CLEANUP_URL}
