from PIL import Image, ImageEnhance
from dxfwrite import DXFEngine as dxf

# 1. Read an image & convert it to a matrix of brightness
name = input('Input name of photo: ')
image = Image.open(name + '.jpg')  # read an image
newWidth = int(input('Input number of circles in X: '))  # input x dimension of new resized image
new_image = image.resize((newWidth, int(image.height * newWidth / image.width))).convert('L')  # resizing and convert to gray 
new_image = ImageEnhance.Contrast(new_image).enhance(2)
new_image.save(name + '_new.jpg')  # save resized image
briPixel = [[new_image.getpixel((i, j)) for j in range(new_image.height - 1)] for i in range(new_image.width)]  #
# matrix of brightness of gray resized image

# 2. Convert brimatrix to vector image of circles
drawing = dxf.drawing(name + '.dxf')
mindim = 50
for j in range(len(briPixel[0])):
    for i in range(len(briPixel)):
        if briPixel[i][j] < (255 - mindim):
            circle = dxf.circle(1 - (briPixel[i][j] / 255), (i * 2.1, -j * 2.1))
            drawing.add(circle)

drawing.save()

