#!/bin/sh

apt update -y && apt upgrade -y && \
  grep -v '^#' ./default.packages | xargs apt install -y
