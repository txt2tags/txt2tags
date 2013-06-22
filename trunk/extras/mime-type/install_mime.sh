#!/usr/bin/env bash

#create the default application desktop:
cp mime/applications/txt2tags.desktop ~/.local/share/applications/

xdg-mime install mime/text/text-x-txt2tags.xml
xdg-mime default txt2tags.desktop text/x-txt2tags


for size in 16 22 24 32 48 64 72 96 128
do
    xdg-icon-resource install --context mimetypes --size $size t2t-icons/${size}x${size}/mimetypes/mime-text-x-txt2tags.png text-x-txt2tags
    echo "generate txt2tags-icon for icon size $size"
done



