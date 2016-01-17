CSC 574 Project 2:
Team Members:
Name : Purna Mani Kumar Ghantasala     Student ID: 200066404
Name : Rashmi Sandilya                 Student ID: 200084902

Step1. Unzip the file CSC574_Final_Project_Deliverables.zip.
Step2. Unzip the file Project2.zip.

All the goals are working perfectly.

Project 2 folder contains following folders.
1. Goal1
2. Goal2
3. Goal3

Goal 1:
1. The Project2 folder contains folder Goal1. Inside the Goal1, there are 2 files outfile.txt and script.sh
2. The script.sh is shell script file and can be executed as below
   ./script.sh
3. After running the script, secret password is stored in Final.txt and secret message is stored in file.txt 

Goal 2:
1. The Project2 folder contains folder Goal2. Inside the Goal2, there are 3 files root-ca.crt which is CA's certificate, 103E.pem, which is my certificate    and the source code file goal2.py.
2. The goal2.py is executed using the following command 
python goal2.py
3. Two output files are generated namely fingerprint.txt and text.txt. fingerprint.txt contains the finger print of the CA certificate. text.txt contains the textual form of our certificate. 

Goal 3:
1. The Project_2 folder contains folder Goal3. Inside the Goal3, there are two files namely goal3.py which contains the source code and mykey.pem which is my private key.
2. The goal3.py is executed using the following command 
python goal3.py
3. The three types of options appears on the command line as follos:
   1. List Database
   2. Send Email
   3. Receive Email
4. User can select the option as appropriate.
5. If option 1 is selected, the files present in the database are listed on the screen.
6. If option 2 is selected, user gets prompt for entering the message to be sent. Next user gets the prompt for the destination Email Id where message is to be sent. Destination Email ID should be entered as "unity"(excluding the domain  name) not unity@ncsu.edu. Ex- For Email ID rsandil@ncsu.edu, user needs to enter "rsandil".
7. If option 3 is selected, user is prompted to input the file path where the received message file is stored.

Obstacles and how they are solved:
1. Using the appropriate command for encryption/decryption/sign and options in the command. Solved by going through OPENSSL manpages and weblinks provided.
2. Message sent by the others could not be verified as they are signed on different formats. Solved by mutual agreement of encrypting and signing by sender and receiver.