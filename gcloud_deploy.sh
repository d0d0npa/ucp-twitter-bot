#!/bin/bash

. ./.env

gcloud functions deploy $TWEET_FUNCTION_NAME \
--project=$GCP_PROJECT \
--gen2 \
--runtime=python310 \
--region=$GCP_REGION \
--source=. \
--entry-point=function \
--timeout=540s \
--trigger-topic=$TWEET_TOPIC_NAME \
--env-vars-file .env.yaml

gcloud functions deploy $FOLLOW_FUNCTION_NAME \
--project=$GCP_PROJECT \
--gen2 \
--runtime=python310 \
--region=$GCP_REGION \
--source=. \
--entry-point=daily \
--trigger-topic=$DAILY_TOPIC_NAME \
--env-vars-file .env.yaml

gcloud functions deploy $FAV_FUNCTION_NAME \
--project=$GCP_PROJECT \
--gen2 \
--runtime=python310 \
--region=$GCP_REGION \
--source=. \
--entry-point=fav \
--trigger-topic=$TWEET_TOPIC_NAME \
--env-vars-file .env.yaml