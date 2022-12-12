from tkinter import filedialog
from turtle import Turtle, Screen
from sys import argv
import argparse
import PIL
from PIL import Image
import colorgram
import random
import os

parser = argparse.ArgumentParser('Generate Hirst\'s Spot Paintings')
group = parser.add_mutually_exclusive_group()
group.add_argument('-r', '--random', action='store_true', help='random colors')
args = parser.parse_args()

# https://stackoverflow.com/questions/13852700/create-file-but-if-name-exists-add-number
def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + "(" + str(counter) + ")" + extension
        counter += 1

    return path

if not args.random:
    # File picker dialog
    filename = filedialog.askopenfilename(initialdir=".",title="Select an image")

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

dotsize = 20
dots_per_row = 10
space_between_dots = 50

screen = Screen()
sc = dots_per_row * space_between_dots + 50
screen.setup(sc, sc)
screen.colormode(255)

pos = (dots_per_row - 1) * space_between_dots / 2
turtle.setx(-pos)
turtle.sety(-pos)

drawn_in_row = 0
for _ in range(dots_per_row**2):
    if args.random:
        color = tuple(random.randint(0,255) for _ in range(3))
    else:
        color = random.choice(color_list)
    turtle.dot(dotsize, color)
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