#! /bin/bash

datetime=`date +%F`
tempdir=$datetime"/"
packname=${datetime}".zip"

cp -r output/ $tempdir
zip -qr $packname $tempdir
rm -rf $tempdir
