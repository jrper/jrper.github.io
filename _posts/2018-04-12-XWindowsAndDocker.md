---
title: Running an X11 connection with docker
tags: docker x11
---

It's conceivable that you might want to run an X11 based application inside a docker container. If the host system is a mac with XQuartz installed, then [this StackOverflow post](https://stackoverflow.com/a/36190462/5880647) contains the kernel of one method to do so. Note that getting this running may require [modifying your XQuartz defaults](https://bugs.freedesktop.org/show_bug.cgi?id=96260) by running the command
```bash
defaults write org.macosforge.xquartz.X11 enable_iglx -bool true
```
in the terminal.

Putting this all together, the following script produces a wrapper which automatically generates an x connection in a docker command.

```
#!/usr/bin/env bash

NIC=vboxnet0

# Grab the ip address of this box
IPADDR=$(ifconfig $NIC | grep "inet " | awk '{print $2}')

DISP_NUM=$(jot -r 1 100 200)  # random display number between 100 and 200

PORT_NUM=$((6000 + DISP_NUM)) # so multiple instances of the container won't interfer with eachother

socat TCP-LISTEN:${PORT_NUM},reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\" 2>&1 > /dev/null &

XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth.$USER.$$
touch $XAUTH
old_auth=`xauth nlist $DISPLAY | sed -e 's/^..../ffff/'`

docker $1 \
    -v $XSOCK:$XSOCK:rw \
    -v $XAUTH:$XAUTH:rw \
    -e DISPLAY=$IPADDR:$DISP_NUM \
    -e XAUTHORITY=$XAUTH \
    "${@:2}"

rm -f $XAUTH
kill %1       # kill the socat job launched above
```
