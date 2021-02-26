from re import sub

class Bag():

    BALLS = {
            "Masterballs"  : {"call":  "mb", "id_shop":    4, "stock": 0, "to_buy":    1, "price": 100000}, # buy only if money > 109 000 coins
            "Premier balls": {"call": "prb", "id_shop": None, "stock": 0, "to_buy": None, "price":   None},
            "Ultraballs"   : {"call":  "ub", "id_shop":    3, "stock": 0, "to_buy":    3, "price":   1500}, # buy only if money >   9 000 coins
            "Greatballs"   : {"call":  "gb", "id_shop":    2, "stock": 0, "to_buy":    5, "price":    500}, # buy only if money >   4 500 coins
            "Pokeballs"    : {"call":  "pb", "id_shop":    1, "stock": 0, "to_buy":    5, "price":    200}, # buy only if money >   1 000 coins
            # "Diveballs"   : {"call":  "db", "id_shop": None, "stock": 0, "to_buy": None, "price":   None}
    }

    BOXES = {
        "Rare boxes":       {"call":  ";open rb", "stock": 0},
        "Super Rare boxes": {"call": ";open srb", "stock": 0},
        "Legendary boxes":  {"call":  ";open lb", "stock": 0},
        "Shiny boxes":      {"call":  ";open sb", "stock": 0},
    }

    LOOTBOXES = { "stock": 0, "expected": " opened", "call": ";lb all"}

    CONSUMABLES = { 
        'Golden Razz Berries' : {"stock": 0, "expected":   ", you", "call": ";grazz all"}, 
        'Repels'              : {"stock": 0, "expected":   ", you", "call": ";repels all"}
    }

    EGGS = {
        "stock": 0,
        "hatch": False,
        "hold" : False
    }

    def __init__(self, driver):
        self.DRIVER = driver

    def __repr__(self) -> str:
        balls = ( '\n'. join( f"""        ║{ f"{ self.BALLS[ball]['stock']:4d} : { ball:<12s}":^25s}║""" for ball in self.BALLS))
        return f"""
        ╔═════════════════════════╗
        ║   Your item inventory   ║
        ╠═════════════════════════╣
        ║        Currencies       ║
        ║{ f'{ self.money:^9,d} : PokeCoins':^25s}║ 
        ╟━━━━━━━━━━━━━━━━━━━━━━━━━╢
        ║          Balls          ║\n{ balls }
        ╟━━━━━━━━━━━━━━━━━━━━━━━━━╢
        ║       Catch Items       ║
        ║{ f"{ self.EGGS['stock'] } : Eggs":^25s}║
        ╚══━━━━═══════════════════╝
        """

    def open_boxes(self) -> bool:
        OPENED = False
        for box in self.BOXES:
            while self.BOXES[box]['stock']:
                OPENED = True
                self.DRIVER.WaitNew(self.BOXES[box]['call'], f"{ self.DRIVER.USERNAME } opened")
                self.BOXES[box]['stock'] -= 1
                self.DRIVER.attente(10, 'opening another box or continue..')
        
        if self.LOOTBOXES['stock']:
            self.DRIVER.WaitNew(self.LOOTBOXES['call'], f'{ self.DRIVER.USERNAME }{ self.LOOTBOXES["expected"] }')
            self.LOOTBOXES['stock'] = 0
            OPENED = True
            self.DRIVER.attente(5, 'ending boxes opening..')
        return OPENED

    def reassort(self) -> None:
        for index, ball in enumerate(self.BALLS.keys()):
            if self.BALLS[ball]['to_buy']    and \
               self.BALLS[ball]['stock'] < 1 and \
               self.money >= sum( self.BALLS[ball]['price'] * self.BALLS[ball]['to_buy'] if self.BALLS[ball]['to_buy'] else 0 for ball in list(self.BALLS.keys())[index:]) + (self.BALLS["Pokeballs"]['price'] * self.BALLS["Pokeballs"]['to_buy'] if ball !='Pokeballs' else 0): 
                print(f"Buying {self.BALLS[ball]['to_buy']} {ball} !")
                self.DRIVER.WaitNew(f';shop buy { self.BALLS[ball]["id_shop"] } { self.BALLS[ball]["to_buy"] }', f'{ self.DRIVER.USERNAME }, you bought')

                self.BALLS[ball]["stock"] += self.BALLS[ball]["to_buy"]
                self.money -= (self.BALLS[ball]['to_buy'] * self.BALLS[ball]['price'])
                self.DRIVER.attente(10, 'next catch or buy..')

    def update_balls(self, msg: str, CAPTURED: bool) -> None:
        if CAPTURED:
             self.money += int(sub(r'(.|\n)*?(\d?[0-9,]+) PokeCoins(.|\n)*' , r'\2', msg).replace(',', ''))

        for ball in self.BALLS:
            if ball in msg:
                self.BALLS[ball]['stock'] = int(sub(rf'(.|\n)*{ ball } ?: (\d?[0-9,]+)(.|\n)*', r'\2', msg).replace(',', ''))

    def get_bag(self) -> None:
        message = self.DRIVER.WaitNew(';items', f"{ self.DRIVER.USERNAME }'s item inventory")

        self.money = int(sub(r'(.|\n)*?(\d?[0-9,]+)x PokeCoins(.|\n)*' , r'\2', message.text).replace(',', ''))
        for ball in self.BALLS:
            self.BALLS[ball]['stock'] = int(sub(rf'(.|\n)*?(\d?[0-9,]+)x { ball }(.|\n)*'  , r'\2', message.text).replace(',', ''))

        for box in self.BOXES:
            self.BOXES[box]['stock'] = int(sub(rf'(.|\n)*?(\d?[0-9,]+)x { box }(.|\n)*'  , r'\2', message.text).replace(',', ''))

        for consumable in self.CONSUMABLES:
            self.CONSUMABLES[consumable]['stock'] = int(sub(rf'(.|\n)*?(\d?[0-9,]+)x { consumable }(.|\n)*'  , r'\2', message.text).replace(',', ''))

        self.LOOTBOXES['stock'] = int(sub(rf'(.|\n)*?(\d?[0-9,]+)x Lootboxes(.|\n)*'  , r'\2', message.text).replace(',', ''))

        self.EGGS['stock'] = int(sub(rf'(.|\n)*?(\d?[0-9,]+)x Eggs(.|\n)*'  , r'\2', message.text).replace(',', ''))
        self.EGGS['hold']  = 'COUNTER' in message.text
        self.EGGS['hatch'] = 'READY' in message.text

    def do_consumables(self) -> None:
        for consumable in self.CONSUMABLES:
            if self.CONSUMABLES[consumable]['stock']:
                self.DRIVER.WaitNew(self.CONSUMABLES[consumable]['call'], f'{ self.DRIVER.USERNAME }{ self.CONSUMABLES[consumable]["expected"] }')
                self.CONSUMABLES[consumable]['stock'] = 0
                self.DRIVER.attente(10, 'using another consumable or continue..')

    def do_eggs(self) -> None:
        if not self.EGGS['hold'] and self.EGGS['stock']:
            if self.EGGS['hatch']:
                self.DRIVER.WaitNew(';egg hatch', 'hatched')
                print(f'An egg was hatched !')
                self.DRIVER.attente(15, 'before holding a new egg')
            self.DRIVER.WaitNew(';egg hold', 'holding')
            print(f'Your now holding an egg !')
            self.EGGS['stock'] -= 1
            self.DRIVER.attente(10, 'next action..')
        
        elif self.EGGS['hatch']:
            self.DRIVER.WaitNew(';egg hatch', 'hatched')
            print(f'An egg was hatched !')
            self.DRIVER.attente(10, 'next action..')