set -e

LAKEFS_ACCESS_KEY_ID="${LAKEFS_ACCESS_KEY_ID:?Укажите LAKEFS_ACCESS_KEY_ID после setup}"
LAKEFS_SECRET_ACCESS_KEY="${LAKEFS_SECRET_ACCESS_KEY:?Укажите LAKEFS_SECRET_ACCESS_KEY после setup}"
LAKEFS_ENDPOINT="http://lakefs:8000/api/v1"
DOCKER_NETWORK="lakefs-hw19_default"

docker run --rm --network "$DOCKER_NETWORK" \
  -e LAKECTL_CREDENTIALS_ACCESS_KEY_ID="$LAKEFS_ACCESS_KEY_ID" \
  -e LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY="$LAKEFS_SECRET_ACCESS_KEY" \
  -e LAKECTL_SERVER_ENDPOINT_URL="$LAKEFS_ENDPOINT" \
  --entrypoint lakectl treeverse/lakefs:1.5.0 \
  repo list || echo "Error"

docker run --rm --network "$DOCKER_NETWORK" \
  -e LAKECTL_CREDENTIALS_ACCESS_KEY_ID="$LAKEFS_ACCESS_KEY_ID" \
  -e LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY="$LAKEFS_SECRET_ACCESS_KEY" \
  -e LAKECTL_SERVER_ENDPOINT_URL="$LAKEFS_ENDPOINT" \
  --entrypoint lakectl treeverse/lakefs:1.5.0 \
  repo create lakefs://firstproj s3://lakefs-artifacts --default-branch main || true

docker run --rm --network "$DOCKER_NETWORK" \
  -e LAKECTL_CREDENTIALS_ACCESS_KEY_ID="$LAKEFS_ACCESS_KEY_ID" \
  -e LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY="$LAKEFS_SECRET_ACCESS_KEY" \
  -e LAKECTL_SERVER_ENDPOINT_URL="$LAKEFS_ENDPOINT" \
  --entrypoint lakectl treeverse/lakefs:1.5.0 \
  branch create lakefs://firstproj/featone --source lakefs://firstproj/main || true

echo "Hello world!" > /tmp/hw19_myfile.txt
docker run --rm --network "$DOCKER_NETWORK" -v /tmp/hw19_myfile.txt:/data/myfile.txt \
  -e LAKECTL_CREDENTIALS_ACCESS_KEY_ID="$LAKEFS_ACCESS_KEY_ID" \
  -e LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY="$LAKEFS_SECRET_ACCESS_KEY" \
  -e LAKECTL_SERVER_ENDPOINT_URL="$LAKEFS_ENDPOINT" \
  --entrypoint lakectl treeverse/lakefs:1.5.0 \
  fs upload lakefs://firstproj/featone/myfile.txt --source /data/myfile.txt

docker run --rm --network "$DOCKER_NETWORK" \
  -e LAKECTL_CREDENTIALS_ACCESS_KEY_ID="$LAKEFS_ACCESS_KEY_ID" \
  -e LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY="$LAKEFS_SECRET_ACCESS_KEY" \
  -e LAKECTL_SERVER_ENDPOINT_URL="$LAKEFS_ENDPOINT" \
  --entrypoint lakectl treeverse/lakefs:1.5.0 \
  commit lakefs://firstproj/featone -m "Add myfile.txt"

docker run --rm --network "$DOCKER_NETWORK" \
  -e LAKECTL_CREDENTIALS_ACCESS_KEY_ID="$LAKEFS_ACCESS_KEY_ID" \
  -e LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY="$LAKEFS_SECRET_ACCESS_KEY" \
  -e LAKECTL_SERVER_ENDPOINT_URL="$LAKEFS_ENDPOINT" \
  --entrypoint lakectl treeverse/lakefs:1.5.0 \
  diff lakefs://firstproj/main lakefs://firstproj/featone

docker run --rm --network "$DOCKER_NETWORK" \
  -e LAKECTL_CREDENTIALS_ACCESS_KEY_ID="$LAKEFS_ACCESS_KEY_ID" \
  -e LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY="$LAKEFS_SECRET_ACCESS_KEY" \
  -e LAKECTL_SERVER_ENDPOINT_URL="$LAKEFS_ENDPOINT" \
  --entrypoint lakectl treeverse/lakefs:1.5.0 \
  merge lakefs://firstproj/featone lakefs://firstproj/main

echo ""
echo "http://127.0.0.1:8000"
