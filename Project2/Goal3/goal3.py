import sys
import os
from subprocess import call, Popen
import subprocess
import random
import string
import csv
import urllib2
import urllib

def send_mail(inmsg, emailID):
    filepath = "database/"
    if not os.path.exists("database"):
        os.makedirs("database")
    filepath = filepath + emailID + ".pem" 
    #print " filepath is: " +filepath
    found = 0
    if os.path.exists(filepath):
        found = 1
        print "Destination certificate exists in local database"
    else:
        #print "Searching in webpage"
        url = "https://courses.ncsu.edu/csc574/lec/001/CertificateRepo"
        response = urllib2.urlopen(url)
        cr = csv.reader(response)
        for row in cr:
            #print row[0]
            if row[0] == emailID:
                dest_cert = urllib.URLopener()
                dest_cert.retrieve(row[1], filepath)
                #print filepath
                status = call(['openssl', 'verify', '-CAfile', 'root-ca.crt', filepath]) 
                if status == 0:
                    found = 1
                    print "Certificate downloaded from repository is verified and added to database"
                else:
                    print "Certificate downloaded from repository verification failed"
                    os.remove(filepath)
                    return
    if found == 0:
        print "Destination certificate not found in repository and also in local database"
        return
    
    key=''.join([random.choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for i in range (0,32)])
    #key = "IamManiKumar"
    #print key
    skey_file=open("skey.txt",'w+')
    skey_file.write(key)
    skey_file.close()
    #status = call(['openssl', 'rsautl', '-encrypt', '-inkey', '103E.pem', '-certin', '-in', 'skey.txt', '-out', 'encskey.txt'])
    status = call(['openssl', 'rsautl', '-encrypt', '-inkey', filepath, '-certin', '-in', 'skey.txt', '-out', 'encskey.txt'])
    enc_key_file=open("encskey.txt",'r')
    encskey = enc_key_file.read()
    enc_key_file.close()
    #print encskey
    #status = call(['openssl', 'rsautl', '-decrypt', '-inkey', 'mykey.pem', '-in', 'encskey.txt', '-out', 'decskey.txt'])
    #dec_key_file=open("decskey.txt",'r')
    #decskey = dec_key_file.read()
    #dec_key_file.close()
    #print decskey
    blankmsg = '\n'
    inmsg_file=open("inmsg.txt",'w+')
    inmsg_file.write(inmsg)
    inmsg_file.close()    
    status = call(['openssl', 'enc', '-aes-256-cbc', '-base64', '-in', 'inmsg.txt', '-k', key, '-out', 'encinmsg.txt'])
    enc_inmsg_file=open("encinmsg.txt",'r')
    encinmsg = enc_inmsg_file.read()
    enc_inmsg_file.close()
    #print encinmsg
    #print len(encinmsg)
    #status = call(['openssl', 'enc', '-aes-256-cbc', '-base64', '-d', '-in', 'encinmsg.txt', '-k', key, '-out', 'decinmsg.txt'])
    #dec_inmsg_file=open("decinmsg.txt",'r')
    #decinmsg = dec_inmsg_file.read()
    #dec_inmsg_file.close()
    #print "Before printing decrypted"
    #print decinmsg
    
    concat_msg = encskey + '\n' + blankmsg + encinmsg
    msg_to_hash=open("message_to_hash.txt",'w+')
    msg_to_hash.write(concat_msg)
    msg_to_hash.close()
    
    status = call(['openssl', 'dgst', '-sha1', '-out', 'sha.txt', 'message_to_hash.txt'])
    hash_msg = open("sha.txt",'r')
    full_hash_msg = hash_msg.read()
    v = full_hash_msg.split(" ")
    #print("before v[1]")
    #print v[1]
    #print len(v[1])
    
    hash1=open("hash.txt",'w+')
    hash1.write(v[1])
    hash1.close()
    
    status = call(['openssl', 'rsautl', '-sign', '-inkey', 'mykey.pem', '-keyform', 'PEM', '-in', 'hash.txt', '-out', 'sign.txt'])
    
    sign =open("sign.txt",'r')
    signature = sign.read();
    #print signature
    
    #status = call(['openssl', 'rsautl', '-inkey', 'pubkey.pem', '-pubin', '-in', 'sign.txt', '-out', 'decsign.txt'])
    
    final_msg = "from: pghanta@ncsu.edu,to: "+ emailID +"@ncsu.edu" + "\n" +"-----BEGIN CSC574 MESSAGE-----" + "\n" + encskey + "\n" + blankmsg + encinmsg + "\n" + blankmsg +signature + "\n"+"-----END CSC574 MESSAGE-----" + "\n"
    
    #final_msg = "from: rsandil@ncsu.edu,to: "+ "mani" +"@ncsu.edu" + "\n" +"-----BEGIN CSC574 MESSAGE-----" + "\n" + "encskey" + "\n" + "\n"  + "encinmsg" + "\n" + "\n" +"signature" + "\n"+"-----END CSC574 MESSAGE-----" + "\n"
    
    
    #print final_msg
    email_msg=open("email_msg.txt",'w+')
    email_msg.write(final_msg)
    email_msg.close()
    print "Email sent successfully"

