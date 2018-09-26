

import tkinter as tk


class My_gui():
    def __init__(self, window_title, geometry):
        self.root = tk.Tk()
        self.root.geometry(geometry)
        self.root.title(window_title)
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
      
        
class Start_battle_gui(My_gui):
    def __init__(self, attacker, defenders):
        My_gui.__init__(self, 'STARTING BATTLE', '350x150+200+200')
        
#        self.label1 = tk.Label(self.frame, text='STARTING BATTLE')
#        self.label1.grid(row=1, column=1)
        
        self.label2 = tk.Label(self.frame, text='Attacker: '+attacker.owner_name)
        self.label2.grid(row=2, column=1)
        
        self.label3 = tk.Label(self.frame, text='Defender: '+defenders[0].owner_name)
        self.label3.grid(row=2, column=2)
        
        self.label4 = tk.Label(self.frame, text=attacker.ship_type)
        self.label4.grid(row=3, column=1)
        
        defenders_string = ''
        for defender in defenders:
            try:
                defenders_string += defender.ship_type+'\n' #works for ships
            except:
                defenders_string += defender.name+'\n' #works for planet
        self.label5 = tk.Label(self.frame, text=defenders_string)
        self.label5.grid(row=3, column=2)
        
        self.ok_button = tk.Button(self.frame, text='OK', command=self.ok_command, bg='orange')
        self.ok_button.grid(row=4, column=2)
                
        self.root.mainloop()
        
        
    def ok_command(self):
        self.root.destroy()
        
        


