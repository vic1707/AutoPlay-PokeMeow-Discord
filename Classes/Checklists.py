from re import sub
from datetime import datetime, timedelta

class Checklists():
    CHECKLIST = {
        'Daily': {'replace': r'\2', 'test':   r'(.|\n)*daily is (.*)?!(.|\n)*', 'fallback': r'(.|\n)*?daily.*in (.*)?.(.|\n)*', 'validator': 'available', 'do_when': None},
        'Swap' : {'replace': r'\2', 'test': r'(.|\n)*You (.*?) .* swap(.|\n)*', 'fallback':   r'(.|\n)*swap.*in (.*)?.(.|\n)*', 'validator':       'can', 'do_when': None},
        'Hunt' : {'replace': r'\2', 'test': r'(.|\n)*You (.*?) .* hunt(.|\n)*', 'fallback':   r'(.|\n)*hunt.*in (.*)?.(.|\n)*', 'validator':       'can', 'do_when': None},
        'Quest': {'replace': r'\2', 'test':   r'(.|\n)*quest is (.*)?!(.|\n)*', 'fallback': r'(.|\n)*?quest.*in (.*)?.(.|\n)*', 'validator': 'available', 'do_when': None, 'cooldown':  120},
        # 'vote' : {'replace': r'\2', 'test':    r'(.|\n)*vote is (.*)?!(.|\n)*', 'fallback':  r'(.|\n)*?vote.*in (.*)?.(.|\n)*', 'validator': 'available', 'do_when': None, 'cooldown':  720}
    }

    def __init__(self, driver):
        self.DRIVER = driver
        if self.checklist():
            self.checklist() # in order to retreive new timers in case of previously doing a task

    def checklist(self):
        return_ = False
        message = self.DRIVER.WaitNew(';checklist', f"{ self.DRIVER.USERNAME }'s Checklist")
        self.DRIVER.attente(5, 'doing first task..')
        for task in self.CHECKLIST:
            if sub(self.CHECKLIST[task]['test'], self.CHECKLIST[task]['replace'], message.text) == self.CHECKLIST[task]['validator']:
                if task != 'vote': 
                    self.DRIVER.WaitNew(f';{ task }', f'{ task }')
                    if task == 'quest':
                        self.CHECKLIST[task]['do_when'] = datetime.now() + timedelta(minutes=self.CHECKLIST[task]['cooldown'])
                    else: return_ = True
                else: 
                    self.DRIVER.Vote()
                    self.CHECKLIST[task]['do_when'] = datetime.now() + timedelta(minutes=self.CHECKLIST[task]['cooldown'])
                self.DRIVER.attente(5, 'next task or continue..')

            else:
                cooldown = datetime.strptime(sub(self.CHECKLIST[task]['fallback'], self.CHECKLIST[task]['replace'], message.text), '%HH %MM %SS').time()
                self.CHECKLIST[task]['do_when'] = datetime.now() + timedelta(hours=cooldown.hour, minutes=cooldown.minute, seconds=cooldown.second)
        return return_

    def verify_checklist(self):
        did_task = False
        for task in self.CHECKLIST:
            if self.CHECKLIST[task]['do_when'] < datetime.now():
                if task != 'vote': 
                    self.DRIVER.WaitNew(f';{ task }', f'{ task }')
                    did_task = True
                else: 
                    self.DRIVER.Vote()
                    self.CHECKLIST[task]['do_when'] = datetime.now() + timedelta(minutes=self.CHECKLIST[task]['cooldown'])
        if did_task: self.checklist()
