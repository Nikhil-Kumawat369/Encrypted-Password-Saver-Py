import bcrypt
import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet

# This Function Takes password & hash it and save userName , password & key in userCredentials.txt
def saveCredentials (userName , hashedPassword , salt) :

    f = open("Encrypted-Password-Saver-Py/Database/userNameDatabase.txt" , "a")
    f.write(userName)
    f.write("\n")
    f.close()

    f = open("Encrypted-Password-Saver-Py/Database/userCredentials.txt" , "ab") 
    f.write(hashedPassword)
    f.write(b" ")
    f.write(base64.b64encode(salt)) # salt contains 0x0A next line character so we encode it in UTF-8 & store it
    f.write(b"\n")
    f.close()



# This function generates the cryptographic key's salt & returns it in the bytes form
def generateKeysSalt () :

    salt = os.urandom(16)

    return salt



# This function generates the cryptographic key on the basis of the salt & returns the key in the encoded form
def generateKey (password , salt) :

    kdf = Scrypt(
        salt = salt ,
        length = 32 ,
        n = 2**14 ,
        r = 8 ,
        p = 1
    )

    key = kdf.derive(password.encode())
    key = base64.b64encode(key)

    return key



#This function checks if the user already exist or not
# If exist -> True
# If not exist -> False
def userNameValidityCheck (userName) :

    f = open("Encrypted-Password-Saver-Py/Database/userNameDatabase.txt" , "r")
    data = f.read()
    data = data.split()
    f.close

    for name in data :

        if userName == name :

            return True
        

    return False



# This function checks the if the password if valid(correct) or not
# If valid -> True
# If not valid -> False
def passwordValidityCheck (password , StoredPassword) :

    passwordValidity = bcrypt.checkpw(password.encode() , StoredPassword)

    return passwordValidity



# This retrieves the hashed password & cryptographic key's salt from DB
def retrieveCredentials (userName) :

    f = open("Encrypted-Password-Saver-Py/Database/userNameDatabase.txt" , "r")
    data = f.read()
    data = data.split()
    f.close

    idx = 0

    for name in data :

        if userName == name :

            break

        idx += 1

    # This logic is tough to understand but we are just mapping user name from file1
    #  to there credentials in file2
    # Direct eg :- if username at idx = 7 then there password on other file id at idx 14 & salt at idx 15
    idx *= 2

    f = open("Encrypted-Password-Saver-Py/Database/userCredentials.txt" , "rb") 
    data = f.read()
    data = data.split()
    f.close()

    hashedPassword = data[idx]
    salt = data[idx+1]
    # Recall we saved it in UTF-8 encoded form to fight the 0x0A newline problem 
    # so we need to decode it back to its original form , the raw bytes
    salt = base64.b64decode(salt) 

    return hashedPassword , salt



# This function actually signs Up & saves all the credentials & also create the personal file for the user 
# So his data is stored in that personal file of the user
def signUp () :

    userName = input("Enter a userName :- ") 
    print("Remember if u forgot the password u will set for ur profile")
    print("Then there is now way to recover , as it uses the highest level of security")
    print("Even we dont know your password , we never store the password u set")
    password = input("Enter a really strong password :- ")

    f = open("Encrypted-Password-Saver-Py/Database/userNameDatabase.txt" , "r") 
    data = f.read()

    data = data.split()

    userNameTaken = False

    # This block check if the user name is already taken or not & also re-asks for a new unique username
    while not userNameTaken :

        for i in data :

            if i == userName :

                userNameTaken = True

        if userNameTaken :

            print("UserName already taken")
            userName = input("Enter a different username :- ")
            userNameTaken = False

        else : 

            break

    #Generating Hash for password
    hashedPassword = bcrypt.hashpw(password.encode() , bcrypt.gensalt())

    #Generate Cryptographic key for encryption & decryption
    salt = generateKeysSalt()

    saveCredentials(userName , hashedPassword , salt)

    # # it creates a user named file & adds a basic data
    file = open("Encrypted-Password-Saver-Py/Database/" + userName + ".txt" , "wb") 
    data = "\n\n" + "Welcome " + userName + "\n\n"

    key = generateKey (password , salt)

    f = Fernet(key)

    data = f.encrypt(data.encode())

    file.write(data)

    file.close()

    print("SignUp done successfully")
    print("Now logIn with the same credentials Whenever u want to access , add etc ur data")
    quit()



