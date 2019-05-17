import re

from classes import *


def processing_add2(msrm_m,xyz):
    i = 0
    min = abs(xyz - msrm_m[0])
    k = 0
    while i < len(msrm_m):
        if abs(xyz - msrm_m[i].x) < min:
            min = abs(xyz - msrm_m[i].x)
            k = msrm_m[i].x
    return k

def processing_add(msrm,msrm_m,x,y=0.0,z=0.0):
    razn_x = processing_add2(msrm_m,x)
    razn_y = processing_add2(msrm_m,y)
    razn_z = processing_add2(msrm_m,z)
    fin = []
    i = 0
    while i < len(msrm):
        if razn_x == msrm[i].x and razn_y == msrm[i].y and razn_z == msrm[i].z:
            fin.append(x - msrm[i].dx)
            fin.append(y - msrm[i].dy)
            fin.append(z - msrm[i].dz)


    return fin

def meas_minimize(meas):
    arr_minimize = []
    i = 1
    j = 0
    mass_x = []
    mass_x.append(meas[0].x)
    while i < len(meas):
        if mass_x[j] > meas[i].x:
            mass_x.append(meas[i].x)
            j += 1
        i += 1
    i = 1
    j = 0
    mass_y = []
    mass_y.append(meas[0].y)
    while i < len(meas):
        if meas[i].y == mass_y[0]:
            break
        if mass_y[j] > meas[i].y:
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
        if mass_z[j] > meas[i].z:
            mass_z.append(meas[i].z)
            j += 1
        i += 1

    i = 0
    while i < len(mass_x):
        prom = meas_minimizes()
        prom.x = mass_x[i]
        prom.y = mass_y[i]
        prom.z = mass_z[i]
        arr_minimize.append(prom)
    return arr_minimize


def processing(strg, msrm,msrm_m):
    if type(strg) is float or int:
        tx = processing_add(msrm,msrm_m,strg)
        return tx[0]
    else:
        if len(strg) == 2:
            ty = processing_add(msrm,msrm_m,strg[0],strg[1])
            ty1 = []
            ty1.append(ty[0])
            ty1.append(ty[1])
            return ty1
        elif len(strg) == 3:
            return processing_add(msrm,msrm_m,strg[0],strg[1],strg[2])
def write(data_ish,data_obr):

    if data_ish.startwith("G53"):
        return "G53 " + data_obr
    elif data_ish.startwith("G91"):
        return "G91 " + data_obr

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
    strg = str(fl)
    if strg[0] == "-":
        return convert_second(strg,1)
    else:
        return convert_second(strg,0)

def types(el):
    if type(el) is float or int:
        return "X" + convert(el)
    else:
        i = 0
        strg = str()
        book = ["X","Y","Z"]
        while i < len(el):
            strg = strg + " " + book[i] + convert(el[i])
        return strg[1:]


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


    


def gcord(str):
    msrm = meas_open()
    msrm_m = meas_minimize(msrm)
    for line in str:
        if line.startswith("G53") or line.startswith("G91"):
            nt = processing(kol(otdel(line)),msrm,msrm_m)
            line = write (line,types(nt))
            print(line)


def meas_open():
    pl = []
    # откроем файл и считаем его содержимое в список
    with open('measurements.txt', 'r') as f_meas:
        for line in f_meas:
            # удалим заключительный символ перехода строки
            currentPlace = line[:-1]

            # добавим элемент в конец списка
            pl.append(currentPlace)
    # print(pl)
    pl.remove("X	Y	Z	DX	DY	DZ")

    i = 0
    pl_obr = []
    while i < len(pl):
        av = Pogresh()
        av.opr(pl[i].split("\t"))
        pl_obr.append(av)
        # pl_obr[i].prints()
        i += 1
    return pl_obr


with open('g.txt','r') as fg:
    #g = fg.read()
    gcord(fg)

#g = g.replace(ab[0],"G5 X10.00 Y50.05 Z40.50")
#print(g)


