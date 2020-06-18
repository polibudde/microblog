#!/bin/bash
set -ex

USERNAME=polibudde
IMAGE=microblog

docker build -t $USERNAME/$IMAGE:latest .
