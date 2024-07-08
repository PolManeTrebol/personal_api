#!/bin/bash

response=$(curl --write-out "%{http_code}" --silent --output /dev/null http://127.0.0.1:5001/v1/api/healthz)

echo "Health check response: $response"  # Add logging

if [[ "$response" -ge 200 && "$response" -lt 500 ]]; then
  exit 0
else
  exit 1
fi
