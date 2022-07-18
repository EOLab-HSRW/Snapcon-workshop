FROM nvcr.io/nvidia/l4t-ml:r32.6.1-py3

ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL /bin/bash

#
# install development packages
#
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            cmake \
		  nano \
    && rm -rf /var/lib/apt/lists/*


#    
# pip dependencies for pytorch-ssd
#
RUN pip3 install --verbose --upgrade Cython && \
    pip3 install --verbose boto3 pandas

#
# install websockets
#
RUN pip3 install websockets


#
# jetson inference
#

COPY . /downloadModels
RUN git clone https://github.com/dusty-nv/jetson-inference.git
ADD downloadModels.sh /jetson-inference/tools
WORKDIR jetson-inference
RUN git submodule update --init 

#
# build source
#
RUN sed -i 's/nvcaffe_parser/nvparsers/g' CMakeLists.txt && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make -j$(nproc) && \
    make install && \
    /bin/bash -O extglob -c "cd /jetson-inference/build; rm -rf -v !(aarch64|download-models.*)" && \
    rm -rf /var/lib/apt/lists/*

#
# download models
#
RUN cd tools && \
    ./downloadModels.sh
