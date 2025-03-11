#!/bin/sh

set -ue

apt update -y && apt upgrade -y &&
  grep -v '^#' ./default.packages | xargs apt install -y
