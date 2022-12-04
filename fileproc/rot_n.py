def rot_n(str, n):
    for ci in range(len(str)):
        c = str[ci]
        if ord(c) >= ord('a') and ord(c) <= ord('z'):
            nc = ord(c) + n
            if nc > ord('z'):
                nc -= 26
            str[ci] = chr(nc)
        elif ord(c) >= ord('A') and ord(c) <= ord('Z'):
            nc = ord(c) + n
            if nc > ord('Z'):
                nc -= 26
            str[ci] = chr(nc)
    
    return ''.join(str)

print(rot_n(list('ABCDEFG XYZ abcdefg xyz +=_0123456789-'),  1))
print(rot_n(list('png jpg jpeg qoi PNG JPG JPEG QOI'), 13))
