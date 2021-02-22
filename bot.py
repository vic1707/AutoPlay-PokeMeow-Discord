from random import randint
from sys import argv
from traceback import format_exc
from argparse import ArgumentParser

from Classes.Fishing import Fish
from Classes.Bag import Bag
from Classes.Pokemon import Pokemon
from Classes.Checklists import Checklists
from Classes.Feedback import Feedback
from Classes.CustomDriver import CustomDriver

"""
TODO
  - captcha ?
"""
ARGS = {
  '-C': {'metavar': 'Channel link', 'help': 'Put the CHANNEL link (between quotes) you want to connect to.'},
  '-U': {'metavar': 'USERNAME', 'help': 'Put your discord USERNAME, between quotes if it has spaces in it.'},
  '-M': {'metavar': 'MAIL', 'help': 'Put your MAIL for connecting discord.'},
  '-P': {'metavar': 'PASSWORD', 'help': 'Put your PASSWORD for connecting discord.'}
}
parser = ArgumentParser(description='A Bot to play Pokemeow on Discord')

for arg in ARGS: parser.add_argument(arg, required=True, type=str, help=ARGS[arg]['help'], metavar=ARGS[arg]['metavar'])

parser.add_argument('-D', metavar='Browser Name', type=str, help='Put your browser name. (ex: "Chrome")', default='Firefox')
parser.add_argument('-FA', metavar='2FA key', type=str, help='Put your 2FA key, if you got one.')
parser.add_argument('-H', action='store_true', help='Set this flag if you want to run the BROWSER in with no GUI')
parser.add_argument('-F', action='store_true', help='Set this flag if you want to fish (will not disable classic pokemons')

ARGUMENTS = parser.parse_args()

try:
    BAKSUCESS = None

    FEEDBACK  = Feedback(ARGUMENTS.F)
    DRIVER    = CustomDriver(ARGUMENTS)
    BAG       = Bag(DRIVER)
    CHECKLIST = Checklists(DRIVER)

    while True:

        if not FEEDBACK.get_total('success') % 20 and FEEDBACK.get_total('success') != BAKSUCESS:
            BAKSUCESS = FEEDBACK.get_total('success')
            BAG.get_bag()
            if BAG.open_boxes(): BAG.get_bag()
            BAG.do_consumables()
            BAG.do_eggs()
            print(BAG)

        BAG.reassort()
        CHECKLIST.verify_checklist()

        if ARGUMENTS.F :
            fish = Fish(BAG, DRIVER)
            FEEDBACK.add_fish(fish)
            print(fish)
            DRIVER.attente( 10 , 'next catch')

        pkmn = Pokemon(BAG, DRIVER)
        FEEDBACK.add_pkmn(pkmn)
        print(pkmn)

        DRIVER.attente( 10 , f'next { "fish" if ARGUMENTS.F else "catch" }.')
        print('##########################################')

except KeyboardInterrupt: pass
except RecursionError: print('MAX RECURSION REACHED')
except: print(format_exc()) # pass

try: 
    print(BAG)
    print(FEEDBACK)
except: pass

try: DRIVER.quit()
except: pass
input('Press Enter to close !!')
