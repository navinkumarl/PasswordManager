#COMPUTER SCIENCE PROJECT IN PYTHON - PASSWORD MANAGER:-

#IMPORTING REQUIRED MODULES:-

import array
import cryptography#TO BE INSTALLED
from cryptography.fernet import Fernet
import mysql.connector
import os
from os import path
import pickle
import random
import re
from tabulate import tabulate#TO BE INSTALLED
import time

#USER DEFINED FUNCTIONS:-

#TO GENERATE A KEY:

def GENERATE_KEY():
    
    if path.exists("secret.key")==False:
        key=Fernet.generate_key()
        f=open("secret.key","wb")
        f.write(key)
        f.close()
    else:
        return
    
#TO LOAD THE KEY:
    
def LOAD_KEY():
    
    GENERATE_KEY()
    return open("secret.key","rb").read()

#ENCRYPTING:

def ENCRYPT(password):
    
    key=LOAD_KEY()
    f=Fernet(key)
    encoded=password.encode()
    encrypted=f.encrypt(encoded)
    return encrypted

#DECRYPTING:

def DECRYPT(password):
    
    key=LOAD_KEY()
    f=Fernet(key)
    decrypted=f.decrypt(password)
    decoded=decrypted.decode()
    return decoded

#CURRENT TIME CALCULATION:

def CURRENT_TIME():
    
    t=round(time.time()*1000)
    return t

#LOCK TIME CALCULATION:

def LOCK_TIME():
    
    t=round(time.time()*1000)
    return t+1800000

#CONDITIONS FOR PASSWORD VALIDATION:

'''
Password Validation :

1.At least 1 letter between [a-z] and 1 letter between [A-Z].
2.At least 1 number between [0-9].
3.At least 1 character from [_$#@].
4.Minimum length 8 characters.
5.Maximum length 16 characters.
'''

#CHECK PASSWORD VALIDITY:

def CHECK(password):
    
    x = True
    
    while x:
        
        if (len(password)<8 or len(password)>16):
            break
        elif not re.search("[a-z]",password):
            break
        elif not re.search("[0-9]",password):
            break
        elif not re.search("[A-Z]",password):
            break
        elif not re.search("[_$#@]",password):
            break
        elif re.search("\s",password):
            break
        else:
            print("Valid Password")
            x=False
            return password
        
    if x==True:
        print("InValid Password")
        return GENERATOR(password)
    
#PASSWORD GENERATOR:
    
def GENERATOR(password):
    
    l=random.randint(8,16)
    d=['0','1','2','3','4','5','6','7','8','9']
    lc=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    uc=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    s=['_','@','$']
    cl=d+lc+uc+s
    rd=random.choice(d)
    rl=random.choice(lc)
    ru=random.choice(uc)
    rs=random.choice(s)
    tp=rd+rl+ru+rs
    p=""
    
    for i in range(l-4):
        tp=tp+random.choice(cl)
        tpl=array.array("u",tp)
        random.shuffle(tpl)
        
    for i in tpl:
        p=p+i
        
    print("A Valid Password Suggested:",p)
    y=input("Do you want to store the randomly generated password for your website(y/n):").upper()
    
    if y=="Y":
        print("The password stored is:",p)
        x=False
        return p
    else:
        print("The password stored is:",password)
        x=True
        return password
    
#CREATE MASTER PASSWORD:
    
def MASTER_PASSWORD():
    
    if path.exists("masterpassword.dat")==False:
        p=input("Enter the new Master Password:")
        mp=ENCRYPT(p)
        f=open("masterpassword.dat","wb")
        pickle.dump(mp,f)
        f.close()
        print("Successfully Created a New Master Password")
        print()
        return p
    else:
        return
    
#CHECK MASTER PASSWORD:
    
def CHECK_MP():
    
    if path.exists("masterpassword.dat")==True:
        mp=input("Enter the Master Password:")
    else:
        mp=MASTER_PASSWORD()
        
    f=open("masterpassword.dat","rb")
    a=pickle.load(f)
    p=DECRYPT(a)
    
    if mp==p:
        c=0
        return
    else:
        c=-1
        
#MAIN PROGRAM:-
        
c=0

#CREATING A CONNECTION TO MYSQL:

db=mysql.connector.connect(host="localhost",user="root",password="root",charset="utf8")
m=db.cursor()

#INTRODUCTION:

print("*"*167)
print("\n\n")
print("\t"*6,"WELCOME TO MY COMPUTER SCIENCE PROJECT-PASSWORD MANAGER IN PYTHON")
print("\n\n")
print("*"*167)
print()
print("\t"*15," DONE BY- NAVIN KUMAR L OF XII E ROLL NO. 27")
print("\n\n")
input("Press Enter to continue")
CHECK_MP()

