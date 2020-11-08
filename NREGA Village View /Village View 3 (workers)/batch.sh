#!/bin/bash

function new_session {
    name='must_'$1
    python /home/accts/ark79/EGC/selenium_demo/aakashpt2/oop/get_mus_oop.py $1
    echo $name
    echo $code
}  


start=$(date +"%T")
for start_val in {0..4672..25}
do
   new_session $start_val &
done

echo "oop"
wait 

python /home/accts/ark79/EGC/selenium_demo/aakashpt2/merger.py
rm -r '/home/accts/ark79/EGC/selenium_demo/aakashpt2/alicia/data'

end=$(date +"%T")
time=$(( $(date -d "$end" "+%s") - $(date -d "$start" "+%s") ))
mail -s "we're done <3" "alicia.kacharia@yale.edu"<< EOF 
this took $time seconds
EOF
