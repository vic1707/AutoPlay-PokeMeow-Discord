from re import sub

class Pokemon(): 

    RARITYS = {
        "Legendary"     :   "Masterballs",
        "Shiny"         :   "Masterballs",
        "Super Rare"    :    "Ultraballs",
        "Rare"          :    "Greatballs",
        "Uncommon"      :     "Pokeballs",
        "Common"        :     "Pokeballs"
    }

    CAPTURED = False

    def __init__(self, bag, driver) -> None:
        self.DRIVER = driver
        self.BAG = bag
        self.message, self.rarity, self.name = self.spawn()

        self.CAPTURED = self.which_ball()
        self.BAG.update_balls(self.message.text, self.CAPTURED)

    def __repr__(self) -> str:
        return f"""It's a {self.name}, it's rarity is {self.rarity}, {'and is now in you PC !' if self.CAPTURED else 'ran away.'}"""
 
    def spawn(self):
        message = self.DRIVER.WaitNew(';p', f"{ self.DRIVER.USERNAME } found")
        return ( message, 
                 sub( r'(.|\n)*?a wild .*!\n(.*) \((.|\n)*', r'\2', message.text ),  
                 sub( r'(.|\n)*?a wild (.*)!(.|\n)*', r'\2', message.text ) )

    def which_ball(self) -> None:
        for index, ball in enumerate(self.BAG.BALLS.keys()):
            if self.RARITYS.get(self.rarity) == ball: 
                if self.BAG.BALLS[ball]['stock'] > 0:
                    return self.DRIVER.WaitChangesOnMessage(self.BAG.BALLS[ball]['call'], self.message)
                    
                else:
                    for i in range(index, len(self.BAG.BALLS.keys())):
                        if self.BAG.BALLS[list(self.BAG.BALLS.keys())[i]]['stock'] > 0:
                            return self.DRIVER.WaitChangesOnMessage(self.BAG.BALLS[list(self.BAG.BALLS.keys())[i]]['call'], self.message)
                            
                    self.DRIVER.SendMessage('I\'m too poor !')