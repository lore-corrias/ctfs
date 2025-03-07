#!/bin/sh

curl "https://raw.githubusercontent.com/MeLThRoX/burp-big-sur-icons/refs/heads/main/src/export/dark.png" -o /usr/share/burpsuite/icon.png

mkdir -p /usr/share/applications

cat <<EOF >/usr/share/applications/burpsuite.desktop
[Desktop Entry]
Name=Burp Suite
GenericName=Web Security Testing Tool
Comment=Web vulnerability scanner and proxy tool
Exec=/bin/sh -c '_JAVA_AWT_WM_NONREPARENTING=1 /usr/bin/burpsuite'
Icon=/usr/share/burpsuite/icon.png
Terminal=false
Type=Application
Categories=Utility;Development;Network;
Keywords=Burp;Security;Testing;Proxy;
EOF
