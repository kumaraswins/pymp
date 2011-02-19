#!/bin/sh

if [[ -d "/usr/share/icons/hicolor/" ]] 
then
  ln -s /opt/pymp/data/icons/16x16/pymp.png /usr/share/icons/hicolor/16x16/apps/pymp.png
  ln -s /opt/pymp/data/icons/26x26/pymp.png /usr/share/icons/hicolor/26x26/apps/pymp.png
  ln -s /opt/pymp/data/icons/40x40/pymp.png /usr/share/icons/hicolor/40x40/apps/pymp.png
  ln -s /opt/pymp/data/icons/48x48/pymp.png /usr/share/icons/hicolor/48x48/apps/pymp.png
  ln -s /opt/pymp/data/icons/64x64/pymp.png /usr/share/icons/hicolor/64x64/apps/pymp.png
  ln -s /opt/pymp/data/icons/scalable/pymp.png /usr/share/icons/hicolor/scalable/apps/pymp.png
fi

exit 0
