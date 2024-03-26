import curses

stdscr = curses.initscr()
init_height, init_width = stdscr.getmaxyx()
curses.start_color()
stdscr.bkgd(curses.COLOR_BLACK)
stdscr.clear()
stdscr.refresh()


def curses_input(prompt):
    curses.echo()  
    curses.curs_set(1) 
    stdscr.addstr(prompt)
    stdscr.refresh()
    user_input = stdscr.getstr().decode(encoding="utf-8")
    return user_input

def curses_print(*args):
    for text in args:
        stdscr.addstr(str(text)+' ')
        stdscr.refresh()
    stdscr.addstr('\n')
    stdscr.refresh()

def wait():
    stdscr.getch()

def get_menu_options():
    options=[]
    options.append('Ajout : Un parent direct')
    options.append('Ajout : Un enfant')
    options.append('Suppression : Elle-même')
    options.append('Suppression : Un parent direct')
    options.append('Suppression : Un enfant')
    options.append('Consultation: arbre généalogique global')
    options.append("Consultation: La partie de l’arbre généalogique de sa famille")
    options.append('Consultation: Sa descendance')
    options.append('Consultation: Son ascendance')
    options.append('Consultation: Sa descendance et son ascendance')
    options.append('Consultation: Les personnes ayant un lien de parenté donné')
    options.append('Consultation: La liste des personnes sans ascendant')
    options.append('Consultation: La liste des personnes sans descendant')
    options.append('Consultation: La liste des personnes ayant le plus grand nombre d’ascendants vivants')
    options.append('Quitter')
    return options

def display_menu():
    menu_items = get_menu_options()
    curses.curs_set(0)  # Hide the cursor
    stdscr.keypad(True)  # Enable keypad input
    curses.noecho()  # Disable automatic echoing of key presses
    stdscr.clear()
    stdscr.refresh()
    stdscr.resize(20, 90)
    stdscr.border()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    option = 0
    while True:
        height, width = stdscr.getmaxyx()
        for i, item in enumerate(menu_items):
            x = width // 2 - len(item) // 2
            y = height // 2 - len(menu_items) // 2 + i
            if i == option:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, item)
        stdscr.move(height // 2 - len(menu_items) // 2 + option, width // 2 - len(menu_items[option]) // 2 - 2)
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP:
            option = (option - 1) % len(menu_items)
        elif key == curses.KEY_DOWN:
            option = (option + 1) % len(menu_items)
        elif key == ord('\n'):
            if option == len(menu_items) - 1:
                break
            else:
                break
    stdscr.border(0)        
    stdscr.clear()
    stdscr.refresh()
    stdscr.resize(init_height, init_width )
    
    if option==14:
        option=0
    else: option+=1
    return option



