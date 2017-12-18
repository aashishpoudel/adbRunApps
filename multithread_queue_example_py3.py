from tkinter import *
import time
import os
from queue import *
import threading
from tkinter import ttk

websites_lists =["https://en.m.wikipedia.org/wiki/" + str(i) for i in range (1850,1880)]


class GUI:
    def __init__(self, master):
        self.master = master
        self.test_button = Button(self.master, command=self.tb_click)
        self.test_button.configure(
            text="Start", background="Grey",
            padx=50
            )
        self.test_button.pack(side=TOP)
        self.close_button = Button(self.master, command=self.tb_close)
        self.close_button.configure(
            text="CLose", background="Grey",
            padx=50
            )
        self.close_button.pack(side=TOP)

    def progress(self):
        self.prog_bar = ttk.Progressbar(
            self.master, orient="horizontal",
            length=200, mode="indeterminate"
            )
        self.prog_bar.pack(side=TOP)

    def tb_close(self):
        self.queue.put("Stop")
        time.sleep(1)
        self.master.quit()

    def tb_click(self):
        self.progress()
        self.prog_bar.start()
        self.queue = Queue()
        ThreadedTask(self.queue).start()
        #self.master.after(100, self.process_queue)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            print("Process_queue msg" +msg)
            # Show result of the task if needed
            if msg in "Stop":
                print(msg + "--print from process_queue")
                self.master.destroy()
            self.prog_bar.stop()
        except Empty:
            #print("The queue is empty -- printed from process_queue")
            self.master.after(100, self.process_queue)

class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        #time.sleep(5)
        #Simulate long running process
        for webpage in websites_lists:
            print(webpage)
            time.sleep(1)
            try:
                msg = self.queue.get(0)
                print("msg after close =" + msg +" (printed within webpage loop)")
                if msg in "Stop":
                    #self._stop_event.set()
                    break
            except:
                print("donothing")

            #mymsg = self.queue.get(0)
            #print(mymsg)



root = Tk()
root.title("Test Button")
main_ui = GUI(root)
root.mainloop()
