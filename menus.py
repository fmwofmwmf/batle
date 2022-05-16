from mods import *

def s_menu(m):
    global menu
    if menu == 1:
        eval_grid()
    if m == 1:
        del inv['store'][:]
        for i in range(9):
            inv['store'].append(button([600 + 70*(i%10), 580, 70, 70], eval('ob'+str(i+1)+'(inter.pos.x,inter.pos.y)'), 'store'))
    menu = m

def menu0():
    fill(255,100)
    quad(0, 0, 740, 0, 640, 100, 0, 100)
    quad(720, 0, 740, 0, 640, 100, 640, 80)
    h=0.3

    quad(720, 0, 740, 0, map(h, 0, 1, 740, 640), map(h, 0, 1, 0, 100), \
          map(h, 0, 1, 720, 640), map(h, 0, 1, 0, 80))
    for i in range(9):
        square(10+70*i, 10, 60)
        if selected == i+1:
            square(15+70*i, 15, 50)
    
    orbit_types = {}
    for i in range(5):
        orbit_types['ob' + str(i+1)] = [0, 0]
    
    for x in orbit:
        orbit_types[x.att['id']][0] += 1
        if not x.state:
            orbit_types[x.att['id']][1] += 1
    
    c = [6, 3, 5, 3, 2]
    
    for i in range(5):
        pushMatrix()
        translate(40+70*i, 40)
        graphics['o'+ str(i+1)]()

        o = orbit_types['ob'+str(i+1)]
        prog_box(-30, 35, c[i], o[0], o[0]-o[1], 60/c[i], 6)
        #prog_bar(-30, 30, 60, 4, o[1], o[0])
        popMatrix()
    fill(255)

class button():

    def __init__(self, d, c, l, interact=lambda: None, graphic=None):
        self.dim = d
        self.c = c
        self.id = l
        self.g=graphic
        self.inter = interact

    def render(self, x=None, y=None):
        pos = [o for o in self.dim]
        if x is not None and y is not None:
            pos = [x, y, self.dim[2], self.dim[3]]
        if self.g != None:
            self.g(*pos)
        else:
            rect(*pos)
        if self.c != None:
            pushMatrix()
            translate(pos[0]+pos[2]/2, pos[1]+pos[3]/2)
            self.c.att['g']()
            popMatrix()
    
    def click(self):
        return mouseX > self.dim[0] and mouseX < self.dim[0]+self.dim[2] \
    and mouseY > self.dim[1] and mouseY < self.dim[1]+self.dim[3]
    
    def interact(self, b):
        if self.id == 'grid' or b.id == 'grid':
            if self.id == b.id:
                self.inter(self, b)
            elif b.id == 'store':
                if self.c==None:
                    self.c = cot.deepcopy(b.c)
            elif self.id == 'bin':
                b.c.delete()
                b.c=None

inv = {'grid':[], 'inv':[], 'storage':[], 'store':[], 'sell':[]}
m=[None]*3
grid_s = [11,7]

def menu1_setup():
    for x in range(5):
        inv['inv'].append(button([25+100*x, 50, 50, 50], None, 'inv'))

    for i, x in enumerate(orbit+[None]*(grid_s[0]*grid_s[1]-len(orbit))):
        inv['grid'].append(button([620 + 60*(i%grid_s[0]), 120+60*(i/grid_s[0]), 60, 60], 
                           x, 'grid', switch))
    inv['grid'][0].c = modifier({'range':2, 'shape':'ROW', 'effect':b_damage, 'order':1})
    inv['grid'][1].c = modifier({'range':1, 'shape':'COL', 'effect':b_damage, 'order':1})
    inv['grid'][2].c = modifier({'range':2, 'shape':'ROW', 'effect':health, 'order':1})
    inv['grid'][3].c = modifier({'range':2, 'shape':'COL', 'effect':health, 'order':1})
    inv['grid'][4].c = modifier({'range':4, 'shape':'ROW', 'effect':health, 'order':1})
    inv['grid'][5].c = modifier({'range':2, 'shape':'COL', 'effect':defense, 'order':1})
    inv['grid'][6].c = modifier({'range':5, 'shape':'ROW', 'effect':defense, 'order':1})
    inv['grid'][7].c = modifier({'range':3, 'shape':'ROW', 'effect':c_damage, 'order':1})
    
    inv['sell'].append(button([1230, 580, 70, 70], None, 'bin', graphic=bin_g))
    
    for i in range(20):
        inv['storage'].append(button([600 + 70*(i%10), 660+70*(i/10), 70, 70], None, 'storage'))

def menu1():
    background(255)
    fill(0)
    text(mouseX, 100, 100)
    text(mouseY, 130, 100)
    fill(255)
    rect(300,100,1000,700)
    line(600,100,600,800)
    line(600,560,1300,560)
    #line(600,580,1300,580)
    
    for x in [v for k in inv for v in inv[k]]:
        x.render()
    if m[0] is not None:
        m[0].render(mouseX-m[1], mouseY-m[2])

def menu1_mousePressed():
    global m
    for x in [v for k in inv for v in inv[k]]:
        if x.click() and x.c != None:
            m = [x, mouseX-x.dim[0], mouseY-x.dim[1]]
            break

def menu1_mouseReleased():
    global m
    if m[0] is not None:
        for x in [v for k in inv for v in inv[k]]:
            if x.click():
                x.interact(m[0])
                break
    m = [None]*3

def eval_grid():
    del orbit[:]
    o_list = {}
    for x in inv['grid']:
        if type(x.c) != None:
            ad(o_list, type(x.c), [x])
            #x.c.mods = []
            #o_list.append(x.c)
            #orbit.append(x.c)
    for x in o_list.get(Ob, []):
        x.c.mods = []
        orbit.append(x.c)
    for x in sorted(o_list.get(modifier, []), key=lambda x: x.c.att['order']):
        for y in x.c.targets(inv['grid'], grid_s, inv['grid'].index(x)):
            print y.c
            if y in o_list.get(Ob, []):
                print y.c
                y.c.mods.append(x.c.att['effect'])
    for x in o_list.get(Ob, []):
        x.c.update()
                    
                
            

def switch(a,b):
    c = b.c
    b.c = a.c
    a.c = c
