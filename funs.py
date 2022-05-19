from setting import *

def prog_bar(x, y, w, h, p, pmax):
    rect(x, y, w, h)
    fill(0)
    rect(x, y, map(p, 0, pmax, 0, w), h)
    fill(255)

def prog_box(x, y, l, e, s, w, h, c=color(255, 0, 0, 200)):
    for i in range(floor(s/float(l)), ceil(e/float(l))):
        rect(x, y+h*i, w*(e%l if (i+1)*l > e else l), h)

    for i in range(ceil(s/float(l))):
        fill(c)
        rect(x, y+h*i, w*(s%l if (i+1)*l > s else l), h)
    
    for i in range(min(e, l)):
        line(x+w*i, y, x+w*i, y+(e/l+(e%l>i))*h)
    fill(255)
    
def drones(a):
    if a:
        orbit.append(eval('ob'+str(g.selected)+'(inter.pos.x, inter.pos.y)'))
    else:
        for x in orbit:
            try:
                if x == 'ob'+str(selected) or x.att['id'] == 'ob'+str(selected):
                    orbit.remove(x)
                    break
            except:
                pass
                
def select(s):
    g.selected = s

def ad(di, keyy, ele):
    if keyy in di:
        di[keyy] += ele
    else:
        di[keyy] = ele
    return di

cirl = lambda c, d, x, y, r: [[sin(radians(360.0/c * i + r))*d + x, \
                               cos(radians(360.0/c * i + r))*d + y] for i in range(c)]

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

def collide(a, b, p):
    col = {}
    ov = []
    # print(len(a+b), 'comp(1)')
    for x in a+b:
        if x is not None and x.state:
            R = (x.pos.x + x.hitbox) // p
            L = (x.pos.x - x.hitbox) // p
            D = (x.pos.y + x.hitbox) // p
            U = (x.pos.y - x.hitbox) // p
            for i in range(int(L), int(R+1)):
                for o in range(int(U), int(D+1)):
                    col = ad(col, str(i)+' '+str(o), [x])
    
    for x in col:
        if len(col[x])>1:
            si = set(col[x]) & set(a)
            if si != {}:
                for i in si:
                    so = set(col[x]) & set(b)
                    if so != {}:
                        for o in so:
                            try:
                                if i.collh(o):
                                    ov.append((i, o))
                            except:
                                if dist(i.pos.x, i.pos.y, o.pos.x, o.pos.y) <= i.hitbox + o.hitbox:
                                    ov.append((i, o))
                    else:
                        break
    return ov

t1 = 0
t11 = 0
lag_q = [False]*10
lag_rep = {'bullets':0, 'l': [0,0,0,0,0,0], 'fps':[17]*300, 'ifps':[17]*300}

def lagg():
    fill(255,100)
    rect(0,600,300,340)
    rect(30,630,240,90)
    fill(255,0,0)
    stroke(255,0,0)
    text(200, 5, 640)
    text(60, 10, 700)
    for x in range(1,10):
        s = 1000/(sum(lag_rep['fps'][30*x:30*(x+1)])/30)
        s0 = 1000/(sum(lag_rep['fps'][30*(x-1):30*(x)])/30)
        line(7+26*x, 720+map(s0, 0, 220, 0, -90), 33+26*x, 720+map(s, 0, 220, 0, -90))
    line(33, 720+map(60, 0, 220, 0, -90), 267, 720+map(60, 0, 220, 0, -90))
    fill(0,0,255)
    stroke(0,0,255)
    text(70, 275, 640)
    sample = 20
    for x in range(1,sample):
        s = 1000/(sum(lag_rep['ifps'][(300/sample)*x:(300/sample)*(x+1)])/(300/sample))
        s0 = 1000/(sum(lag_rep['ifps'][(300/sample)*(x-1):(300/sample)*(x)])/(300/sample))
        line(7+(260/sample)*x, 720+map(s0, 0, 70, 0, -90), 7+(260/sample)*(x+1), 720+map(s, 0, 70, 0, -90))
    stroke(0)
    fill(0)
    text ('[fps] {}'.format(1000/(sum(lag_rep['fps'][240:])/60)), 50, 620)
    text ('[ifps] {}'.format(1000/(sum(lag_rep['ifps'][240:])/60)), 110, 620)
    text ('[bullets] {}'.format(lag_rep['bullets']), 170, 620)
    text ('[SLEEP] {}'.format(lag_rep['l'][0]), 20, 740)
    text ('[DRONE] {}'.format(lag_rep['l'][1]), 100, 740)
    text ('[MAIN] {}'.format(lag_rep['l'][2] - lag_rep['l'][1]), 20, 760)
    text ('[ENEMY] {}'.format(lag_rep['l'][3] - lag_rep['l'][2]), 100, 760)
    text ('[PROJ] {}'.format(lag_rep['l'][4] - lag_rep['l'][3]), 20, 780)
    fill(255)
    
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
