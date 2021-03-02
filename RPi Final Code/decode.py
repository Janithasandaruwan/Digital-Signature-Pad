import base64
from PIL import Image
from io import BytesIO

#with open("Images/dog.jpg", "rb") as image_file:
#    data = base64.b64encode(image_file.read())

#f = open("Images/image.txt", "wb")
#f.write(data)
#f.close()

f = open("sign.txt", "r")
codes = f.read()

im = Image.open(BytesIO(base64.b64decode(codes)))
im.save('Decode/sign.jpg', 'JPEG')