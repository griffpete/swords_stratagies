import random

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





Welcome my Lord, you are the commander of a great army. It is up to you to conquer the 5 kingdoms!
It is advised to scout kingdoms before attacking, every castle has it's strengths and weaknesses.
Good luck!

*type 'help' if needed for a list of commands
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
        'Gwyned': {
            'about': 'The great city of Gwynedd is gaurded by countless catapults that destroy enemies from afar',
            'stats': {'walls': 25, 'terain': 100,'defense': 50},
            'reward': {'Trebuchets': 5},
            'destroy': 'Infantry',
            'death message': 'The great catapults destroyed all your infantry.',
            'victory message': 'The great catapults destroyed half your infantry'

        },
        'Elvandor': {
            'about': "A small castle gaurded by villagers, shouldn't take much to capture",
            'stats': {'walls': 10, 'terain': 15,'defense': 10},
            'reward': {'Infantry': 25},
            'destroy': 'Archers',
            'death message': 'The small castle stood strong and took all your archers as prisoners',
            'victory message': 'The small castle targeted your archers and killed off half'


        },    
        'Avalon': {
            'about': 'Monstrous walls that took 100 years to craft, the great castle of Avalon is said to be impenatrable...',
            'stats': {'walls': 100, 'terain': 100,'defense': 100},
            'reward': {'Archers': 1000},
            'destroy': 'Cavalry',
            'death message': 'The thousands of archers in the great wall killed off all of your horses',
            'victory message': 'Your entire army died in the proccess, but you rule all the kingdoms now!'
        },
        'Liagor': {
            'about': 'The castle of Liagor is surronded by deep trenches full of spearmen',
            'stats': {'walls': 10, 'terain': 25,'defense': 75},
            'reward': {'Cavalry': 10},
            'destroy': 'Trebuchets',
            'death message': 'The trenches engoulfed any trebechets deployed.',
            'victory message': 'The trenches destroyed half your trebuechets, be more carefull with them!'
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
        return '\nYour army grew too weak' + "\nGame Over."
    elif player['wins'] == 4:
        world['status'] = 'won'
        return '\nYou arise victorious!' + "\nGreat Game."
    return ''

#figures out which commands are possible
def get_options(world):
    if world['status'] != 'playing':
        return ''
    
    commands = ['quit', 'troops', 'help', 'map']
      
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
            
    return '---------'

def helper():
    return """
    Available Commands:
    - quit
        * ends the game

    - map
        * shows kingdoms around you that are available to attack
        
    - troops
        * shows currents troops in castle

    - scout 'kingdom'
        * tells information about a kingdom

    - attack 'kingdom'
        * attacks kingdom (get troops on victory, loose troops on defeat)
    """

#Shows current number of troops
def troops(world):
    print('Current troops: ')
    troops = world['player']['stats']
    info = ''
    for troop, number in troops.items():
        info += f'{troop} ({number}), '
    info = info.rstrip(', ')

    return info

#shos name of kingdom and description
def scout(world, command):
    name = command[6:]
    location = world['map'][name]
    about = location['about']
    return (name + ": " + about)

#uses a while loop to take input for ammount of troops if it is correct it will increase win, or increase loss
def attack(world, command):
    name = command[7:]
    location = world['map'][name]
    player = world['player']
    player_stats = player['stats']
    
    rnjesus = random.randint(3, 8)
    deployed = {}

    #takes user input for troops, checks to make sure it is an integar and in the valid number range
    for x in player_stats.keys():
        correct_value = False
        while correct_value == False:
            if player_stats[x] == 0:
                correct_value = True
                deployed[x] = 0
                continue

            try:
                answer = input(x + ' (0 - ' + str(player_stats[x]) + ') - ')
                if answer == "quit":
                    world['status'] = 'quit'
                    return "Forfeiting war"
                
                answer = int(answer)
                if answer <= player_stats[x] and answer >= 0:
                    deployed[x] = answer
                    player_stats[x] -= round(deployed[x] / rnjesus)
                    correct_value = True
                else:
                    print('Invalid')
            except ValueError:
                print('Invalid')

    reward_name = next(iter(location['reward']))
    reward_value = list(location['reward'].values())[0]
    destroy = location['destroy']
    death_message = location['death message']
    victory_message = location['victory message']

    #takes new dictionary and sends it to see if attack was succesfull
    if check_attack(world, deployed, name):
        player['wins'] += 1
        player['attacked'].append(name)
        #adds reward to player inventory
        player_stats[reward_name] += reward_value
        player_stats[destroy] -= round(deployed[destroy] / 2)
        return "\nVictory!"+ '\n' + str(rnjesus) + "0% of troops survived" + "\nReward +" + str(reward_value) + ' ' +reward_name + '\n' + victory_message
    else:
        player['loses'] += 1
        player_stats[destroy] -= deployed[destroy]
        player_stats[destroy] = max(0, player_stats[destroy])
        return "\nDefeat!"+ '\n' + str(10 - rnjesus) + "0% of troops fleed home" + "\n" + death_message
       

#takes in new troops that where entered, and name of kingdom. compares it too kingdom stats to determine if the attack was successfull
def check_attack(world, troops, name):
    kingdom_stats = world['map'][name]['stats']
    walls = kingdom_stats['walls']
    terain = kingdom_stats['terain']
    defense = kingdom_stats['defense']

    win_rate = 0
    trebuchets = troops['Trebuchets'] * 25
    archers = troops['Archers']
    cavalry = troops['Cavalry'] * 10
    infantry = troops['Infantry']

    #compares archers and trebuchets against walls
    if trebuchets + archers >= walls:
        win_rate += 5
    elif trebuchets + archers >= walls / 2:
        win_rate += 3
    
    #compares cavalry against the terrain
    if cavalry >= terain:
        win_rate += 5
    elif cavalry >= terain / 2:
        win_rate += 2

    #infantry and archers against defense
    if infantry + archers >= defense:
        win_rate += 6
    elif infantry + archers >= defense / 2:
        win_rate += 1

    if win_rate >= 10:
        return True
    else:
        return False
    
    #{'Archers': 15,'Infantry': 30,'Trebuchets': 2, 'Cavalry': 5}
    #{'walls': 10, 'territory': 15,'defense': 10}


#says all locations that have not been defeated yet
def gps(world):
    unattacked_locations = []
    for location in world['map']:
        if location not in world['player']['attacked']:
            unattacked_locations.append(location)
    return ', '.join(unattacked_locations)
        
#renders the ending, there is only three
def render_ending(world):
    if world['status'] == 'won':
        return "Quiting game..."
    elif world['status'] == 'lost':
        return "Quiting game..."
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



