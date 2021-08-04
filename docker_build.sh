#! /bin/bash
docker rmi -f cyclone/notice
docker rm -f c_notice
docker build . -t cyclone/notice
docker run --name c_notice -itd  -p 8888:8888 cyclone/notice