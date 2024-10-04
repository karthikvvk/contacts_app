from time import sleep
from datetime import date
import os
from tkinter import *
from tkinter import ttk as vvk
from tkinter import filedialog


try:
    from pymongo import MongoClient
except:
    os.system('"pip install pymongo" > NUL')
    from pymongo import MongoClient
    import pymongo

"""root_dir = os.getcwd()
req_mods = {"oopen" : "openeasy"}
req_mods_lnk = {"oopen" : "https://github.com/karthikvvk/openeasy.git"}
for hi in req_mods:
    if os.path.exists(hi):
        pass
    else:
        os.system(f"git clone {req_mods_lnk[hi]}")
"""

import jsonhd as op

theme = '#323232'
ft_theme = '#e8e8e8'
file_name = "settings.json"
today = date.today()


client = MongoClient('mongodb://localhost:27017/')
db = client['contact_app']

def show_db():
    return client.list_database_names()

def search_database():
    database_names = client.list_database_names()
    for k in database_names:
        if k == "contact_app":
            return True

def show_tables():
    return db.list_collection_names()

def search_table(table):
    for k in show_tables():
        if k == table:
            return True


if search_table("password"):
    pass_table = db["password"]
else:
    pass_table = db.create_collection("password")
user_table = ''
backup_table = ''


if op.ensure_file_exists(file_name) or op.read_file(file_name) == {}:
    op.write_file(file_name, {"login":"false", "backup":"false", "theme": theme, "user":"", "password":""})
    
rrk = op.read_file(file_name)
login, backup, theme, user, password = rrk["login"],  rrk["backup"], rrk["theme"],  rrk["user"], rrk["password"]


if user and search_table(user):
    user_table = db[user]

if backup == "true" and search_table(f"{user}_backup"):
    backup_table = db[f"{user}_backup"]




ico_lis = ['contacts.ico', 'delete.ico', 'edit.ico', 'new contact.ico', 'reset.ico', 'search.ico', 'setup.ico',
           'uninstall.ico', 'warning.ico']
for i in ico_lis:
    op.ensure_file_exists(i)


def backup_onoff():
    if backup == "true":
        return "On"
    else:
        return  "Off"


def log_pg():
    print(login)
    if login == "false":
        thunder = Tk()
        thunder.geometry('300x200')
        thunder.configure(bg=theme)
        thunder.title('Contacts set up')
        def create_acc():
            new = Tk()
            new.geometry('600x450')
            new.title('Create account')
            new.configure(bg=theme)

            def create():
                global user_table
                acc_nm = acc_name.get()
                pas = password.get()
                try:
                    if search_table(f"{acc_nm}_conapp"):
                        exit()
                    else:
                        user_table = db.create_collection(f"{acc_nm}_conapp")
                    pass_table.insert_one({f'{acc_nm}_conapp':f"{pas}"})
                    sleep(1)
                    op.update(file_name, {"login":"true", "backup":backup, "theme": theme, "user":acc_nm, "password":pas})
                except:
                    tep = Label(new, text='Account Already exists: ', fg=ft_theme, bg=theme)
                    tep.grid(row=5, column=2)
                    tep.after(2700, lambda: tep.destroy())
                thunder.destroy()
                new.destroy()

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

        def logins():
            logins = Tk()
            logins.geometry('350x250')
            logins.title('Login')
            logins.configure(bg=theme)
            acc_name = StringVar(logins, value='')
            password = StringVar(logins, value='')

            def login_submit():
                global backup
                acc_nm = acc_name.get() + '_conapp'
                pas = password.get()
                g = pass_table.find_one({user})
                p = show_tables()

                if acc_nm in p:
                    if g == pas:
                        if search_table(f'{acc_nm}_backup'):
                            backup = 'true'
                        else:
                            backup = 'false'
                        thunder.destroy()
                        logins.destroy()
                        op.update(file_name, {"login":"true", "backup":backup, "theme": theme, "user":acc_nm, "password":pas})
                    else:
                        y = Label(logins, text='Wrong password', fg='red', bg='white')
                        y.grid(row=3, column=0)
                        y.after(2700, lambda: y.destroy())
                        
                else:
                    y = Label(logins, text='account not found', fg='red', bg='white')
                    y.grid(row=4, column=0)
                    y.after(2700, lambda: y.destroy())

            Label(logins, text='Account name: ', fg=ft_theme, bg=theme).grid(row=0, column=0)
            Label(logins, text='Password: ', fg=ft_theme, bg=theme).grid(row=1, column=0)
            acnam = Entry(logins, textvariable=acc_name)
            acnam.focus_set()
            acnam.grid(row=0, column=1)
            Entry(logins, textvariable=password).grid(row=1, column=1)
            vvk.Button(logins, text='Login', command=login_submit).grid(row=2, column=0)
            logins.mainloop()

        vvk.Button(thunder, text='Login', command=logins).grid(row=0, column=0)
        vvk.Button(thunder, text='Sign up', command=create_acc).grid(row=0, column=1)

        thunder.mainloop()


