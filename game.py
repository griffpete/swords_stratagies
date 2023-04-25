def render_introduction():
    return '''

                             -|             |-
         -|                  [-_-_-_-_-_-_-_-]                  |-
         [-_-_-_-_-]          |             |          [-_-_-_-_-]
          | o   o |           [  0   0   0  ]           | o   o |
           |     |    -|       |           |       |-    |     |
           |     |_-___-___-___-|         |-___-___-___-_|     |
           |  o  ]              [    0    ]              [  o  |
           |     ]   o   o   o  [ _______ ]  o   o   o   [     | ----__________
_____----- |     ]              [ ||||||| ]              [     |
           |     ]              [ ||||||| ]              [     |
       _-_-|_____]--------------[_|||||||_]--------------[_____|-_-_
      ( (__________------------_____________-------------_________) )
      
                             Sword and Strategy





Welcome my Lord, type 'help' if needed for a list of commands
'''

def create_world():
    return {
      'map': create_map(),
      'player': create_player(),
      'status': "playing"
    }

def create_map():
    return {
        'Home': {
            'about': 'home sweet home',
        },
        'Gwynedd': {
            'about': 'The great city of Gwynedd is gaurded by countless catapults that destroy enemies from afar',
            'stats': {'walls': 25, 'territory': 50,'defense': 50},

        },
        'Elvandor': {
            'about': "A small castle gaurded by villagers, shouldn't take much to capture",
            'stats': {'walls': 10, 'territory': 15,'defense': 10},
        },
                
        'Avalon': {
            'about': 'Monstrous walls that took 100 years to craft, the great castle of Avalon is said to be impenatrable...',
            'stats': {'walls': 100, 'territory': 20,'defense': 75},
        },
        'Liagor': {
            'about': 'The castle of Liagor is surronded by deep trenches full of spearmen',
            'stats': {'walls': 10, 'territory': 100,'defense': 75},
        }

    
    }

#playerstats
def create_player():
    return {
        'location': 'home',
        'stats': {'Archers': 15,'Infantry': 30,'Trebuchets': 2, 'Cavalry': 5},
        'wins': 0,
        'attacked':['Home'],
        'loses': 0
    }

#writes out the world for current posistion
def render(world):
    return (render_location(world) + render_player(world))
    
#shows current location
def render_location(world):
    return """
        /
*//////{<>==================>
        \ """

def render_player(world):
    player = world['player']

    if player['loses'] == 2:
        world['status'] = 'lost'
        return 'Your army grew too weak'
    elif player['wins'] == 4:
        world['status'] = 'won'
        return 'You arise victories!'
    return ''

#takes in number of victores and returns something an ally to be printed if victoers is meet
def render_allies(world, name):
    ally = {'name': 'none', 'description': 'none'}
    if name == 'Harad':
        ally['name'] = 'Harad'
        ally['description'] = 'A noble king from the south with a prospericous army'

    elif name == 'Belstead':
        ally['name'] = 'Belstead'
        ally['description'] = 'A rich lord from the west with a greed for weatlth'
        
    return ("You are approched by " + ally['name'] + "\n" + ally['description'] + "\n" + "Would you like to ally ('yes' / 'no')" + "\n")

#figures out which commands are possible
def get_options(world):
    commands = ['quit', 'troops', 'help', 'yes', 'no', 'map']
      
    for location in world['map']:
        
        if location not in world['player']['attacked']:
            commands.append('scout ' + location)
            commands.append('attack ' + location)


                
    return commands

#if a command is entered somthing happes
def update(world, command):
    wins = world['player']['wins']
    if command == "quit":
        world['status'] = 'quit'
        return "Forfeiting war"
    elif wins >= 2 and wins < 3:
        return render_allies(world, 'Harad')
    
    elif wins >= 3 and wins < 4:
        return render_allies(world, 'Belstead')
    
    elif command == 'troops':
        return troops(world)

    elif command == 'help':
        return helper()

    elif command.startswith('scout'):
        return scout(world, command)

    elif command.startswith('attack'):
        return attack(world, command)
    
    elif command == 'map':
        return gps(world)
            
    return

def helper():
    return """
    Available Commands:
    - quit
        * ends the game

    - map
        *shows kingdoms around you that are available to attack
        
    - troops
        * shows currents troops in castle

    - scout 'kingdom'
        * tells information about a kingdom

    - attack 'kingdom'
        * attacks kingdom (get troops on victory, loose troops on defeat)
    """

def troops(world):
    print('Current troops: ')
    troops = world['player']['stats']
    info = ''
    for troop, number in troops.items():
        info += f'{troop} ({number}), '
    info = info.rstrip(', ')

    return info

def scout(world, command):
    name = command[6:]
    location = world['map'][name]
    about = location['about']
    return ("You are scouting " + name + "\n" + about + "\n")

def attack(world, command):
    name = command[7:]
    location = world['map'][name]
    kingdom_stats = location['stats']
    player_stats = world['player']['stats']
    player_loses = world['player']['loses']
    player_wins = world['player']['wins']

    answer = ''
    while answer not in options:
        answer = input(' - ')
        if answer not in options:
            print('Invalid command- ' + answer)
    
    
    if name == 'Elvandor':    
        if True:
            player_loses['loses'] += 1
            return
        else:
            player_wins['wins'] += 1
            return
       
    elif name == 'Liagor':
        return
    elif name == 'Gwynedd':
        return
    elif name == 'Avalon':
        return
    return 

def gps(world):
    unattacked_locations = []
    for location in world['map']:
        if location not in world['player']['attacked']:
            unattacked_locations.append(location)
    return ', '.join(unattacked_locations)
        
#renders the ending, there is only three
def render_ending(world):
    if world['status'] == 'won':
        return "Victory!"
    elif world['status'] == 'lost':
        return "Defeat..."
    elif world['status'] == 'quit':
        return "Quiting game..."

#has a while loop to take commands only if they're possible
def choose(options):
    answer = ''
    while answer not in options:
        answer = input(' - ')
        if answer not in options:
            print('Invalid command- ' + answer)
    return answer

############# Main Function ##############
# Do not modify anything below this line #
##########################################
def main():
    '''
    Run your game using the Text Adventure console engine.
    Consumes and produces nothing, but prints and indirectly takes user input.
    '''
    print(render_introduction())
    world = create_world()
    while world['status'] == 'playing':
        print(render(world))
        options = get_options(world)
        command = choose(options)
        print(update(world, command))
    print(render_ending(world))

if __name__ == '__main__':
    main()



