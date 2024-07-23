from PIL import Image, ImageFilter, ImageOps

WIDTH = 30
HEIGHT = 15


def process_image():
    with open('./input_images/guitar.jpg', 'rb') as f:
        img = Image.open(f)
        # grayscale
        img = img.convert('L')

        # resize
        img = img.resize((WIDTH, HEIGHT))

        # edge detection
        img = ImageOps.expand(img, border=5, fill=255)
        img = img.filter(ImageFilter.FIND_EDGES)
        img = img.crop((5, 5, WIDTH+5, HEIGHT+5))

        # thresholding
        px = img.load()
        for x in range(WIDTH):
            for y in range(HEIGHT):
                px[x, y] = 255 if px[x, y] < 100 else 20

    return img


def show_image(img):
    display_img = img.resize((WIDTH*100, HEIGHT*100), Image.NEAREST)
    display_img.show()


if __name__ == '__main__':
    img = process_image()
    show_image(img)
