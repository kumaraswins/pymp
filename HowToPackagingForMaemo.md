

# How to create a package for maemo #

Goto the scratchbox packaging directory

```
target=pymp-VERSION
mv `find . -maxdepth 1 -type f` packages
hg clone https://pymp.googlecode.com/hg/ $target
cd `ls -t | head -1`
tar -zcf $target.tar.gz src

```

Log into scratchbox and go to the directory

```
dh_make -e markus.scharnowski@gmail.com -f `ls -t | head -1` -c GPL -S
rm ./debian/*.ex ./debian/*.EX
cp ./debianFiles/debian/* ./debian/
dch -i #add something to ./debian/changelog
dpkg-buildpackage -rfakeroot -b
cp debian/changelog debianFiles/debian #for uploading new changelog

```

## Prepare for upload to builder ##

Move away old builds

```
mv `find . -maxdepth 1 -type f` packages/
```

In scratchbox

```
dpkg-buildpackage -rfakeroot -uc -us -sa
dpkg-buildpackage -rfakeroot -uc -us -sa -b

```

With `dpkg-buildpackage -rfakeroot -uc -us -sa -S` binaries would be lost - such as icons.

And upload

```
scp -p *.tar.gz *.diff.gz *change* *.dsc emesem@drop.maemo.org:/var/www/extras-devel/incoming-builder/fremantle/
```

## Query the build ##

  * http://maemo.org/packages/view/pymp/
  * https://garage.maemo.org/builder/fremantle/?C=M;O=D

## After everything went fine ##

Outside scratchbox

```
hg commit -m 'New changelog'
hg push

```

After that update the development directory

```
hg pull
hg update

```

### Tagging ###

And dont forget to tag the new versions if they should be released!

```
echo `date +%F` > latestVersion
hg commit -m 'latestVersion'
hg tag -f -r tip latestVersion
rev=`hg tags | grep latestVersion | cut -d ':' -f 2`
echo $rev
hg tag -f -r $rev `date +%F` #assuming no commiting around midnight
```

## Generating latesFiles file ##

```
find . -name ".hg" -type d -printf "\t" -execdir pwd \; -execdir hg status -c -m -a -d \; -printf "\n" | grep src/ | awk ' {print $2} ' | xargs replacePartOfString.py -d src/ -f | sort > latestFiles
```
# Adding an image to debian/control #

```
uuencode -m $target $target | sed -e s,^,\ ,  > $target.base64
```

# Resources #

  * http://wiki.maemo.org/Packaging
  * http://wiki.maemo.org/Packaging#Adding_an_icon_and_desktop_file
  * http://old-en.opensuse.org/Maemo5 Scratchbox installation for opensuse
  * http://showmedo.com/videotutorials/video?name=linuxJensMakingDeb Video for creating a `*`.deb with a python program