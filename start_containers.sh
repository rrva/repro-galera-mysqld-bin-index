#!/bin/sh
IMAGE=galera-repro
HOST1=$(docker run --name xdb1 -d $IMAGE)
HOST2=$(docker run --name xdb2 -d $IMAGE)
HOST3=$(docker run --name xdb3 -d $IMAGE)
IP1=$(docker inspect --format='{{.NetworkSettings.IPAddress}}' $HOST1)
IP2=$(docker inspect --format='{{.NetworkSettings.IPAddress}}' $HOST2)
IP3=$(docker inspect --format='{{.NetworkSettings.IPAddress}}' $HOST3)
./env/bin/fab -u root -p docker -H $IP1,$IP2,$IP3 setup
./env/bin/fab -u root -p docker -H $IP1,$IP2,$IP3 check
docker rm -f $HOST1 $HOST2 $HOST3
