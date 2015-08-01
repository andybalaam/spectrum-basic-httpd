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

# Collect the meta-variables into an array
declare -a META_VARS=(
    "${AUTH_TYPE}"
    "${CONTENT_LENGTH}"
    "${CONTENT_TYPE}"
    "${GATEWAY_INTERFACE}"
    "${PATH_INFO}"
    "${PATH_TRANSLATED}"
    "${QUERY_STRING}"
    "${REMOTE_ADDR}"
    "${REMOTE_HOST}"
    "${REMOTE_IDENT}"
    "${REMOTE_USER}"
    "${REQUEST_METHOD}"
    "${SCRIPT_NAME}"
    "${SERVER_NAME}"
    "${SERVER_PORT}"
    "${SERVER_PROTOCOL}"
    "${SERVER_SOFTWARE}"
)

# Collect our stdin into an array
declare -a INPUT
while read LINE; do
{
    INPUT[${#INPUT[@]}]=${LINE}
}; done

NUM=10

function string_line()
{
    echo ${NUM}' DATA "'$(echo -n "$1" | sed 's/"/""/g')'"' >> $BAS
    NUM=$((${NUM} + 10))
}
function int_line()
{
    echo ${NUM}' DATA '$1 >> $BAS
    NUM=$((${NUM} + 10))
}

# Write the meta-variables as DATA statements, starting with how many there are
int_line ${#META_VARS[@]}
for MV in "${META_VARS[@]}"; do string_line $MV; done

# Write the stdin as DATA statements, starting with how many lines there are
int_line ${#INPUT[@]}
for INP in "${INPUT[@]}"; do string_line $INP; done

# Write the program we have been told to run into the program
# (Note the feeble attempt to prevent path traversal attacks)
cat /var/www/html${PATH_INFO/..//g} >> $BAS

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

