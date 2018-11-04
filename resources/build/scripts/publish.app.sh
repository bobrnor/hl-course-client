#!/usr/bin/env bash

set -e

cd "${0%/*}"

source .version
NEW_VERSION="$(./semver.sh bump minor ${VERSION})"

echo "bumping version: ${VERSION} => ${NEW_VERSION}"

mkdir -p ../.app/
pip freeze > ../.app/requirements.txt
cp -a ./../../../src/ ../.app/
docker build -t bobrnor/hl-course-client:${NEW_VERSION} ../.

source docker.io.auth

docker login -u ${USERNAME} -p ${PASSWORD}
docker push bobrnor/hl-course-client:${NEW_VERSION}
docker logout

echo "VERSION=${NEW_VERSION}" > .version