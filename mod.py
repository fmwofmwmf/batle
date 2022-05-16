from thingys import *

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

class modifier(object):
    def __init__(self, att={'range':1, 'shape':'ROW', 'effect':b_damage, 'g':None, 'order':1}):
        self.att = att
        self.att['g'] = self.graphic
    
    def targets(self, li, sz, pos):
        if self.att['shape'] == 'ROW':
            return li[pos-min(pos%sz[0],self.att['range']):pos+min(sz[0]-(pos%sz[0])-1,self.att['range'])+1]
        elif self.att['shape'] == 'COL':
            return [li[pos%sz[0]+i*sz[0]] for i in range(max(pos//sz[0]-2, 0), min(sz[1], pos//sz[0]+3))]

    def graphic(self):
        strength = {1:[0,155,0], 2:[255,165,0], 3:[0,0,255], 4:[255,0,0], 5:[0]}
        stroke(*strength[self.att['range']])
        strokeWeight(3)
        if self.att['shape'] == 'ROW':
            line(25,0,-25,0)
        elif self.att['shape'] == 'COL':
            line(0,-25,0,25)
        circle(0,0,30)
        strokeWeight(2)
        if self.att['effect'] == b_damage:
            line(0,-5,-5,3)
            line(0,-5,5,3)
        elif self.att['effect'] == health:
            quad(-0.5,8,0,-3,-5,-8,-10,-2)
            quad(0.5,8,0,-3,5,-8,10,-2)
        elif self.att['effect'] == defense:
            quad(-0.5,10,0,-7,-7,-7,-7,5)
            quad(0.5,10,0,-7,7,-7,7,5)
        elif self.att['effect'] == c_damage:
            quad(-10,0,0,-10,10,0,0,10)
        strokeWeight(1)
        fill(255)
        stroke(0)

def coll_rect(a, b):
    laser = PVector(1,0)
    laser.rotate(a.dim[2])
    laser.normalize()
    laser.mult(a.dim[1])
    angle = laser.heading()
    target_rotated = a.pos.copy().sub(b.pos).rotate(-angle).mult(-1)
    # line(b.pos.x, b.pos.y, a.pos.x, a.pos.y)
    return target_rotated.y > -(b.hitbox+a.dim[0]) and target_rotated.y < b.hitbox+a.dim[0] \
    and target_rotated.x > 0 and target_rotated.x < laser.mag()

def laser_ren(ob, s):
    ob.att['age']['a']+=1
    if ob.att['age']['a'] >= ob.att['age']['max']:
        s.remove(ob)
    pushMatrix()
    translate(ob.pos.x, ob.pos.y)
    rotate(ob.dim[2]-HALF_PI)
    sharp = 5.0
    wid = ceil(sqrt(ob.dim[0]/2))
    grad1 = exp(-(sharp/ob.att['age']['max']*2*ob.att['age']['a']-sharp)**2)
    ob.att['dmg']['contact']=grad1*ob.att['dmg']['max']
    
    if ob.att['age']['a']<ob.att['age']['max']/2:
        stroke(color(150, 150, 255))
        line(0, 0, ob.dim[0]/2, ob.dim[1])
    for x in range(ob.dim[0]/wid):
        grad0 = -abs(x-ob.dim[0]/(wid*2))/float(ob.dim[0]/(wid*2))+1
        c = lerpColor(color(255, 255, 255, 0), color(150, 150, 255), grad1*grad0)
        stroke(c)
        strokeWeight(wid)
        line(-ob.dim[0]/2+wid*x, 0, wid*x, ob.dim[1])
        strokeWeight(1)
    stroke(0)
    popMatrix()
