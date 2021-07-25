from os import system, path, listdir
from PIL import Image

def load_colours(color_loc):
    colors = []
    with open(color_loc, 'rb') as f:
        while True:
            b = f.read(3)
            if not b: break
            colors.append(tuple(int(b[i]) for i in range(3)))
    return colors

def select_palette():
    base_dir = "data/palettes"
    while True:
        system("cls")
        items = sorted([path.join("/", x) for x in listdir(base_dir)])
        print(f"SELECT COLOR PALETTE\nDir: {base_dir}")
        for i in range(len(items)):
            print(f"{i}: {items[i]}")
        if base_dir != "data/palettes":
            print(f"{len(items)}: ..")
        index = int(input("Enter Index: "))
        if index == len(items) and base_dir != "data/palettes":
            base_dir = '/'.join(base_dir.split("/")[:-1])
        elif ".palette" in items[index]:
            return base_dir + items[index]
        else:
            base_dir += items[index]
            
def create_palette_image(colours):
    palette = Image.new(mode="RGB",size=(16,16))
    pixels = palette.load()
    for i in range(palette.size[0]):
        for j in range(palette.size[1]):
            pixels[i,j] = colours[min(len(colours)-1,(j*16)+i)]
    palette.save("palette.png")

create_palette_image(load_colours(select_palette()))
system("cls")
dithering = input("Dithering (may slow down processing) [y/n]:") == 'y'
dithering = "floyd_steinberg" if dithering else "none"

system(f"echo 3 && ffmpeg -i {input('Video Name: ')} -i palette.png -filter_complex \"paletteuse=dither={dithering}\" -pix_fmt yuv420p output.mp4")
system("cls")