#!/bin/sh

if [[ $# -ne 1 ]]
then
  echo usage: `basename $0` VERSION
  exit 0
fi

find -name x | xargs rm -f
cp -r src pymp
tar -cvf pymp-$1.tar.gz `find pymp -type f | grep -v "~" | grep -v ".pyc" | grep -v .log`
rm -rf pymp

exit 0
