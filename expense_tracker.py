import sqlite3 as sq 
from sqlite3 import Error
import matplotlib.pyplot as plt 
import PySimpleGUI as sg 
from datetime import date as dt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

""" This is an expense tracker app, the app can provide insight into your monthly spending based on your set budget
    let you see where your money is going. it also has a dashboard. This app was developed using PySimpleGUI
"""

#sg.preview_all_look_and_feel_themes()
sg.theme('BlueMono')  #This wil be the app color
date = dt.today().strftime("%Y-%m-%d") #get date 


#create database connection where user and expense data will reside

def database_connection(db_file):

    conn = None

    try:
        conn = sq.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table):       #this function will be used to create the table

        c = conn.cursor()
        c.execute(create_table)

def table():

    database = "expense_tracker.db"
    conn = database_connection(database)

    with conn:

        create_user_table = ''' CREATE TABLE IF NOT EXISTS Users (
                                id integer PRIMARY KEY,
                                email text NOT NULL,
                                username text NOT NULL,
                                password text NOT NULL,
                                budget integer NOT NULL
                                );'''

        create_expense_table = '''CREATE TABLE IF NOT EXISTS Expenses (
                                id integer PRIMARY KEY,
                                userid integer NOT NULL,
                                category text NOT NULL,
                                income_expense text NOT NULL,
                                amount integer NOT NULL,
                                date text NOT NULL,
                                FOREIGN KEY (userid) REFERENCES Users (id)
                                );'''

        create_log_table = '''CREATE TABLE IF NOT EXISTS UserLog (
                                id integer PRIMARY KEY,
                                userid integer NOT NULL,
                                date text NOT NULL,
                                FOREIGN KEY (userid) REFERENCES Users (id)
                                );'''

        create_table(conn, create_user_table)
        create_table(conn, create_expense_table)
        create_table(conn, create_log_table)

if __name__ == "__main__":          # User, expense and log table will be created here 
    table() 

def new_user(conn, create_user):            #create new user here

    try:
        c = conn.cursor()
        sql = '''INSERT INTO Users(email, username, password, budget)  
                 VALUES(?,?,?,?);'''
        c.execute(sql,create_user)

    except Error as e:
        print(e)

def insert_user():

    database = "expense_tracker.db"

    conn = database_connection(database)

    with conn:
        create_user =(email, username, password, budget)
        new_user(conn, create_user)


def new_expense(conn, create_expense):  #expense record for each user

    try:
        c = conn.cursor()
        sql = ''' INSERT INTO Expenses(userid, category, income_expense,amount, date)
                  VALUES(?,?,?,?,?)'''
        c.execute(sql,create_expense)

    except Error as e:
        print(e)

def insert_expense():

    database = "expense_tracker.db"

    conn = database_connection(database)

    with conn:
        create_expense = (userid, category,income_expense, amount, date)
        new_expense(conn, create_expense)

def new_log(conn, create_new_log):  #log table to track logged in user

    try:
        c = conn.cursor()
        sql = ''' INSERT INTO UserLog(userid,date)
                  VALUES(?,?)
             '''
        c.execute(sql,create_new_log)

    except Error as e:
        print(e)

def insert_log():

    database = "expense_tracker.db"

    conn = database_connection(database)
    

    with conn:
        create_new_log = (userid, date)
        new_log(conn, create_new_log)


#image used as logo stored in base64
logo = b'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'
#main page layout broken into bits to help with alignment
logo_layout = [
                 [sg.Image(data=logo, key = '-logo-')]  
              ]

old_user_layout =[
                    [sg.Text('New User?',font=('Verdana', 14, 'italic'))],
                    [sg.Button('Sign Up')],
                    [sg.Text('Registered?', font=('Verdana', 14, 'italic'))],
                    [sg.Button('Sign In')]
                 ]
#combination of new_user_layout, old_user_layout and the main page
layout = [
            [sg.Text('Track Your Expenses', font=('Verdana', 16,'italic'))],
            [sg.Column(logo_layout,key ='-id-', pad= ((10,1),(20,1))), sg.Column(old_user_layout, key ='-old-', pad =((40,1),(60,1))) ],
            [sg.Button('Exit')]
         ]

window = sg.Window('Expense Tracker', layout)

signup_active = False

signin_active = False

login_active = False

