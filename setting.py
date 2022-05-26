from obj import *

inter = Main(8, 800, 450, s=20, att = {
                                    'dmg':{'contact':10, 'w1':100},
                                    'h':{'H':4500, 'MH':5000, 'R':-10, 'S':'BAR'}})

ob0 = lambda x,y: Ob(11, x, y, s=10, att={'h':{'H':200, 'MH':200, 'S':'TRANS'}, 'dmg':{'contact':10, 'b':
                                    lambda x,y,v,a=1: Shoot(20, x, y, v, att = {
                                    'dmg':{'P':20, 'contact':10000},
                                    'age':{'max':300, 'a':1},
                                    'g':None, 'id':'', 
                                    'bhv':{}}),
                                    'c':0, 'CD':10}, 'g':o0, 'id':'ob0'})
ob1 = lambda x,y: Ob(11, x, y, s=10, att={'h':{'H':200, 'MH':200, 'S':'TRANS'}, 'dmg':{'contact':10, 'b':
                                    lambda x,y,v,a=1: Shoot(7, x, y, v, att = {
                                    'dmg':{'P':1, 'contact':50*a},
                                    'age':{'max':90, 'a':1},
                                    'g':None, 'id':'', 
                                    'bhv':{}}),
                                    'c':0, 'CD':30}, 'g':o1, 'id':'ob1'})
ob2 = lambda x,y: Ob(11, x, y, s=10, att={'h':{'H':200, 'MH':200, 'S':'TRANS'}, 'dmg':{'contact':10, 'b':
                                    lambda x,y,v,a=1: Shoot(20, x, y, v, att = {
                                    'dmg':{'P':5, 'contact':35},
                                    'age':{'max':60, 'a':1},
                                    'g':None, 'id':'', 
                                    'bhv':{'vel': lambda t, v: v.copy().normalize().mult(t),
                                       'dmg': lambda t, v: v.mag()*15*a}}), 'c':0, 'CD':60}, 'g':o2, 'id':'ob2'})
ob3 = lambda x,y: Ob(11, x, y, s=10, att={'h':{'H':200, 'MH':200, 'S':'TRANS'}, 'dmg':{'contact':10, 'b':
                                    lambda x,y,v,a=1: Shoot(0.2, x, y, v, s=7, att = {
                                    'dmg':{'P':60, 'contact':5},
                                    'age':{'max':300, 'a':1},
                                    'g':None, 'id':'', 
                                    'bhv':{'dmg': lambda t, v: min(30, t/2)*a}}),
                                    'c':0, 'CD':150}, 'g':o3, 'id':'ob3'})
ob4 = lambda x,y: Ob(11, x, y, s=10, att={'h':{'H':200, 'MH':200, 'S':'TRANS'}, 'dmg':{'contact':10, 'b':
                                    lambda x,y,v,a=1: Shoot(5, x, y, v, att = {
                                    'dmg':{'P':1, 'contact':150*a},
                                    'age':{'max':60, 'a':1},
                                    'g':None, 'id':'', 
                                    'bhv':{'fun': lambda o: 
                                           (o.shoot(proj, [o.v.copy().rotate(-PI/16), o.v.copy().rotate(PI/16),
                                                           o.v.copy().rotate(-PI/8), o.v.copy().rotate(PI/8)],
                                            {'age': {'max':60, 'a':1}, 'bhv':{}})
                                            if o.att['age']['a'] == 1 else False)}}),
                                    'c':0, 'CD':100}, 'g':o4, 'id':'ob4'})
ob5 = lambda x,y: Ob(11, x, y, s=10, att={'h':{'H':200, 'MH':200, 'S':'TRANS'}, 'dmg':{'contact':10, 'b':
                                    lambda x,y,v,a=1: Shoot(3, x, y, v, att = {
                                    'dmg':{'P':20, 'contact':0},
                                    'age':{'max':dist(mouse.pos.x, mouse.pos.y, x, y)/3, 'a':1},
                                    'g':None, 'id':'',
                                    'bhv':{'fun': lambda o: 
                                           (o.shoot(proj, [o.v.copy().rotate(x*PI/8) for x in range(16)],
                                            {'age': {'max':80, 'a':1}, 'dmg':{'P':2, 'contact':50*a}, 'bhv':{}})
                                            if o.att['age']['a'] == round(o.att['age']['max'])-1 else False
                                            )}}),
                                    'c':0, 'CD':300}, 'g':o5, 'id':'ob5'})
ob6 = lambda x,y: Ob(11, x, y, s=10, att={'h':{'H':200, 'MH':200, 'S':'TRANS'}, 'dmg':{'contact':10, 'b':
                                    lambda x,y,v,a=1: Shoot(4, x, y, v, s=2, att = {
                                    'dmg':{'P':1000, 'contact':10*a},
                                    'age':{'max':600, 'a':1},
                                    'g':None, 'id':'', 
                                    'bhv':{'fun': based}})
                                    ,'c':0, 'CD':60}, 'g':o1, 'id':'ob6'})
