from menus import *




input = {'w':False,'a':False,'s':False,'d':False, ' ':False, 'LEFT':False, 'MIDDLE':False, 'RIGHT':False}
cool_input = {0: {
                  '1': lambda x=1: select(x), '2': lambda x=2: select(x), '3': lambda x=3: select(x),
                  '4': lambda x=4: select(x), '5': lambda x=5: select(x), '6': lambda x=6: select(x),
                  '7': lambda x=7: select(x), '8': lambda x=8: select(x), '9': lambda x=9: select(x),
                   'i':lambda: drones(True), 'o':lambda: drones(False), 'q':lambda m=1: s_menu(m)},
                1:{'q':lambda m=0: s_menu(m)}
              }

def s_menu(m):
    global menu
    if menu == 1:
        eval_grid()
    if m == 1:
        del inv['store'][:]
        for i in range(9):
            inv['store'].append(button([600 + 70*(i%10), 580, 70, 70], eval('ob'+str(i+1)+'(inter.pos.x,inter.pos.y)'), 'store'))
    menu = m
w = 0

waves = {0:[[0, 0]],
         1:[[1, 1], [[em5, 5]]],
         2:[[1, 1], [[em2, 5]]],
         3:[[5, 1], [[em3, 5]]],
         4:[[5, 1], [[em4, 5]]],
         5:[[5, 1], [[em5, 5]]],
         6:[[5, 1], [[em6, 5]]],
         7:[[5, 1], [[em1, 20],[em2, 20],[em3, 20],[em4, 20],[em5, 20],[em6, 20]]],
         8:[[5, 1], [[em1, 20]]],
         9:[[20, 1], [[em1, 20]]],}

rotation = 0

menu = 0
menus = {0:menu0, 1:menu1}

def setup():
    frameRate(60)
    size(1600,900)
    inter.weapons['CENTER']=[proj, [lambda x,y,v: Shoot(15, x, y, v, s=20, 
                        att={'age':{'max':300, 'a':1}, 'dmg':{'P':100, 'contact':200}, 'g':w1, 'bhv':{}}), 0, 60]]
    inter.weapons['RIGHT']=[drone0, [lambda x,y,v: NotCircle(0, x, y, s=20, 
                        att={'age':{'max':60, 'a':1},'h':{'H':1000000, 'MH':1000000}, 'dmg':{'P':100, 'contact':0, 'max':120}, 'g':w1, 'bhv':{}},
                         dim=[50,600,inter.rot], coll=coll_rect, ren=laser_ren, stor=drone0), 0, 30]]
    menu1_setup()



t1 = 0
lag_q = [False]*10
lag_rep = {'bullets':0, 'l': [0,0,0,0,0,0], 'fps':[17]*300}
def draw():
    global t1
    lag_rep['fps'].pop(0)
    lag_rep['bullets'] = len(proj)
    lag_rep['fps'].append(millis() - t1)
    
    lag_rep['l'][0] = millis() - t1 - lag_rep['l'][5]
    t1 = millis()
    mouse.pos.x=mouseX#+inter.pos.x-800
    mouse.pos.y=mouseY#+inter.pos.y-450
    
    
    fill(0)
    text(w, 100, 100)
    text(waves[w][0][1], 100, 200)
    fill(255)
    
    if menu == 0:
        background(255)
        #grid()
        pushMatrix()
        #translate(-inter.pos.x+800, -inter.pos.y+450)
        circle(mouse.pos.x, mouse.pos.y, 5)
        lag_rep['l'][1]=millis() - t1
        e_loop()
        lag_rep['l'][2]=millis() - t1
        ob_loop()
        lag_rep['l'][3]=millis() - t1
        proj_loop()
        lag_rep['l'][4]=millis() - t1
        inter_loop()
        inputs()
        popMatrix()
    else:
        lag_rep['l'][1]=0
        lag_rep['l'][2]=0
        lag_rep['l'][3]=0
        lag_rep['l'][4]=millis() - t1
    menus[menu]()
    lag_rep['l'][5]=millis() - t1
    lagg()


