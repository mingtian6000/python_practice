import turtle

import math

from random import randint

def set_random_color(t):
    r = randint(0, 255) / 255
    g = randint(0, 255) / 255
    b = randint(0, 255) / 255
    t.color(r, g, b)

def draw_fancy_petal(t, size, angle):
    t.pensize(1)
    set_random_color(t)
    t.begin_fill()
    for i in range(2):
        t.circle(size, angle)
        t.left(180 - angle)
        t.end_fill()

screen = turtle.Screen()
screen.colormode(1.0)
screen.bgcolor("black")
t = turtle.Turtle()
t.speed(1)

size = 80
petals = 12
angle = 90
for _ in range(petals):
    draw_fancy_petal(t, size, angle)
    t.left(360/petals)
    
t.hideturtle()
screen.mainloop()