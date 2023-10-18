from product import *

def list2table(arr:list[Product]):
    table = ""
    for i in arr:
        table += i.nama