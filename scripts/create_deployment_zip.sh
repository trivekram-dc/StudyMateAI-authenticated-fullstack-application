#!/usr/bin/env bash
set -euo pipefail
archive="studymate-ai-deployment.zip"
rm -f "$archive"
zip -r "$archive" . -x '.git/*' -x 'backend/.venv/*' -x 'backend/instance/*' -x 'frontend/node_modules/*' -x 'frontend/dist/*' -x 'backend/frontend_dist/*' -x '*/__pycache__/*' -x '*.pyc' -x '.env' -x 'backend/.env' -x 'frontend/.env'
echo "Created $archive"
