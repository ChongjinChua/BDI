#! /bin/bash

target_path='../../output_files/analysis.ods'

#close existing soffice, or else it will cause trouble
#kill running soffice process, -c for count, -e to display what is killed
echo "killing all soffice processes..."
pkill -c -e soffice

#create sub-shell that runs in background
echo "running soffice in the background..."
(soffice --calc --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager" --norestore --nologo --nodefault) &

#sleep for 4 seconds to make sure that connection has been established
echo "sleep for 4 seconds..."
sleep 4

#check if analysis.ods exists already. If so, delete it and call Prep_output_file.py. Prep_output_file.py always create a new analysis.ods
if [[ -e $target_path ]]; then
    echo "analysis.ods exist. removing..."
    rm $target_path
fi

#execute python script that prepares output file 
echo "Preparing output file..."
./Prep_output_file.py > debug.txt

#kill running soffice process, -c for count, -e to display what is killed
echo "killing all soffice processes..."
pkill -c -e soffice
sleep 1

#open up analysis.ods in the background
if [[ -e $target_path ]]; then
    echo "opening analysis.ods..."
    (soffice --norestore $target_path) &
else
    echo "analysis.ods doesn't exist!"
fi
