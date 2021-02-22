from datetime import datetime

class Feedback():
    CAPTURED = {
        "Legendary"     : {'total': 0,'failed': 0, 'success': 0, 'SuccessNames': [], 'FailedNames': []},
        "Shiny"         : {'total': 0,'failed': 0, 'success': 0, 'SuccessNames': [], 'FailedNames': []},
        "Super Rare"    : {'total': 0,'failed': 0, 'success': 0},
        "Rare"          : {'total': 0,'failed': 0, 'success': 0},
        "Uncommon"      : {'total': 0,'failed': 0, 'success': 0},
        "Common"        : {'total': 0,'failed': 0, 'success': 0}
    }

    FISHS = {'total': 0,'failed': 0, 'success': 0, 'none': 0, 'SuccessNames': [], 'FailedNames': []}

    def __init__(self, FISH) -> None:
        self.FISH = FISH
        self.demarrage = datetime.now()
        print(f'It\'s { self.demarrage.strftime("%H:%M:%S") }, working time !')


    def add_pkmn(self, pkmn) -> None:
        for rarity in self.CAPTURED:
            if rarity == pkmn.rarity:
                if pkmn.CAPTURED:
                    self.CAPTURED[rarity]['success'] += 1
                    if rarity == 'Legendary' or rarity == 'Shiny': self.CAPTURED[rarity]['SuccessNames'].append(pkmn.name)
                else:
                    self.CAPTURED[rarity]['failed'] += 1
                    if rarity == 'Legendary' or rarity == 'Shiny': self.CAPTURED[rarity]['FailedNames'].append(pkmn.name)

                self.CAPTURED[rarity]['total'] += 1

    def add_fish(self, fish) -> None:
        if fish.CAPTURED:
            self.FISHS['success'] += 1
            if fish.BALL == 'Masterballs': self.FISHS['SuccessNames'].append(fish.name)
        elif fish.CAPTURED == None:
            self.FISHS['none'] += 1
        else:
            self.FISHS['failed'] += 1
            if fish.BALL == 'Masterballs': self.FISHS['FailedNames'].append(fish.name)
            
        self.FISHS['total'] += 1

    def get_total(self, cat: str) -> int: return sum(self.CAPTURED[rarity][cat] for rarity in self.CAPTURED) + self.FISHS['success']

    def get_duration(self):
        hours, remainder = divmod((datetime.now() - self.demarrage).seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{hours:02}H {minutes:02}m {seconds:02}s'

    def __repr__(self) -> str:
        caught = ( '\n'. join( f"""        ║{ f"{ self.CAPTURED[rarity]['success']:4d} : { rarity:<12s}":^22s}║""" for rarity in self.CAPTURED))
        missed = ( '\n'. join( f"""        ║{ f"{ self.CAPTURED[rarity]['failed']:4d} : { rarity:<12s}":^22s}║"""  for rarity in self.CAPTURED))
        total  = ( '\n'. join( f"""        ║{ f"{ self.CAPTURED[rarity]['total']:4d} : { rarity:<12s}":^22s}║"""   for rarity in self.CAPTURED))
        return f"""
        ╔══════════════════════╗
        ║       Duration       ║
        ║{self.get_duration():^22s}║ 
        ╟━━━━━━━━━━━━━━━━━━━━━━╢
        ║{ f"TOTAL FOUND : {self.get_total('total')}":^22s}║
        ╟----------------------╢\n{ total }
        ╟━━━━━━━━━━━━━━━━━━━━━━╢
        ╟       DETAILS        ╢
        ╟----------------------╢
        ║{ f"Caught : { self.get_total('success') }":^22s}║\n{ caught }
        ║----------------------║
        ║{ f"Missed : { self.get_total('failed') }":^22s}║\n{ missed }
        ╚══━━━━════════════════╝
        """ + (f"""
        ╔══════════════════════╗
        ║        Fishs         ║
        ║{ f"TOTAL TRIED : {self.FISHS['total']}":^22s}║
        ╟━━━━━━━━━━━━━━━━━━━━━━╢
        ╟       DETAILS        ╢
        ╟----------------------╢
        ║{ f"Didn't show up : { self.FISHS['none'] }":^22s}║
        ╟----------------------╢
        ║{ f"Caught : { self.FISHS['success'] }":^22s}║
        ║----------------------║
        ║{ f"Missed : { self.FISHS['failed'] }":^22s}║
        ╚══━━━━════════════════╝
        """ if self.FISH else '\r\nFishs weren\'t asked.\n')  + f"""
        \r{ f"Important fishes catched : { self.FISHS['SuccessNames'] }" if self.FISHS['SuccessNames'] else "" }
        \r{ f"Important fishes missed : { self.FISHS['FailedNames'] }" if self.FISHS['FailedNames'] else "" }
        \r{ f"Important Legendary catched : { self.CAPTURED['Legendary']['SuccessNames'] }" if self.CAPTURED['Legendary']['SuccessNames'] else "" }
        \r{ f"Important Legendary missed : { self.CAPTURED['Legendary']['FailedNames'] }" if self.CAPTURED['Legendary']['FailedNames'] else "" }
        \r{ f"Important Shiny catched : { self.CAPTURED['Shiny']['SuccessNames'] }" if self.CAPTURED['Shiny']['SuccessNames'] else "" } 
        \r{ f"Important Shiny missed : { self.CAPTURED['Shiny']['FailedNames'] }" if self.CAPTURED['Shiny']['FailedNames'] else "" } 
        """
