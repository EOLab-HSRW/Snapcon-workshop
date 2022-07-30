#!/usr/bin/env bash
# run the container
sudo xhost +si:localuser:root

sudo docker run -it \
    --restart always \
    --runtime nvidia \
    --security-opt  seccomp=unconfined \
    --network host \
    -v /tmp/.X11-unix/:/tmp/.X11-unix \
    -v /tmp/argus_socket:/tmp/argus_socket \
    -v /etc/enctune.conf:/etc/enctune.conf \
    -v $PWD/python:/jetson-inference/snapcon/python \
    -v $PWD/snap:/jetson-inference/snapcon/snap \
    --device /dev/video0 \
    --device /dev/video1 \
    --name container_snapcon \
    snapcon-workshop:heidelberg
