#!/bin/sh

ip=192.168.22.139
port=8080

url=http://${ip}:${port}/timestamp
echo $url
server_time=$(curl --no-progress-meter ${url});
local_time=$(date +%s);
difference=$(echo $local_time - $server_time | bc)
echo $difference

#exit



for relay in 0 1 2 3;
do
    for status in On Off;
    do

        nonce="foobarmoep"
	timestamp_temp=$(date +"%s")
	timestamp=$(echo "$timestamp_temp - $difference "|bc)
	echo $diffrence
	echo $timestamp
	#exit
        fookey="random number"


	hash_string=${nonce}${timestamp}${fookey}
        signature=$(echo -n "${hash_string}" | sha256sum | sed -e 's/  -//')

        #echo $hash_string
	#echo $signature

	echo "foo"
	params="status=${status}&relay=${relay}"
	echo $params
	echo "bar"

        curl -v -d $params -H "TimeStamp: ${timestamp}" -H "Signature: ${signature}" -H "Nonce: ${nonce}"  http://${ip}:${port}/relay

	#exit
	sleep 1
    done


done