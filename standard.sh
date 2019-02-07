#!/usr/bin/env bash

test -x

if [ "$#" = 0 ]; then
    echo "standard.sh images_dir"
    exit
fi

imgdir="$1"
number=1

for img in  "$imgdir"/*?*;do
    format_number=$(printf "%04d" $number)
    image_extension=$(file "$img" | cut -d':' -f 2 | cut -d' ' -f 2)
    image_extension=${image_extension// /}
    image_extension=${image_extension,,}
    echo $image_extension

    case $image_extension in
        png|jpeg|jpg) echo "ok";;
        * ) 
        echo "Invalid image $img:$image_extension"
        continue ;;
    esac 

    mv "$img" "$imgdir/$format_number.$image_extension"
    echo "$imgdir/$format_number.$image_extension"
    number=$[number+1]
done