while True:
    event, value = window.Read()
    if event in (None,'Exit'):
        break
    elif event == 'Sign Up' and not signup_active:    #call up sign up window 
        signup_active = True
        window.Hide()
        signup_text_layout =[
                                [sg.Text('Email:' ,font=('Verdana',10))],
                                [sg.Text('Username:', font=('Verdana',10))],
                                [sg.Text('Password:', font=('Verdana',10))],
                                [sg.Text('Budget:', font=('Verdana',10))]
                            ]

        signup_input_layout = [
                                [sg.InputText(key='-email-')],
                                [sg.InputText(key='-username-')],
                                [sg.InputText(key='-password-', password_char="*")],
                                [sg.InputText(key='-budget-')]
                              ]

        signup_layout =[
                         [sg.Text('Create an account')],
                         [sg.Column(signup_text_layout, key='-textcol-'), sg.Column(signup_input_layout, key='-inputcol-')],
                         [sg.Button('Save'), sg.Button('Exit')]
                       ]

        signup_window = sg.Window('Sign Up', signup_layout)

        while True:
            event, values = signup_window.Read()
            if event in (None,'Exit'):
                signup_window.Close()
                signup_active = False
                window.UnHide()
                break
            elif event == 'Save':
                email = values['-email-'].strip()
                username = values['-username-'].strip()
                password = values['-password-'].strip()
                budget = values['-budget-'].strip()

                #check if email already exists
                database = "expense_tracker.db"
                conn = database_connection(database)
                validate = conn.cursor()
                validate.execute('SELECT email from Users where email = ?',(email,))
                check_email = validate.fetchall()
                if len(check_email) >= 1:
                    sg.popup("Email already exist please login in")
                else:
                    insert_user()

                sg.popup('Registration complete, please exit')

    elif event == 'Sign In' and not signin_active: #call sign in window
        signin_active = True
        window.Hide()

        signin_text_layout =[
                             [sg.Text('Email', font=('Verdana', 10))],
                             [sg.Text('Password', font=('Verdana', 10))]
                            ]

        signin_input_layout=[
                             [sg.InputText(key='-log_email-')],
                             [sg.InputText(key = '-log_password-', password_char="*")]
                            ]

        signin_layout=[
                        [sg.Text('Sign In'),sg.InputText(default_text = date, key = '-date-', visible= False)],
                        [sg.Column(signin_text_layout,key ='-text_signin-'), sg.Column(signin_input_layout, key='-input_signin-')],
                        [sg.Button('Log In'), sg.Button('Exit')]
                      ]
        signin_window = sg.Window('Sign In', signin_layout)

        while True:

            event, values = signin_window.Read()
            if event in (None, 'Exit'):
                signin_window.Close()
                signin_active=False
                window.UnHide()
            elif event == 'Log In' and not login_active:
                email = values['-log_email-'].strip()
                password = values['-log_password-'].strip()
                date = values['-date-']
                

                #check if user exists
                database = "expense_tracker.db"
                conn = database_connection(database)
                validate_user = conn.cursor()
                validate_user.execute('SELECT id, username FROM Users where email =? and password =?',(email,password))

                username_id = validate_user.fetchall()
                

                if len(username_id) < 1:
                    sg.popup('User does not exist, create an account')
                else:
                    user = username_id[0]
                    userid = user[0]
                    username = user[1]
                    welcome_message = "Welcome to your expense tracker %s" % username
                    insert_log()
                    sg.popup('User Logged In')

                #Close the sign in page and open the active user page
                login_active = True
                signin_window.Hide()

                user_text_layout =[
                                    [sg.Text('Income/Expense:')],
                                    [sg.Text('Category:')],
                                    [sg.Text('Amount:')]
                                  ]

                user_input_layout = [
                                     [sg.Combo(['Income','Expense'], key='-type-')],
                                     [sg.Combo(['Food','Phone Bill','Utilities', 'Entertainment','Bank Transfers','Miscellaneous','Salary'], key='-category-')],
                                     [sg.InputText(key='-amount-')]
                                    ]

                user_layout =[
                              [sg.Text(welcome_message, font=('Verdana', 10))],
                              [sg.InputText(default_text=userid, key='id', visible = False),sg.InputText(default_text = date, key = '-date-', visible= False)],
                              [sg.Column(user_text_layout), sg.Column(user_input_layout)],
                              [sg.Button('Save'), sg.Button('Get Insight'), sg.Button('Exit')]
                             ]


                user_window = sg.Window('Expense Tracker',user_layout)

                while True:
                    event, values = user_window.Read()
                    if event in (None, 'Exit'):
                        user_window.Close()
                        login_active = False
                        window.UnHide()
                    elif event == 'Save':
                        userid = values['id']
                        income_expense = values['-type-']
                        category = values['-category-']
                        amount = values['-amount-'].strip()
                        date = values['-date-']
                        insert_expense()
                        user_window['id'].Update('')
                        user_window['-type-'].Update('')
                        user_window['-category-'].Update('')
                        user_window['-amount-'].Update('')
                        user_window['-date-'].Update('')



window.close()