def lagg():
    fill(255,100)
    rect(0,600,300,340)
    rect(20,630,260,90)
    for x in range(1,10):
        s = 1000/(sum(lag_rep['fps'][30*x:30*(x+1)])/30)
        s0 = 1000/(sum(lag_rep['fps'][30*(x-1):30*(x)])/30)
        line(7+26*x, 720+map(s0, 0, 70, 0, -90), 33+26*x, 720+map(s, 0, 70, 0, -90))
    fill(0)
    text ('[fps] {}'.format(1000/(sum(lag_rep['fps'][240:])/60)), 50, 620)
    text ('[bullets] {}'.format(lag_rep['bullets']), 150, 620)
    text ('[DRAW] {}'.format(lag_rep['l'][0]), 20, 740)
    text ('[GRID] {}'.format(lag_rep['l'][1]), 100, 740)
    text ('[ENEMY] {}'.format(lag_rep['l'][2] - lag_rep['l'][1]), 20, 760)
    text ('[DRONE] {}'.format(lag_rep['l'][3] - lag_rep['l'][2]), 100, 760)
    text ('[PROJ] {}'.format(lag_rep['l'][4] - lag_rep['l'][3]), 20, 780)
    text ('[MENU] {}'.format(lag_rep['l'][5] - lag_rep['l'][4]), 100, 780)
    fill(255)

def grid():
    for x in range(5):
        line(400*x-inter.pos.x%400, 0, 400*x-inter.pos.x%400, 900)
        line(0, 400*x-inter.pos.y%400, 1600, 400*x-inter.pos.y%400)

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
        enemy[x].render(0.70, inter)


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
    
    inter.render(0.97, input)
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
                orbit_types[x][i].render(0.70, mouse)
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
    it = 0
    for x in col:
        if len(col[x])>1:
            si = set(col[x]) & set(a)
            if si != {}:
                for i in si:
                    so = set(col[x]) & set(b)
                    if so != {}:
                        for o in so:
                            it +=1
                            try:
                                if i.collh(o):
                                    ov.append((i, o))
                            except:
                                if dist(i.pos.x, i.pos.y, o.pos.x, o.pos.y) <= i.hitbox + o.hitbox:
                                    ov.append((i, o))
                    else:
                        break
    return ov

        
cirl = lambda c, d, x, y, r: [[sin(radians(360.0/c * i + r))*d + x, \
                               cos(radians(360.0/c * i + r))*d + y] for i in range(c)]

mouse_button_to_string = {LEFT:'LEFT', CENTER:'CENTER', RIGHT:'RIGHT'}



def mousePressed():
    input[mouse_button_to_string[mouseButton]] = True
    
    if menu==1:
        menu1_mousePressed()
        
def mouseReleased():
    input[mouse_button_to_string[mouseButton]] = False
    if mouse_button_to_string[mouseButton] in inter.weapons:
        inter.shoot(mouse_button_to_string[mouseButton])
    
    if menu == 1:
        menu1_mouseReleased()
        
        
def keyPressed():
    if key in input:
        input[key] = True
    elif key in cool_input[menu]:
        #try:
            cool_input[menu][key]()
        #except:
            #pass
    if key == 'n':
        for x in orbit:
            x.mods.append(b_damage)
            x.update()


def keyReleased():
    if key in input:
        input[key] = False
    if key in inter.weapons:
        inter.shoot(key)

def inputs():
    if input['w']:
        a = 0.2
        if input['a'] and input['d']:
            a*=3
        if input[' ']:
            a*=3
        
        inter.v.add(PVector(cos(inter.rot)*a, sin(inter.rot)*a))
    if input['s']:
        inter.v.sub(PVector(cos(inter.rot)*0.1, sin(inter.rot)*0.1))
    if input['a']:
        inter.rot-=0.03
        if input[' ']:
            inter.rot-=0.03
            inter.v.add(PVector(cos(inter.rot-HALF_PI)*0.1, sin(inter.rot-HALF_PI)*0.1))
    if input['d']:
        inter.rot+=0.03
        if input[' ']:
            inter.rot+=0.03
            inter.v.add(PVector(cos(inter.rot+HALF_PI)*0.1, sin(inter.rot+HALF_PI)*0.1))
    if input['LEFT']:
        for o in [x for x in orbit if x.state]:
            o.shoot(proj, PVector(mouse.pos.x-o.pos.x, mouse.pos.y-o.pos.y))
