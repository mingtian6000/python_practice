import turtle

def draw_square(t):
    for _ in range(4):
        t.forward(100)
        t.right(90)
        
wn = turtle.Screen()
t = turtle.Turtle()
for _ in range(4):
    draw_square(t)
    t.right(90)
wn.mainloop()