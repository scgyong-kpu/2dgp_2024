import turtle as t

def tree(length):
    t.forward(length)
    if length > 50:
        sub = length * 0.8
        t.left(20)
        tree(sub)
        t.right(40)
        tree(sub)
        t.left(20)
    t.backward(length)

t.left(90)
tree(100)
t.exitonclick()
