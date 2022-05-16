from menus import *
input = {'w':False,'a':False,'s':False,'d':False, ' ':False,
          'LEFT':False, 'MIDDLE':False, 'RIGHT':False}
cool_input = {0: {
                  '1': lambda x=1: select(x), '2': lambda x=2: select(x), '3': lambda x=3: select(x),
                  '4': lambda x=4: select(x), '5': lambda x=5: select(x), '6': lambda x=6: select(x),
                  '7': lambda x=7: select(x), '8': lambda x=8: select(x), '9': lambda x=9: select(x),
                   'i':lambda: drones(True), 'o':lambda: drones(False), 'q':lambda m=1: s_menu(m)},
                1:{'q':lambda m=0: s_menu(m)}
              }

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