log_pg()

rrk = op.read_file(file_name)
login, backup, theme, user, password = rrk["login"],  rrk["backup"], rrk["theme"],  rrk["user"], rrk["password"]
print(search_table(user))

rrk = op.read_file(file_name)

if search_table(user):
    pass
else:
    op.write_file(file_name, {"login":"false", "backup":"false", "theme": theme, "user":"", "password":""})
    os.abort()

def do_backup():
    if backup == "true":
        sync_b.configure(state=ACTIVE)
        del_backup_b.configure(state=ACTIVE)
        cursor = user_table.find()
        ft = list(cursor)
        backup_table = db[f'{user}_backup']

        for doc in ft:
            data = {
                'first_name': doc[0],
                'sur_name': doc[1],
                'phone': doc[2],
                'ph_label': doc[3],
                'address': doc[4],
                'email_address': doc[5],
                'em_label': doc[6],
                'significant_date': doc[7],
                'relationship': doc[8],
                'date_add': today
            }
            try:
                backup_table.insert_one(data)
                sleep(1)
            except:
                pass

        Label(groot, text='Your backup is on\n'
                            'To use this app with all your contacts inn\nclick sync ', justify='left', bg=theme,
                fg=ft_theme).grid(
            row=4, column=5)
    groot.mainloop()


def back_up():
    if backup == 'false':
        backup = 'true'
        do_backup()
        op.update(file_name, {'backup':backup})
        backup_b.configure(text=f'Back up is {"On" if backup == "true" else "Off"} click to change')
    elif backup == 'true':
        backup = 'false'
        do_backup()
        op.update(file_name, {'backup':backup})
        Label(groot, text='Your backup is off', justify='left', bg=theme,
                fg=ft_theme).grid(
            row=5, column=5)
        backup_b.configure(text=f'Back up is {"On" if backup == "true" else "Off"} click to change')


