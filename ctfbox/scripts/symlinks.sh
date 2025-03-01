#!/bin/sh

ln -sf /usr/bin/distrobox-host-exec /usr/bin/podman && \
  ln -sf /usr/bin/distrobox-host-exec /usr/bin/podman-compose && \
  ln -sf /usr/bin/distrobox-host-exec /usr/bin/docker && \
  ln -sf /usr/bin/distrobox-host-exec /usr/bin/docker-compose && \
  ln -sf /usr/bin/distrobox-host-exec /usr/bin/devpod
