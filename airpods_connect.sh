#!/bin/bash

echo "Connect to Airpods..."

while true
do

bluetoothctl pair 00:00:00:00:00:00
bluetoothctl trust 00:00:00:00:00:00
bluetoothctl connect 00:00:00:00:00:00
if [[ $? -eq 0 ]]
then
    echo "Succes!"
    echo "The connection to the Headphones is working!"
    exit 0
else
    echo "Unable to make an connection with the Headphones!"
    echo "Testing again...(to interrupt: Ctrl + c)"
fi

done
