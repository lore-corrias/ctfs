#!/bin/sh

git clone https://github.com/neovim/neovim /tmp/nvim && \
  cd /tmp/nvim && \
  make CMAKE_BUILD_TYPE=RelWithDebInfo && \
  
