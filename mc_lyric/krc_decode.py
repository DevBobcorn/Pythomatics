import zlib

#       [ '@', 'G', 'a', 'w', '^', '2', 't', 'G', 'Q', '6', '1', '-', 'Î', 'Ò', 'n', 'i' ]
magic = [  64,  71,  97, 119,  94,  50, 116,  71,  81,  54,  49,  45, 206, 210, 110, 105 ]; 

root = 'mc_lyric/lyrics'

srcName = 'キタニタツヤ - 悪夢'

with open(f'{root}/{srcName}.krc', 'rb+') as src:
    bites = src.read(); # Take a bite of the file >_<
    assert(bites[0:4] == b'krc1') # First 4 bytes, should be 'krc1'
    zipByte = bytearray(bites[4:]) # Skip first 4 bytes

    for idx in range(len(zipByte)): # Per-byte operation
        zipByte[idx] = zipByte[idx] ^ magic[idx % 16]

    decoded = zlib.decompress(zipByte).decode('utf-8').replace('\r', '')

    with open(f'{root}/{srcName}.txt', 'w+', encoding='utf-8') as dst:
        dst.write(decoded)