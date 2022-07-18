#!/usr/bin/env bash
# run the container
sudo xhost +si:localuser:root

sudo docker run -it \
    --runtime nvidia \
    --rm \
    --security-opt  seccomp=unconfined \
    --network host \
    -v /tmp/.X11-unix/:/tmp/.X11-unix \
    -v /tmp/argus_socket:/tmp/argus_socket \
    -v /etc/enctune.conf:/etc/enctune.conf \
    --device /dev/video0 \
    --device /dev/video1 \
    snapcon-workshop:heidelberg
