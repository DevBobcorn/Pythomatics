rg = [0, 1, 31, 32, 62, 63]

for i in rg:
    a = "/tellraw @a {\"text\":\""
    for j in range(35):
        index = (i << 6) + j
        #a += f"\\ue{(hex(index))[2:].zfill(3)}"
        a += f"\\uefff"

    a += "\"}"

    print(a)