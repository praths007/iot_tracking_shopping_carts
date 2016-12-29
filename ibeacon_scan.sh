#!/bin/bash
# iBeacon Scan 

## Receiver id and receiver co-ordinates to be defined by user

RECV_ID='recv_1' # Receiver number
X_COR_RECV=0 # Receiver X co-ordinate
Y_COR_RECV=0 # Receiver Y co-ordinate
INTERVAL_SECONDS = 3 # Time interval for which we want to group the records together

## User input ends 

if [[ $1 == "parse" ]]; then
  packet=""
  capturing=""
  count=0
  while read line
  do
    count=$[count + 1]
    if [ "$capturing" ]; then
      if [[ $line =~ ^[0-9a-fA-F]{2}\ [0-9a-fA-F] ]]; then
        packet="$packet $line"
      else
        if [[ $packet =~ ^04\ 3E\ 2A\ 02\ 01\ .{26}\ 02\ 01\ .{14}\ 02\ 15 ]]; then
          UUID=`echo $packet | sed 's/^.\{69\}\(.\{47\}\).*$/\1/'`
          MAJOR=`echo $packet | sed 's/^.\{117\}\(.\{5\}\).*$/\1/'`
          MINOR=`echo $packet | sed 's/^.\{123\}\(.\{5\}\).*$/\1/'`
          POWER=`echo $packet | sed 's/^.\{129\}\(.\{2\}\).*$/\1/'`
          UUID=`echo $UUID | sed -e 's/\ //g' -e 's/^\(.\{8\}\)\(.\{4\}\)\(.\{4\}\)\(.\{4\}\)\(.\{12\}\)$/\1-\2-\3-\4-\5/'`
          MAJOR=`echo $MAJOR | sed 's/\ //g'`
          MAJOR=`echo "ibase=16; $MAJOR" | bc`
          MINOR=`echo $MINOR | sed 's/\ //g'`
          MINOR=`echo "ibase=16; $MINOR" | bc`
          POWER=`echo "ibase=16; $POWER" | bc`
          POWER=$[POWER - 256]
          RSSI=`echo $packet | sed 's/^.\{132\}\(.\{2\}\).*$/\1/'`
 	  RSSI=`echo "ibase=16; $RSSI" | bc`
          RSSI=$[RSSI - 256]
	  TIME_STAMP=`date`
	  TIME=`date +%s`
	  

	  KEY=$(($TIME/$INTERVAL_SECONDS))
	  UNIX_TIME=$(($KEY*$INTERVAL_SECONDS))


          if [[ $2 == "-b" ]]; then
		# Below lines are the output format, changing this will change the format of script output  
	    echo "$RECV_ID$UNIX_TIME$UUID$MAJOR$MINOR,$UUID,$MAJOR,$MINOR,$POWER,$RSSI,$TIME_STAMP,$RECV_ID,$X_COR_RECV,$Y_COR_RECV"
          else
    	    echo "$RECV_ID$UNIX_TIME$UUID$MAJOR$MINOR,$UUID,$MAJOR,$MINOR,$POWER,$RSSI,$TIME_STAMP,$RECV_ID,$X_COR_RECV,$Y_COR_RECV"
	
          fi
        fi
        capturing=""
        packet=""
      fi
    fi

    if [ ! "$capturing" ]; then
      if [[ $line =~ ^\> ]]; then
        packet=`echo $line | sed 's/^>.\(.*$\)/\1/'`
        capturing=1
      fi
    fi
  done
else
  sudo hcitool lescan --duplicates 1>/dev/null &
  if [ "$(pidof hcitool)" ]; then
    sudo hcidump --raw | ./$0 parse $1
  fi
fi
