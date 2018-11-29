#!/bin/sh 

# do cat depression_text_samples_extended.json | python -m json.tool > depression_text_samples_pretty.json
for i in $(ls -p $1 | grep -v /);
do
   echo Doing $i
   mkdir -p $1/pretty
   FILENAME=$i | sed -e 's/\..*$//'
   echo > $1/pretty/$i
   cat $1/$i | python -m json.tool > $1/pretty/$i
done