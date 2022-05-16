from img import *
import copy as cot

class thingy(object):
    def __init__(self, speed, x, y, s, att={'dmg':{}, 'id':''}):
        self.mods = []
        self.att = att
        self.b_att = att
        self.speed = speed
        self.pos = PVector(x, y)
        self.v = PVector(0, 0)
        self.hitbox = s
        self.state = True

class Ob(thingy):
    def __init__(self, speed, x, y, s=10, att={'h':{'H':200, 'MH':200}, 'dmg':{'contact':50}, 'g':None, 'id':''}):
        att['dmg'].setdefault('bd', 1)
        super(Ob, self).__init__(speed, x, y, s, att)

    def walk(self, targets, weights=None):
        x, y = 0, 0
        for u in targets:
                x+=u[0]
                y+=u[1]
        t = PVector(x/len(targets), y/len(targets))
        t.sub(self.pos)
        if abs(t.x)*2 > width:
            t.x=-t.x
        if abs(t.y)*2 > height:
            t.y=-t.y
        t.limit(self.speed)
        self.v.add(t)
    
    def hmod(self, d):
        if self.att['h']['H'] > self.att['h']['MH']:
            self.att['h']['H'] = self.att['h']['MH']
        if d<0:
            self.att['h']['H'] -= d
        else:
            self.att['h']['H'] -= max(d*(1-self.att['h'].get('DR%', 0))-self.att['h'].get('DRF',0), 0)
        
        if self.att['h']['H']<=0:
            return self
        return None
    
    def shoot(self, p, d):
        if self.att['dmg']['c']<=0 and 'b' in self.att['dmg']:
            p.append(self.att['dmg']['b'](self.pos.x, self.pos.y, d, self.att['dmg']['bd']))
            self.att['dmg']['c']=self.att['dmg']['CD']
            
    def move(self, ease=0):
        self.v.mult(ease)
        self.v.limit(self.speed)
        self.pos.add(self.v)
        self.pos = PVector(self.pos.x%width, self.pos.y%height)
        if 'c' in self.att['dmg'] and self.att['dmg']['c']>0:
            self.att['dmg']['c']-=1
        
        if 'R' in self.att['h']:
            self.hmod(self.att['h']['R'])
        
    def render(self, target=None):
        if self.att['g'] is not None:
            #pushMatrix()
            translate(self.pos.x, self.pos.y)
            
            if target is not None:
                r = -atan2(target.pos.x-self.pos.x, target.pos.y-self.pos.y)
                rotate(r)
            else:
                rotate(self.v.angle())
            if (self.att['h']['S']=='TRANS'):
                stroke(map(self.att['h']['H'], 0, self.att['h']['MH'], 255, 0), 0, 0)
            self.att['g']()
            stroke(0)
            
            rotate(-r)
            if (self.att['h']['S']=='BAR'):
                self.hbar()
            translate(-self.pos.x, -self.pos.y)
            #popMatrix()
        else:
            circle(self.pos.x, self.pos.y, 20)
    
    def delete(self):
        for x in [orbit, drone0, enemy]:
            if self in x:
                x.pop(x.index(self))
    
    def update(self):
        self.att = cot.deepcopy(self.b_att)
        for x in self.mods:
            x(self)
    
    def hbar(self):
        rect(-1.5*self.hitbox,5+self.hitbox,3*self.hitbox,5)
        fill(255,0,0)
        rect(-1.5*self.hitbox,5+self.hitbox,map(self.att['h']['H'], 0, self.att['h']['MH'], 0, 3*self.hitbox),5)
        fill(255)

class NotCircle(Ob):
    def __init__(self, speed, x, y, s=10, att={}, dim=None, coll=None, ren=None, stor=None, funs=[]):
        super(NotCircle, self).__init__(speed, x, y, s, att)
        self.coll=coll
        self.ren=ren
        self.dim=dim
        self.stor=stor
        self.funs=funs
    
    def collh(self, other):
        return self.coll(self, other)

    def render(self):
        self.ren(self, self.stor)
        for x in self.funs:
            x(self)
        

class Shoot(thingy):
    def __init__(self, speed, x, y, v, s=3, att={'dmg':{}, 'bhv':{}, 'age':{'max':0, 'a':1}, 'g':None, 'id':''}):
        super(Shoot, self).__init__(speed, x, y, s, att)
        self.v = v
        self.v.normalize()
        self.v.mult(speed)

    def collision(self):
        if self.att['age']['a']>=self.att['age']['max']:
            return self
        return None
    
    def shoot(self, p, d, att):
        for i in range(len(d)):
            o = cot.deepcopy(self)
            o.v = d[i]
            if type(att)==list:
                o.att.update(att[i])
            else:
                o.att.update(cot.deepcopy(att))
            #print o
            p.append(o)
    
    def beh(self):
        if 'vel' in self.att['bhv']:
            self.v=self.att['bhv']['vel'](self.att['age']['a'], self.v)
        if 'dmg' in self.att['bhv']:
            self.att['dmg']['contact']=self.att['bhv']['dmg'](self.att['age']['a'], self.v)
        if 'fun' in self.att['bhv']:
            self.att['bhv']['fun'](self)
    def move(self):
        if self.att['bhv'] != {}:
            self.beh()
        self.pos.add(self.v)
        self.att['age']['a']+=1
        
    def render(self, c=[0], trail=None):
        if self.att['g'] == None:
            noStroke()
            fill(*c)
            circle(self.pos.x, self.pos.y, self.hitbox*2)
            fill(255)
            stroke(0)
        else:
            pushMatrix()
            translate(self.pos.x, self.pos.y)
            rotate(-atan2(self.v.x, self.v.y))
            self.att['g']()
            popMatrix()
        

class Enemy(Ob):
    def __init__(self, speed, x, y, s=10, att={}):
        super(Enemy, self).__init__(speed, x, y, s, att)
    
    def collision(self):
        pass
    

class Main(Ob):
    def __init__(self, speed, x, y, s, att):
        self.rot = 0
        self.weapons = {}
        super(Main, self).__init__(speed, x, y, s, att)

    def move(self, ease):
        self.v.limit(self.speed)
        self.v.mult(ease)
        self.pos.add(self.v)
        self.pos = PVector(self.pos.x%width, self.pos.y%height)
        for x in self.weapons:
            if self.weapons[x] is not None:
                self.weapons[x][1][1]-=1
        
        if 'R' in self.att['h']:
            self.hmod(self.att['h']['R'])

    def render(self, inp):
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        rotate(self.rot-HALF_PI)
        triangle(0, 15, 10, -15, -10, -15)
        if inp['a']:
            if inp[' ']:
                triangle(0, -15, -11, -27, -8, -15)
            triangle(0, -15, -7, -20, -8, -15)
        if inp['d']:
            if inp[' ']:
                triangle(0, -15, 11, -27, 8, -15)
            triangle(0, -15, 7, -20, 8, -15)
        if inp['w']:
            if inp[' ']:
                triangle(0, -33, 7, -15, -7, -15)
            triangle(0, -23, 5, -15, -5, -15)
        stroke(0)
        popMatrix()

    def shoot(self, ke):
        #print 'pog'
        if self.weapons[ke][1] is not None and self.weapons[ke][1][1]<=0:
            self.weapons[ke][0].append(self.weapons[ke][1][0](self.pos.x, self.pos.y, PVector(cos(self.rot), sin(self.rot))))
            self.weapons[ke][1][1]=self.weapons[ke][1][2]
