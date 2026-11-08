def main():
    menu()

def loggedinmenu():
    menuui = input('''
    Enter 1 for log out
    Enter 2 for shutdown
    ''')
    if menuui == "1":
        menu()
    elif menuui == "2":
        return
    else:
        print("Invalid option")

def menu():
    menuui = input('''
    Enter 1 for login
    Enter 2 for New user
    Enter 3 for shutdown
    ''')

    if menuui == "1":
        login()
    elif menuui == "2":
        newlogin()
    elif menuui == "3":
        print("Shutting down")
        return
    else:
        print("Invalid option")
        menu()


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    with open("logins.txt") as file:
        for line in file:
            user, saved_password = line.strip().split(",", 1)

            if user == username and saved_password == password:
                print("Successfully logged in")
                loggedinmenu()

    print("Incorrect username or password")
    login()

def newlogin():
    newuser = input("Enter new username: ")

    with open("logins.txt") as file:
        if any(line.split(",", 1)[0].strip() == newuser for line in file):
            print("User already exists")
            newlogin()

    newpass = input("Enter new password: ")

    with open("logins.txt", "a") as file:
        file.write(f"{newuser},{newpass}\n")

    print("User created successfully")
    menu()


main()