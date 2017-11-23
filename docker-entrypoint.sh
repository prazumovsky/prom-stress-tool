#!/bin/bash
if [[ $READ ]]; then
    prom-stress-tool -r -l $PROMETHEUS -rp $READ_PERIOD -j $JOB_NAME -i $INSTANCE;
else
    prom-stress-tool -P $PORT -n $COUNT -s $SPEED;
fi