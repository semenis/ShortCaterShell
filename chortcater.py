import json
import subprocess
import os


class chortcater:
    def __init__(self):
        self.file = 'links.json'
        self.osname = os.name
        self.data = {}

    def load(self):
        with open(self.file) as f:
            self.data = json.load(f)

    def save(self):
        with open(self.file, 'w') as f:
            f.write(json.dumps(self.data))

    def add_new_sc(self, shortcat, command):
        self.data[shortcat] = command

    def del_old_sc(self, shortcat):
        del self.data[shortcat]

    def exe(self, shortcat, shell=False, additional_args=None):
        try:
            if additional_args:
                subprocess.call(self.data[shortcat].split() + [additional_args])
            else:
                subprocess.call(self.data[shortcat].split())
        except KeyError as com:
            print(
                'Command {} not found, if you need to add command use `add_new_sc("shortcat", "command")`'.format(com))
        except Exception as e:
            print(e)

    def pyexe(self, command):
        print('Running ' + command)
        exec(command)

    def init_standart_sc(self):
        if self.osname == "posix":
            self.data['poweroff'] = "poweroff"
            self.data['reboot'] = "shutdown -r now"
            self.data['print'] = 'echo '
            self.data['ping'] = 'ping ya.ru'
        elif self.osname == "nt":
            self.data['poweroff'] = "shutdown -s -t 0"
            self.data['reboot'] = "shutdown -r -t 0"


a = chortcater()
a.load()
a.init_standart_sc()
a.exe('print', additional_args='Shortcat shell started')
import sys

for i in sys.stdin:
    i = i.strip()
    if len(i) > 10 and i[:10] == 'add_new_sc':

        # For example use this command
        # add_new_sc('t1', 'ping ya.ru')
        # add_new_sc('t2', 'echo Developer')

        print(i[10:].replace('(', '').replace(')', '').replace("'", '').strip().split(', '.replace('(', '')))
        a.add_new_sc(i[10:].replace('(', '').replace(')', '').replace("'", '').strip().split(', '.replace('(', ''))[0],
                     i[10:].replace('(', '').replace(')', '').replace("'", '').strip().split(', '.replace('(', ''))[1])
    elif len(i) > 7 and i[:6] == 'python':
        a.pyexe(i[7:])
    elif i == 'exit':
        a.save()
        sys.exit(0)
    elif i == 'save':
        print('Saved..')
        a.save()
    else:
        a.exe(i)
