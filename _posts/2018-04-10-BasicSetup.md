---
title: A basic Dockerfile
tags: docker
---

Lets write ourselves a generic Dockerfile using build-args to update an image for `apt` based distros

```bash
ARG DISTRO=ubuntu
ARG BASEIMAGE=xenial
FROM ${DISTRO}:${BASEIMAGE}

# This DockerFile is looked after by
LABEL maintainer "James Percival <me@example.com>"

# Update the system
RUN apt update && apt -y dist-upgrade
```

You can then build images with e.g.

```bash
docker build -t debian-stable --build-arg DISTRO=debian --build-arg BASEIMAGE=stable Dockerfile
```

and then fire up a root session with

```bash
docker run --rm --it debian-stable bash
```
