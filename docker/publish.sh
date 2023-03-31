#!/bin/bash

docker run --privileged --rm tonistiigi/binfmt --install all

VERSION=0.1.0

docker buildx build --push --platform linux/amd64 -t fabianhk/nano-siem:amd64-${VERSION} -f docker/Dockerfile .
docker buildx build --push --platform linux/arm64 -t fabianhk/nano-siem:arm64-${VERSION} -f docker/Dockerfile .
docker manifest rm fabianhk/nano-siem:${VERSION}
docker manifest create fabianhk/nano-siem:${VERSION} fabianhk/nano-siem:amd64-${VERSION} fabianhk/nano-siem:arm64-${VERSION}
docker manifest push fabianhk/nano-siem:${VERSION}
