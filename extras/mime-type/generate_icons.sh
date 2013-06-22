#!/usr/bin/env bash

mkdir -p t2t-icons/16x16/mimetypes/
mkdir -p t2t-icons/22x22/mimetypes/
mkdir -p t2t-icons/24x24/mimetypes/
mkdir -p t2t-icons/32x32/mimetypes/
mkdir -p t2t-icons/48x48/mimetypes/
mkdir -p t2t-icons/64x64/mimetypes/
mkdir -p t2t-icons/72x72/mimetypes/
mkdir -p t2t-icons/96x96/mimetypes/
mkdir -p t2t-icons/128x128/mimetypes/

rm t2t-icons/16x16/mimetypes/*.png
rm t2t-icons/22x22/mimetypes/*.png
rm t2t-icons/24x24/mimetypes/*.png
rm t2t-icons/32x32/mimetypes/*.png
rm t2t-icons/48x48/mimetypes/*.png
rm t2t-icons/64x64/mimetypes/*.png
rm t2t-icons/72x72/mimetypes/*.png
rm t2t-icons/96x96/mimetypes/*.png
rm t2t-icons/128x128/mimetypes/*.png


for icon in text-x-txt2tags.png
do 
convert $icon -geometry '16x16>' -unsharp 0.8x0.6+0.8 t2t-icons/16x16/mimetypes/mime-$icon 
convert $icon -geometry '22x22>' -unsharp 0.8x0.6+0.8 t2t-icons/22x22/mimetypes/mime-$icon
convert $icon -geometry '24x24>' -unsharp 0.8x0.6+0.8 t2t-icons/24x24/mimetypes/mime-$icon
convert $icon -geometry '32x32>' -unsharp 0.8x0.6+0.8 t2t-icons/32x32/mimetypes/mime-$icon 
convert $icon -geometry '48x48>' -unsharp 0.6x0.5+0.6 t2t-icons/48x48/mimetypes/mime-$icon
convert $icon -geometry '64x64>' -unsharp 0.6x0.5+0.6 t2t-icons/64x64/mimetypes/mime-$icon
convert $icon -geometry '72x72>' -unsharp 0.6x0.5+0.6 t2t-icons/72x72/mimetypes/mime-$icon
convert $icon -geometry '96x96>' -unsharp 0.6x0.5+0.6 t2t-icons/96x96/mimetypes/mime-$icon
convert $icon -geometry '128x128>'                    t2t-icons/128x128/mimetypes/mime-$icon
echo "$icon icon generated"
done



