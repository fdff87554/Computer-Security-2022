import base64

# key in nine.exe: LwcvGwPze6PKg9eLY6/Lk7P7Y8+/m89jO2O/m8eLY5tjz7+7p4Njh6PXY9+bp5Obs4vT6
key = "wcvGwPze6PKg9eLY6/Lk7P7Y8+/m89jO2O/m8eLY5tjz7+7p4Njh6PXY9+bp5Obs4vT6"
key = base64.b64decode(key)
print(key)
tmp = [k^135 for k in key]
print(tmp)
for i in tmp:
    print(chr(i), end="")
