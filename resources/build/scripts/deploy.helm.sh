#!/usr/bin/env bash

cd "${0%/*}"

source .version
helm upgrade --install hl-course-client-release --namespace hl-course-ns --set "app.version=${VERSION}" ../helm/