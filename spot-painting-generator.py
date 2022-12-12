from tkinter import filedialog
from turtle import Turtle, Screen
import colorgram
import random
import PIL
from PIL import Image
import os

# https://stackoverflow.com/questions/13852700/create-file-but-if-name-exists-add-number
def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + "(" + str(counter) + ")" + extension
        counter += 1

    return path

# File picker dialog
filename = filedialog.askopenfilename(initialdir = ".",title ="Select an image")

# Load image
try:
    im = Image.open(filename)
except OSError:
    print('Could not open image.')
    exit()

# Resize image
im.thumbnail((400, 400))

try:
    color_list = [tuple(i for i in color.rgb) for color in colorgram.extract(im, 30)]
except PIL.UnidentifiedImageError:
    print('Could not extract colors from image')
    exit()

turtle = Turtle()
turtle.penup()
turtle.speed(0)
turtle.hideturtle()

dotsize = 30
dots_per_row = 10
space_between_dots = 70

screen = Screen()
sc = dots_per_row * space_between_dots + 200
screen.setup(sc, sc)
screen.colormode(255)

pos = (dots_per_row - 1) * space_between_dots / 2
turtle.setx(-pos)
turtle.sety(-pos)

drawn_in_row = 0
for _ in range(dots_per_row**2):
    turtle.dot(dotsize, random.choice(color_list))
    turtle.forward(space_between_dots)
    drawn_in_row += 1
    if drawn_in_row >= dots_per_row:
        drawn_in_row = 0
        turtle.setx(-pos)
        turtle.sety(turtle.ycor() + space_between_dots)

if not os.path.exists('results/'):
    os.mkdir('results')

filename = uniquify('results/work-of-art.png')

# Save image as an Encapsulated PostScript (EPS) 
ts = turtle.getscreen()
ps = ts.getcanvas().postscript(file=filename, pagewidth=1920)

# Convert EPS to PNG
im = Image.open(filename)
fig = im.convert('RGBA')
fig.save(filename, lossless = True)

screen.exitonclick()