"""
This is program is a "Contacts Book"  made using "tkinter"  module of "python".
It uses python (Front-end) and MYSQL (Back-end).

Advantages:
1. Uses local database and text files to store contacts and application settings. 
2. Sharing of contacts is possible through text files.
3. User can have "seperate password" for each accounts.
4. Contacts can be backed-up in MYSQL itself(automaticly).
5. AUTOMATED TASKS: Package installation, Package creation(oopen module), Database creation, Backup(according to user setting)
, Icons for title bar(in absents of image files).

Disadvantages:
1. do not use "csv" files.
2. Dumb GUI.
3. Account handling is difficult.
4. All contacts are stored in same database

"This program is created to learn "tkinter" module by implementing it".
"This program may contain "bugs".
"This program do not contain any 'spyware', 'adware' or any kind of viruses."
"This program use CMD for downloading MYSQL package from OFFICIAL sites only."
"""

from datetime import date
import os, runpy
from tkinter import *
from tkinter import ttk as vvk

try:
    import mysql.connector
except:
    os.system('cmd /c "pip install mysql.connector-python"')
    import mysql.connector

root_dir = os.getcwd()
req_mods = {"oopen" : "openeasy"}
req_mods_lnk = {"oopen" : "https://github.com/karthikvvk/make-life-easy-python-packages-oopen/blob/main/make-life-easy-python-packages-oopen/openeasy.py"}
for hi in req_mods:
    if os.path.exists(hi):
        pass
    else:
        os.mkdir(hi)
    open(f"{root_dir}\\{hi}\\{req_mods[hi]}.py", 'w').close()
    open(f"{root_dir}\\{hi}\\__init__.py", 'w').close()
    os.system(f"curl -o {root_dir}\\{hi}\\{req_mods[hi]}.py {req_mods_lnk[hi]}")
from oopen import openeasy as op

theme = '#323232'
ft_theme = '#e8e8e8'
today = date.today()
op.o_append('settings.txt')
rrk = op.o_read('settings.txt')
kkr = rrk.split(',')

ico_lis = ['contacts.ico', 'delete.ico', 'edit.ico', 'new contact.ico', 'reset.ico', 'search.ico', 'setup.ico',
           'uninstall.ico', 'warning.ico']
for i in ico_lis:
    op.checker(i)


def show_db(cursor):
    cursor.execute('show databases')
    rss = cursor.fetchall()
    lis = []
    for k in range(len(rss)):
        t = str(rss[k]).rstrip("'),")
        gm = t.lstrip("('")
        lis.append(gm)
    return lis


def search_database(cursor, database):
    cursor.execute('show databases')
    rk = cursor.fetchall()
    for k in range(len(rk)):
        t = str(rk[k]).rstrip("'),")
        gm = t.lstrip("('")
        if gm == database:
            return True


def show_tables(cursor):
    cursor.execute('show tables')
    rsr = cursor.fetchall()
    lis = []
    for k in range(len(rsr)):
        t = str(rsr[k]).rstrip("'),")
        gm = t.lstrip("('")
        lis.append(gm)
    return lis


def search_table(cursor, table):
    cursor.execute('show tables')
    rec = cursor.fetchall()

    for k in range(len(rec)):
        t = str(rec[k]).rstrip("'),")
        gm = t.lstrip("('")
        if gm == table:
            return True


def connection_setup():
    hulk = Tk()
    hulk.geometry('500x500')
    hulk.iconbitmap('setup.ico')
    hulk.title('Contacts app MYSQL connection')
    hulk.configure(bg=theme)

    user_name_tv = StringVar()
    host_name_tv = StringVar()
    password_tv = StringVar()

    def submit_connection():
        user_n = user_name_tv.get()
        passwd = password_tv.get()
        host_n = host_name_tv.get()
        try:
            mysql.connector.connect(user=user_n, host=host_n, passwd=passwd)
            if 'on' in kkr:
                op.o_write('settings.txt',
                           f'username= {user_n},password= {passwd},hostname= {host_n},on,#e8e8e8,yes,sun')
                hulk.destroy()
            else:
                op.o_write('settings.txt',
                           f'username= {user_n},password= {passwd},hostname= {host_n},off,#e8e8e8,yes,sun')

                hulk.destroy()
        except:
            t = Label(hulk, text='Please enter the details correctly', bg='white', fg='red')
            t.grid(row=3, column=3)
            t.after(3000, lambda: t.destroy())

    Label(hulk, text='Enter your MYSQL user name: ', bg=theme, fg=ft_theme).grid(row=0, column=0)
    Label(hulk, text='Enter your MYSQL password:', bg=theme, fg=ft_theme).grid(row=1, column=0)
    Label(hulk, text='Enter your MYSQL host name:', bg=theme, fg=ft_theme).grid(row=2, column=0)
    st1 = Entry(hulk, textvariable=user_name_tv)
    st1.focus_set()
    st1.grid(row=0, column=1)
    Entry(hulk, textvariable=password_tv).grid(row=1, column=1)
    Entry(hulk, textvariable=host_name_tv).grid(row=2, column=1)
    vvk.Button(hulk, text='Connect', command=submit_connection).grid(row=3, column=0)
    hulk.mainloop()


if 'sun' not in kkr:
    connection_setup()

std = op.o_read('settings.txt')
user_n = ''
passwd = ''
host_n = ''
sp_lis = std.split(',')

for i in sp_lis:
    if 'username=' in i:
        acc = i.lstrip('username=')
        r = acc.strip()
        user_n += r
    if 'hostname=' in i:
        acc = i.lstrip('hostname=')
        r = acc.strip()
        host_n += r
    if 'password=' in i:
        acc = i.lstrip('password=')
        r = acc.strip()
        passwd += r

if not len(passwd) > 0:
    os.abort()

try:
    mydatabase = mysql.connector.connect(user=user_n, host=host_n, passwd=passwd)
    mycor = mydatabase.cursor()
except:
    connection_setup()
    mydatabase = mysql.connector.connect(user=user_n, host=host_n, passwd=passwd)
    mycor = mydatabase.cursor()

mycor.reset()
if search_database(mycor, 'contact_app'):
    pass
else:
    mycor.execute('create database if not exists contact_app')
