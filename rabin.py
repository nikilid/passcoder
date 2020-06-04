import random
import math
import base64


def test_millera_rabina(n, count_round):
	if n == 2 or n == 3 :
		return True
	if (n & 1 == 0) or (n == 1):
		return False
	s = 0
	t = n - 1
	while ((t & 1) != 1):
		t >>= 1
		s += 1
	for i in range(count_round):
		a = random.randint(2, n-2)
		x = pow(a, t, n)
		if (x == 1 or x == n - 1):
			continue
		for j in range(s-1):
			pow(x, 2, n)
			if (x == 1):
				return False
			if (x == n - 1):
				break
		else:
			return False
	return True


def kgen(count_bit):
	
	p = q = 0
	random.seed()
	while p == 0:
		a = random.getrandbits(count_bit-2)
		p = (a<<2)+3
		if (test_millera_rabina(p,int(math.log2(p))) == False):
			p = 0
	while q == 0:
		a = random.getrandbits(count_bit-2)
		q = (a<<2)+3
		if (test_millera_rabina(q, int(math.log2(q))) == False):
			q = 0
	#print(p, ' ', q)
	return (p, q, p*q)

def encrypt(n, pas):
	#print('Введите имя пароля:')
	#name = input()
	#print('Введите пароль:')
	#pas = input()
	password = int.from_bytes(str.encode(pas)+b'10', 'big')
	#print(password)
	cipher = pow(password, 2, n)
	cipher = cipher.to_bytes((cipher.bit_length() + 7) // 8, byteorder='big')
	return base64.b32encode(cipher)

def q_comp(a, p): #4, 7
	s = p - 1         #6
	m = 0
	while ((s & 1) != 1):
		s >>= 1           #3
		m += 1			#m=1
	#b  невычет найти
	b = 2  
	while (True):         
		if (pow(b, (p-1)>>1, p) == 1):
			b += 1                 #b = 3
		else:
			break
	b_b = pow(b, s, p)
	res_j = 0
	#if (m == 1):
	#	res_j = 0
	if (m > 1):
		a_b = pow(a, s, p)
		for i in range(m - 1):
			a_mas[i] = pow(a_b, 2 << i, p)
			b_mas[i] = pow(b_b, 2 << i, p)
		res_j = 0
		for t in range(m - 1):
			eps = a_mas[m-2-t]
			for ind in range(t):
				eps *= pow(b_mas[m-2-(t-ind-1)], j[ind])
			j[t] = (1-eps)/2
			res_j += j[t]*pow(2,t) 
	x = pow(b_b, res_j, p)*pow(a, (s+1)>>1, p)
	x %= p
	return x

def nod(a, b):
	if (b == 0):
		return (a, 1, 0)
	(d, kb, kc) = nod(b, a%b)
	return (d, kc, kb - (a // b)*kc)

def decryption(cipher, p, q, n):
	m_p = q_comp(cipher%p, p)
	#print(cipher%p, p, m_p)
	m_q = q_comp(cipher%q, q)
	#print(cipher%q, q, m_q)
	d = 1
	if (q > p):
		(d, kq, kp) = nod(q, p)
	else:
		(d, kp, kq) = nod(p, q)
	if (d != 1):
		print(d)
		return 1
	q_1 = kq % p
	p_1 = kp % q
#	print (q_1, p_1)
	m_1 = (m_p*q*(q_1) + m_q*p*(p_1))%n
	pas_1 = m_1.to_bytes((m_1.bit_length() + 7) // 8, byteorder='big')
	if (pas_1[-2:] == b'10'):
		return(pas_1[:-2])
	m_2 = n-m_1
	pas_1 = m_2.to_bytes((m_2.bit_length() + 7) // 8, byteorder='big')
	if (pas_1[-2:] == b'10'):
		return(pas_1[:-2])
	m_3 = (m_p*q*(q_1) - m_q*p*(p_1))%n
	pas_1 = m_3.to_bytes((m_3.bit_length() + 7) // 8, byteorder='big')
	if (pas_1[-2:] == b'10'):
		return(pas_1[:-2])
	m_4 = n-m_3
	pas_1 = m_4.to_bytes((m_4.bit_length() + 7) // 8, byteorder='big')
	if (pas_1[-2:] == b'10'):
		return(pas_1[:-2])
	return b'No password'

def registration():
	nbit = 256
	(p, q, n) = kgen(nbit)	
	f_pub = open("public_key.txt", 'w')
	k = f_pub.write(str(n))
	if (k != len(str(n))):
		print('Ошибка сохранения открытого ключа')
		return 1
	f_pub.close()
	f_priv = open('privat_key.txt', 'w')
	p_seed = input("Введите пароль от закрытого ключа: \n")
	p_seed = int.from_bytes(str.encode(p_seed), 'big')
	random.seed(p_seed)
	a = random.getrandbits(nbit<<1)
	p ^= (a&(pow(2, nbit+1)-1))
	q ^= (a >> nbit) 
	k = f_priv.write(str(p ) + '\n' )
	k1 = f_priv.write(str(q))	
	if (k + k1 != len(str(p)) + len(str(q))+1):
		print('Ошибка сохранения закрытого ключа')
		return 1
	f_priv.close()
	return 0

def start():
	f = open('config.txt', 'r')
	for line in F:
		new = int(line)
		path_public_key = line
		path_privat_key = line

def encrypt_password():
	path = input("Укажите файл, содержащий открытый ключ: \n")
	f = open(path, 'r')
	n = int(f.read())
	f.close()
	password = input("Введите пароль, который хотите зашифровать: \n")
	print('Зашифрованный пароль:')
	print(encrypt(n, password))

def decrypt_password(nbit):
	path = input("Укажите файл, содержащий открытый ключ: \n")
	f = open(path, 'r')
	n = int(f.read())
	f.close()
	path = input("Укажите файл, содержащий закрытый ключ: \n")
	f = open(path, 'r')
	p = int(f.readline())
	q = int(f.readline())
	p_seed = input("Введите пароль от закрытого ключа: \n")
	p_seed = int.from_bytes(str.encode(p_seed), 'big')
	random.seed(p_seed)
	a = random.getrandbits(nbit<<1)
	p ^= (a&(pow(2, nbit+1)-1))
	q ^= (a >> nbit) 
	print(a)
	f.close()
	cipher = (input("Введите зашифрованный пароль: \n"))
	cipher = (base64.b32decode(cipher))
	cipher = int.from_bytes(cipher, 'big')
	print('Пароль:')
	print(decryption(cipher, p, q, n))

nbit = 256
flag = int(input("Выберете режим работы программы: \n 1 - регистрация \n 2 - шифрование нового пароля \n 3 - расшифрование пароля \n"))
if (flag == 1):
	if (registration()):
		print('Ошибка')
if (flag == 2):
	encrypt_password()
if (flag == 3):
	decrypt_password(nbit)
		
