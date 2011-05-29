#!/bin/sh

if [[ $# -ne 1 ]]
then
  echo usage: `basename $0` VERSION
  exit 0
fi

dir="tmp"`date +%s`
mkdir $dir
for i in `find . -name ".hg" -type d -printf "\t" -execdir pwd \; -execdir hg status -c -m -a -d \; -printf "\n" | grep src/ | awk ' {print $2} '`
do
  echo cp --parents $i $dir
  cp --parents $i $dir
done

cp -r $dir/src pymp
tar -cvf pymp-$1.tar.gz `find pymp -type f`
rm -rf pymp
rm -rf $dir

exit 0
