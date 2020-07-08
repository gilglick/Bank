# HW3 JONATHAN KARTA 
from tkinter import *
from tkinter import messagebox

running = True
press_stop = False


class Application(object):

    def __init__(self, master, generator, graph):
        # Root configuration
        self.generator = generator
        self.graph = graph
        self.gene = None
        self.master = master
        self.master.title("Jon's bank")
        self.master.geometry("620x200+350+200")
        self.master.resizable(False, False)

        # Top and Bottom frame configuration
        self.top = Frame(self.master, height=50, width=600, relief=RIDGE, borderwidth=4)
        self.bottom = Frame(self.master, height=150, width=600, relief=RIDGE, borderwidth=2)
        self.top.pack(side=TOP, fill="both")
        self.bottom.pack(side=BOTTOM, fill="both")

        # Start icons configuration
        self.start_icon = PhotoImage(file='icons/start.png')
        self.start_button = Button(self.top, text="START", image=self.start_icon, compound=LEFT, font="ariel 12 bold"
                                   , state='normal', command=self.start_event)
        self.start_button.pack(side=LEFT, padx=10)

        # Stop icons configuration
        self.stop_icon = PhotoImage(file='icons/stop1.png')
        self.stop_button = Button(self.top, text="STOP", image=self.stop_icon, compound=LEFT, font="ariel 12 bold",
                                  state='disabled', command=self.stop_event)
        self.stop_button.pack(side=LEFT, padx=10)

        # Restart icons configuration
        self.restart_icon = PhotoImage(file='icons/restart1.png')
        self.restart_button = Button(self.top, text="RESTART", image=self.restart_icon, compound=LEFT,
                                     font="ariel 12 bold", command=self.restart_event)
        self.restart_button.pack(side=LEFT, padx=10)

        # Restart icons configuration
        self.graph_icon = PhotoImage(file='icons/graph1.png')
        self.graph_button = Button(self.top, text="GRAPH", image=self.graph_icon, compound=LEFT, font="ariel 12 bold",
                                   command=self.graph_event)
        self.graph_button.pack(side=LEFT, padx=10)

        # Bottom Frame configuration design
        self.labelFrame = LabelFrame(self.bottom, height=150, width=600, text="Set configuration")
        self.labelFrame.pack(fill="both")
        self.var = IntVar()
        self.check_box = Checkbutton(self.labelFrame, variable=self.var, onvalue=1, offvalue=0, text="Include")
        self.check_box.grid(row=0, column=0, pady=5)
        self.label = Label(self.labelFrame, text="Character")
        self.label.grid(row=1, column=0, pady=5)
        self.entry = Entry(self.labelFrame, width=20)
        self.entry.grid(row=1, column=1, pady=10)
        self.labelFrame.pack(fill="both")

    def start_event(self):
        global running
        running = True
        if not press_stop:
            letter = self.entry.get()
            if letter and len(letter) == 1:
                if self.var.get() == 0:
                    self.gene = self.generator.generator_word(letter, "Exclude")
                else:
                    self.gene = self.generator.generator_word(letter, "Include")
            else:
                messagebox.showinfo("Typing Error", "You need to insert one character exactly ")
                return
        self.start_button['state'] = "disabled"
        self.stop_button['state'] = 'normal'
        self.entry['state'] = "disabled"
        self.check_box['state'] = "disabled"

        def retrieve():
            if running:
                try:
                    print(next(self.gene))
                except StopIteration:
                    print(f"------ Printing finished of words with letter {self.entry.get()}! ------")
                    self.start_button['state'] = "normal"
                    self.stop_button['state'] = 'disabled'
                    return

                self.start_button.after(1000, retrieve)

        retrieve()

    def stop_event(self):
        global running, press_stop
        running, press_stop = False, True
        self.start_button['state'] = "normal"
        self.stop_button['state'] = 'disabled'

    def restart_event(self):
        global press_stop, running
        press_stop, running = False, False
        self.entry.delete(0, 'end')
        self.var.set(0)
        self.start_button['state'] = "normal"
        self.stop_button['state'] = 'disabled'
        self.entry['state'] = "normal"
        self.check_box['state'] = "normal"
        print(f"------ Restarted the game! ------")

    def graph_event(self):
        self.graph.analysis_graph()
        self.graph.show_graph()


class Generator(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def generator_word(self, letter, flag):
        with open(self.file_name, 'r') as f:
            for line in f:
                for word in line.split(","):
                    if flag == "Include" and letter.lower() in word.lower():
                        yield word
                    if flag == "Exclude" and letter.lower() not in word.lower():
                        yield word


class Graph(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.character_dict = dict()

    def initialize_dict(self):
        for i in range(ord('a'), ord('k')):
            self.character_dict[chr(i)] = 0

    def analysis_graph(self):
        self.initialize_dict()
        with open(self.file_name, "r") as f:
            for line in f:
                for word in line.split(","):
                    for letter in word:
                        if letter in self.character_dict.keys():
                            self.character_dict[letter] = self.character_dict.get(letter) + 1

    def show_graph(self):
        import matplotlib.pyplot as plt
        character_list = [key for key in self.character_dict]
        frequency_list = [val for val in self.character_dict.values()]
        plt.bar(character_list, frequency_list, label="Frequency graph")
        plt.legend()
        plt.xlabel('Characters')
        plt.ylabel('Frequency')
        plt.title('Frequency Graph')
        plt.show()


if __name__ == '__main__':
    root = Tk()
    app = Application(root, Generator("file.txt"), Graph("file.txt"))
    root.mainloop()
