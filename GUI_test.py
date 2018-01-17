import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=200, height=200)
canvas.pack(fill="both", expand=True)

ball = canvas.create_oval(50,0,100,50, fill="red")

def animate(obj_id):
    canvas.move(obj_id, 0, 3)
    x0,y0,x1,y1 = canvas.coords(obj_id)
    if y0 > canvas.winfo_height():
        canvas.coords(obj_id, 50,-50, 100, 0)
    canvas.after(50, animate, obj_id)

animate(ball)
root.mainloop()