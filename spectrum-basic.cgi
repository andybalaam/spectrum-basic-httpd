#!/bin/bash

END_MARKER="ENDSPECTRUMBASIC"

BAS=/tmp/tmp.bas
TAP=/tmp/tmp.tap
OUT=/tmp/out.txt
PBM=/tmp/out.pbm

rm -f $BAS

echo '1000 LPRINT "Content-type: text/html"' >> $BAS
echo '1010 LPRINT ""' >> $BAS
echo '1020 LPRINT "Hello"' >> $BAS

echo '9999 LPRINT "'$END_MARKER'"' >> $BAS

/bas2tap/bas2tap -q -w -a $BAS $TAP

rm -f $OUT $PBM

xvfb-run fuse-sdl \
    --tape $TAP \
    --printer --textfile=$OUT --graphicsfile=$PBM \
    > /dev/null &
PID=$!

while [ ! -e $OUT ] ; do sleep 1; done

while true; do
{
    grep -q "$END_MARKER" $OUT && break
    sleep 1
}; done

kill %1
kill $PID

cat $OUT | grep -v "$END_MARKER"

#
#while read LN; do
#{
#    if [ "$LN" == "$END_MARKER" ] ; then
#    {
#        kill %1
#        killall Xvfb
#        break
#    }
#    else
#    {
#        echo "$LN"
#    };fi
#}; done < $OUT

#rm -f $OUT $PBM

