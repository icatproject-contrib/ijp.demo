#!/bin/bash
# Sleep counter script
echo "Supplied args: $*"
#!/bin/bash

count=0
sleep_time=0
while [[ $# > 1 ]]
do
    key="$1"
    shift

    case $key in
	--count)
	    count="$1"
	    shift
	    ;;
	--sleep)
	    sleep_time="$1"
	    shift
	    ;;
	*)
            # unknown option
	    echo "Unexpected argument: $key"
	    ;;
    esac
done
# Check that we *do* have these values set
# TODO check that they are reasonable values!
go_away=0
if [ $count -eq 0 ]
then
  echo "Count not set"
  go_away=1
fi
if [ $sleep_time -eq 0 ]
then
  echo "Sleep time not set"
  go_away=1
fi
if [ $go_away -eq 1 ]
then
  exit 1
fi
for i in $(seq 1 $count);
do
    echo "Count $i: sleeping for $sleep_time ..."
    sleep $sleep_time
done
echo Finished
