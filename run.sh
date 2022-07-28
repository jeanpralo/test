#!/bin/bash


docker build . -t fergus-challenge

docker run --rm -it -p 5000:5000 fergus-challenge