#MENU DRIVEN PROGRAM:

while True:
    
    #CORRECT MASTER PASSWORD:
    
    if c==0:
        print()
        print("\n1.Sign Up\n2.Login\n3.Exit\n")
        ch=int(input("Enter the choice:"))
        print()
        
        #CREATING A DATABASE AND REQUIRED TABLES:
        
        m.execute("create database if not exists Password_Manager")
        m.execute("use Password_Manager")
        m.execute("create table if not exists Master(User char(20) primary key,Password varchar(255) not null,Security_Question char(250) not null,Answer varchar(255) not null,Time bigint)") 
        m.execute("create table if not exists Passwords(User char(20) not null,Website_Name char(50) not null,User_Name char(50) not null,Password varchar(255) not null)")
        db.commit()
        
        #SIGN UP:
        
        if ch==1:
            sn=input("Enter User Name:")
            sp=input("Enter Password:")
            esp=ENCRYPT(sp)
            q=input("Enter your Security Question:")
            a=input("Enter your Answer for your Security Question:")
            ea=ENCRYPT(a)
            m.execute("insert ignore into Master values(%s,%s,%s,%s,%s)",(sn,esp,q,ea,0))
            db.commit()
            
            print("Successfully Added a New User")
            print()
            
            ch1=input("Do you want to continue by logging in(y/n):").upper()
            print()
            
            if ch1=="Y":
                ch=2
            else:
                continue
        
        #LOGIN:
        
        if ch==2:
            ln=input("Enter User Name:")
            m.execute("select User from Master")
            r=m.fetchall()
            
            for i in r:
                
                if (ln,)==i:
                    break
                
            else:
                print("User Name does not exist")
                print()
                continue
            m.execute('select Time from Master where User="'+ln+'"')
            [(r,)]=m.fetchall()
            
            #CHECKING LOCK TIME:
            
            if CURRENT_TIME()>int(r):
                m.execute('update Master set Time=0 where User="'+ln+'"')
                db.commit()
                m.execute('select Password from Master where User="'+ln+'"')
                [(s,)]=m.fetchall()
                k=s.encode()
                b=3
                
                while b>0:
                    
                    print("You have",b,"Attempts Left")
                    lp=input("Enter Password:")
                    
                    if lp!=DECRYPT(k):
                        b-=1
                    else:
                        break
                    
            else:
                m.execute('select Time from Master where User="'+ln+'"')
                [(f,)]=m.fetchall()
                print("You have been locked out due to multiple failed attempts. Try again after",(f-CURRENT_TIME())//60000,"Minutes")
                print()
                continue
            
            #UPDATING LOCK TIME:
            
            if b==0:
                m.execute('update Master set Time="'+str(LOCK_TIME())+'"where User="'+ln+'"')
                db.commit()
                m.execute('select Time from Master where User="'+ln+'"')
                [(f,)]=m.fetchall()
                print("You have been locked out due to multiple failed attempts. Try again after",(f-CURRENT_TIME())//60000,"Minutes")
                print()
                d=0
                continue
            else:
                d=1
                
            #SERVICES FOR LOGGED IN USERS:
                
            if d==1:
                print("You have succesfully logged in")
                print()
                
                while True:
                    
                    print("\n1.Add a New Password\n2.Display Passwords\n3.Delete a Password\n4.Change Passwords\n5.Logout\n")
                    ch2=int(input("Enter the choice:"))
                    print()
                    
                    #1.ADD A NEW PASSWORD:
                    
                    if ch2==1:
                        wn=input("Enter Website Name:")
                        un=input("Enter User Name:")
                        print("\nPassword Validation :\n\n")
                        print("1.At least 1 letter between [a-z] and 1 letter between [A-Z].")

                        print("At least 1 number between [0-9].")
                        print("3.At least 1character from [_$#@].")
                        print("4.Minimum length 8 characters.")
                        print("5.Maximum length16 characters.\n")
                        p=input("Enter Password:")
                        k=CHECK(p)
                        m.execute("insert into Passwords values(%s,%s,%s,%s)",(ln,wn,un,ENCRYPT(k)))
                        db.commit()
                        
                        print("Successfully Added a New Password")
                        print()
                        
                        ch3=input("Do you want to continue?(y/n):").upper()
                        print()
                        
                        if ch3=="Y":
                            continue
                        else:
                            ch2=5
                            
                    #2.DISPLAY PASSWORDS:
                            
                    elif ch2==2:
                        m.execute('select Website_Name,User_Name,Password from Passwords where User="'+ln+'"')
                        q=m.fetchall()
                        print("List of Passwords for",ln)
                        print()
                        l=[]
                        
                        for i in q:
                            
                            c=0
                            l1=[]
                            
                            for j in i:
                                
                                if c==2:
                                    l1.append(DECRYPT(j.encode()))
                                else:
                                    l1.append(j)
                                    c+=1
                            l.append(l1)
                        t=tabulate(l,headers=["Website Name","User Name","Password"],tablefmt="orgtbl")
                        print(t)
                        
                        ch3=input("Do you want to continue?(y/n):").upper()
                        print()
                        
                        if ch3=="Y":
                            continue
                        else:
                            ch2=5
                            
                    #3.DELETE A PASSWORD:
                            
                    elif ch2==3:
                        w=input("Enter Website Name:")
                        u=input("Enter User Name:")
                        m.execute('delete from Passwords where User_Name="'+u+'"and Website_Name="'+w+'"')
                        db.commit()
                        
                        print("Successfully Deleted a Password")
                        print()
                        
                        ch3=input("Do you want to continue?(y/n):").upper()
                        print()
                        
                        if ch3=="Y":
                            continue
                        else:
                            ch2=5
                            
                    #4.CHANGE PASSWORDS:
                            
                    elif ch2==4:
                        print("a.Change Password of User_Name\nb.Change Password of Website\nc.Change Master Password\n")
                        ch5=input("Enter the choice:").upper()
                        print()
                        
                        #A.LOGIN ID:
                        
                        if ch5=="A":
                            tp=input("Enter New Password for Login:")
                            np=ENCRYPT(tp).decode()
                            m.execute('update Master set Password="'+np+'"where User="'+ln+'"')
                            db.commit()
                            
                            print("Successfully Changed Login Password")
                            print()
                            
                            ch3=input("Do you want to continue?(y/n):").upper()
                            print()
                            
                            if ch3=="Y":
                                continue
                            else:
                                ch2=5
                                
                        #B.WEBSITE:
                                
                        elif ch5=="B":
                            w=input("Enter Website Name:")
                            u=input("Enter User Name:")
                            m.execute('select Website_Name,User_Name from Passwords where User_Name="'+u+'"')
                            n=m.fetchall()
                            
                            if (w,u) in n:
                                tp=input("Enter New Password for Website:")
                                np=ENCRYPT(tp).decode()
                                m.execute('update Passwords set Password="'+np+'"where User="'+ln+'"and Website_Name="'+w+'"and User_Name="'+u+'"')
                                db.commit()
                                
                                print("Successfully Changed a Password")
                                print()
                                
                            else:
                                print("The Password you have entered does not exist")
                                print()
                                
                            ch3=input("Do you want to continue?(y/n):").upper()
                            print()
                            
                            if ch3=="Y":
                                continue
                            else:
                                ch2=5
                                
                        #C.MASTER PASSWORD:
                                
                        elif ch5=="C":
                            tp=input("Enter New Master Password:")
                            np=ENCRYPT(tp)
                            f1=f=open("masterpassword.dat","wb")
                            f2=f=open("temp.dat","wb")
                            pickle.dump(np,f2)
                            f1.close()
                            f2.close()
                            os.remove("masterpassword.dat")
                            os.rename("temp.dat","masterpassword.dat")
                            
                            print("Successfully Changed Master Password")
                            print()
                            
                            ch3=input("Do you want to continue?(y/n):").upper()
                            print()
                            
                            if ch3=="Y":
                                continue
                            else:
                                ch2=5
                                
                        #INVALID CHOICE:
                                
                        else:
                            print("Invalid Option")
                            print()
                            continue
                        
                    #INVALID CHOICE:
                        
                    '''else:
                        print("Invalid Choice")
                        print()
                        continue'''
                    
                    #5.LOGOUT:

                    if ch2==5:
                        print("You have succesfully logged out")
                        print()
                        break
                    
                    #INVALID CHOICE:
                    
                    if ch2 not in [1,2,3,4,5]:
                        print("Invalid Choice")
                        print()
                        continue
                    
                    
            else:
                m.execute('select Time from Master where User="'+ln+'"')
                [(f,)]=m.fetchall()
                print("You have been locked out due to multiple failed attempts. Try again after",(f-CURRENT_TIME())//60000,"Minutes")
                print()
                continue
            
            
        #EXITING THE PROGRAM:
            
        if ch==3:
            print("Exiting the Program")
            print()
            db.close()
            m.close()
            break
        
        if ch not in [1,2,3]:
            print("Invalid Choice")
            print()
            continue
        
    #WRONG MASTER PASSWORD:
        
    elif c==-1:
        print("You have entered the wrong Master Password. Closing the Program")
        print()
        db.close()
        m.close()
        break

    
