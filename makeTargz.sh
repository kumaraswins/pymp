#!/bin/sh

if [[ $* -ne 1 ]]
then
  echo usage: `basename $0` VERSION
  exit 0
fi

cp -r src pymp
tar -cvf pymp-$1.tar.gz `find pymp -type f | grep -v "~" | grep -v ".pyc"`
rm -rf pymp

exit 0
