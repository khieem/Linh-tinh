def gcd(a, b):
    x, y = a, b
    while y != 0:
        r = x % y
        x = y
        y = r
    return x

def modular_inverse(a, b):
    _b = b
    x1,x2, y1,y2 = 0,1,1,0
    while b != 0:
        q, r = a//b, a%b
        x, y = x2-x1*q, y2-y1*q
        a, b, x2,x1, y2,y1 = b,r,x1,x,y1,y
    if x2 != 0: x2 = x2+_b
    return x2

def modular_exponentiation(b, n, m):
    n = bin(n)
    x = 1
    power = b%m
    for i in range(len(n)-1, 1, -1):
        if n[i] == '1': x = (x*power)%m
        power = (power*power) % m
    return x

def double_and_add(a,b, p, Px, Py, d):
    d = bin(d)
    Tx = Px
    Ty = Py
    for i in range(len(d)-1, 0, -1):
        Tx, Ty = add_point(a, b, p, Tx, Ty, Tx, Ty)
        if n[i] == '1': Tx, Ty = add_point(a, b, p, Tx, Ty, Px, Py)
    return Tx, Ty

def add_point(a, b, p, Px, Py, Qx, Qy):
    if Px == Qx and Py == p-Qy:
        return float('inf'), float('inf')
    elif Px == Qx and Py == Qy:
        ld = ( (3*Px*Px + a) * modular_inverse(2*Py,p) )%p
    elif Px != Qx:
        ld = ((Qy-Py) * modular_inverse(Qx-Px,p))%p
    x3 = (p+ ld*ld - Px - Qx)%p
    return x3, (p+ld*(Px - x3) - Py)%p


def sinh_diem(a, b, p, x1, y1):
    elliptic = []
    elliptic.append((x1,y1))
    elliptic.append((x1,y1))

    while True:
        x2, y2 = elliptic[-1]
        if x2 == float('inf'): break
        x3, y3 = add_point(a,b,p,x1,y1,x2,y2)
        elliptic.append((x3,y3))
    return elliptic[1:]

'''
elt = sinh_diem(1,1,43,40,10)
for i in range(len(elt)):
    print(i+1, elt[i])
print('duong cong co: {} diem'.format(len(elt)))
print(add_point(1,1,43,11,15,0,42))
'''

import re
while True:
    bieu_thuc = input()
    if bieu_thuc == 'exit': break
    gcd_pattern = 'gcd'
    modular_pattern = 'mod'
    a = re.search(modular_pattern, bieu_thuc)
    if a != None:
        e1 = re.search('^\d+', bieu_thuc)
        a = int(e1.group())

        em = re.search('\d+$', bieu_thuc)
        m = int(em.group())

        eb = re.search('-1', bieu_thuc)
        if eb == None:
            b = int(re.search('\^\d+', bieu_thuc).group()[1:])
            print(modular_exponentiation(a, b, m))
        else:
            print(modular_inverse(a, m))
    else:
        a = int(re.search('\(\d+', bieu_thuc).group()[1:])
        b = int(re.search(',\d+', bieu_thuc).group()[1:])
        print(gcd(a, b))