def new_contact(restore=False):
    root = Tk()
    root.title(f'New contact ({user})')
    root.configure(bg=theme)
    root.geometry('1366x768')

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

        contact = {
            "first_name": first_name,
            "sur_name": sur_name,
            "phone": phone,
            "ph_label": ph_label,
            "address": address,
            "email_address": email_address,
            "em_label": em_label,
            "significant_date": significant_date,
            "relationship": relationship,
            "date_add": today
        }

        try:
            user_table.insert_one(contact)
            sleep(1)
            cr = Label(root, text='Contact created', justify='left', bg=theme, fg=ft_theme)
            cr.grid(row=6, column=4)
            cr.after(1500, lambda: cr.destroy())
            exp_b.configure(state=ACTIVE)
        except pymongo.errors.DuplicateKeyError:
            new = Label(root, text=f'Contact with this number\n{phone} already exist', justify='left', bg=theme, fg=ft_theme)
            new.grid(row=7, column=4)
            new.after(1500, lambda: new.destroy())

        do_backup()


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
    scarlet = Tk()
    scarlet.geometry('900x600')
    scarlet.title(f'select a contact ({user})')
    scarlet.configure(bg=theme)
    det = user_table.find()
    detail = []
    for dt in det:
        detail.append(dt['_id'])

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
            root.title(f'edit contact ({user})')
            root.configure(bg=theme)
            root.geometry('1366x768')
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

                user_table.update_one({"phone": reff}, {"$set": {
                    "first_name": lit[0],
                    "sur_name": lit[1],
                    "phone": lit[2],
                    "ph_label": lit[3],
                    "address": lit[4],
                    "email_address": lit[5],
                    "em_label": lit[6],
                    "significant_date": lit[7],
                    "relationship": lit[8],
                    "date_add": today
                }})
                root.destroy()
                do_backup()

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
    root = Tk()
    root.geometry('900x600')
    root.title(f'Delete ({user})')
    root.configure(bg=theme)
    det = user_table.find()
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
        wanda.title(f'Conformation to delete ({user})')
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
                user_table.delete_one({"first_name": item})

            wanda.destroy()
            del_l = Label(root, text='Contacts deleted', bg=theme, fg=ft_theme)
            del_l.grid(row=0, column=4)
            del_l.after(2700, lambda: del_l.destroy())


        Label(wanda, text='Are you sure to delete?'
                            '\nThis function cannot be undone', bg=theme, fg=ft_theme).grid(row=0, column=0)
        vvk.Button(wanda, text='Delete', command=del_con).grid(row=1, column=0)
        vvk.Button(wanda, text='Cancel', command=wanda.destroy).grid(row=1, column=1)
        wanda.mainloop()

    def del_all():
        strange = Tk()
        strange.geometry('300x200')
        strange.title(f'Conformation to delete ({user})')
        strange.configure(bg=theme)

        def del_all_con():
            user_table.delete_many({})  # delete all documents in the collection
            del_l = Label(groot, text='Contacts deleted', bg=theme, fg=ft_theme)
            del_l.grid(row=0, column=5)
            del_l.after(2700, lambda: del_l.destroy())
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
    black_widow = Tk()
    black_widow.geometry('300x200')
    black_widow.title(f'Logout ({user})')
    black_widow.configure(bg=theme)

    def close_wind():
        try:
            groot.destroy()
            black_widow.destroy()
        except:
            pass


    def logout_submit():
        close_wind()
        op.write_file(file_name, {"login":"false", "backup":"false", "theme": theme, "user":"", "password":""})
        log_pg()

    vvk.Button(black_widow, text=f'remove selected accounts', command=logout_submit).grid(row=2, column=0)
    vvk.Button(black_widow, text='Cancel', command=black_widow.destroy).grid(row=1, column=1)
    black_widow.mainloop()


def resetting():
    restore = Tk()
    restore.geometry('400x300')
    restore.configure(bg=theme)
    restore.title(f'Confirm to reset ({user})')
    Label(restore, text='Are you sure.\nDo you want to reset the contacts app\n'
                        'WARNING! All of your accounts will be logged out\nYou have to restart from first',
            justify='center', bg=theme, fg='red').grid(row=0, column=0)

    def reset_confirm():
        groot.destroy()
        restore.destroy()
        op.write_file(file_name, {"login":"false", "backup":"false", "theme": theme, "user":"", "password":""})

        log_pg()

    vvk.Button(restore, text='Reset', command=reset_confirm).grid(row=1, column=0)
    vvk.Button(restore, text='Cancel', command=restore.destroy).grid(row=1, column=1)
    restore.mainloop()




