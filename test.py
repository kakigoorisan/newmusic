a = [412,352,-124,513,-9421,9328]
tmp = a[0]
for i in range(len(a)):
    if tmp > a[i] : 
        tmp = a[i]
print(tmp)