def receive_mail(recv_file):
    #print recv_file
    if os.path.exists(recv_file):
        #print "proceed"
        lines = open(recv_file).read().split("\n\n")
        #for row in lines:
        #    print row
        #    print "text"
        if lines[2][0] == '\n':
            temp = lines[2][1:]
            lines[2] = temp
        temp = lines[1] + '\n'
        lines[1] = temp
        #print "lines from here"
        #print lines[0]
        #print "ok"
        #print lines[1]
        #print "ok"
        #print lines[2]
        
        encline0 = lines[0].split("-----BEGIN CSC574 MESSAGE-----\n" );
        emailHead = encline0[0].split("@ncsu.edu")
        fromEmail = emailHead[0][6:]
        encRcvSkey = encline0[1]
        encRcvmsg = lines[1]
        encline2 = lines[2].split("\n-----END CSC574 MESSAGE-----")
        encRecvsign = encline2[0]
        
        frcvskey =open("encRcvSkey.txt",'w+')
        frcvskey.write(encRcvSkey)
        frcvskey.close()
        
        frcvmsg =open("encRcvmsg.txt",'w+')
        frcvmsg.write(encRcvmsg)
        frcvmsg.close()
        
        frcvsign =open("encRecvsign.txt",'w+')
        frcvsign.write(encRecvsign)
        frcvsign.close()
        
        
        filepath = "database/"
        filepath = filepath + fromEmail + ".pem" 
        
        if not os.path.exists("database"):
            os.makedirs("database")
        found = 0
        if os.path.exists(filepath):
            found = 1
            print "Destination certificate exists in local database"
        else:
            #print "Searching in webpage"
            url = "https://courses.ncsu.edu/csc574/lec/001/CertificateRepo"
            response = urllib2.urlopen(url)
            cr = csv.reader(response)
            for row in cr:
                #print row[0]
                if row[0] == fromEmail:
                    dest_cert = urllib.URLopener()
                    dest_cert.retrieve(row[1], filepath)
                    status = call(['openssl', 'verify', '-CAfile', 'root-ca.crt', filepath]) 
                    if status == 0:
                        found = 1
                        print "Certificate downloaded from repository is verified and added to database"
                    else:
                        print "Certificate downloaded from repository verification failed"
                        os.remove(filepath)
                        return
        if found == 0:
            print "Destination certificate not found in repository and also in local database"
            return
         
        v = Popen(['openssl', 'x509', '-pubkey', '-noout', '-in', filepath],stdout=subprocess.PIPE).communicate()
        public = v[0]
        pub_file = open("senderPubkey.pem", 'w+')
        pub_file.write(public)
        pub_file.close()
        status = call(['openssl', 'rsautl', '-inkey', 'senderPubkey.pem', '-pubin', '-in', 'encRecvsign.txt', '-out', 'decRecvsign.txt'])
        
        rcvd_concat_msg = encRcvSkey + "\n" + "\n" + encRcvmsg
        rcvd_msg_to_hash=open("rcvd_message_to_hash.txt",'w+')
        rcvd_msg_to_hash.write(rcvd_concat_msg)
        rcvd_msg_to_hash.close()
    
        status = call(['openssl', 'dgst', '-sha1', '-out', 'rcvd_sha.txt', 'rcvd_message_to_hash.txt'])
        rcvd_hash_msg = open("rcvd_sha.txt",'r')
        rcvd_full_hash_msg = rcvd_hash_msg.read()
        v = rcvd_full_hash_msg.split(" ")
        #print "computed hash from rcvmsg: \n"+ v[1]
        #print len(v[1])
    
        rcv_hash=open("decRecvsign.txt",'r')
        decRecvsign = rcv_hash.read()
        #print "decrypted sign from rcvmsg: \n"+decRecvsign
        rcv_hash.close()
        
        if v[1] == decRecvsign:
            print "Signature in the mail is verified"
        else:
            print "Signature verification failed. Message rejected!"
            return
            
        status = call(['openssl','rsautl','-decrypt','-in','encRcvSkey.txt','-inkey','mykey.pem', '-out', 'recv_skey.txt'])
        fskey = open("recv_skey.txt", "r");
        rcvd_skey = fskey.read();
        fskey.close()
        
        status = call(['openssl', 'enc', '-aes-256-cbc', '-base64', '-d', '-in', 'encRcvmsg.txt', '-k', rcvd_skey, '-out', 'rcvd_msg.txt'])
        rcvd_msg_file=open("rcvd_msg.txt",'r')
        rcvd_msg = rcvd_msg_file.read()
        rcvd_msg_file.close()
        print "Received message is \n" + rcvd_msg
              
    else: 
        print "Received email path does not exist" 
        return

def list_database():
    if not os.path.exists("database"):
        print "Database is empty"
        return
    check = 0
    for file in os.listdir("database"):
        check = 1
        if file.endswith(".pem"):
            print(file)
    if check == 0:
        print "Database is empty"
    
#v = Popen(['openssl', 'x509', '-pubkey', '-noout', '-in', '103E.pem'],stdout=subprocess.PIPE).communicate()
#print v[0]
#public = v[0]
#pub_file = open("pubkey.pem", 'w+')
#pub_file.write(public)
#pub_file.close()
#print v[1]
#print "v print done"

print "1. List Database"
print "2. Send Email"
print "3. Receive Email"
print "Enter your choice:"
choice = raw_input()

if choice == '2':
    print "Enter your input"
    str = raw_input()
    print "Enter the destination emailID without @ncsu.edu"
    emailID = raw_input()
    #print "Received input is : ", str
    send_mail(str, emailID)
else: 
    if choice == '3':
        print("Enter the received email file")
        recv_file = raw_input()
        receive_mail(recv_file)
    else:
        if choice == '1':
            list_database()
        else:
            print "Not a valid option"
            
