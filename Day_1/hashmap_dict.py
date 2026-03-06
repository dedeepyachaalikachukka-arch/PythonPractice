my_dict = {'a' : 5, 'b' : 2, 'c' : 8, 'd' : 1}
my_nodict = {'p' : 10, 'q' : 7, 'r' : 3, 's' : 14}

sorted_dict_A = dict(sorted(my_dict.items(), key=lambda item: item[1]))
sorted_dict_D = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True))

for key, value in sorted(my_nodict.items(), key=lambda item: item[1]):
    print(key, value)

print("Ascending: " ,sorted_dict_A)
print("Descending: " ,sorted_dict_D)
