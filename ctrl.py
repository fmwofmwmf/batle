from menus import *

menu = 0
menus = {0:menu0, 1:menu1}

input = {'w':False,'a':False,'s':False,'d':False, ' ':False,
          'LEFT':False, 'MIDDLE':False, 'RIGHT':False}
cool_input = {0: {
                  '1': lambda x=1: select(x), '2': lambda x=2: select(x), '3': lambda x=3: select(x),
                  '4': lambda x=4: select(x), '5': lambda x=5: select(x), '6': lambda x=6: select(x),
                  '7': lambda x=7: select(x), '8': lambda x=8: select(x), '9': lambda x=9: select(x),
                   'i':lambda: drones(True), 'o':lambda: drones(False), 'q':lambda m=1: s_menu(m)},
                1:{'q':lambda m=0: s_menu(m)}
              }

