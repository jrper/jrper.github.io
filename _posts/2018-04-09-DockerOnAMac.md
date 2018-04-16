---
title: Using Docker on a mac
tags: docker
---

There are now several different ways to run Docker containers on an Apple Mac. First, there's an app for that [Docker for Mac](https://docs.docker.com/docker-for-mac/). Second, there's command line options, which spin up a [VirtualBox](https://www.virtualbox.org) virtual machine running [boot2docker](https://github.com/boot2docker/boot2docker) and run the actual image/container from inside there.

The first option installs and runs like any other OSX app from a ```.dmg```. However it doesn't really support multiple simultaneous users, which isn't good if you want to use it for something like CI with Jenkins. The second option has packages for MacPorts and for [HomeBrew](https://pilsniak.com/how-to-install-docker-on-mac-os-using-brew/). Interaction with this is via the docker-machine command, so that, given a machine created with
```bash
docker-machine create <MACHINE NAME>
```
you start and setup your environment with
```bash
docker-machine start <MACHINE NAME>
eval $( docker-machine env <MACHINE NAME> )
```

Now you can run stuff with the usual `docker <COMMAND>` syntax.