def search():
    loki = Tk()
    loki.geometry('1366x768')
    loki.configure(bg=theme)
    loki.title(f'Search ({user})')

    Label(loki, text='Enter the category* :', bg=theme, fg=ft_theme).grid(row=0, column=9)
    Label(loki, text='Enter the detail     :', bg=theme, fg=ft_theme).grid(row=1, column=9)

    cond = StringVar(loki, value='')
    name = StringVar(loki, value='')

    Entry(loki, textvariable=cond).grid(row=0, column=10)
    Entry(loki, textvariable=name).grid(row=1, column=10)

    def searching():
        fst = cond.get()
        snd = name.get()
        qrs = []

        def diffe(categ, detail):
            es = [{categ: {'$regex': detail, '$options': 'i'}},
                {categ: {'$regex': '^' + detail, '$options': 'i'}},
                {categ: {'$regex': detail + '$', '$options': 'i'}}]
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
                qrs.append({})
        elif len(snd) > 0:
            if snd.isdigit():
                diffe('phone', snd)
            else:
                qrs.append({})
        else:
            qrs.append({})

        try:
            detail = user_table.find(qrs[0])
        except:
            pass
        try:
            detail = user_table.find(qrs[1])
        except:
            pass
        try:
            detail = user_table.find(qrs[2])
        except:
            pass

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
    op.write_file(f"contact_exports_{today}.json", user_table.find())
    Label(groot, text='Please visit the folder where you saved this contacts app\n'
                        f'in your system the contact_exports_{today}.json\n'
                        'file to share the contacts', fg=ft_theme, bg=theme).grid(row=1, column=5)


def import_con():
    try:
        data = op.read_file(filedialog.askopenfilename(title="Select a file", filetypes=[("JSON files", "*.json")]))
        for item in data:
            contact = {
                "first_name": item["first_name"],
                "sur_name": item["sur_name"],
                "phone": item["phone"],
                "ph_label": item["ph_label"],
                "address": item["address"],
                "email_address": item["email_address"],
                "em_label": item["em_label"],
                "significant_date": item["significant_date"],
                "relationship": item["relationship"],
                "date_add": today
            }
            try:
                user_table.insert_one(contact)
                sleep(1)
            except:
                pass
        
        
    except:
        no_file = Label(groot, text='No file found to import', fg=ft_theme, bg=theme)
        no_file.grid(row=2, column=5)
        no_file.after(2700, lambda: no_file.destroy())


def display_contact():
    loki = Tk()
    loki.geometry('1366x768')
    loki.configure(bg=theme)
    loki.title(f'All contacts ({user})')
    detail = user_table.find()

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
        a = detail[i]["first_name"]
        b = detail[i]["sur_name"]
        c = detail[i]["phone"]
        d = detail[i]["ph_label"]
        e = detail[i]["address"]
        f = detail[i]["email_address"]
        g = detail[i]["em_label"]
        h = detail[i]["significant_date"]
        j = detail[i]["relationship"]
        k = detail[i]["date_add"]

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
    johnny_deep.title(f'Delete account ({user})')
    johnny_deep.configure(bg=theme)
    Label(johnny_deep, text='Are you sure?\nYou want to delete this account\nThis process cannot be reverted.',
            bg=theme, fg=ft_theme).grid(row=0, column=0)

    def del_acc_conf():
        johnny_deep.destroy()
        groot.destroy()
        try:
            user_table.drop()
            if backup_table:
                backup_table.drop()
        except:
            pass
        op.write_file(file_name, {"login":"false", "backup":"false", "theme": theme, "user":"", "password":""})
        log_pg()

    vvk.Button(johnny_deep, text='Continue', command=del_acc_conf).grid(row=1, column=0)
    vvk.Button(johnny_deep, text='Cancel', command=johnny_deep.destroy).grid(row=1, column=1)
    johnny_deep.mainloop()


