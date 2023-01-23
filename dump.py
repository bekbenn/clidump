#!/usr/bin/env python3
import sys,uuid,string
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("/Users/benitojoefino/ia/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
dbc = db.collection('info')

mac_doc = db.collection('devices').document(hex(uuid.getnode())).get()
if not(mac_doc.exists):
    db.collection('devices').document(hex(uuid.getnode())).set({'logged_into':'none'})

def log_status():
    global logged_in,username
    logged_in = False
    if (db.collection('devices').document(hex(uuid.getnode())).get(field_paths={u'logged_into'}).to_dict()).get('logged_into') != 'none':
        username = (db.collection('devices').document(hex(uuid.getnode())).get(field_paths={u'logged_into'}).to_dict()).get('logged_into')
        logged_in = True

def log_in():
    global logged_in,username
    log_status()
    if logged_in == False:
        exist = False
        correct_pass = False
        valid_chars = string.ascii_letters + string.digits
        print("do you have an account?\n1. yes\n2. no")
        have_acc = input("choice: ")
        while have_acc != "1" and have_acc != "2" and have_acc != "quit": #validation
            print("choices are only 1 or 2.")
            have_acc = input("choice: ")
        if have_acc == "1":
            while exist == False:
                valid_name = False
                repeat = 0
                while valid_name == False:
                    if repeat >= 1:
                        print("username must not contain any special characters!")
                    username = input("username: ")
                    valid_name = all(char in valid_chars for char in username)
                    repeat += 1
                if username != "quit":
                    docs = dbc.where('username','==',username).get()
                    for doc in docs:
                        exist = True
                    if exist == False:
                        print("account not found.")
                else:
                    exist = True
            if username == "quit":
                print("quitting!")
            else:
                while correct_pass == False:
                    password = input("password: ")
                    if password == (doc.to_dict()).get('password'):
                        print("logged in.")
                        db.collection('devices').document(hex(uuid.getnode())).update({'logged_into':username})
                        correct_pass = True
                        logged_in = True
                    elif password == "quit":
                        print("quit it is...")
                        correct_pass = True
                    else:
                        print("incorrect password.")
        elif have_acc == "2":
            print("")
            create_account()
        else:
            print("quit it is...")
    else:
        print("ure already logged into "+username+".")
    print("")

def create_account():
    valid_chars = string.ascii_letters + string.digits
    print("would you like to make a new account?\n1. yes\n2. already registered")
    new_acc = input("choice: ")
    while new_acc != "1" and new_acc != "2" and new_acc != "quit":
        print("choices are only 1 or 2.")
        new_acc = input("choice: ")
    if new_acc == "1":
        exist = True
        while exist == True: 
            valid_name = False
            exist = False
            repeat = 0
            while valid_name == False:
                if repeat >= 1:
                    print("username must not contain any special characters!")
                username = input("username: ")
                valid_name = all(char in valid_chars for char in username)
                repeat += 1
            docs = dbc.where('username','==',username).get()
            for doc in docs:
                exist = True
                print("account already exists.")
        if username != "quit":
            password = input("password: ")
            if password =="quit":
                print("quitting...")
            else:
                dbc.document(username).set({'username':username,'password':password,'dumps':[],'tags':[]})
                print("account made! time to login.")
                print("")
                log_in()
        else:
            print("quitting...")
    elif new_acc == "2":
        print("")
        log_in()
    else:
        print("quit it is...")
    print("")

def output_content():
    global dump_choices
    counter = 1
    dump_choices = []
    get_dumps = ((dbc.document(username).get(field_paths={u'dumps'})).to_dict())
    for dumps in (get_dumps.get('dumps')):
        print(str(counter)+". "+dumps)
        dump_choices.append(str(counter))
        counter += 1

def bd(dump): #braindump = add dumps to firebase
    global logged_in,username,get_dumps,get_tags
    log_status()
    if logged_in == True:
        get_dumps = ((dbc.document(username).get(field_paths={u'dumps'})).to_dict())
        get_tags = ((dbc.document(username).get(field_paths={u'tags'})).to_dict())
        dump_list = get_dumps.get('dumps')
        tag_list = get_tags.get('tags')
        already_outputted = []
        available_choices = ["0"]
        if dump == "":
            print("where's the dump man?")
        elif dump in dump_list:
            print("it's in ur notes already old man!")
        else:
            print("what's its tag?")
            print("0. add new tag")
            counter = 1
            for tag in tag_list:
                if not(tag in already_outputted):
                    print(str(counter) + ". " + tag)
                    already_outputted.append(tag)
                    available_choices.append(str(counter))
                    counter += 1
            tag_name = input("choice: ")
            while not(tag_name in available_choices) and tag_name != "quit": #validation
                print("invalid input. try again.")
                tag_name = input("choice: ")
            if tag_name == "quit":
                print("ish so indecisive-")
            elif int(tag_name) != 0:
                tag_list.append(already_outputted[int(tag_name)-1])
                dbc.document(username).update({'dumps':firestore.ArrayUnion([dump])})
                dbc.document(username).update({'tags':tag_list})
                print("note added!")
            else:
                new_tag = input("new tag: ")
                while (new_tag != "quit" and (new_tag in tag_list)) or new_tag == "":
                    print("tag already exists")
                    new_tag = input("new tag: ")
                if new_tag == "quit":
                    print("quitiiing...")
                else:
                    yes_or_no = input("are you sure\n1. yes\n2. no\nchoice: ")
                    while (yes_or_no != "1" and yes_or_no != "2" and yes_or_no != "quit") and yes_or_no == "2":
                        if yes_or_no != "1" and yes_or_no != "2" and yes_or_no != "quit":
                            print("choices are only 1 or 2.")
                        else:
                            print("changing?")
                        new_tag = input("new tag: ")
                        yes_or_no = input("are you sure\n1. yes\n2. no\nchoice: ")
                    if yes_or_no == "quit":
                        print("bruh ait...")
                    elif yes_or_no == "2":
                        print("then...?")
                    else:
                        dbc.document(username).update({'dumps':firestore.ArrayUnion([dump])})
                        dbc.document(username).update({'tags':firestore.ArrayUnion([new_tag])})
                        print("note added!")
    else:
        print('ure not logged in. do so using the "log_in" command')
    print("")

def vd(): #viewdump = view the dump file
    global logged_in,username,get_dumps,get_tags
    log_status()
    if logged_in == True:
        output_content()
    else:
        print('ure not logged in. do so using the "log_in" command')
    print("")
        
def sbt(tag): #searchbytag = search for dumps based on inputted tag
    global logged_in,username,get_dumps,get_tags
    log_status()
    if logged_in == True:
        get_dumps = ((dbc.document(username).get(field_paths={u'dumps'})).to_dict())
        get_tags = ((dbc.document(username).get(field_paths={u'tags'})).to_dict())
        dump_list = get_dumps.get('dumps')
        tag_list = get_tags.get('tags')
        if tag in tag_list:
            print("dumps with #" + tag)
            counter = 0
            for tags in tag_list:
                if tag != "" and tags == tag:
                    print(str(counter+1)+". "+dump_list[counter])
                counter += 1
        else:
            print("tag doesn't exist.")
    else:
        print('ure not logged in. do so using the "log_in" command')
    print("")

def rd(): #removedump = remove dump from firebase
    global logged_in,username, dump_choices
    log_status()
    if logged_in == True:
        output_content()
        get_dumps = ((dbc.document(username).get(field_paths={u'dumps'})).to_dict())
        get_tags = ((dbc.document(username).get(field_paths={u'tags'})).to_dict())
        dump_list = get_dumps.get('dumps')
        tag_list = get_tags.get('tags')
        remove_line = int(input("which dump do you wish to remove: "))
        while remove_line != "quit" and not(str(remove_line) in dump_choices): #validation
            print("not even there?!")
            remove_line = int(input("which dump do you wish to remove: "))
        if remove_line == "quit":
            print("ish so indecisive-")
        else:
            del tag_list[remove_line-1]
            dbc.document(username).update({'dumps':firestore.ArrayRemove([dump_list[remove_line-1]])})
            dbc.document(username).update({'tags':tag_list})
            print("dump removed.")
    else:
        print('ure not logged in. do so using the "log_in" command')
    print("")

def ed(): #editdump = overwrite a dump on firebase
    global dump_choices,username
    log_status()
    if logged_in == True:
        output_content()
        get_dumps = ((dbc.document(username).get(field_paths={u'dumps'})).to_dict())
        get_tags = ((dbc.document(username).get(field_paths={u'tags'})).to_dict())
        dump_list = get_dumps.get('dumps')
        tag_list = get_tags.get('tags')
        index = input("which dump would you like to edit: ")
        while not(index in dump_choices) and index != "quit":
            index = input("which dump would you like to edit: ")
        if index in dump_choices:
            new_dump = input("new dump: ")
            if new_dump == "quit":
                print("quitting...")
            elif new_dump in dump_list:
                print("dump already exists!")
            else:
                new_tag = input("tag name: ")
                if new_tag == "quit":
                    print("quit it is!")
                else:
                    dump_list[int(index)-1] = new_dump
                    tag_list[int(index)-1] = new_tag
                    dbc.document(username).update({'dumps':dump_list,'tags':tag_list})
        else:
            print("okay quit it is...")
    else:
        print('ure not logged in. do so using the "log_in" command')
    print("")

def log_out():
    global logged_in
    log_status()
    if logged_in == True:
        print("are you sure?\n1. yes\n2. no")
        choice = input("choice: ")
        while (choice != "1" and choice != "2"):
            print("choices are only 1 or 2.")
            choice = input("choice: ")
        if choice == "1":
            print("logging out...")
            db.collection('devices').document(hex(uuid.getnode())).update({'logged_into':'none'})
            print("logged out.")
        elif choice == "2":
            print("bruh")
    else:
        print("ure not even logged in-")
    print("")