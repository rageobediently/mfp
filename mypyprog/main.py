import re
from mypyprog.classes import *

def processing_add(msrm,msrm_m,x,y=0.0,z=0.0):
    i = 0
    min = abs(x - msrm_m[0].x)
    razn_x = msrm_m[0].x
    while i < len(msrm_m):
        if abs(x - msrm_m[i].x) < min:
            min = abs(x - msrm_m[i].x)
            razn_x = msrm_m[i].x
        i += 1

    i = 0
    min = abs(y - msrm_m[0].y)
    razn_y = msrm_m[0].y
    while i < len(msrm_m):
        if abs(y - msrm_m[i].y) < min:
            min = abs(y - msrm_m[i].y)
            razn_y = msrm_m[i].y
        i += 1

    i = 0
    min = abs(z - msrm_m[0].z)
    razn_z = msrm_m[0].z
    while i < len(msrm_m):
        if abs(z - msrm_m[i].z) < min:
            min = abs(z - msrm_m[i].z)
            razn_z = msrm_m[i].z
        i += 1

    fin = []
    i = 0
    while i < len(msrm):
        if razn_x == msrm[i].x and razn_y == msrm[i].y and razn_z == msrm[i].z:
            fin.append(x - msrm[i].dx)
            fin.append(y - msrm[i].dy)
            fin.append(z - msrm[i].dz)
        i+=1
    return fin

def meas_minimize(meas):
    arr_minimize = []
    i = 1
    j = 0
    mass_x = []
    mass_x.append(meas[0].x)
    while i < len(meas):
        if mass_x[j] < meas[i].x:
            mass_x.append(meas[i].x)
            j += 1
        i += 1
    i = 1
    j = 0
    mass_y = []
    mass_y.append(meas[0].y)
    while i < len(meas):
        if mass_y[j] < meas[i].y:
            mass_y.append(meas[i].y)
            j += 1
        i += 1
    i = 1
    j = 0
    mass_z = []
    mass_z.append(meas[0].z)
    while i < len(meas):
        if meas[i].z == mass_z[0]:
            break
        if mass_z[j] < meas[i].z:
            mass_z.append(meas[i].z)
            j += 1
        i += 1

    i = 0
    while i < len(mass_z):
        prom = Measminimizes()
        prom.ww(mass_x[i],mass_y[i],mass_z[i])
        arr_minimize.append(prom)
        i += 1
    return arr_minimize


def processing(strg, msrm,msrm_m):
    if type(strg) is list:
        if len(strg) == 2:
            ty = processing_add(msrm,msrm_m,strg[0],strg[1])
            ty1 = []
            ty1.append(ty[0])
            ty1.append(ty[1])
            return ty1
        elif len(strg) == 3:
            return processing_add(msrm,msrm_m,strg[0],strg[1],strg[2])
    else:
        tx = processing_add(msrm, msrm_m, strg)
        return tx[0]

def write(data_ish,data_obr):

    if data_ish.startswith("G53"):
        return "G53 " + data_obr + "\n"
    elif data_ish.startswith("G91"):
        return "G91 " + data_obr + "\n"

def convert_second(strg,k):
    strg = strg[k::]
    strg1 = strg[0:strg.find(".")]
    strg2 = strg[strg.find(".")+1:]
    while len(strg1) !=3:
        strg1 = "0" + strg1
    while len(strg2) !=3:
        strg2 = strg2 + "0"
    if k == 0:
        return strg1 + "." + strg2
    else:
        return "-" + strg1 + "." + strg2

def convert(fl):
    fl = round(fl,3)
    strg = str(fl)
    if strg[0] == "-":
        return convert_second(strg,1)
    else:
        return convert_second(strg,0)

def types(el):
    if type(el) is list:
        i = 0
        strg = str()
        book = ["X", "Y", "Z"]
        while i < len(el):
            strg = strg + " " + book[i] + convert(el[i])
            i += 1
        return strg[1:]
    else:
        return "X" + convert(el)



def otdel(lin):
    a = (lin[4::])
    return a

def videl(tline):
    tline = otdel(tline)
    return tline

def only_one (xyz):
    stri = xyz[1::]
    return float(stri)


def two_or_three_el (xyz):
    abc = re.findall('\-?\d\d\d\.\d\d\d',xyz)
    abc1 = []
    a = float(abc[0])
    abc1.append(a)
    a = float(abc[1])
    abc1.append(a)
    if len(abc) > 2:
        a = float(abc[2])
        abc1.append(a)
    return abc1

def kol(line):
    a = re.findall('\-?\d\d\d\.\d\d\d',line)
    if len(a) == 1:
        return only_one(line)
    elif len(a) >= 2:
        return two_or_three_el(line)

def meas_open():
    pl = []
    # откроем файл и считаем его содержимое в список
    with open('measurements.txt', 'r') as f_meas:
        for line in f_meas:
            # удалим заключительный символ перехода строки
            currentPlace = line[:-1]

            # добавим элемент в конец списка
            pl.append(currentPlace)
    pl.remove("X	Y	Z	DX	DY	DZ")

    i = 0
    pl_obr = []
    while i < len(pl):
        av = Pogresh()
        av.opr(pl[i].split("\t"))
        pl_obr.append(av)
        i += 1
    return pl_obr

def gcord(strr):
    msrm = meas_open()
    msrm_m = meas_minimize(msrm)
    strrr = str()
    for line in strr:
        if line.startswith("G53") or line.startswith("G91"):
            nt = processing(kol(otdel(line)),msrm,msrm_m)
            line = write(line,types(nt))
        strrr+= line
    return strrr

with open('g.txt','r') as fg:
    wrf = gcord(fg)
with open('g.txt','w') as wfg:
    wfg.write(wrf)