# This function actually takes username and password amd verifies its authenticity 
# If verified it & generates cryptographic key & returns userName & key
def logIn () : 

    userName = input("Enter your userName :- ")

    # It checks if the username is valid or not
    if not userNameValidityCheck(userName) :

        print("User doesn't exists")
        print("Try to login a valid username")
        print("OR")
        print("SignUp")

        quit()

    password = input("Enter your password :- ")

    StoredPassword , storedSalt = retrieveCredentials(userName)

    if passwordValidityCheck(password , StoredPassword) :

        print("Login Successful")

    else : 

        print("Invalid Password")
        print("Try another password")

        quit()

    # Now as user have logged successfully so lets generate there cryptographic key 
    # Which will be used to encrypt & decrypt there data
    key = generateKey(password , storedSalt)

    return userName , key



# This function uses signUp & LogIn function & it sets a good intro for the user 
# it manages invalid option selection too
# it also returns the key id user is logIn and verified
def intro () :

    print("=" * 65)
    print("Welcome to the Secure Encrypted Data Storage System")
    print("This system allows you to securely store and retrieve")
    print("your sensitive data in encrypted form.")
    print("User authentication is required to protect your data integrity.")
    print("=" * 65)

    print("\nPlease choose an option:")
    print("Sign Up (Create a new secure account) [Enter 1]")
    print("Log In  (Access your encrypted data) [Enter 2]")
    choice = input("Enter Your Choice :- ")

    if not choice.isdigit() : 

        print("InValid Option Selected\nTry Again Later")
        quit()

    choice = int(choice)

    if choice == 1 :

        signUp()

        return None , None # The default return

    elif choice == 2 :

        userName , key = logIn() 

        return userName , key

    else : 

        print("InValid Option Selected\nTry Again Later")
        quit()

    

# This Function takes Input from user & stores it in encrypted format in there own private file in the DB
def addData (userName , key) :

    f = Fernet(key)

    print("\nYou may now begin adding your data below.")
    print("Type your content freely. When you are finished, type 'END' on a new line and press Enter to submit.\n")

    file = open("Encrypted-Password-Saver-Py/Database/" + userName + ".txt" , "rb")  # because encrypted data is in bytes form not str
    fullData = file.read()
    file.close()

    f = Fernet(key)
    fullData = f.decrypt(fullData)
    fullData = fullData.decode() # because we gave encoded data while encrypting it so the decrypted data is encoded , we need to decode it before display

    while True :

        data = input() 

        if data == "END" :

            fullData = f.encrypt(fullData.encode())

            file = open("Encrypted-Password-Saver-Py/Database/" + userName + ".txt" , "wb")  # because encrypted data is in bytes form not str
            file.write(fullData)
            file.close()

            print("\n✔ Data Saved Securely.")
            print("Your information is encrypted and cannot be decrypted without your authorized credentials.")

            break

        data += "\n"
        fullData += data



# This function fetches the data & decrypts it & displays on the screen
def displayData (userName , key) :

    file = open("Encrypted-Password-Saver-Py/Database/" + userName + ".txt" , "rb")  # because encrypted data is in bytes form not str
    data = file.read()
    f = Fernet(key)
    data = f.decrypt(data)
    data = data.decode() # because we gave encoded data while encrypting it so the decrypted data is encoded , we need to decode it before display
    print(data)

    file.close()



# Lets start the main code body here

# If user selects signUp the this further code wont be executes as there is quit() at end of signUp
userName ,  key = intro()

print("Please choose an option to continue:")
print("1️⃣  Add new data to your secure database [Enter 1]")
print("2️⃣  View the data already stored in your database [Enter 2]\n")

choice = input("Enter Your Choice :- ")

if not choice.isdigit() : 

    print("InValid Option Selected\nTry Again Later")
    quit()

choice = int(choice)

if choice == 1 :

    addData (userName , key)

elif choice == 2 :

    displayData(userName , key)

else : 

    print("InValid Option Selected\nTry Again Later")
    quit()
    




























# # The variables used 
# userName = None
# password = None

# userName = "Person5"
# password = "Nikhil"

# # it creates a user named file
# f = open("Encrypted-Password-Saver-Py/Database/" + userName + ".txt" , "x") 
# f.close()

# key = b"key"

# signUp (userName , password)