def del_backup():
    barbosa = Tk()
    barbosa.geometry('300x200')
    barbosa.title(f'Delete backup ({user})')
    barbosa.configure(bg=theme)
    Label(barbosa, text='Are you sure?\nYou want to delete backup\nThis process cannot be reverted.',
        bg=theme, fg=ft_theme).grid(row=0, column=0)

    def del_backup_conf():
        db[f"{rrk}_backup"].drop()
        backup = 'false'
        barbosa.destroy()
        bk_del = Label(groot, text='Backup deleted', justify='left', bg=theme, fg=ft_theme)
        del_backup_b.configure(state=DISABLED)
        backup_b.configure(text=f'Back up is {"On" if backup == "true" else "Off"} click to change')
        sync_b.configure(state=DISABLED)
        Label(groot, text='Your backup is off', justify='left', bg=theme,
            fg=ft_theme).grid(
            row=5, column=5)
        bk_del.grid(row=7, column=5)
        bk_del.after(2700, lambda: bk_del.destroy())
        op.update(file_name, {'backup':'false'})

    vvk.Button(barbosa, text='Continue', command=del_backup_conf).grid(row=1, column=0)
    vvk.Button(barbosa, text='Cancel', command=barbosa.destroy).grid(row=1, column=1)
    barbosa.mainloop()


def close_all():
    abort = Tk()
    abort.geometry('300x200')
    abort.title(f'Exit ({user})')
    abort.configure(bg=theme)
    Label(abort, text='Are you sure. Do you want to exit', bg=theme, fg=ft_theme).grid(row=0, column=0)
    vvk.Button(abort, text='Yes', command=os.abort).grid(row=1, column=0)
    vvk.Button(abort, text='Cancel', command=abort.destroy).grid(row=1, column=1)
    abort.mainloop()


def mode():
    data = op.read_file(file_name)
    theme = data["theme"]
    if theme == "#323232":
        ft_theme = "#e8e8e8"
    elif theme == "#e8e8e8":
        ft_theme = "#323232"
    groot.configure(bg=theme)



def sync():
    backup_documents = list(user_table.find())
    for document in backup_documents:
        backup_table.insert_one(document)
        sleep(1)
        exp_b.configure(state=ACTIVE)
        sync_comp = Label(groot, text='Sync completed', bg=theme, fg=ft_theme)
        sync_comp.grid(row=6, column=5)
        sync_comp.after(2700, lambda: sync_comp.destroy())


groot = Tk()
groot.title(f'Contacts ({user})')
groot.geometry('1366x768')
groot.configure(bg=theme)

vvk.Button(groot, text="Show contacts", command=display_contact, width=30).grid(row=0, column=0)
vvk.Button(groot, text='New contact', command=new_contact, width=30).grid(row=0, column=1)
vvk.Button(groot, text='Search contacts', command=search, width=30).grid(row=0, column=2)
vvk.Button(groot, text="Delete contacts", command=delete_con, width=30).grid(row=0, column=3)
vvk.Button(groot, text="reset", command=resetting, width=30).grid(row=0, column=4)
exp_b = vvk.Button(groot, text="Export contacts", command=export_con, width=30, state=DISABLED)
exp_b.grid(row=1, column=0)
if user_table.count_documents({}) > 0:
        exp_b.configure(state=ACTIVE)
vvk.Button(groot, text="Import contacts", command=import_con, width=30).grid(row=1, column=1)
vvk.Button(groot, text="Delete account", command=delete_acc, width=30).grid(row=1, column=2)
vvk.Button(groot, text='Change Theme', command=mode, width=30).grid(row=1, column=3)
del_backup_b = vvk.Button(groot, text="Delete backup", command=del_backup, width=30, state=DISABLED)
del_backup_b.grid(row=1, column=4)
sync_b = vvk.Button(groot, text="Restore backed up contacts", command=sync, width=30, state=DISABLED)
backup_b = vvk.Button(groot, text=f'Back up is {"On" if backup == "true" else "Off"} click to change', command=back_up, width=30)
backup_b.grid(row=2, column=0)
sync_b.grid(row=2, column=1)
vvk.Button(groot, text="Logout", command=logout, width=30).grid(row=2, column=2)
vvk.Button(groot, text="Exit the app", command=close_all, width=30).grid(row=2, column=3)
vvk.Button(groot, text="edit contact", command=sel_edit_con, width=30).grid(row=2, column=4)

do_backup()
