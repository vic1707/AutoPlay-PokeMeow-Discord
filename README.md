# ⚠️ This project is not updated anymore and won't ever be, Pokemeow moved to slashcommand and I don't want to rework on that project anymore. The logic should still be fine and replacing the `CustiomDriver` with slashSommands interactions should be enough to get it to work again.

I'm not using this bot anymore, but it should still be working great. 
The most common and known issues are :
- not being able to launch the browser -> this is due to the webdrivers provided in this repo being out of date for most of them, try updating them by downloading the latest versions and replacing the existing files (**keep the same names**).
- Unable to resolve a **login** captcha -> that's unfortunately normal, bot controlled browser cause this, we can't do anything to it.

~~If my bot doesn't work for you I would advise you to try [the one created by Mehul343](https://github.com/Mehul343/PokeGrinder) which shouldn't encounter login issues since it logs in via the discord API (far better than using a browser!).~~
His repo was deleted.

# + be aware that i won't answer any incomplete issue, I need the command used (hide your credentials), a screenshot of the cmd prompt and context of the browser window

# AutoPlay PokeMeow Discord 🤖
The timings between each catchs and fishs are defined line 60 for the fishes and line 67 ( both in `bot.py`) for classic pokemons. The bare minimum is 10seconds (or Pokemeow will tell you to wait).
I would advise you to set it to a random number by replacing the `10` by something like `randint(10, 20)` (10 will be the minimum waiting time and 20 the maximum).

## Supported features
This bot can currently handle :
1. All the checklist commands (so `;daily`, `;hunt` etc...)
// NO VOTE ANYMORE BECAUSE CAPTCHA
2. Vote for Pokemeow every 12H (can fail sometimes, top.gg added a captcha)
// NO VOTE ANYMORE BECAUSE CAPTCHA
3. Throw Pokeballs depending on the rarity of the Pokemon
4. Buy Pokeballs when you're out of stock (only if you can buy a certain amount of each less effective balls : see dedicated section)
5. Handle your eggs
6. Use all your Repels and Golden Razz Berries
7. Open every boxes in your bag
8. Can fish for you (via an argument)

## How buying works 
With the default settings, the bot will buy :
- 1 Masterball only if you have more than 109K coins
- 3 Ultraballs if > 9K
- 5 Superballs if > 4500
- 5 Pokeballs if > 1k

⚠️ So if it didn't bought any balls it means that you were a little bit too poor ⚠️ 

This is a security to avoid situations where you buy 1 Masterball at 100K and don't have enought coins left to buy lesser effectives balls.

## Installating

### On your pc
1. Install your favorite version of python 3 and add it to PATH.
2. If not done already download this repo on your computer as zip and unzip it.
3. Inside of the repo type the following command `python -m pip install -r requirements.txt` (If your on a linux distribution or MacOS you got a specify the python version so it's `python3 ...`)

### On your discord
4. a. You got to activate your Pokemeow account (type `;p` at least once)

   b. I recommand you to have at least 1,000 Coins.


## Launching 

In order to launch the bot you have to type the following command: `python bot.py` (`python3 bot.py` if you're on Linux or MACos) with some required arguments :
- `-U` : Your displayed username on the discord server you wan't to use this bot (put it inside quotes it it contains a space or if your not sure).
- `-M` : Your Discord mail adress.
- `-P` : Your Discord Password.
- `-C` : The direct link to the channel of your choice (between quotes just in case :wink:)

The following arguments depends on your personnal setup, and are optionnal : 
- `-F` : If you want this program to fish for you.
- `-FA` : If you got the 2FA authetification, you have to put the 2FA key. Because 2FA is designed to prevent from bots this program won't be able to run in headless mode and you'll have to type manually the code that the bot will give you.
- `-H` : For Headless mode (without the Browser window), ⚠️ This will not work if you have activate 2FA !
- `-D` : If you want to use another driver, Firefox is the default one. Add 'Chrome' after the flag in order to use Chrome.
- `-BACKWARDS` : If the bot is typing backwards, this will reverse everything the bot is typing on discord.

So to load the script you have to type in your Terminal or CMD some thing like : 
`python bot.py -U 'John Doe' -M 'johndoe@gmail.com' -P 'dQw4w9WgXcQ' -C 'CHANNEL LINK'` and every other flag needed for your use case.
(or `python3` for Linux or MacOS)

⚠️ You can of course create a .sh or .bat file in order to execute the command without repetively type the command but rememeber this is a big security breach and we're not responsive for any dataleaking ⚠️

## Stoping
To stop the program simply type Ctrl + C in the command promt, or close the browser if not in Headless mode, or close directly the command promt.


## Adding new webdrivers
If you want your favorite browser to be supported, visit : https://www.selenium.dev/documentation/en/getting_started_with_webdriver/browsers/ and see if your's part of the supported drivers of Selenium.


## Disclamer ⚠️
- We're of course not responsible for any ban you recieve for using this bot.
- For now only Firefox, Opera, Edge and Chrome are supported.
- Edge is only supported on Windows.
- Running multiple bots in one channel is definitively not recommanded.
