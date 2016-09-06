# First program;
a = 1
b = 2
c = a / (b + 1)
text = 'result:'
print(text, c)

for i in [1,1,2,3,5,8]:
    print(i)
print('Done')

for i in [1,1,2,3,5,8]:
    if i%2 == 0:
        print('even',i)
    else:
        print('odd',i)
print('Done')

alphabet = "abcdefghijklmnopqrstuvwxyz"
print(alphabet[1])
print("length of alphabet:",len(alphabet))
a = 'abc'
print('a:',a)
print('a*3:',a*3)
print('&'.join(['abc','adsa']).upper())

print("subAlphabet[0:3]",alphabet[0:3])

print(alphabet[i:])
print(alphabet[0::4])
print('asdf\N{LATIN CAPITAL LETTER O WITH DIAERESIS}')
print(type(a))
print(int('12'))
key1 = ["ord","ord2"]
key2 = ["ord3","ord4"]
k = (key1,key2)
print(k)