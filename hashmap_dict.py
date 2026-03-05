my_dict = {'a' : 5, 'b' : 2, 'c' : 8, 'd' : 1}

sorted_dict_A = dict(sorted(my_dict.items(), key=lambda item: item[1]))
sorted_dict_D = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True))

print("Ascending: " ,sorted_dict_A)
print("Descending: " ,sorted_dict_D)