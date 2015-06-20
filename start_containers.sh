#!/bin/sh
IMAGE=galera-repro
HOST1=$(docker run --name xdb1 -d $IMAGE)
HOST2=$(docker run --name xdb2 -d $IMAGE)
HOST3=$(docker run --name xdb3 -d $IMAGE)
docker run --link xdb1:xdb1 --link xdb2:xdb2 --link xdb3:xdb3 galera-repro-fab /w/env/bin/fab --fabfile=/w/fabfile.py -u root -p docker -H xdb1,xdb2,xdb3 setup
