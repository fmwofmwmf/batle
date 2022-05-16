from ctrl import *
spawn = True
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
    
    for x in range(len(enemy)):
        enemy[x].walk([[inter.pos.x, inter.pos.y]])
        if enemy[x].att['id'] in e_shoot:
            enemy[x].shoot(e_proj, PVector(inter.pos.x-enemy[x].pos.x, inter.pos.y-enemy[x].pos.y))
        enemy[x].render(inter)

d_c = 0
def inter_loop():
    m = 60
    global d_c
    for t in collide([inter], enemy, 40):
        #print(t[0].health)
        try:
            if t[0].hmod(t[1].att['dmg']['contact']) is not None:
                print('losed')
            if t[1].hmod(t[0].att['dmg']['contact']) is not None:
                enemy.pop(enemy.index(t[1]))
        except:
            pass
    
    inter.render(input)
    rect(inter.pos.x-20,inter.pos.y+15,40,5)
    fill(255,0,0)
    rect(inter.pos.x-20,inter.pos.y+15,map(inter.att['h']['H'], 0, inter.att['h']['MH'], 0, 40),5)
    fill(255)
    # print([type(x) for x in orbit])
    if True in [not x.state for x in orbit]:
        rect(inter.pos.x-20,inter.pos.y-20,40,5)
        fill(0)
        rect(inter.pos.x-20,inter.pos.y-20,map(d_c, 0, m, 0, 40),5)
        fill(255)
        d_c += 1
        if d_c >= m:
            a = orbit[orbit.index([x for x in orbit if not x.state][0])]
            a.state = True
            a.pos = inter.pos.copy()
            a.att['h']['H'] = a.att['h']['MH']
            d_c = 0
            
    for t in collide(drone0, enemy, 20000):
        # print(t[0].health)
        try:
            if t[0].hmod(t[1].att['dmg']['contact']) is not None:
                drone0.pop(drone0.index(t[0]))
            if t[1].hmod(t[0].att['dmg']['contact']) is not None:
                enemy.pop(enemy.index(t[1]))
        except:
            pass
    
    
    for x in drone0:
        x.render()

rotation = 0
def ob_loop():
    global rotation
    c=millis()
    for t in collide(orbit, enemy, 40):
        # print(t[0].health)
        try:
            if t[0].hmod(t[1].att['dmg']['contact']) is not None:
                t[0].state=False
            if t[1].hmod(t[0].att['dmg']['contact']) is not None:
                enemy.pop(enemy.index(t[1]))
        except:
            pass

    
    orbit_types = {}
    for x in orbit:
        ad(orbit_types, (x if type(x) == str else x.att['id']), [x])

    m = 10
    pushMatrix()
    for y, x in enumerate(sorted([x for x in orbit_types], key = lambda x: len(orbit_types[x]))):
        s = len(orbit_types[x])
        # print s, max(y*20, s*PI), inter.pos.x, inter.pos.y, (rotation%360)
        p = cirl(s, max(m+20, s*PI), inter.pos.x, inter.pos.y, (rotation/sqrt(max(m+20, s*PI)/10))%360)
        m = max(m+20, s*PI)
        
        for i in range(s):
            circle(p[i][0]%width, p[i][1]%height, 5)
            if orbit_types[x][i].state:
                orbit_types[x][i].walk([[p[i][0]%width, p[i][1]%height]])
                orbit_types[x][i].render(mouse)
    popMatrix()
        
    rotation += 2 + input[' ']*4
    
    
        

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
                    print('losed')
            
        except:
            pass
    for x in proj+e_proj:
        if x in e_proj:
            x.render([255,0,0])
        else:
            x.render()
        d = x.collision()
        if d is not None:
            decay.append(d)
    for x in decay:
        try:
            proj.pop(proj.index(x))
            
        except:
            try:
                e_proj.pop(e_proj.index(x))
            except:
                pass
