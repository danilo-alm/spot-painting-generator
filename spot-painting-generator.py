from tkinter import filedialog
from turtle import Turtle, Screen
from sys import argv
import argparse
import PIL
from PIL import Image
import colorgram
import random
import os

# Configuring parser
parser = argparse.ArgumentParser('Generate Hirst\'s Spot Paintings')
parser.add_argument('-w', '--width', metavar='', type=int, required=False, help='number of dots in width')
parser.add_argument('-H', '--height', metavar='', type=int, required=False, help='number of dots in height')
parser.add_argument('-s', '--size', metavar='', type=int, required=False, help='dot size (default 20)')
parser.add_argument('-d', '--distance', metavar='', type=int, required=False, help='distance between each dot (default 50)')
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

dotsize = args.size if args.size else 20
space_between_dots = args.distance if args.distance else 50
dots_height = args.height if args.height else 10
dots_width = args.width if args.width else 10

screen = Screen()
h = dots_height * space_between_dots + space_between_dots
w = dots_width * space_between_dots + space_between_dots
screen.setup(w, h)
screen.screensize(w - 2, h - 2)
screen.colormode(255)

xpos = (dots_width - 1) * space_between_dots / 2
turtle.setx(-xpos)

ypos = (dots_height - 1) * space_between_dots / 2
turtle.sety(-ypos)

drawn_in_row = 0
for _ in range(dots_height * dots_width):
    if args.random:
        color = tuple(random.randint(0,255) for _ in range(3))
    else:
        color = random.choice(color_list)
    turtle.dot(dotsize, color)
    turtle.forward(space_between_dots)
    drawn_in_row += 1
    if drawn_in_row >= dots_width:
        drawn_in_row = 0
        turtle.setx(-xpos)
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