from math import floor, ceil

def segitiga(alas:int):
    for i in range(ceil(alas/2)):
        print(" "*(floor(alas/2)-((i+1) if (alas % 2 == 0) else i)), end="")
        print("*"*(((i+1)*2) if (alas % 2 == 0) else (i*2+1)))


def persegi_panjang(panjang:int, lebar:int):
    for i in range(lebar):
        print("*"*(panjang))

        
        
persegi_panjang(20, 5)


