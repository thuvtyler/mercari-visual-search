#!/bin/bash
set -euo pipefail

RUN_PIPELINE_MODE="${RUN_PIPELINE:-auto}"
DATA_READY=true

if [ ! -f "mercari_listings.json" ] || [ ! -f "clip_embeddings.npz" ]; then
  DATA_READY=false
fi

if [ "${RUN_PIPELINE_MODE}" = "always" ]; then
  echo "RUN_PIPELINE=always - refreshing Mercari data before launch"
  python run_pipeline.py
elif [ "${RUN_PIPELINE_MODE}" = "auto" ]; then
  if [ "${DATA_READY}" = "false" ]; then
    echo "Mercari dataset missing - running pipeline before launch"
    python run_pipeline.py
  else
    echo "Found existing dataset artifacts - skipping pipeline"
  fi
else
  echo "RUN_PIPELINE=${RUN_PIPELINE_MODE} - skipping data pipeline"
fi

exec "$@"
