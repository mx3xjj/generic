#!/bin/bash

# error message
error_msg ()
{
	echo 1>&2 "Error: $1"
}

# get input parameters
RSTUDIO=true
SHINY=false
REXAMPLES=false
USER="hadoop"
USERPW="hadoop"
PLYRMR=false
RHDFS=false
UPDATER=true
LATEST_R=false
RSTUDIOPORT=8787
SPARKR=false
SPARKLYR=false
RSTUDIO_URL="https://download2.rstudio.org/rstudio-server-rhel-1.0.153-x86_64.rpm"
MIN_USER_ID=400 # default is 500 starting from 1.0.44, EMR hadoop user id is 498
SHINY_URL="https://download3.rstudio.org/centos5.9/x86_64/shiny-server-1.5.1.834-rh5-x86_64.rpm"
CLOUDYR=false

while [ $# -gt 0 ]; do
	case "$1" in
		--sparklyr)
			SPARKLYR=true
			;;
  	--rstudio)
      RSTUDIO=true
  		;;
  	--rstudio-url)
      shift
      RSTUDIO_URL=$1
  		;;
		--no-rstudio)
			RSTUDIO=false
			;;
		--shiny)
			SHINY=true
			;;
  	--shiny-url)
      shift
      SHINY_URL=$1
  		;;
		--rexamples)
			REXAMPLES=true
			;;
		--plyrmr)
			PLYRMR=true
			;;
		--rhdfs)
			RHDFS=true
			;;
  	--updateR)
      UPDATER=true
  		;;
		--no-updateR)
			UPDATER=false
			;;
		--latestR)
			LATEST_R=true
			UPDATER=false
			;;
    --sparkr)
    	SPARKR=true
    	;;
    --rstudio-port)
      shift
      RSTUDIOPORT=$1
      ;;
		--user)
		   shift
		   USER=$1
		   ;;
 		--user-pw)
 		   shift
 		   USERPW=$1
 		   ;;
    --cloudyr)
     	CLOUDYR=true
     	;;
		-*)
			# do not exit out, just note failure
			error_msg "unrecognized option: $1"
			;;
		*)
			break;
			;;
	esac
	shift
done

# get positional args
while getopts h:t:r:p:v: OPTION
do
     case $OPTION in
         h)
             CONFIGURATION_CSV=$OPTARG
             ;;
         t)
             TEST=$OPTARG
             ;;
         r)
             SERVER=$OPTARG
             ;;
         p)
             PASSWD=$OPTARG
             ;;
         v)
             VERBOSE=1
             ;;
         *)
             error_msg "unrecognized option: $1"
             exit 1
             ;;
     esac
done
