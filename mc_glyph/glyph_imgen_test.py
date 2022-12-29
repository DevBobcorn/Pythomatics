#rg = [0, 1, 31, 32, 62, 63]
rg = range(21)

savePath = 'C:\\Users\\DevBo\\AppData\\Roaming\\.minecraft\\saves\\FONTEST\\datapacks'

with open(f'{savePath}\\mc_glyph\\data\\glyph_image\\functions\\test.mcfunction', 'w+') as f:
    for i in rg:
        a = 'tellraw @a {\"text\":\"'
        for j in range(64):
            index = (i << 6) + j
            a += f'\\ue{(hex(index))[2:].zfill(3)}'

        a += '\"}\n'

        f.write(a)
