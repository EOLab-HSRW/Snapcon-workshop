# Snapcon-workshop
Object detection and image classification with Snap<em>!</em> and Nvidia Jetson.
## Table of content
* [Requirements](#requirements)
* [Setup](#setup)
  * [Building the Container](#building-the-container)
  * [Running the Container](#running-the-container)
* [Running the program](#running-the-program)
  * [Image Classification](#image-classification)
    * [Nvidia Jetson](#nvidia-jetson)
    * [Snap<em>!</em>](#nvidia-jetson)
  * [Object detection](#object-detection)
    * [Nvidia Jetson](#nvidia-jetson)
    * [Snap<em>!</em>](#nvidia-jetson)
## Requirements
* Nvidia Jetson with Jetpack 4.6
* Docker
## Setup
### Building the Container
Use the [`docker/build.sh`](docker/build.sh) to build docker container.
```bash
$ git clone https://github.com/EOLab-HSRW/Snapcon-workshop.git
$ cd Snapcon-workshop
$ docker/build.sh
```
### Running the Container
Use the [`docker/run.sh`](docker/run.sh) to run docker container.
```bash
$ docker/run.sh
```
## Running the program
You can run image classification and object detection program.
### Image Classification
Run python websocket server in Nvidia Jetson and open classification program in Snap!.
#### Nvidia Jetson
Run [`python/Classification.py`](python/Classification.py) in Nvidia Jetson.
``` bash
python3 python/Classification.py
```
> **note**:  If it is the first time running the program, please wait couple of minutes for TensorRT to finish optimizing the network. <br/>
#### Snap<em>!</em>
Open  [`snap/Snap!_with_classification.xml`](snap/Snap!_with_classification.xml) with Snap<em>!</em>.
> **note**: Please use offline version of Snap<em>!</em> with Google Chrome browser to avoid any malfunction. <br/>

Write down your Nvidia Jetson ip adress as input for `connect block` **< ws://ip_address:4040 >**.
  ![connect_block](/assests/Snap!/connect_block.png)
> **note**: You can use `ifconfig` command in Nvidia Jetson to obtain ip address. <br/>

### Object detection
Run python websocket server in Nvidia Jetson and open object detection program in Snap<em>!</em>.
#### Nvidia Jetson
Run [`python/Detection.py`](python/Detection.py) in Nvidia Jetson.
``` bash
python3 python/Detection.py
```
> **note**:  If it is the first time running the program, please wait couple of minutes for TensorRT to finish optimizing the network. <br/>
#### Snap<em>!</em>
Open  [`snap/Snap!_with_detection.xml`](snap/Snap!_with_detection.xml) with Snap<em>!</em>.
> **note**: Please use offline version of Snap<em>!</em> with Google Chrome browser to avoid any malfunction. <br/>

Write down your Nvidia Jetson ip adress as input for `connect block` **< ws://ip_address:4040 >**.
  ![connect_block](/assests/Snap!/connect_block.png)
> **note**: You can use `ifconfig` command in Nvidia Jetson to obtain ip address. <br/>
