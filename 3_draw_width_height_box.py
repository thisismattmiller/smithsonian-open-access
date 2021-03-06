from PIL import Image, ImageDraw
import json

data = json.load(open('stats/width_height.json'))

canvas_w = 25000
canvas_h = 25000

im = Image.new('RGBA', (canvas_w, canvas_h), (255, 255, 255))
draw = ImageDraw.Draw(im)


for x in data:
	print(data[x])
	height = float(data[x]['hw'][0])
	width = float(data[x]['hw'][1])


	draw.rectangle((canvas_w / 2 - (width/2*32), canvas_h / 2 - (height/2*32), canvas_w / 2 + (width/2*32), canvas_h / 2 + (height/2*32)), outline=(0, 0, 0, 50))



im.save('dimensions.png', 'PNG')


