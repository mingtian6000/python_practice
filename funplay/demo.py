import turtle
#just draw a line, and quickly flashout
# t = turtle.Turtle()
# t.forward(100)

#will keep the window open until you close it
wn = turtle.Screen()
t = turtle.Turtle()
for _ in range(4):
    t.forward(100)
    t.right(90)
    
t.circle(50)

# follow the circle direction
length = 2
for _ in range(10):
    t.forward(length)
    t.right(1)
    length += 3
wn.mainloop()


