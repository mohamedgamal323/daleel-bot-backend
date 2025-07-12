#!/bin/bash
set -e

echo "Running backend tests..."
cd "$(dirname "$0")/.."
python -m pytest src/backend/tests/ -v

echo "Backend tests completed successfully!"
