from loop import *
import time
# img > obj > setting > funs > mods > menus > ctrl > loop > batlee

def setup():
    frameRate(200)
    size(1600,900)
    inter.weapons['CENTER']=[proj, [lambda x,y,v: Shoot(15, x, y, v, s=20, 
                        att={'age':{'max':300, 'a':1}, 'dmg':{'P':100, 'contact':200}, 'g':w1, 'bhv':{}}), 0, 60]]
    inter.weapons['RIGHT']=[drone0, [lambda x,y,v: NotCircle(0, x, y, s=20, 
                        att={'age':{'max':60, 'a':1},'h':{'H':1000000, 'MH':1000000}, 'dmg':{'P':100, 'contact':0, 'max':240}, 'g':w1, 'bhv':{}},
                         dim=[50,1850,inter.rot], coll=coll_rect, ren=laser_ren, stor=drone0, funs=[laser_track]), 0, 30]]
    orbit.append(ob0(0,0))
    menu1_setup()
    global b
    b = thread(main_thread)

def draw():
    global t1
    lag_rep['fps'].pop(0)
    lag_rep['bullets'] = len(proj)
    lag_rep['fps'].append(millis() - t1)

    t1 = millis()
    mouse.pos.x=mouseX +inter.pos.x-800
    mouse.pos.y=mouseY +inter.pos.y-450
    #print ctrl.menu
    
    if g.menu == 0:
        run = True
        background(255)
        grid()
        pushMatrix()
        translate(-inter.pos.x+800, -inter.pos.y+450) # TORUS
        circle(mouse.pos.x, mouse.pos.y, 5)
        lag_rep['l'][1]=millis() - t1
        render()
        lag_rep['l'][2]=millis() - t1
        
        lag_rep['l'][3]=millis() - t1
        proj_loop()
        lag_rep['l'][4]=millis() - t1
        inputs()
        popMatrix()
    else:
        run = False
        lag_rep['l'][1]=0
        lag_rep['l'][2]=0
        lag_rep['l'][3]=0
        lag_rep['l'][4]=millis() - t1
    menus[g.menu]()
    
    try:
        lagg()
    except:
        pass

run = True
no_exit = True

def main_thread():
    while no_exit:
        if run:
            global t11
            lag_rep['ifps'].pop(0)
            lag_rep['ifps'].append(millis() - t11)
            lag_rep['l'][0] = millis() - t11 - lag_rep['l'][4]
            
            t11=millis()
            
            ob_loop()
            lag_rep['l'][1]=millis() - t11
            
            inter_loop()
            lag_rep['l'][2]=millis() - t11
            
            e_loop()
            lag_rep['l'][3]=millis() - t11
            
            for x in proj + e_proj:
                x.move()
            lag_rep['l'][4]=millis() - t11
        
        #print lag_rep['ifps'][len(lag_rep['ifps'])-1]/1000.0
        time.sleep(min(lag_rep['ifps'][len(lag_rep['ifps'])-1]/1000.0, 1/60.0))
    print 'closed!!'

def grid():
    for x in range(5):
        line(400*x-inter.pos.x%400, 0, 400*x-inter.pos.x%400, 900)
        line(0, 400*x-inter.pos.y%400, 1600, 400*x-inter.pos.y%400)
        
mouse_button_to_string = {LEFT:'LEFT', CENTER:'CENTER', RIGHT:'RIGHT'}

def mousePressed():
    input[mouse_button_to_string[mouseButton]] = True
    
    if g.menu==1:
        menu1_mousePressed()
        
def mouseReleased():
    input[mouse_button_to_string[mouseButton]] = False
    if mouse_button_to_string[mouseButton] in inter.weapons:
        inter.shoot(mouse_button_to_string[mouseButton])
    
    if g.menu == 1:
        menu1_mouseReleased()
        
        
def keyPressed():
    if key in input:
        input[key] = True
    elif key in cool_input[g.menu]:
        #try:
            cool_input[g.menu][key]()
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
    if key == 'p':
        global no_exit
        no_exit = False
        exit()

def inputs():
    if input['w']:
        a = 0.05
        if input['a'] and input['d']:
            a*=3
        if input[' ']:
            a*=3
        
        inter.v.add(PVector(cos(inter.rot)*a, sin(inter.rot)*a))
    if input['s']:
        inter.v.sub(PVector(cos(inter.rot)*0.1, sin(inter.rot)*0.1))
    if input['a']:
        inter.rot-=0.015
        if input[' ']:
            inter.rot-=0.015
            inter.v.add(PVector(cos(inter.rot-HALF_PI)*0.1, sin(inter.rot-HALF_PI)*0.1))
    if input['d']:
        inter.rot+=0.015
        if input[' ']:
            inter.rot+=0.015
            inter.v.add(PVector(cos(inter.rot+HALF_PI)*0.1, sin(inter.rot+HALF_PI)*0.1))
    if input['LEFT']:
        for o in [x for x in orbit if x.state]:
            o.shoot(proj, PVector(mouse.pos.x-o.pos.x, mouse.pos.y-o.pos.y))
