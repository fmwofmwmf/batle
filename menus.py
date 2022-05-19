from mods import *

def menu0():
    fill(255,100)
    quad(0, 0, 740, 0, 640, 100, 0, 100)
    quad(720, 0, 740, 0, 640, 100, 640, 80)
    h=0.3

    quad(720, 0, 740, 0, map(h, 0, 1, 740, 640), map(h, 0, 1, 0, 100), \
          map(h, 0, 1, 720, 640), map(h, 0, 1, 0, 80))
    for i in range(9):
        square(10+70*i, 10, 60)
        if g.selected == i+1:
            square(15+70*i, 15, 50)
    
    orbit_types = {}
    for i in range(10):
        orbit_types['ob' + str(i)] = [0, 0]
    
    for x in orbit:
        orbit_types[x.att['id']][0] += 1
        if not x.state:
            orbit_types[x.att['id']][1] += 1
    
    c = [6, 3, 5, 3, 2, 5, 1, 1, 1]
    
    for i in range(9):
        pushMatrix()
        translate(40+70*i, 40)
        graphics['o'+ str(i+1)]()

        o = orbit_types['ob'+str(i+1)]
        prog_box(-30, 35, c[i], o[0], o[0]-o[1], 60/c[i], 6)
        #prog_bar(-30, 30, 60, 4, o[1], o[0])
        popMatrix()
    fill(255)

class button():
    def __init__(self, d, c, l, interact=None, fun=None, graphic=None):
        self.dim = d
        self.c = c
        self.id = l
        self.g=graphic
        self.inter = interact
        self.fun = fun

    def render(self, x=None, y=None):
        pos = [o for o in self.dim]
        if x is not None and y is not None:
            pos = [x, y, self.dim[2], self.dim[3]]
        if self.g != None:
            self.g(*pos)
        else:
            rect(*pos)
            if self.id == 'store' and inv['store'].index(self) == grid_page:
                rect(pos[0]+5, pos[1]+5, pos[2]-10, pos[3]-10)
        if self.c != None:
            pushMatrix()
            translate(pos[0]+pos[2]/2, pos[1]+pos[3]/2)
            self.c.att['g']()
            popMatrix()
    
    def click(self):
        return mouseX > self.dim[0] and mouseX < self.dim[0]+self.dim[2] \
    and mouseY > self.dim[1] and mouseY < self.dim[1]+self.dim[3]
    
    def interact(self, b):
        if self==b:
            if self.fun is not None:
                self.fun()
            return
        if 'grid' in b.id + self.id:
            if self.id == b.id:
                self.inter(self, b)
                
            elif b.id == 'storage':
                #if self.c==None:
                self.c = cot.deepcopy(b.c)
                if type(self.c)==mod:
                    self.c.pos(self)
            elif self.id == 'bin':
                b.c.delete()
                b.c=None

inv = {'grid':[], 'inv':[], 'storage':[], 'store':[], 'sell':[]}
m=[None]*3
grid_page = 0
grid_s = [5,5]

def menu1_setup():
    for x in range(5):
        inv['inv'].append(button([25+100*x, 50, 50, 50], None, 'inv'))
    for o in range(9):
        inv['grid'+str(o)] = []
        for i, x in enumerate(orbit+[None]*(grid_s[0]*grid_s[1]-len(orbit))):
            inv['grid'+str(o)].append(button([620 + 60*(i%grid_s[0]), 120+60*(i/grid_s[0]), 60, 60], 
                            x, 'grid'+str(o), switch))
    
    for i in range(9):
            inv['store'].append(button([600 + 70*(i%10), 580, 70, 70], 
                                       eval('ob'+str(i+1)+'(inter.pos.x,inter.pos.y)'), 'store',
                                        fun=lambda a=i:switch_grid(a)))
            
    inv['sell'].append(button([1230, 580, 70, 70], None, 'bin', graphic=bin_g))
    
    s = [mod('n', ['', '#'], inv, grid_s, [0,0,-1]),
         mod('s', ['#', ''], inv, grid_s, [0,0,-1]),
         mod('l', ['#', '#'], inv, grid_s, [0,0,-1]),
         mod('l', ['<v', '<v'], inv, grid_s, [0,0,-1]),
         mod('l', ['<^', '<^'], inv, grid_s, [0,0,-1]),
         mod('l', ['>^', '>^'], inv, grid_s, [0,0,-1]),
         mod('l', ['>v', '>v'], inv, grid_s, [0,0,-1]),] + [None]*20
    
    for i in range(20):
        inv['storage'].append(button([600 + 70*(i%10), 660+70*(i/10), 70, 70], s[i], 'storage'))
    
    resize_grid(0,0)

def resize_grid(x, y):
    global grid_s
    for o in range(9):
        for yy in range(grid_s[1]):
            for i in range(x):
                inv['grid'+str(o)].insert(int((grid_s[0]+x)*(yy+1)+i-x), button([620 + 60*(grid_s[0]+i)
                                                  ,120+60*yy, 60, 60], None, 'grid'+str(o), switch))
        for xx in range(y):
            for i in range(grid_s[0]+x):
                inv['grid'+str(o)].append(button([620 + 60*i, 120+60*(grid_s[1]+xx), 60, 60], 
                            None, 'grid'+str(o), switch))
    grid_s[0] += x
    grid_s[1] += y
            
    

def switch_grid(m):
    global grid_page
    grid_page=m

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
    
    for x in [v for k in inv if 'grid' not in k for v in inv[k]]+inv['grid'+str(grid_page)]:
        x.render()
    if m[0] is not None:
        m[0].render(mouseX-m[1], mouseY-m[2])

def menu1_mousePressed():
    global m
    for x in [v for k in inv if 'grid' not in k for v in inv[k]]+inv['grid'+str(grid_page)]:
        if x.click() and x.c != None:
            m = [x, mouseX-x.dim[0], mouseY-x.dim[1]]
            break

def menu1_mouseReleased():
    global m
    if m[0] is not None:
        for x in [v for k in inv if 'grid' not in k for v in inv[k]]+inv['grid'+str(grid_page)]:
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
        
menus = {0:menu0, 1:menu1}

def s_menu(m):
    if g.menu == 1:
        del orbit[:]
        parse(inv['grid0'], grid_s, ob1, orbit)
    if m == 1:
        pass
        
    g.menu=m
    
def switch(a,b):
    c = b.c
    b.c = a.c
    a.c = c
    if type(a.c)==mod:
        a.c.pos(a)
    if type(b.c)==mod:
        b.c.pos(b)
