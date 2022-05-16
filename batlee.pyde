from loop import *
import time
# img > obj > setting > funs > mods > menus > ctrl > loop > batlee

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
    thread(main_thread)
    if menu == 0:
        run = True
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
        run = False
        lag_rep['l'][1]=0
        lag_rep['l'][2]=0
        lag_rep['l'][3]=0
        lag_rep['l'][4]=millis() - t1
    menus[menu]()
    lag_rep['l'][5]=millis() - t1
    lagg()


run = True
def main_thread():
    while True:
        if run:
            for x in orbit:
                x.move(0.70)
            inter.move(0.97)
            for x in enemy:
                x.move(0.70)
            for x in proj + e_proj:
                x.move()
            time.sleep(16)

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
