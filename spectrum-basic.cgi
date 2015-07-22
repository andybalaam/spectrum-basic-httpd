#!/bin/bash

set -e

LOG=/tmp/log.txt

touch $LOG
env >> $LOG
echo "Started" >> $LOG

END_MARKER="ENDSPECTRUMBASIC"

BAS=/tmp/tmp.bas
TAP=/tmp/tmp.tap
OUT=/tmp/out.txt
PBM=/tmp/out.pbm
XERR=/tmp/xvfb-run-errors.txt

rm -f $BAS

echo '1000 LPRINT "Content-type: text/html"' >> $BAS
echo '1010 LPRINT ""' >> $BAS
echo '1020 LPRINT "Hello"' >> $BAS

echo '9999 LPRINT "'$END_MARKER'"' >> $BAS

echo "Made basic: " >> $LOG
cat $BAS >> $LOG

/bas2tap/bas2tap -q -w -a $BAS $TAP

echo "Made tap" >> $LOG

rm -f $OUT $PBM

xvfb-run -e $XERR fuse-sdl \
    --tape $TAP \
    --no-sound \
    --printer --textfile=$OUT --graphicsfile=$PBM \
    >> $LOG 2>&1 &
PID=$!

echo "Started xvfb-run" >> $LOG

while [ ! -e $OUT ] ; do sleep 1; done

echo "Found out file" >> $LOG

while true; do
{
    grep -q "$END_MARKER" $OUT && break
    sleep 1
    echo "Not found end marker yet" >> $LOG
}; done

echo "Found end marker" >> $LOG

kill %1
xargs kill -9 < /tmp/.X99-lock

cat $OUT | grep -v "$END_MARKER"

