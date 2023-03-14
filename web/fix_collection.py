import os, glob, shutil

for folder in glob.glob(r'web\downloaded\proc\*'):
    print(f'Fixing collection at {folder}')

    # Sanity check
    assert(os.path.exists(fr'{folder}\1.jpg'))
    assert(os.path.exists(fr'{folder}\4.jpg'))

    size1 = os.path.getsize(fr'{folder}\1.jpg')
    size4 = os.path.getsize(fr'{folder}\4.jpg')
    
    assert(size1 == size4)

    # Remove redundant files
    os.remove(fr'{folder}\1.jpg')
    os.remove(fr'{folder}\2.jpg')
    os.remove(fr'{folder}\3.jpg')

    fi = 4

    # Batch rename
    while True:
        if os.path.exists(fr'{folder}\{fi}.jpg'):
            os.rename(fr'{folder}\{fi}.jpg', fr'{folder}\{fi - 3}.jpg')
            fi += 1
        else:
            break