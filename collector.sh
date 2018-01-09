#!/usr/bin/env bash

declare -a arr=(
"/user/twitter/FlumeData.1467360970190"
"/user/twitter/FlumeData.1467360970191"
"/user/twitter/FlumeData.1467360970192"
"/user/twitter/FlumeData.1467360970193"
)

for i in "${arr[@]}"
do
echo "$i"
hdfs dfs -get "$i" /home/user/
python collect_sentiments.py
rm FlumeData*
done

