import tkinter as tk
from collections import deque
import random
import math

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Queue Visualizer (Simple)")
        self.root.geometry("1000x600")

        self.case = "printer"
        self.running = False

        self.reset_data()
        self.build_ui()
        self.loop()

    def reset_data(self):
        self.queue = deque()
        self.printed = 0

        self.players = ["A","B","C","D","E"]
        self.hot_index = 0

        self.pq = []

        self.graph = {
            "A":["B","C"],
            "B":["D","E"],
            "C":["F"],
            "D":[],
            "E":[],
            "F":[]
        }
        self.visited = []
        self.bfs_q = deque(["A"])

        self.bandara_q = deque()
        self.counters = [None,None]
        self.timer = [0,0]
        self.served = 0

    def build_ui(self):
        top = tk.Frame(self.root)
        top.pack()

        for name in ["printer","hot","rs","bfs","bandara"]:
            tk.Button(top, text=name.upper(),
                      command=lambda n=name:self.switch(n)).pack(side="left")

        control = tk.Frame(self.root)
        control.pack()

        self.entry = tk.Entry(control)
        self.entry.pack(side="left")

        tk.Button(control, text="Enqueue", command=self.enqueue).pack(side="left")
        tk.Button(control, text="Dequeue", command=self.dequeue).pack(side="left")
        tk.Button(control, text="Start", command=lambda:self.set_run(True)).pack(side="left")
        tk.Button(control, text="Stop", command=lambda:self.set_run(False)).pack(side="left")
        tk.Button(control, text="Reset", command=self.reset).pack(side="left")

        self.canvas = tk.Canvas(self.root, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.stat = tk.Label(self.root, text="")
        self.stat.pack()

    def switch(self, c):
        self.case = c

    def set_run(self, val):
        self.running = val

    def reset(self):
        self.reset_data()

    def enqueue(self):
        val = self.entry.get()
        if val:
            if self.case == "printer":
                self.queue.append(val)
            elif self.case == "rs":
                self.pq.append((random.randint(0,3), val))
            elif self.case == "bandara":
                self.bandara_q.append(val)
            self.entry.delete(0,"end")

    def dequeue(self):
        if self.case == "printer" and self.queue:
            self.queue.popleft()
            self.printed +=1

    def loop(self):
        self.canvas.delete("all")

        if self.case=="printer":
            self.draw_printer()
        elif self.case=="hot":
            self.draw_hot()
        elif self.case=="rs":
            self.draw_rs()
        elif self.case=="bfs":
            self.draw_bfs()
        elif self.case=="bandara":
            self.draw_bandara()

        self.root.after(400, self.loop)

    # ======================
    def draw_printer(self):
        for i,item in enumerate(self.queue):
            x=50+i*80
            self.canvas.create_rectangle(x,300,x+60,350, fill="cyan")
            self.canvas.create_text(x+30,325,text=item, fill="black")

        if self.running and self.queue and random.random()<0.3:
            self.queue.popleft()
            self.printed+=1

        self.stat.config(text=f"Queue: {len(self.queue)} | Printed: {self.printed}")

    # ======================
    def draw_hot(self):
        cx,cy,r=500,300,180

        for i,p in enumerate(self.players):
            angle=i*(2*math.pi/len(self.players))
            x=cx+r*math.cos(angle)
            y=cy+r*math.sin(angle)

            self.canvas.create_oval(x-25,y-25,x+25,y+25, fill="blue")
            self.canvas.create_text(x,y,text=p, fill="white")

        if self.running and len(self.players)>1:
            self.hot_index=(self.hot_index+1)%len(self.players)

            if random.random()<0.1:
                self.players.pop(self.hot_index)

        self.stat.config(text=f"Players: {len(self.players)}")

    # ======================
    def draw_rs(self):
        self.pq.sort(key=lambda x:x[0])

        for i,(p,val) in enumerate(self.pq):
            x=50+i*80
            color=["red","orange","yellow","green"][p]
            self.canvas.create_rectangle(x,300,x+60,360, fill=color)
            self.canvas.create_text(x+30,330,text=val)

        if self.running and self.pq and random.random()<0.3:
            self.pq.pop(0)

        self.stat.config(text=f"Queue: {len(self.pq)}")

    # ======================
    def draw_bfs(self):
        pos={
            "A":(500,100),"B":(300,250),"C":(700,250),
            "D":(200,400),"E":(400,400),"F":(700,400)
        }

        for n in self.graph:
            for nei in self.graph[n]:
                self.canvas.create_line(*pos[n],*pos[nei], fill="white")

        for n in self.graph:
            color="green" if n in self.visited else "blue"
            x,y=pos[n]
            self.canvas.create_oval(x-25,y-25,x+25,y+25, fill=color)
            self.canvas.create_text(x,y,text=n, fill="white")

        if self.running and self.bfs_q:
            node=self.bfs_q.popleft()
            self.visited.append(node)

            for nei in self.graph[node]:
                if nei not in self.visited and nei not in self.bfs_q:
                    self.bfs_q.append(nei)

        self.stat.config(text=f"Visited: {len(self.visited)}")

    # ======================
    def draw_bandara(self):
        if self.running and random.random()<0.3:
            self.bandara_q.append(random.randint(1,99))

        for i,p in enumerate(self.bandara_q):
            x=50+i*60
            self.canvas.create_rectangle(x,400,x+40,440, fill="cyan")
            self.canvas.create_text(x+20,420,text=p)

        for i in range(2):
            x=400+i*200
            self.canvas.create_rectangle(x,200,x+100,300, fill="gray")

            if self.counters[i] is None and self.bandara_q:
                self.counters[i]=self.bandara_q.popleft()
                self.timer[i]=random.randint(2,5)

            if self.counters[i]:
                self.timer[i]-=1
                self.canvas.create_text(x+50,250,text=self.counters[i])

                if self.timer[i]<=0:
                    self.counters[i]=None
                    self.served+=1

        self.stat.config(text=f"Queue: {len(self.bandara_q)} | Served: {self.served}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()