mydatabase.commit()
my_database = mysql.connector.connect(user=user_n, host=host_n, passwd=passwd, database="contact_app")
my_cor = my_database.cursor()


def log_pg():
    global my_database, my_cor
    if 'yes' in std:
        thunder = Tk()
        thunder.geometry('300x200')
        thunder.configure(bg=theme)
        thunder.title('Contacts set up')
        thunder.iconbitmap(r'setup.ico')

        def create_acc():
            global my_database, my_cor
            new = Tk()
            new.geometry('600x450')
            new.title('Create account')
            new.iconbitmap(r'new contact.ico')
            new.configure(bg=theme)

            def create():
                acc_nm = acc_name.get()
                pas = password.get()
                b = f'CREATE TABLE if not exists {acc_nm}_conapp (first_name varchar(50) default "-", sur_name varchar(50) default "-", ' \
                    'phone varchar(20)  primary key, ph_label varchar(50) default "-", address varchar(50) default "-", ' \
                    'email_address varchar(50) default "-", em_label varchar(50) default "-", significant_date ' \
                    'varchar(50) default "-", relationship varchar(50) default "-", date_add varchar(30))'
                c = f'CREATE TABLE if not exists password (account varchar(50), passwd varchar(70))'
                f = 'insert into password values("{}", "{}")'.format(f'{acc_nm}_conapp', pas)

                global my_cor, my_database
                my_cor.execute(b)
                my_cor.execute(c)
                my_cor.execute(f)
                my_database.commit()
                op.o_append('databases.txt', f'{acc_nm}_conapp,')
                op.o_write('data settings.txt', f'{acc_nm}_conapp')
                try:
                    thunder.destroy()
                except:
                    pass
                new.destroy()
                op.o_write('settings.txt',
                           f'username= {user_n},password= {passwd},hostname= {host_n},off,#e8e8e8,no,sun')

            acc_name = StringVar(new, value='')
            password = StringVar(new, value='')
            Label(new, text='Account name: ', fg=ft_theme, bg=theme).grid(row=0, column=0)
            Label(new, text='Password: ', fg=ft_theme, bg=theme).grid(row=1, column=0)
            en = Entry(new, textvariable=acc_name)
            en.focus_set()
            en.grid(row=0, column=1)
            Entry(new, textvariable=password).grid(row=1, column=1)
            vvk.Button(new, text='Create', command=create).grid(row=2, column=0)
            Label(new, text='FOR ACCOUNT:\n*The only allowed special symbol for \naccount name is "_" (under score)\n'
                            '\nFOR PASSWORD: \n*The only allowed special symbols for\npassword is   ~!@#$%^&*()_+=-`][;.,*}{|:?><'
                            '\nThe below symbols must not be included\n(front slash, back slash, single quots)\n'
                            'Length of password must not exceed 70 characters',
                  fg=ft_theme, bg=theme, justify='left').grid(row=4, column=2)
            new.mainloop()

        def login():
            login = Tk()
            login.geometry('350x250')
            login.title('Login')
            login.configure(bg=theme)
            login.iconbitmap(r'contacts.ico')
            acc_name = StringVar(login, value='')
            password = StringVar(login, value='')

            def login_submit():
                global my_cor, my_database
                acc_nm = acc_name.get() + '_conapp'
                pas = password.get()
                my_cor.execute('select * from password')
                g = my_cor.fetchall()
                lgacc = []
                for i in g:
                    if i[0] == acc_nm:
                        lgacc.append(i)
                    else:
                        continue
                if len(lgacc) > 0:
                    for i in range(len(g)):
                        if lgacc[i][0] == acc_nm and lgacc[i][1] == pas:
                            if search_table(my_cor, f'{acc_nm}_backup_conapp'):
                                bak = 'on'
                            else:
                                bak = 'off'
                            op.o_write('data settings.txt', f'{acc_nm}')
                            op.o_write('databases.txt', f'{acc_nm},')
                            thunder.destroy()
                            login.destroy()
                            op.o_write('settings.txt',
                                       f'username= {user_n},password= {passwd},hostname= {host_n},no,#e8e8e8,{bak},sun')
                            break
                        else:
                            y = Label(login, text='Wrong password', fg='red', bg='white')
                            y.grid(row=3, column=0)
                            y.after(3000, lambda: y.destroy())
                            break
                else:
                    y = Label(login, text='account not found', fg='red', bg='white')
                    y.grid(row=4, column=0)
                    y.after(3000, lambda: y.destroy())

            Label(login, text='Account name: ', fg=ft_theme, bg=theme).grid(row=0, column=0)
            Label(login, text='Password: ', fg=ft_theme, bg=theme).grid(row=1, column=0)
            acnam = Entry(login, textvariable=acc_name)
            acnam.focus_set()
            acnam.grid(row=0, column=1)
            Entry(login, textvariable=password).grid(row=1, column=1)
            vvk.Button(login, text='Login', command=login_submit).grid(row=2, column=0)
            login.mainloop()

        vvk.Button(thunder, text='Login', command=login).grid(row=0, column=0)
        vvk.Button(thunder, text='Sign up', command=create_acc).grid(row=0, column=1)

        thunder.mainloop()


log_pg()

try:
    my_database = mysql.connector.connect(user=user_n, host=host_n, passwd=passwd, database="contact_app")
except:
    mycor.execute('create database if not exists contact_app')
    my_database = mysql.connector.connect(user=user_n, host=host_n, passwd=passwd, database="contact_app")
my_cor = my_database.cursor()

acc = op.o_read('data settings.txt')
acc_lis = op.o_read('databases.txt').split(',')
acc_lis.pop()


acc_fh_re = op.o_read('settings.txt')
if 'on' in acc_fh_re:
    backup_status = 'on'
else:
    backup_status = 'off'

