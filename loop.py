from ctrl import *

spawn = True
rotation = 0
d_c = 0
def render():
    global d_c, rotation
    m = 1
    c = millis()
    for x in range(len(enemy)):
        try:
            enemy[x].render(inter)
        except:
            pass
    
    inter.render(input)
    rect(inter.pos.x-20,inter.pos.y+15,40,5)
    fill(255,0,0)
    rect(inter.pos.x-20,inter.pos.y+15,map(max(inter.att['h']['H'],0), 0, inter.att['h']['MH'], 0, 40),5)
    fill(255)
    
    if True in [not x.state for x in orbit]:
        rect(inter.pos.x-20,inter.pos.y-20,40,5)
        fill(0)
        rect(inter.pos.x-20, inter.pos.y-20, map(d_c, 0, m, 0, 40),5)
        fill(255)
        d_c += 1
        if d_c >= m:
            a = orbit[orbit.index([x for x in orbit if not x.state][0])]
            a.state = True
            a.pos = inter.pos.copy()
            a.att['h']['H'] = a.att['h']['MH']
            d_c = 0
    
    for x in drone0:
        x.render()
    pushMatrix()
    for x in orbit:
        if x.state:
            x.render(mouse)
    popMatrix()
    
    

    rotation += 2 + input[' ']*4
    
    for x in proj:
        x.render()
    for x in e_proj:
        x.render([255,0,0])

def e_loop():
    global w
    if spawn:
        if (len(enemy)<waves[w][0][0] and waves[w][0][1] > 1):
            waves[w][0][1] -= 1
            for e in waves[w][1]:
                for i in range(e[1]):
                    enemy.append(e[0](int(random(2))*1600+inter.pos.x-800, random(900)+inter.pos.y-450))
            
        elif enemy==[]:
            waves[w][0][1] -= 1
            w+=1
            for e in waves[w][1]:
                #print(e)
                for i in range(e[1]):
                    enemy.append(e[0](int(random(2))*1600, random(900)))
    grid_enemy = {}
    en_to_grid = {}
    p = 30
    for x in enemy:
        R = (x.pos.x + x.hitbox) // p
        L = (x.pos.x - x.hitbox) // p
        D = (x.pos.y + x.hitbox) // p
        U = (x.pos.y - x.hitbox) // p
        for i in range(int(L), int(R+1)):
            for o in range(int(U), int(D+1)):
                grid_enemy = ad(grid_enemy, str(i)+' '+str(o), [x])
                en_to_grid[x] = en_to_grid.get(x, []) + [str(i)+' '+str(o)]
    
    for x in en_to_grid:
        others = []
        for y in en_to_grid[x]:
            others += grid_enemy[y]
        others = list(set(others))
        others.remove(x)
        if others is None:
            others = []
        x.walk([[inter.pos.x, inter.pos.y]]+[[u.pos.x, u.pos.y] for u in others], 
               [lambda v:v]+[lambda v:v.setMag(-sqrt(v.mag())*10)]*len(others))
        
        if x.att['id'] in e_shoot:
            x.shoot(e_proj, PVector(inter.pos.x-x.pos.x, inter.pos.y-x.pos.y))
        x.move(0.70, factor=lambda e: sqrt(dist(inter.pos.x, inter.pos.y, e.pos.x, e.pos.y))
                    if dist(inter.pos.x, inter.pos.y, e.pos.x,e.pos.y) > 1000 else 1, max_=True)
'''
    for x in range(len(enemy)):
        #try:        
            enemy[x].walk([[inter.pos.x, inter.pos.y]])
            if enemy[x].att['id'] in e_shoot:
                enemy[x].shoot(e_proj, PVector(inter.pos.x-enemy[x].pos.x, inter.pos.y-enemy[x].pos.y))
            enemy[x].move(0.70, factor=lambda e: sqrt(dist(inter.pos.x, inter.pos.y, e.pos.x,e.pos.y))
                           if dist(inter.pos.x, inter.pos.y, e.pos.x,e.pos.y) > 1000 else 1, max_=True)
            #print enemy[x].pos.copy().sub(inter.pos)
        #except:
                #pass    
'''
def inter_loop():
    inter.move(0.97)
    for t in collide([inter], enemy, 40):
        #print(t[0].health)
        try:
            if t[0].hmod(t[1].att['dmg']['contact']) is not None:
                print t[0].att['h']['H']
            if t[1].hmod(t[0].att['dmg']['contact']) is not None:
                enemy.pop(enemy.index(t[1]))
        except:
            pass

    for t in collide(drone0, enemy, 20000):
        # print(t[0].health)
        try:
            if t[0].hmod(t[1].att['dmg']['contact']) is not None:
                drone0.pop(drone0.index(t[0]))
            if t[1].hmod(t[0].att['dmg']['contact']) is not None:
                enemy.pop(enemy.index(t[1]))
        except:
            pass

def ob_loop():
    for t in collide(orbit, enemy, 40):
        # print(t[0].health)
        try:
            if t[0].hmod(t[1].att['dmg']['contact']) is not None:
                t[0].state=False
            if t[1].hmod(t[0].att['dmg']['contact']) is not None:
                enemy.pop(enemy.index(t[1]))
        except:
            pass
    
    for x in orbit:
        x.move(0.70)
    
    orbit_types = {}
    for x in orbit:
        ad(orbit_types, (x if type(x) == str else x.att['id']), [x])

    m = 10
    for y, x in enumerate(sorted([x for x in orbit_types], key = lambda x: len(orbit_types[x]))):
        s = len(orbit_types[x])
        p = cirl(s, max(m+20, s*PI), inter.pos.x, inter.pos.y, (rotation/sqrt(max(m+20, s*PI)/10))%360)
        m = max(m+20, s*PI)
        
        for i in range(s):
            # orbit_types[x][i].walk([[p[i][0]%width, p[i][1]%height]]) # TORUS
            orbit_types[x][i].walk([[p[i][0], p[i][1]]]) # NORMAL

def proj_loop():
    decay = []
    for t in collide(proj, enemy, 50):
        t[0].att['dmg']['P']-=1
        if t[0].att['dmg']['P'] <= 0:
            decay.append(t[0])
        try:
            if t[1].hmod(t[0].att['dmg']['contact']) is not None:
                enemy.pop(enemy.index(t[1]))
        except:
            pass
    for t in collide(orbit, e_proj, 40)+collide([inter], e_proj, 40):
        print(t)
        t[1].att['dmg']['P']-=1
        if t[1].att['dmg']['P'] <= 0:
            decay.append(t[1])
        try:
            if t[0].hmod(t[1].att['dmg']['contact']) is not None:
                if t[0] in orbit:
                    t[0].state=False
                elif t[0] in drone0:
                    drone0.pop(drone0.index(t[1]))
                else:
                    print t[0].att['h']['H']
        except:
            pass
    for x in proj+e_proj:
        if x.collision() is not None:
            decay.append(x)
    for x in decay:
        try:
            proj.pop(proj.index(x))
            
        except:
            try:
                e_proj.pop(e_proj.index(x))
            except:
                pass
