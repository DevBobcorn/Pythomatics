from PIL import Image, ImageOps, ImageStat
import os, glob, json
from json import JSONEncoder

proc_types = [
    'block',
    'item'
]

recolor_dict = {
    'minecraft:block/water_flow': (63, 118, 228),
    'minecraft:block/water_overlay': (63, 118, 228),
    'minecraft:block/water_still': (63, 118, 228),
    
    'minecraft:block/birch_leaves': (128, 167, 55),
    'minecraft:block/spruce_leaves': (97, 153, 97),
    'minecraft:block/lily_pad': (32, 128, 48),
    
    'minecraft:block/grass_block_top': (121, 192, 90),
    'minecraft:block/grass_block_side_overlay': (121, 192, 90),
    'minecraft:block/grass': (121, 192, 90),
    'minecraft:block/fern': (121, 192, 90),
    'minecraft:block/tall_grass_bottom': (121, 192, 90),
    'minecraft:block/tall_grass_top': (121, 192, 90),
    'minecraft:block/large_fern_bottom': (121, 192, 90),
    'minecraft:block/large_fern_top': (121, 192, 90),
    'minecraft:block/sugar_cane': (121, 192, 90),

    'minecraft:block/oak_leaves': (119, 171, 47),
    'minecraft:block/acacia_leaves': (119, 171, 47),
    'minecraft:block/jungle_leaves': (119, 171, 47),
    'minecraft:block/dark_oak_leaves': (119, 171, 47),
    'minecraft:block/vine': (119, 171, 47),
}

skip_list = []

def recolor(srci, col):
    #Preserve the alpha value before converting it..
    r,g,b,alpha = srci.split()
    gray = srci.convert('L')
    rec = ImageOps.colorize(gray, (0,0,0), (255,255,255), col, 0 ,255 ,157).convert('RGBA')
    #Recover its transparency..
    rec.putalpha(alpha)
    #rec.show()
    return rec

def getTranspMeanColor(im):
    color = ImageStat.Stat(im).mean
    r = round(color[0])
    g = round(color[1])
    b = round(color[2])
    a = round(color[3])
    return [ r, g, b, a ]

size = 1024
rct = 16
lncnt = int(size / rct) # How many textures in a line
print('Textures in a line: ' + str(lncnt))

atlas = Image.new('RGBA', (size, size), (0, 0, 0, 0))

offset = 0
i = 0
j = 0

indexOffset = 65536

atlas_dict = { }

root_path = f'{os.getcwd()}/mc_atlas'
res_path = f'{os.getcwd()}/mc_atlas/assets'

class TextureInfo:
  def __init__(self, idx, x, y, desc, color):
    self.index = idx
    self.x = x
    self.y = y
    self.code = getCodeForIndex(idx)
    self.codePoint = getCodePointForIndex(idx)
    self.desc = desc
    self.color = color

class TextureInfoEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def getUpperHalf(c):
    return int(((c - 0x10000) - (c % 0x400)) / 0x400) + 0xd800

def getLowerHalf(c):
    return (c % 0x400) + 0xdc00

def getCodeForIndex(index: int): # index range: [0, 65536)
    if index < 0x1900: # index range [0, 6400)
        # Use Unicode Private Use Area U+E000 to U+F8FF (6400 code points)
        return f'\\u{((hex(index + 0xe000))[2:]).zfill(4)}'
    elif index < 71934: # index range [6400, 71934)
        # Use Unicode Private Use Area-A U+F0000 to U+FFFFD (65534 code points)
        codePoint = 0xf0000 + (index - 0x1900)
        return f'\\u{hex(getUpperHalf(codePoint))[2:]}\\u{hex(getLowerHalf(codePoint))[2:]}'
    else: # Treat as 0
        return '\\ue000'

def getCodePointForIndex(index: int): # index range: [0, 65536)
    if index < 0x1900: # index range [0, 6400)
        # Use Unicode Private Use Area U+E000 to U+F8FF (6400 code points)
        return f'{str(hex(index + 0xe000))}'
    elif index < 71934: # index range [6400, 71934)
        # Use Unicode Private Use Area-A U+F0000 to U+FFFFD (65534 code points)
        codePoint = 0xf0000 + (index - 0x1900)
        return f'{str(hex(codePoint))[2:]}'
    else: # Treat as 0
        return 'e000'

namespaces = os.listdir(res_path)
for nspath in namespaces:
    print(f'NameSpace: {nspath}')
    
    for proc_type in proc_types:
        paths = glob.iglob(f'{res_path}/{nspath}/textures/{proc_type}/**/*?.png', recursive=True) # Also search sub-folders...

        pathLen = len(f'{res_path}/{nspath}/textures/')

        for path in paths:
            texname = f'{nspath}:{path[pathLen:-4]}'
            texname = texname.replace('//', '/').replace('\\', '/')

            if texname in skip_list:
                print(f'Skipping {texname}')
                continue
            
            print(f'Processing {texname}')
            
            tex = Image.open(path).convert('RGBA')

            # Rescale if necessary
            if tex.width != rct:
                print(f'Rescaling {texname} to {rct}')
                tex = tex.resize((rct, round(tex.height / tex.width) * rct))

            # Crop if necessary
            if tex.width != tex.height:
                print(f'Cropping {texname}')
                tex = tex.crop((0, 0, tex.width, tex.width))
            
            # Recolor if necessary
            if recolor_dict.__contains__(texname):
                print(f'Recoloring {texname}')
                tex = recolor(tex, recolor_dict[texname])

            index = j * lncnt + i + indexOffset

            # Store its information
            info = TextureInfo(index, i * rct, j * rct, path[pathLen:-4], getTranspMeanColor(tex))
            atlas_dict[texname] = info

            # Paste it onto the atlas
            atlas.paste(tex, (info.x, info.y))
            
            i += 1
            offset += 1
            if i == lncnt:
                i = 0
                j += 1

atlasBackground = Image.new('RGBA', (size, size), (0, 0, 0, 31))
atlas = Image.alpha_composite(atlasBackground, atlas)

with open(f'{root_path}/mc_atlas_dict.json', 'w+') as f:
    data = json.dumps(atlas_dict, indent=4, separators=(',', ': '), cls=TextureInfoEncoder)
    f.write(data)

atlas.save(f'{root_path}/mc_atlas.png')
print('Done.')
