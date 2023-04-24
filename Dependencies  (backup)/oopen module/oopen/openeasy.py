"""
This is a module made using python to make the file handling easier.
It uses python's inbuilt functions with conditional statements and loops to accomplish the task.
It also uses os module to operatee over the files.
"""
import os


def checker(name):
    if os.path.exists(name):
        return True
        pass
    else:
        g = open(name, 'w')
        g.close()
        return False


def o_write(name, write_data, newline=False, de_limiter=''):
    checker(name)

    def write(write_dat, delimiter=''):
        for i in write_dat:
            fhw.write(i + delimiter)
            fhw.flush()

    fhw = open(name, 'w')

    if newline:
        typ = type(write_data)

        if typ == list or typ == tuple:
            if len(de_limiter) > 0:
                for i in write_data:
                    fhw.write(str(i)+de_limiter+'\n')
                    fhw.flush()
            else:
                for i in write_data:
                    fhw.write(str(i)+'\n')
                    fhw.flush()
        elif typ == str:
            fhw.write(str(write_data)+'\n')
    else:
        fhw.write(str(write_data))
    fhw.close()


def o_read(name, line=False, delimiter=''):
    checker(name)
    fhr = open(name, 'r')
    read = fhr.read()
    if line:
        if len(delimiter) > 0:
            sp = read.split(delimiter)
        else:
            sp = read.split('\n')
        return sp
    fhr.close()
    return read


def o_replace(name, old, new):
    re = open(name)
    ree = re.read()
    fh = open(name, 'w')
    wr = ree.replace(old, new)
    fh.write(wr)
    fh.close()


def o_append(name, append_data='', newline=False):
    checker(name)
    fha = open(name)
    data = fha.read()
    if newline:
        fh = open(name, 'w')
        if len(data) > 0:
            fh.write(data + '\n' + append_data)
        else:
            fh.write(append_data)
        fh.close()
    else:
        fh = open(name, 'w')
        fh.write(data + append_data)
        fh.close()
