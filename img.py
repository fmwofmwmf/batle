import glo as g
orbit = []
drone0 = []
enemy = []
proj = []
e_proj = []

# https://processing.org/examples/regularpolygon.html haha i morburglarized the code
def poly(x, y, r, n):
    angle = TWO_PI/n
    beginShape()
    for i in range(0,TWO_PI,angle):
        sx = x + cos(i)*r
        sy = y + sin(i)*r
        vertex(sx, sy)
    endShape(CLOSE)
    

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
    
def e1b():
    r = 150.0
    rh = 150.0
    ra = r*cos(30.0*PI/180)
    ro = r*sin(30.0*PI/180)
    cd1 = 100.0
    cd2 = 50.0
    cr3 = 33.0
    c2dr = 1.0/2.0 # secondary circle distance ratios, of hexagon radius, from center (e.g. 1/3 means it is placed 1/3 of distance from center to edge of hexagon)
    c3dr = 4.0/5.0 # tertiary circle distance ratios, of hexagon radius, from center (e.g. 1/3 means it is placed 1/3 of distance from center to edge of hexagon)

    fill(255)
    beginShape()
    vertex(0,-r)
    vertex(ra,-ro)
    vertex(ra,ro)
    vertex(0,r)
    vertex(-ra,ro)
    vertex(-ra,-ro)
    vertex(0,-r)
    endShape()
    
    fill(255)
    beginShape()
    vertex(0,-(cd1+cd2)/2)
    vertex((cd1+cd2)/2*ra/r,-(cd1+cd2)/2*ro/r)
    vertex((cd1+cd2)/2*ra/r,(cd1+cd2)/2*ro/r)
    vertex(0,(cd1+cd2)/2)
    vertex(-(cd1+cd2)/2*ra/r,(cd1+cd2)/2*ro/r)
    vertex(-(cd1+cd2)/2*ra/r,-(cd1+cd2)/2*ro/r)
    vertex(0,-(cd1+cd2)/2)
    endShape()
    
    

    circle(0,-r*c2dr,cd2)
    circle(0,r*c2dr,cd2)
    circle(ra*c2dr,-ro*c2dr, cd2)
    circle(ra*c2dr, ro*c2dr, cd2)
    circle(-ra*c2dr, ro*c2dr, cd2)
    circle(-ra*c2dr, -ro*c2dr, cd2)
    
    circle(0,-r*c3dr,cr3)
    circle(0,r*c3dr,cr3)
    circle(ra*c3dr,-ro*c3dr, cr3)
    circle(ra*c3dr, ro*c3dr, cr3)
    circle(-ra*c3dr, ro*c3dr, cr3)
    circle(-ra*c3dr, -ro*c3dr, cr3)
    
    circle(0,0,cd1)

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
