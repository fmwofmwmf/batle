import glo as g
orbit = []
drone0 = []
enemy = []
proj = []
e_proj = []

def o0():
    triangle(0, 10, 5, -10, -5, -10)

def o1():
    #triangle(0, 5, 10, -10, -10, -10)
    #triangle(0, 10, 5, -10, -5, -10)
    triangle(0, 8, 7, -8, -7, -8)

def o2():
    #triangle(0, 10, 5, -10, -5, -10)
    #circle(0, 0, 10)
    quad(0, 13, 5, -5, 0, -10, -5, -5)

def o3():
    #circle(0, 0, 15)
    #square(-5, -5, 10)
    square(-7.5, -7.5, 15)

def o4():
    #triangle(0, 10, 5, -10, -5, -10)
    #square(-5, -5, 10)
    quad(0,10,-7,-7,0,0,7,-7)

def o5():
    #triangle(0, 10, 10, -10, -10, -10)
    #rect(-5, -10, 10, 20)
    quad(5,10,-5,10,-8,-10,8,-10)

def o6():
    quad(5,10,-5,10,-8,-10,8,-10)
def o7():
    quad(5,10,-5,10,-8,-10,8,-10)
def o8():
    quad(5,10,-5,10,-8,-10,8,-10)
def o9():
    quad(5,10,-5,10,-8,-10,8,-10)
graphics = {}
for i in range(10):
        graphics['o'+str(i)] = eval('o'+str(i))
#################################

def e1():
    square(-10,-10,20)

def e2():
    triangle(0, 10, 5, -10, -5, -10)

def e3():
    fill(255,0,0)
    circle(0,0,10)
    fill(255)
    
def e4():
    square(-15,-15,30)
    square(-5,-5,10)

#################################
def b3():
    quad(-7,0,0,-7,7,0,0,7)
    square(-3,-3,6)

def w1():
    arc(0, 0, 40, 20, -0.5*QUARTER_PI, 4.5*QUARTER_PI, PIE)

def bin_g(x,y,l,w):
    fill(255,100,100)
    rect(x,y,l,w)
    fill(255)
