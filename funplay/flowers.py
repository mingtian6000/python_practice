import turtle
import math

screen = turtle.Screen()
screen.bgcolor('black')
t = turtle.Turtle()
t.speed(0)  
def draw_petal(t, size):
	t.pensize(2)
	t.color('pink')
	t.begin_fill()
	t.circle(size, 60)
	t.left(120)
	t.circle(size, 60)
	t.left(120)
	t.end_fill()
	
for i in range(6):
	draw_petal(t, 100)
	t.left(60)

t.hideturtle()
screen.mainloop()