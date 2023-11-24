houses = {
    "A1":100,
    "A2":550,
    "A3":270,
    "A4":300,
    "B1":600,
    "B2":650,
    "B3":680
}

budget = 5000

def get_max_house(houses:dict[str, int], budget:int):
    number_of_house = 0
    bought_houses = []
    sorted_house = dict(sorted(houses.items(), key=lambda x:x[1], reverse=False))
    index = 0
    while budget > sorted_house[list(sorted_house.keys())[0]] and index < len(sorted_house)-1:
        if budget < sorted_house[list(sorted_house.keys())[index]]:
            break
        
        budget -= sorted_house[list(sorted_house.keys())[index]]
        bought_houses.append(list(sorted_house.keys())[index])
        number_of_house += 1
        index += 1
        
    return number_of_house, bought_houses

num, b_houses = get_max_house(houses, budget)
        

print("You can buy", num, "house(s)")
print(b_houses)