if len(acc) > 0:
    if search_table(my_cor, acc):
        pass
    else:
        op.o_write('settings.txt', f'username= {user_n},password= {passwd},hostname= {host_n},off,#e8e8e8,yes,sun')
        os.abort()

    if '#323232' in std:
        theme = '#323232'
        ft_theme = '#e8e8e8'
    else:
        theme = '#e8e8e8'
        ft_theme = 'black'
    qry1 = ''
    qry2 = ''
    qry3 = ''


    def do_it():
        global my_database, my_cor
        if backup_status == 'on':
            sync_b.configure(state=ACTIVE)
            del_backup_b.configure(state=ACTIVE)
            my_cor.execute(f'select * from {acc}')
            ft = my_cor.fetchall()
            for i in range(len(ft)):
                try:
                    v = ft[i]
                    first_name = v[0]
                    sur_name = v[1]
                    phone = v[2]
                    ph_label = v[3]
                    address = v[4]
                    email_address = v[5]
                    em_label = v[6]
                    significant_date = v[7]
                    relationship = v[8]
                    b = f'INSERT INTO {acc}_backup_conapp (first_name, sur_name, phone, ph_label, address, email_address, em_label, significant_date, relationship, date_add) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    a = (first_name, sur_name, phone, ph_label, address, email_address, em_label, significant_date,
                         relationship, today)
                    try:
                        my_cor.execute(b, a)
                        my_database.commit()
                    except:
                        pass

                except:
                    pass
            Label(groot, text='Your backup is on\n'
                              'To use this app with all your contacts inn\nclick sync ', justify='left', bg=theme,
                  fg=ft_theme).grid(
                row=4, column=5)
        groot.mainloop()


    def back_up():
        global backup_status, my_database, my_cor
        if backup_status == 'off':
            backup_status = 'on'
            try:
                my_cor.reset()
                sync_b.configure(state=ACTIVE)
                del_backup_b.configure(state=ACTIVE)
                b = f'CREATE table {acc}_backup_conapp (first_name varchar(50) default "-", sur_name varchar(50) default "-", phone varchar(20)  primary key, ph_label varchar(50) default "-", address varchar(50) default "-", email_address varchar(50) default "-", em_label varchar(50) default "-", significant_date varchar(50) default "-", relationship varchar(50) default "-", date_add varchar(30))'
                my_cor.execute(b)
                my_database.commit()

                do_it()
            except:
                pass
            op.o_replace(name='settings.txt', old='off', new='on')
            backup_b.configure(text=f'Back up is {backup_status} click to change')
            do_it()
        elif backup_status == 'on':
            backup_status = 'off'
            op.o_replace('settings.txt', 'on', 'off')
            Label(groot, text='Your backup is off', justify='left', bg=theme,
                  fg=ft_theme).grid(
                row=5, column=5)
            backup_b.configure(text=f'Back up is {backup_status} click to change')


    def new_contact():

        root = Tk()
        root.title(f'New contact ({acc})')
        root.configure(bg=theme)
        root.geometry('1366x768')
        root.iconbitmap(r'new contact.ico')

        first_name_tv = StringVar(root, value='')
        sur_name_tv = StringVar(root, value='')
        phone_tv = StringVar(root, value='')
        address_tv = StringVar(root, value='')
        email_tv = StringVar(root, value='')
        ph_type_tv = StringVar(root, value='')
        em_type_tv = StringVar(root, value='')
        re_type_tv = StringVar(root, value='')
        significant_date_tv = StringVar(root, value='')

        def submit():
            first_name = first_name_tv.get()
            sur_name = sur_name_tv.get()
            phone = phone_tv.get()
            ph_label = ph_type_tv.get()
            address = address_tv.get()
            email_address = email_tv.get()
            em_label = em_type_tv.get()
            significant_date = significant_date_tv.get()
            relationship = re_type_tv.get()

            a = f'INSERT INTO {acc} (first_name, sur_name, phone, ph_label, address, email_address, em_label, ' \
                'significant_date, relationship, date_add)' 'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            b = (first_name, sur_name, phone, ph_label, address, email_address, em_label, significant_date, relationship
                 , today)
            try:
                my_cor.execute(a, b)
                cr = Label(root, text='Contact created', justify='left', bg=theme, fg=ft_theme)
                cr.grid(row=6, column=4)
                cr.after(1500, lambda: cr.destroy())
                my_database.commit()
                exp_b.configure(state=ACTIVE)
            except:
                new = Label(root, text=f'Contact with this number\n{phone}already exist', justify='left', bg=theme,
                            fg=ft_theme)
                new.grid(row=7, column=4)
                new.after(1500, lambda: new.destroy())

            do_it()

        Label(root, text='First name: ', bg=theme, fg=ft_theme).grid(row=0, column=0)
        Entry(root, textvariable=first_name_tv).grid(row=0, column=1)

        Label(root, text='Sur name: ', bg=theme, fg=ft_theme).grid(row=1, column=0)
        Entry(root, textvariable=sur_name_tv).grid(row=1, column=1)

        Label(root, text='Phone no: ', bg=theme, fg=ft_theme).grid(row=2, column=0)
        Entry(root, textvariable=phone_tv).grid(row=2, column=1)

        Label(root, text='Address: ', bg=theme, fg=ft_theme).grid(row=3, column=0)
        Entry(root, textvariable=address_tv).grid(row=3, column=1)

        Label(root, text='Email: ', bg=theme, fg=ft_theme).grid(row=4, column=0)
        Entry(root, textvariable=email_tv).grid(row=4, column=1)

        Label(root, text='Significant date: ', bg=theme, fg=ft_theme).grid(row=5, column=0)
        Entry(root, textvariable=significant_date_tv).grid(row=5, column=1)

        Label(root, text='''Select phone no type as given: 
                --> Mobile
                --> office
                --> Home -->>
                --> Fax
                --> Pager ''', justify='left', bg=theme, fg=ft_theme).grid(row=2, column=2)
        Entry(root, textvariable=ph_type_tv).grid(row=2, column=3)

        Label(root, text='''Select email type as given: 
            --> Family
            --> Friend
            --> School -->>
            --> Office
            --> Neighbour
            --> none ''', justify='left', bg=theme, fg=ft_theme).grid(column=2, row=4)
        Entry(root, textvariable=em_type_tv).grid(row=4, column=3)

        Label(root, text='''Select the relation as given: 
            --> Family
            --> Friend
            --> School -->>
            --> Office
            --> Neighbour
            --> none ''', justify='left', bg=theme, fg=ft_theme).grid(column=2, row=3)
        Entry(root, textvariable=re_type_tv).grid(row=3, column=3)

        vvk.Button(root, text='Submit', command=submit).grid(row=5, column=3)


    def cr_checkbox(tk_window_object, sequence, bg='white', fg='black', row=0, column=0):
        len_seq = len(sequence)
        vari = []
        row_l = []

        for y in range(row, len_seq + row):
            row_l.append(y)

        for i in range(len_seq):
            vari.append('a' + str(i))
            vari[i] = IntVar(tk_window_object, value=0)

        for i in range(len_seq):
            Checkbutton(tk_window_object, text=sequence[i], variable=vari[i], bg=bg, justify='left', fg=fg).grid(
                row=row_l[i], column=column)
        return [len_seq, vari, sequence, vvk]


    def sel_edit_con():
        global my_cor, y, my_database
        scarlet = Tk()
        scarlet.geometry('900x600')
        scarlet.iconbitmap(r'edit.ico')
        scarlet.title(f'select a contact ({acc})')
        scarlet.configure(bg=theme)
        my_cor.execute(f"select * from {acc}")
        det = my_cor.fetchall()
        detail = []
        for dt in det:
            detail.append(dt[0])

        if not detail:
            Label(scarlet, text='Nothing to show').grid()
        else:
            chk = cr_checkbox(tk_window_object=scarlet, sequence=detail, bg=theme, fg=ft_theme)

            def edit_con():
                value = []
                scarlet.destroy()
                for ind in range(chk[0]):
                    val = chk[1][ind].get()
                    if val == 1:
                        value.append(chk[2][ind])
                ref = (value[0],)
                reff = det[detail.index(ref[0])][2]
                indx = detail.index(ref[0])
                root = Tk()
                root.title(f'edit contact ({acc})')
                root.configure(bg=theme)
                root.iconbitmap(r'edit.ico')
                root.geometry('1366x768')
                my_cor.reset()
                first_name_tv = StringVar(root, value='')
                sur_name_tv = StringVar(root, value='')
                phone_tv = StringVar(root, value='')
                address_tv = StringVar(root, value='')
                email_tv = StringVar(root, value='')
                ph_type_tv = StringVar(root, value='')
                em_type_tv = StringVar(root, value='')
                re_type_tv = StringVar(root, value='')
                significant_date_tv = StringVar(root, value='')

                def submit():
                    first_name = first_name_tv.get()
                    sur_name = sur_name_tv.get()
                    phone = phone_tv.get()
                    ph_label = ph_type_tv.get()
                    address = address_tv.get()
                    email_address = email_tv.get()
                    em_label = em_type_tv.get()
                    significant_date = significant_date_tv.get()
                    relationship = re_type_tv.get()
                    lis = [first_name, sur_name, phone, ph_label, address, email_address, em_label,
                           significant_date,
                           relationship]
                    lit = []
                    for i in range(9):
                        ele = lis[i]
                        if len(ele) > 0:
                            lit.append(ele)
                        else:
                            lit.append(det[indx][i])

                    a = f'update {acc} set first_name = "{lit[0]}", sur_name = "{lit[1]}", phone = "{lit[2]}", ph_label = "{lit[3]}", address = "{lit[4]}", email_address = "{lit[5]}", em_label =  "{lit[6]}", significant_date = "{lit[6]}", relationship = "{lit[7]}", date_add = "{today}" where phone = "{reff}"'
                    my_cor.execute(a)
                    my_database.commit()
                    root.destroy()
                    do_it()

                Label(root, text='First name: ', bg=theme, fg=ft_theme).grid(row=0, column=0)
                Entry(root, textvariable=first_name_tv).grid(row=0, column=1)

                Label(root, text='Sur name: ', bg=theme, fg=ft_theme).grid(row=1, column=0)
                Entry(root, textvariable=sur_name_tv).grid(row=1, column=1)

                Label(root, text='Phone no: ', bg=theme, fg=ft_theme).grid(row=2, column=0)
                Entry(root, textvariable=phone_tv).grid(row=2, column=1)

                Label(root, text='Address: ', bg=theme, fg=ft_theme).grid(row=3, column=0)
                Entry(root, textvariable=address_tv).grid(row=3, column=1)

                Label(root, text='Email: ', bg=theme, fg=ft_theme).grid(row=4, column=0)
                Entry(root, textvariable=email_tv).grid(row=4, column=1)

                Label(root, text='Significant date: ', bg=theme, fg=ft_theme).grid(row=5, column=0)
                Entry(root, textvariable=significant_date_tv).grid(row=5, column=1)

                Label(root, text='''Select phone no type as given: 
                            --> Mobile
                            --> office
                            --> Home -->>
                            --> Fax
                            --> Pager ''', justify='left', bg=theme, fg=ft_theme).grid(row=2, column=2)
                Entry(root, textvariable=ph_type_tv).grid(row=2, column=3)

                Label(root, text='''Select email type as given: 
                        --> Family
                        --> Friend
                        --> School -->>
                        --> Office
                        --> Neighbour
                        --> none ''', justify='left', bg=theme, fg=ft_theme).grid(column=2, row=4)
                Entry(root, textvariable=em_type_tv).grid(row=4, column=3)

                Label(root, text='''Select the relation as given: 
                        --> Family
                        --> Friend
                        --> School -->>
                        --> Office
                        --> Neighbour
                        --> none ''', justify='left', bg=theme, fg=ft_theme).grid(column=2, row=3)
                Entry(root, textvariable=re_type_tv).grid(row=3, column=3)
                Label(root,
                      text='NOTE: The field which needs to be changed\n'
                           'alone can be filled, others can be ignored').grid(row=6, column=4)
                vvk.Button(root, text='save changes', command=submit).grid(row=5, column=3)
                root.mainloop()

            vvk.Button(scarlet, text='edit selected', command=edit_con).grid(row=0, column=1)

            scarlet.mainloop()


    def delete_con():
        global my_cor, y, my_database
        root = Tk()
        root.geometry('900x600')
        root.title(f'Delete ({acc})')
        root.iconbitmap(r'delete.ico')
        root.configure(bg=theme)
        my_cor.execute(f"select * from {acc}")
        det = my_cor.fetchall()
        detail = []

        for dt in det:
            detail.append(dt[0])

        if len(detail) == 0:
            Label(root, text='nothing to show').grid(row=0, column=0)
            exp_b.configure(state=DISABLED)

        chk = cr_checkbox(tk_window_object=root, sequence=detail, bg=theme, fg=ft_theme)

        def del_selected():
            wanda = Tk()
            wanda.geometry('300x200')
            wanda.title(f'Conformation to delete ({acc})')
            wanda.iconbitmap(r'warning.ico')
            wanda.configure(bg=theme)

            def del_con():
                value = []
                root.destroy()
                for ind in range(chk[0]):
                    val = chk[1][ind].get()
                    if val == 1:
                        value.append(chk[2][ind])

                exp_b.configure(state=ACTIVE)
                for item in value:
                    bb = f"delete from {acc} where first_name = '{item}'"
                    my_cor.execute(bb)
                    my_database.commit()
                wanda.destroy()
                del_l = Label(root, text='Contacts deleted', bg=theme, fg=ft_theme)
                del_l.grid(row=0, column=4)
                del_l.after(3000, lambda: del_l.destroy())

            Label(wanda, text='Are you sure to delete?'
                              '\nThis function cannot be undone', bg=theme, fg=ft_theme).grid(row=0, column=0)
            vvk.Button(wanda, text='Delete', command=del_con).grid(row=1, column=0)
            vvk.Button(wanda, text='Cancel', command=wanda.destroy).grid(row=1, column=1)
            wanda.mainloop()

        def del_all():
            strange = Tk()
            strange.geometry('300x200')
            strange.iconbitmap(r'warning.ico')
            strange.title(f'Conformation to delete ({acc})')
            strange.configure(bg=theme)

            def del_all_con():
                my_cor.execute(f'delete from {acc}')
                del_l = Label(groot, text='Contacts deleted', bg=theme, fg=ft_theme)
                del_l.grid(row=0, column=5)
                del_l.after(3000, lambda: del_l.destroy())
                my_database.commit()
                exp_b.configure(state=DISABLED)
                strange.destroy()
                root.destroy()

            Label(strange, text='Are you sure to delete?'
                                '\nThis function cannot be undone', bg=theme, fg=ft_theme).grid(row=0, column=0)
            vvk.Button(strange, text='Delete', command=del_all_con).grid(row=1, column=0)
            vvk.Button(strange, text='Cancel', command=strange.destroy).grid(row=1, column=1)

        vvk.Button(root, text='Delete selected contacts', command=del_selected).grid(row=0, column=1)
        vvk.Button(root, text='Delete all contacts', command=del_all).grid(row=0, column=2)
        vvk.Button(root, text='Cancel', command=root.destroy).grid(row=0, column=3)


    def logout():
        global my_cor, y, my_database
        black_widow = Tk()
        black_widow.geometry('300x200')
        black_widow.title(f'Logout ({acc})')
        black_widow.iconbitmap(r'delete.ico')
        black_widow.configure(bg=theme)

        def close_wind():
            try:
                groot.destroy()
                black_widow.destroy()
            except:
                pass

        def re_login():
            if len(op.o_read('databases.txt')) > 0:
                ironman = Tk()
                ironman.geometry('450x350')
                ironman.title(f'Login')
                ironman.configure(bg=theme)
                ironman.iconbitmap(r'contacts.ico')

                lg = cr_checkbox(tk_window_object=ironman, sequence=acc_lis, bg=theme, fg=ft_theme)
                value = []

                def submit():
                    ironman.destroy()
                    for ind in range(lg[0]):
                        val = lg[1][ind].get()
                        if val == 1:
                            value.append(lg[2][ind])
                    if len(value) > 0:
                        if value[0] in db_search():
                            op.o_write('data settings.txt', value[0])
                    else:
                        os.abort()
                    runpy.run_path('contacts.py')

                vvk.Button(ironman, text='continue', command=submit).grid()
                Label(ironman, text='select to login again', bg=theme, fg=ft_theme).grid()
                ironman.mainloop()
                op.o_write('settings.txt',
                           f'username= {user_n},password= {passwd},hostname= {host_n},on,#e8e8e8,yes,sun')
            else:
                op.o_write('settings.txt',
                           f'username= {user_n},password= {passwd},hostname= {host_n},off,#e8e8e8,yes,sun')

        def logout_con_all():
            close_wind()
            op.o_write('data settings.txt', '')
            op.o_write('settings.txt',
                       f'username= {user_n},password= {passwd},hostname= {host_n},on,#e8e8e8,yes,sun')
            log_pg()

        def logout_con():
            close_wind()
            inp_val = []
            value = []
            for ind in range(re[0]):
                val = re[1][ind].get()
                if val == 1:
                    value.append(re[2][ind])

            if len(value) > 0:
                for j in value:
                    op.o_replace('databases.txt', j + ',', '')
            op.o_write('data settings.txt', '')
            op.o_write('settings.txt',
                       f'username= {user_n},password= {passwd},hostname= {host_n},on,#e8e8e8,yes,sun')
            re_login()

        re = cr_checkbox(black_widow, acc_lis, column=0, row=3)

        vvk.Button(black_widow, text=f'remove selected accounts', command=logout_con).grid(row=2, column=0)
        vvk.Button(black_widow, text=f'remove all accounts', command=logout_con_all).grid(row=1, column=0)
        vvk.Button(black_widow, text='Cancel', command=black_widow.destroy).grid(row=1, column=1)
        black_widow.mainloop()


    def db_search():
        lst = show_tables(my_cor)
        tab = []
        for i in range(len(lst)):
            if lst[i].endswith('_conapp'):
                tab.append(lst[i])
        return tab


    def resetting():
        restore = Tk()
        restore.geometry('400x300')
        restore.configure(bg=theme)
        restore.iconbitmap(r'reset.ico')
        restore.title(f'Confirm to reset ({acc})')
        Label(restore, text='Are you sure.\nDo you want to reset the contacts app\n'
                            'WARNING! All of your accounts will be logged out\nYou have to restart from first',
              justify='center', bg=theme, fg='red').grid(row=0, column=0)

        def reset_confirm():
            groot.destroy()
            restore.destroy()
            op.o_write('databases.txt', '')
            op.o_write('settings.txt', '')
            op.o_write('data settings.txt', '')

            runpy.run_path('contacts.py')

        vvk.Button(restore, text='Reset', command=reset_confirm).grid(row=1, column=0)
        vvk.Button(restore, text='Cancel', command=restore.destroy).grid(row=1, column=1)
        restore.mainloop()


    def search():
        loki = Tk()
        loki.geometry('1366x768')
        loki.configure(bg=theme)
        loki.iconbitmap(r'contacts.ico')
        loki.title(f'Search ({acc})')

        Label(loki, text='Enter the category* :', bg=theme, fg=ft_theme).grid(row=0, column=9)
        Label(loki, text='Enter the detail     :', bg=theme, fg=ft_theme).grid(row=1, column=9)

        cond = StringVar(loki, value='')
        name = StringVar(loki, value='')

        Entry(loki, textvariable=cond).grid(row=0, column=10)
        Entry(loki, textvariable=name).grid(row=1, column=10)

        def searching():
            global qry1, qry2, qry3
            fst = cond.get()
            snd = name.get()
            qrs = []

            def diffe(categ, detail):
                es = [f"select * from {acc} where {categ} like '%{detail}%' order by first_name",
                      f"select * from {acc} where {categ} like '{detail}%' order by first_name",
                      f"select * from {acc} where {categ} like '%{detail}' order by first_name"]
                for i in range(3):
                    qrs.append(es[i])

            if len(fst) > 0:
                b = '*'
                if 'sur' in fst:
                    b = 'sur_name'
                elif 'fir' in fst:
                    b = 'first_name'
                elif 'phone' in fst:
                    b = 'phone'
                elif fst.startswith('ph') and fst.endswith('le'):
                    b = 'ph_label'
                elif 'email' in fst:
                    b = 'email_address'
                elif fst.startswith('e') and fst.endswith('ss'):
                    b = 'em_label'
                elif 'address' in fst:
                    b = 'address'
                elif 'date' or 'day' in fst:
                    b = 'significant_date'
                elif 'relation' in fst:
                    b = 'relationship'

                if len(snd) > 0:
                    diffe(b, snd)
                else:
                    qrs.append(f"select * from {acc} group by {b}")
            elif len(snd) > 0:
                if snd.isdigit():
                    diffe('phone', snd)
                else:
                    qrs.append(f"select * from {acc} order by first_name")
            else:
                qrs.append(f"select * from {acc} order by first_name")
            try:
                my_cor.execute(qrs[0])
            except:
                pass
            try:
                my_cor.execute(qrs[1])
            except:
                pass
            try:
                my_cor.execute(qrs[2])
            except:
                pass

            detail = my_cor.fetchall()

            Label(loki, text='First name    ', bg=theme, justify='left', fg=ft_theme).grid(row=5, column=0)
            Label(loki, text='Sur name    ', bg=theme, justify='left', fg=ft_theme).grid(row=5, column=1)
            Label(loki, text='Phone no    ', bg=theme, justify='left', fg=ft_theme).grid(row=5, column=2)
            Label(loki, text='Ph_label    ', bg=theme, justify='left', fg=ft_theme).grid(row=5, column=3)
            Label(loki, text='Address    ', bg=theme, justify='left', fg=ft_theme).grid(row=5, column=4)
            Label(loki, text='Email_address    ', bg=theme, justify='left', fg=ft_theme).grid(row=5, column=5)
            Label(loki, text='Em_label    ', bg=theme, justify='left', fg=ft_theme).grid(row=5, column=6)
            Label(loki, text='Significant_date    ', bg=theme, justify='left', fg=ft_theme).grid(row=5, column=7)
            Label(loki, text='Relationship    ', bg=theme, justify='left', fg=ft_theme).grid(row=5, column=8)
            Label(loki, text='Date created    ', bg=theme, justify='left', fg=ft_theme).grid(row=5, column=9)

            for i in range(len(detail)):
                a = detail[i][0]
                b = detail[i][1]
                c = detail[i][2]
                d = detail[i][3]
                e = detail[i][4]
                f = detail[i][5]
                g = detail[i][6]
                h = detail[i][7]
                j = detail[i][8]
                k = detail[i][9]
                p = i + 7

                aa = Label(loki, text=a, justify='left', bg=theme, fg=ft_theme)
                aa.grid(row=p, column=0)
                bb = Label(loki, text=b, justify='left', bg=theme, fg=ft_theme)
                bb.grid(row=p, column=1)
                cc = Label(loki, text=c, justify='left', bg=theme, fg=ft_theme)
                cc.grid(row=p, column=2)
                dd = Label(loki, text=d, justify='left', bg=theme, fg=ft_theme)
                dd.grid(row=p, column=3)
                ee = Label(loki, text=e, justify='left', bg=theme, fg=ft_theme)
                ee.grid(row=p, column=4)
                ff = Label(loki, text=f, justify='left', bg=theme, fg=ft_theme)
                ff.grid(row=p, column=5)
                gg = Label(loki, text=g, justify='left', bg=theme, fg=ft_theme)
                gg.grid(row=p, column=6)
                hh = Label(loki, text=h, justify='left', bg=theme, fg=ft_theme)
                hh.grid(row=p, column=7)
                jj = Label(loki, text=j, justify='left', bg=theme, fg=ft_theme)
                jj.grid(row=p, column=8)
                kk = Label(loki, text=k, justify='left', bg=theme, fg=ft_theme)
                kk.grid(row=p, column=9)

        vvk.Button(loki, text='Submit', command=searching).grid(row=1, column=11)

        loki.mainloop()


    def export_con():
        my_cor.execute(f'select * from {acc}')
        ft = my_cor.fetchall()
        op.o_write('share contacts.txt', '')
        for i in range(len(ft)):
            l = str(ft[i])
            r = l.rstrip(')')
            lf = r.lstrip('(')
            op.o_append('share contacts.txt', lf, newline=True)
        Label(groot, text='Please visit the folder where you saved this contacts app\n'
                          'in your system the share contacts.txt\n'
                          'file to share the contacts', fg=ft_theme, bg=theme).grid(row=1, column=5)


    def import_con():
        try:
            ln = op.o_read('share contacts.txt', line=True)
            if not ln:
                imp = Label(groot, text='No contacts to import', fg=ft_theme, bg=theme)
                imp.grid(row=3, column=5)
                imp.after(3000, lambda: imp.destroy())
            else:
                for i in ln:
                    l = str(i)
                    ll = l.lstrip("(")
                    r = ll.rstrip(")")
                    f = ''
                    for j in r:
                        if j == '"' or j == "'":
                            f += ''
                        else:
                            f += j
                    v = f.split(',')
                    first_name = v[0]
                    sur_name = v[1]
                    phone = v[2]
                    ph_label = v[3]
                    address = v[4]
                    email_address = v[5]
                    em_label = v[6]
                    significant_date = v[7]
                    relationship = v[8]
                    b = f'INSERT INTO {acc} (first_name, sur_name, phone, ph_label, address, email_address, ' \
                        'em_label, significant_date, relationship, date_add)' \
                        'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    a = (first_name, sur_name, phone, ph_label, address, email_address, em_label, significant_date,
                         relationship, today)
                    my_cor.execute(b, a)
                    my_database.commit()
                imp_sucs = Label(groot, text='Contacts imported', fg=ft_theme, bg=theme)
                imp_sucs.grid(row=4, column=5)
                exp_b.configure(state=ACTIVE)
                imp_sucs.after(3000, lambda: imp_sucs.destroy())

        except:
            no_file = Label(groot, text='No file found to import', fg=ft_theme, bg=theme)
            no_file.grid(row=2, column=5)
            no_file.after(3000, lambda: no_file.destroy())


    def display_contact():
        loki = Tk()
        loki.geometry('1366x768')
        loki.configure(bg=theme)
        loki.iconbitmap(r'contacts.ico')
        loki.title(f'All contacts ({acc})')
        my_cor.execute(f"select * from {acc} order by first_name")
        detail = my_cor.fetchall()

        Label(loki, text='First name    ', bg=theme, justify='left', fg=ft_theme).grid(row=0, column=0)
        Label(loki, text='Sur name    ', bg=theme, justify='left', fg=ft_theme).grid(row=0, column=1)
        Label(loki, text='Phone no    ', bg=theme, justify='left', fg=ft_theme).grid(row=0, column=2)
        Label(loki, text='Ph_label    ', bg=theme, justify='left', fg=ft_theme).grid(row=0, column=3)
        Label(loki, text='Address    ', bg=theme, justify='left', fg=ft_theme).grid(row=0, column=4)
        Label(loki, text='Email_address    ', bg=theme, justify='left', fg=ft_theme).grid(row=0, column=5)
        Label(loki, text='Em_label    ', bg=theme, justify='left', fg=ft_theme).grid(row=0, column=6)
        Label(loki, text='Significant_date    ', bg=theme, justify='left', fg=ft_theme).grid(row=0, column=7)
        Label(loki, text='Relationship    ', bg=theme, justify='left', fg=ft_theme).grid(row=0, column=8)
        Label(loki, text='Date created    ', bg=theme, justify='left', fg=ft_theme).grid(row=0, column=9)

        for i in range(len(detail)):
            p = i + 1
            a = detail[i][0]
            b = detail[i][1]
            c = detail[i][2]
            d = detail[i][3]
            e = detail[i][4]
            f = detail[i][5]
            g = detail[i][6]
            h = detail[i][7]
            j = detail[i][8]
            k = detail[i][9]

            aa = Label(loki, text=a, justify='left', bg=theme, fg=ft_theme)
            aa.grid(row=p, column=0)
            bb = Label(loki, text=b, justify='left', bg=theme, fg=ft_theme)
            bb.grid(row=p, column=1)
            cc = Label(loki, text=c, justify='left', bg=theme, fg=ft_theme)
            cc.grid(row=p, column=2)
            dd = Label(loki, text=d, justify='left', bg=theme, fg=ft_theme)
            dd.grid(row=p, column=3)
            ee = Label(loki, text=e, justify='left', bg=theme, fg=ft_theme)
            ee.grid(row=p, column=4)
            ff = Label(loki, text=f, justify='left', bg=theme, fg=ft_theme)
            ff.grid(row=p, column=5)
            gg = Label(loki, text=g, justify='left', bg=theme, fg=ft_theme)
            gg.grid(row=p, column=6)
            hh = Label(loki, text=h, justify='left', bg=theme, fg=ft_theme)
            hh.grid(row=p, column=7)
            jj = Label(loki, text=j, justify='left', bg=theme, fg=ft_theme)
            jj.grid(row=p, column=8)
            kk = Label(loki, text=k, justify='left', bg=theme, fg=ft_theme)
            kk.grid(row=p, column=9)
        loki.mainloop()


    def delete_acc():
        johnny_deep = Tk()
        johnny_deep.geometry('300x200')
        johnny_deep.title(f'Delete account ({acc})')
        johnny_deep.iconbitmap(r'delete.ico')
        johnny_deep.configure(bg=theme)
        Label(johnny_deep, text='Are you sure?\nYou want to delete this account\nThis process cannot be reverted.',
              bg=theme, fg=ft_theme).grid(row=0, column=0)

        def del_acc_conf():
            johnny_deep.destroy()
            groot.destroy()
            try:
                my_cor.execute(f'drop table {acc}')
                my_cor.execute(f'drop table {acc}_backup_conapp')
            except:
                pass
            op.o_write('data settings.txt', '')
            op.o_replace('databases.txt', acc + ',', '')
            op.o_write('settings.txt', f'username= {user_n},password= {passwd},hostname= {host_n},off,#e8e8e8,yes,sun')
            runpy.run_path('contacts.py')

        vvk.Button(johnny_deep, text='Continue', command=del_acc_conf).grid(row=1, column=0)
        vvk.Button(johnny_deep, text='Cancel', command=johnny_deep.destroy).grid(row=1, column=1)
        johnny_deep.mainloop()


    def del_backup():
        barbosa = Tk()
        barbosa.geometry('300x200')
        barbosa.title(f'Delete backup ({acc})')
        barbosa.iconbitmap(r'delete.ico')
        barbosa.configure(bg=theme)
        Label(barbosa, text='Are you sure?\nYou want to delete backup\nThis process cannot be reverted.',
              bg=theme, fg=ft_theme).grid(row=0, column=0)

        def del_backup_conf():
            global backup_status, y, my_database, my_cor
            my_cor.reset()
            my_cor.execute(f'drop table {acc}_backup_conapp')
            my_database.commit()
            backup_status = 'off'
            barbosa.destroy()
            bk_del = Label(groot, text='Backup deleted', justify='left', bg=theme, fg=ft_theme)
            del_backup_b.configure(state=DISABLED)
            backup_b.configure(text=f'Back up is {backup_status} click to change')
            sync_b.configure(state=DISABLED)
            Label(groot, text='Your backup is off', justify='left', bg=theme,
                  fg=ft_theme).grid(
                row=5, column=5)
            bk_del.grid(row=7, column=5)
            bk_del.after(3000, lambda: bk_del.destroy())
            op.o_replace('settings.txt', 'on', 'off')

        vvk.Button(barbosa, text='Continue', command=del_backup_conf).grid(row=1, column=0)
        vvk.Button(barbosa, text='Cancel', command=barbosa.destroy).grid(row=1, column=1)
        barbosa.mainloop()


    def close_all():
        abort = Tk()
        abort.geometry('300x200')
        abort.title(f'Exit ({acc})')
        abort.iconbitmap(r'delete.ico')
        abort.configure(bg=theme)
        Label(abort, text='Are you sure. Do you want to exit', bg=theme, fg=ft_theme).grid(row=0, column=0)
        vvk.Button(abort, text='Yes', command=os.abort).grid(row=1, column=0)
        vvk.Button(abort, text='Cancel', command=abort.destroy).grid(row=1, column=1)
        abort.mainloop()


    def switch():
        global acc_lis
        elon = Tk()
        elon.title(f'switching account from ({acc})')
        elon.configure(bg=theme)
        elon.geometry('450x350')
        elon.iconbitmap(r'contacts.ico')
        acc_lis = (op.o_read('databases.txt').rstrip(',')).split(',')
        lg = cr_checkbox(tk_window_object=elon, sequence=acc_lis, bg=theme, fg=ft_theme)
        value = []

        def submit():
            for ind in range(lg[0]):
                val = lg[1][ind].get()
                if val == 1:
                    value.append(lg[2][ind])
            if len(value) > 0:
                if value[0] in db_search():
                    op.o_write('data settings.txt', value[0])
                    elon.destroy()
                    groot.destroy()
                    runpy.run_path('contacts.py')

        vvk.Button(elon, text=f'switch', command=submit).grid(row=0, column=1)
        elon.mainloop()


    def mode():
        qq = op.o_read('settings.txt')
        global theme
        global ft_theme
        if '#323232' in qq:
            theme = '#e8e8e8'
            ft_theme = '#323232'
            op.o_replace('settings.txt', '#323232', theme)
            groot.configure(bg=theme)
        else:
            theme = '#323232'
            ft_theme = '#e8e8e8'
            op.o_replace('settings.txt', '#e8e8e8', theme)
            groot.configure(bg=theme)


    def show_all():
        n = 0
        peter = Tk()
        peter.title(f'viewing all accounts from ({acc})')
        peter.configure(bg=theme)
        peter.geometry('450x350')
        peter.iconbitmap(r'contacts.ico')
        all_tab = show_tables(my_cor)
        for i in all_tab:
            if i.endswith("_conapp") and not i.endswith("_backup_conapp"):
                Label(peter, text=f'{n + 1}.{i}', fg=ft_theme, bg=theme).grid(row=n, column=0)
                n += 1
        peter.mainloop()


    def add_acc():
        global std
        op.o_write('settings.txt', f'usepeterrname= {user_n},password= {passwd},hostname= {host_n},off,#e8e8e8,yes,sun')
        std = op.o_read('settings.txt')
        log_pg()


    def sync():
        my_cor.execute(f'select * from {acc}_backup_conapp')
        ft = my_cor.fetchall()
        for j in ft:
            b = f'INSERT INTO {acc} (first_name, sur_name, phone, ph_label, address, email_address, em_label, significant_date, relationship, date_add) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            my_cor.execute(b, j)
            my_database.commit()
        exp_b.configure(state=ACTIVE)
        sync_comp = Label(groot, text='Sync completed', bg=theme, fg=ft_theme)
        sync_comp.grid(row=6, column=5)
        sync_comp.after(3000, lambda: sync_comp.destroy())


    groot = Tk()
    groot.title(f'Contacts ({acc})')
    groot.geometry('1366x768')
    groot.iconbitmap(r'contacts.ico')
    groot.configure(bg=theme)

    vvk.Button(groot, text="Show contacts", command=display_contact, width=30).grid(row=0, column=0)
    vvk.Button(groot, text='New contact', command=new_contact, width=30).grid(row=0, column=1)
    vvk.Button(groot, text='Search contacts', command=search, width=30).grid(row=0, column=2)
    vvk.Button(groot, text="Delete contacts", command=delete_con, width=30).grid(row=0, column=3)
    vvk.Button(groot, text="reset", command=resetting, width=30).grid(row=0, column=4)
    exp_b = vvk.Button(groot, text="Export contacts", command=export_con, width=30, state=DISABLED)
    exp_b.grid(row=1, column=0)
    my_cor.execute(f'select * from {acc}')
    ft = my_cor.fetchall()
    if len(ft) > 0:
        exp_b.configure(state=ACTIVE)
    vvk.Button(groot, text="Import contacts", command=import_con, width=30).grid(row=1, column=1)
    vvk.Button(groot, text="Delete account", command=delete_acc, width=30).grid(row=1, column=2)
    vvk.Button(groot, text='Change Theme', command=mode, width=30).grid(row=1, column=3)
    del_backup_b = vvk.Button(groot, text="Delete backup", command=del_backup, width=30, state=DISABLED)
    del_backup_b.grid(row=1, column=4)
    sync_b = vvk.Button(groot, text="Restore backed up contacts", command=sync, width=30, state=DISABLED)
    backup_b = vvk.Button(groot, text=f'Back up is {backup_status} click to change', command=back_up, width=30)
    backup_b.grid(row=2, column=0)
    sync_b.grid(row=2, column=1)
    vvk.Button(groot, text="Logout", command=logout, width=30).grid(row=2, column=2)
    vvk.Button(groot, text="show all acounts", command=show_all, width=30).grid(row=3, column=2)
    vvk.Button(groot, text="Exit the app", command=close_all, width=30).grid(row=2, column=3)
    vvk.Button(groot, text="edit contact", command=sel_edit_con, width=30).grid(row=2, column=4)
    vvk.Button(groot, text="add another account", command=add_acc, width=30).grid(row=3, column=0)
    vvk.Button(groot, text="switch account", command=switch, width=30).grid(row=3, column=1)

    do_it()
