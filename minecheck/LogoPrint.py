from PIL import Image
import sys

# img = Image.open("crafting_table.png")
img = Image.open("minecraft-logo.png")
gray_img = img.convert('L')
width    = img.width
height   = img.height
scale    = width // 130
#char_lst = ' .:-=+*#%@'
char_lst = '@%#*+=-:. '
char_len = len(char_lst)

for y in range(0, height, scale):
    for x in range(0, width, scale):
        choice =gray_img.getpixel((x, y)) * char_len // 255
        if choice==char_len:
            choice=char_len-1
        sys.stdout.write(char_lst[choice])
    sys.stdout.write('\n')
    sys.stdout.flush()