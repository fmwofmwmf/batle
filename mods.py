from funs import *

def c_damage(ob):
    ob.att['dmg']['contact'] = ob.att['dmg'].get('contact', 0) * 2 + 1000  

def b_damage(ob):
    ob.att['dmg']['bd'] = ob.att['dmg'].get('bd', 1) * 2   
    print(ob.att['dmg']['bd'])
    
def health(ob):
    ob.att['h']['MH'] = ob.att['h'].get('MH', 0)*1.5 + 1000
    ob.att['h']['R'] = ob.att['h'].get('R', 0) - 5
    ob.att['h']['H'] = ob.att['h'].get('H', 0) + 1000
    print ob.att['h']['MH']
    
def defense(ob):
    ob.att['h']['DR%'] = ob.att['h'].get('DR%', 0)+1
    print ob.att['h']['DR%']

class mod(object):
    def __init__(self, name, d, li, scal, pos, content=None):
        for i in range(2):
            d[i] = d[i].replace('#', '^v<>')
        self.att = {'name':name, 'in':d[0], 'out':d[1], 'pos':pos, 'eval':eval(name), 'g': self.display, 'c':content}
        if pos[2] != -1:
            li['grid'+str(pos[2])][pos[0]+pos[1]*scal[0]].c = self

    def evaluate(self, banned=[]):
        return self.att['eval'](self, banned)
    
    def pos(self, sup):
        self.att['pos'][0] = (sup.dim[0]-620)/60
        self.att['pos'][1] = (sup.dim[1]-120)/60
        self.att['li'] = sup.id[4:]
    
    def display(self):
        r = {'>': 0, '<': PI, '^': -PI/2, 'v': PI/2}
        n = {'s':'o', 'l':'', 'n':'+'}
        fill(0)
        text(n[self.att['name']], -4, 5)
        fill(100,255,100)
        for p in self.att['in']:
            rotate(r[p])
            triangle(8,0,18,10,18,-10)
            rotate(-r[p])
        fill(255,100,100)
        for p in self.att['out']:
            rotate(r[p])
            triangle(30,0,20,10,20,-10)
            rotate(-r[p])
        fill(255)
            
    def direction(self, li, port):
        d = {'>': [1, 0], '<': [-1, 0], '^': [0, -1], 'v': [0, 1]}
        q = []
        for x in self.att[port]:
            q.append([d[x][i] + li[i] for i in range(2)])
        return q

dim = [9, 10]
ev = {}

def parse(grid, dim, ob, li):
    global ev
    ev = {}
    s=[]
    for i, x in enumerate(grid):
        if x.c is not None:
            ev[c([i%dim[0], i//dim[0]])] = x
            #print i, c([i%dim[0], i//dim[0]]), x.c.att['name']
            if x.c.att['name'] == 's':
                s.append(x)
    
    out = {}
    print 'ev', ev
    for x in s:
        ret = x.c.evaluate()
        for y in ret:
                out[y] = out.get(y, 0) + ret[y]
    
    mods = {}
    print out
    o = ob(inter.pos.x, inter.pos.y)
    for x in out:
        for y in range(out[x]):
            if x != 'count':
                o.mods.append(mods[x]())
    for _ in range(min(out.get('count', 0), 50)):
        li.append(cot.deepcopy(o))


c = lambda l: str(l[0]) + ' ' + str(l[1])


def n(o, banned):
    li = [ev.get(c(x), 'n') for x in o.direction(o.att['pos'], 'in')]
    q = {'count': 1}
    for x in [a for a in li if a != 'n' and (a not in banned)]:
        if o.att['pos'][:2] in x.c.direction(x.c.att['pos'], 'out'):
            ret = x.c.evaluate(banned + [o])
            for y in ret:
                q[y] = q.get(y, 0) + ret[y]
    return q


def l(o, banned):
    li = [ev.get(c(x), 'n') for x in o.direction(o.att['pos'], 'in')]
    q = {}
    for x in [a for a in li if a != 'n' and (a.c not in banned)]:
        if o.att['pos'][:2] in x.c.direction(x.c.att['pos'], 'out'):
            ret = x.c.evaluate(banned + [o])
            
            for y in ret:
                q[y] = q.get(y, 0) + ret[y]
    return q


def s(o, _):
    li = [ev.get(c(x), 'n') for x in o.direction(o.att['pos'], 'in')]
    print 'li', o.direction(o.att['pos'], 'in')
    q = {}
    for x in [a for a in li if a != 'n']:
        print o.att['pos'][:2], x.c.direction(x.c.att['pos'], 'out')
        if o.att['pos'][:2] in x.c.direction(x.c.att['pos'], 'out'):
            ret = x.c.evaluate([])
            for y in ret:
                q[y] = q.get(y, 0) + ret[y]
    return q
