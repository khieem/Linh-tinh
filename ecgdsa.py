from Crypto.Util import number
from Crypto.Random import random
from Crypto.Hash import SHA256
import math


# tìm tập thặng dư bậc 2 qua phương trình y^2 == x^3 + ax + b (mod p)
def thang_du_bac_2(a, b, p):
   Qp = dict()
   for i in range(1, p//2+1):
      Qp[i**2%p] = i
   return Qp

def f(a, b, p, x):
   return (x**3 + a*x + b) % p

# tìm tất cả các điểm trên E
def tim_diem(a, b, p, Qp):
   kq = []
   for x in range(0, p):
      fx = f(a, b, p, x)
      if fx in Qp.keys():
         kq.append((x, Qp[fx]))
         kq.append((x, p-Qp[fx]))
   return kq

def modular_inverse(a, b):
   _b = b
   x1,x2, y1,y2 = 0,1,1,0
   while b != 0:
      q, r = a//b, a%b
      x, y = x2-x1*q, y2-y1*q
      a,b,x2,x1,y2,y1 = b,r,x1,x,y1,y
   if x2 != 0: x2 = x2+_b
   return x2


def add(a, b, p, P, Q):
   Px, Py = P
   Qx, Qy = Q
   if Px == float('inf'): return Q
   if Qx == float('inf'): return P
   if Px == Qx and Py == p-Qy:
      return float('inf'), float('inf')
   elif Px == Qx and Py == Qy:
      ld = ( (3*Px*Px + a) * modular_inverse(2*Py,p) )%p
   elif Px != Qx:
      ld = ((Qy-Py) * modular_inverse(Qx-Px,p))%p
   x3 = (p+ ld*ld - Px - Qx)%p
   return x3, (p+ld*(Px - x3) - Py)%p

def multiply(a, b, p, P, d):
   d = bin(d)[2:]
   N = P
   Q = (float('inf'), float('inf'))
   for i in range(len(d)-1, -1, -1):
      if d[i] == '1':
         Q = add(a, b, p, Q, N)
      N = add(a, b, p, N, N)
   return Q

# sinh đường cong Elliptic với điểm sinh P cho trước
def sinh_diem(a, b, p, P):
   (x1, y1) = P
   elliptic = []
   elliptic.append((x1,y1))
   elliptic.append((x1,y1))
   i = 0
   while True:
      i += 1
      print(i)
      x2, y2 = elliptic[-1]
      if x2 == float('inf'): break
      x3, y3 = add(a,b,p,(x1,y1),(x2,y2))
      elliptic.append((x3,y3))
   return elliptic[1:]

# sinh đường cong Elliptic với điểm sinh ngẫu nhiên 
def Elliptic(a, b, p):
   Qp = thang_du_bac_2(a, b, p)
   points = tim_diem(a, b, p, Qp)

   P = points[random.randint(0, len(points)-1)]
   E = sinh_diem(a, b, p, P)
   
   # kiểm tra số điểm bằng Hasse's theorem trong trường hợp số điểm không nguyên tố
   while p+1-2*math.sqrt(p) > len(E) or len(E) > p+1+2*math.sqrt(p):
      P = points[random.randint(0, len(points)-1)]
      E = sinh_diem(a, b, p, P)
   return E

###########   ECGDSA   #################

print()
print('TẠO KHÓA')
# p = number.getPrime(160)
p = 1073690596787957956865482319367245570834443721383
print('Chọn p nguyên tố có độ dài 160 bit -> p = {}'.format(p))
a, b = 480439537590583964136724125167174542066547069420, 995523096901131811761244377670707858943772430093
print('Đường Elliptic được chọn là E: y^2 == x^3 + ax + b (mod p) với:\n\t\t\t    a = {}\n\t\t\t    b = {}\n\t\t\t    p = {}'.format(a, b, p))

G = (538732367104305756000220783597579892468303814751, 468681968178470512665409812421241633594568924469)
n = 3976631839955399840242534686574973247163397117
d = int(input('Người gửi chọn 1 số ngẫu nhiên d trong khoảng [1, {}] dùng làm khóa riêng: '.format(n-1)))
Q = multiply(a, b, p, G, modular_inverse(d, n))
print('Khóa riêng của A: {}'.format(d))
print('Công khai Ep(a, b)')
print('\t  n = {}'.format(n))
print('\t  G = ({}, {})'.format(G[0], G[1]))
print('\t  Q = ({}, {})'.format(Q[0], Q[1]))
x = input('Nhập thông điệp muốn kí: ')
print()

print('A TẠO CHỮ KÝ')
r = s = 0
while True:
   k = random.randint(1, n-1)
   print('Chọn k = {}'.format(k))
   (x1, y1) = multiply(a, b, p, G, k)
   print('(x1, y1) = ({}, {})'.format(x1, y1))
   r = x1%n
   print('r = {} mod {} = {}'.format(x1, n, r))
   if r == 0:
      print('r = 0, chọn lại k!')
      continue

   print('\nThông điệp: {}'.format(x))
   hsh = SHA256.new(x.encode('utf-8'))
   h = int(hsh.hexdigest(), 16)
   print('SHA256 = {}'.format(hsh.hexdigest()))

   s = (k*r - h) * d % n
   print('\ns = {}'.format(s))
   if s == 0:
      print('s = 0, chọn lại k!')
      continue
   print()
   print('Chữ kí của A trên thông điệp là ({}, {})'.format(r,s))
   break

print()
print('B XÁC THỰC CHỮ KÝ')
r, s = [int(x) for x in input('Nhập r, s trong chữ kí (r, s) nhận được từ A: ').split()]
w = modular_inverse(r, n)
u1 = h*w % n
u2 = s*w % n
x0, y0 = add(a, b, p, multiply(a, b, p, G, u1), multiply(a, b, p, Q, u2))
v = x0 % n
print('w = {}'.format(w))
print('u1 = {}'.format(u1))
print('u2 = {}'.format(u2))
print('(x0, y0) = ({}, {})'.format(x0,y0))
print('v = {} mod {} = {}'.format(x0, n, v))
print('v ' + ('=' if v == r else '!=') + ' r ---> ' + ('ĐÚNG' if v == r else 'SAI'))
