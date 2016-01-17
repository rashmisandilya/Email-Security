#!/bin/bash
clear

rm -f Probable.txt
rm -f Final.txt
rm -f file.txt
rm -f new_file.txt

for n in {a..z}{a..z}{a..z};do 
    echo -n " $n";  
    openssl enc -des-cbc -base64 -d -in outfile.txt -k $n -out file.txt
    if [ $? -eq 0 ] ; then 
	echo "Probable"
	echo "$n" >> Probable.txt
    else
        echo "Not Probable"		
    fi
done

echo "Probables are :"

while read line; do    
    echo $line
    rm -f file.txt
    rm -f new_file.txt
    openssl enc -des-cbc -base64 -d -in outfile.txt -k $line -out file.txt
    tr -cd '\11\12\15\40-\176' < file.txt > new_file.txt
    if cmp file.txt new_file.txt >/dev/null 2>&1; then
        echo "$line" >> Final.txt
    fi    
done < Probable.txt

while read line; do
    echo "Secret Password is $line"
    rm -f file.txt
    rm -f new_file.txt
    openssl enc -des-cbc -base64 -d -in outfile.txt -k $line -out file.txt
    echo "Secret Message is "
    cat file.txt
done < Final.txt
