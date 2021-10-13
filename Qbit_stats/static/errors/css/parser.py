file = str(input("file >>>"))
expansion = str(input("expansion >>>"))
units = str(input("units >>>"))

nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

input_text = open(file + "." + expansion, "r")
output_text = open(file + "1." + expansion, "w")
print(file + "." + expansion)

while True:
    temp = str(input_text.readline())
    print(temp)
    string = ""
    go = False
    j = 0
    d_len = 0
    for i in range(len(temp)):
        i -= d_len
        if temp[i] in nums:
            string += temp[i]
            if not go:
                j = i
            go = True
        else:
            if go:
                try:
                    if temp[i] == 'p' and temp[i+1] == 'x':
                        len_temp1 = len(temp)
                        temp = temp[:j] + str(int(string)//2) + temp[i:]
                        len_temp2 = len(temp)
                        d_len += len_temp1 - len_temp2
                        print(d_len, temp)
                        string = ""
                except:
                    pass
            go = False
            
    output_text.write(temp)
    
    if temp == "/*end*/":
        break

input_text.close()
output_text.close()
