from pick import pick
from questionary import questionary

def menu():
    menu = questionary.select(
        "===== LIBRARY  SYSTEM =====\n",
        choices=["Login", "New User", "Shutdown"]
    ).ask()
    if menu == "Login":
        login()
    if menu == "New User":
        newuser()
    if menu == "Shutdown":
        quit

def login():
    print("=== LIBRARY SYSTEM LOGIN ===\n")
    username = questionary.text("Enter Username:").ask()
    password = questionary.password("Enter Password:").ask()
    confirm = questionary.select(
        "Do you want to submit?",
        choices=["Confirm & Login", "Cancel"]
    ).ask()
    if confirm == "Cancel":
        menu()
    with open("logins.txt", "a+") as logins:
        lines = [line.strip() for line in logins.readlines()]
        for i in range(0, len(lines), 2):
            if lines[i] == username:
                userpass = lines[i+1]
                validuser = True
                if userpass == password:
                    validpass = True
                else:
                    validpass = False
            else:
                validuser = False
    if validuser == True and validpass == True:
        loggedinmenu()
    elif validuser == True and validpass == False:
        print("Login failed, Password Invalid")
        login()
    elif validuser == False and validpass == True:
        print("Login failed, Username Invalid")
        login()
    else:
        print("Login failed")
        login()

def newuser():
    print("newuser")

def loggedinmenu():
    print("===== LIBRARY  SYSTEM LOGGEDIN =====\n")

menu()