def based(ob):
    a = PVector(0,1).rotate(-atan2(mouse.pos.x-ob.pos.x, mouse.pos.y-ob.pos.y)+PI/(2**7))
    a.mult(map(dist(mouse.pos.x, mouse.pos.y, ob.pos.x, ob.pos.y), 0, 1600, 1, 0))
    ob.v.add(a)
    ob.v.limit(10)

ob7 = lambda x,y: Ob(9, x, y, s=10, att={'h':{'H':200, 'MH':200, 'S':'TRANS'}, 'dmg':{'contact':10, 'c':0, 'CD':50}, 'g':o1, 'id':'ob7'})
ob8 = lambda x,y: Ob(9, x, y, s=10, att={'h':{'H':200, 'MH':200, 'S':'TRANS'}, 'dmg':{'contact':10, 'c':0, 'CD':50}, 'g':o1, 'id':'ob8'})
ob9 = lambda x,y: Ob(9, x, y, s=10, att={'h':{'H':200, 'MH':200, 'S':'TRANS'}, 'dmg':{'contact':10, 'c':0, 'CD':50}, 'g':o1, 'id':'ob9'})

em0 = lambda x,y,h=1: Enemy(0, x, y, s=10, att={'h':{'H':100000*h, 'MH':100000*h, 'S':'BAR'},
                                                 'dmg':{'contact':0}, 'id':'e0', 'g':e4})
em1 = lambda x,y,h=1: Enemy(2, x, y, s=10, att={'h':{'H':10000*h, 'MH':10000*h, 'S':'BAR'},
                                                 'dmg':{'contact':10}, 'id':'e1', 'g':e1})
em2 = lambda x,y,h=1: Enemy(4, x, y, s=10, att={'h':{'H':4000*h, 'MH':4000*h, 'S':'BAR'},
                                                 'dmg':{'contact':50}, 'id':'e2', 'g':e2})
em3 = lambda x,y,h=1: Enemy(7, x, y, s=5, att={'h':{'H':1000*h, 'MH':1000*h, 'S':'BAR'},
                                                'dmg':{'contact':2000}, 'id':'e3', 'g':e3})
em4 = lambda x,y,h=1: Enemy(1, x, y, s=15, att={'h':{'H':50000*h, 'MH':50000*h, 'S':'BAR'},
                                                 'dmg':{'contact':100}, 'id':'e4', 'g':e4})
e_shoot='e5e6'
em5 = lambda x,y,h=1: Enemy(1, x, y, s=10, att={'h':{'H':1000*h, 'MH':1000*h, 'S':'BAR'}, 'dmg':{'contact':10, 'b':
                                    lambda x,y,v,a=1: Shoot(5, x, y, v, att = {
                                    'dmg':{'P':1, 'contact':200},
                                    'age':{'max':200, 'a':1},
                                    'g':None, 'id':'', 'bhv':{}}),
                                    'bd':1, 'c':0, 'CD':50}, 'id':'e5', 'g':e1})
em6 = lambda x,y,h=1: Enemy(0.1, x, y, s=10, att={'h':{'H':10000*h, 'MH':10000*h, 'S':'BAR'}, 'dmg':{'contact':10, 'b':
                                    lambda x,y,v,a=1: Shoot(1, x, y, v, s=10, att = {
                                    'dmg':{'P':15, 'contact':100},
                                    'age':{'max':1500, 'a':1},
                                    'g':None, 'id':'', 'bhv':{}}),
                                    'bd':1, 'c':0, 'CD':800}, 'id':'e6', 'g':e4})
em1b = lambda x,y,h=1: Enemy(0.02, x, y, s=150, att={'h':{'H':60000000*h, 'MH':60000000*h, 'R':-10, 'S':'BAR'}, 'dmg':{'contact':200, 'b':
                                    lambda x,y,v,a=1: Shoot(1, x, y, v, s=10, att = {
                                    'dmg':{'P':15, 'contact':100},
                                    'age':{'max':1500, 'a':1},
                                    'g':None, 'id':'', 'bhv':{}}),
                                    'bd':1, 'c':0, 'CD':800}, 'id':'e6', 'g':e1b})

w = 0

waves = {0:[[0, 0]],
         1:[[1, 1], [[em1b, 1]]],
         2:[[1, 1], [[em2, 5]]],
         3:[[5, 1], [[em3, 5]]],
         4:[[5, 1], [[em4, 5]]],
         5:[[5, 1], [[em5, 5]]],
         6:[[5, 1], [[em6, 5]]],
         7:[[5, 1], [[em1, 20],[em2, 20],[em3, 20],[em4, 20],[em5, 20],[em6, 20]]],
         8:[[5, 1], [[em1, 20]]],
         9:[[20, 1], [[em1, 20]]],}

mouse = thingy(0, 0, 0, 0)
