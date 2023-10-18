class Product:
    def __init__(self, nama:str, harga:int, kategori:str):
        self.nama = nama
        self.harga = harga
        self.kategori = kategori

class Makanan(Product):
    def __init__(self, nama:str, harga:int, varian:str="tidak ada", varian_ke:int=0):
        Product.__init__(self, nama, harga, "Makanan")
        self.varian_ke = varian_ke
        self.varian = varian
        
class Pakaian(Product):
    def __init__(self, nama:str, harga:int, size:list[str], varian:str="tidak ada", varian_ke:int=0, warna:list[str]=["default"]):
        Product.__init__(self, nama, harga, "Pakaian")
        self.varian = varian
        self.varian_ke = varian_ke
        self.size = size

list_pakaian = [
    Pakaian("Ayaka Set", 35900, ["M", "L", "XL"], "Japanese Type", 1),
    Pakaian("Ayaka Set", 37900, ["M", "L", "XL"], "France Type", 2),
    Pakaian("GreenField", 12900, ["M", "L", "XL"], warna=["Hitam", "Merah", "Hijau", "Putih"])
]

list_makanan = [
    Makanan("Cookies", 2500, "Dark Chocolate", 1),
    Makanan("Cookies", 3000, "Vanilla Ocean", 2),
    Makanan("Cookies", 2500, "Red Velvet", 3),
    Makanan("Japanese Custard", 5000, "Melted Cheese", 1),
    Makanan("Japanese Custard", 5500, "Melted Choco", 2),
]

