#! /bin/bash

datetime=`date +%F`
tempdir=$datetime"/"
zipfilename=${datetime}".zip"

cp -r output/ $tempdir
zip -qr $zipfilename $tempdir
rm -rf $tempdir
