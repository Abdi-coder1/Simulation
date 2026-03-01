from tkinter import *
from model import*
import random,time


root = Tk() # creat and setup the main graphical object

canvas = Canvas(root, bg="white", width=800, height=600) # setup window
canvas.pack()
#root.mainloop()  no need  if simulation loop is upp 


def to_canvas_coord(canvas,x): 
    """ 
    Given a position, calulate the corresponding coordinate on the screen.
    :param canvas; the current drawing canvas
    :param x; a vector object
    :return; a list for posetions
    """
    scale = canvas.winfo_reqheight()/20
    canvas_x = canvas.winfo_reqwidth()/2 + x.x * scale
    canvas_y = canvas.winfo_reqheight()/2 - x.y * scale

    canvas_vector = Vec(canvas_x,canvas_y)
    return [canvas_vector.x,canvas_vector.y] 

def move_oval_to(canvas, o, u1_vec, u2_vec):
    """
    Move a given Oval with its bounding box, to a new location.
    :param o; the current oval
    :param u1_vec,u2_vec; the two vector objects. 
    """
    u1_canvas_pos = to_canvas_coord(canvas,u1_vec)
    u2_canvas_pos = to_canvas_coord(canvas,u2_vec)
    canvas.coords(o, u1_canvas_pos[0], u1_canvas_pos[1], 
                  u2_canvas_pos[0], u2_canvas_pos[1])

def create_oval(canvas, particle):
    n = random.randrange(-10,10)
    o = canvas.create_oval(n,n,n+1,n+1)
    vector_pair = particle.bounding_box()
    move_oval_to(canvas,o,vector_pair[0],vector_pair[1])
    return o

def simulation_loop(f, timestep, particles):

    ovals = []
    for particle in particles:
        ovals.append(create_oval(canvas,particle))
    time_1 = time.time()
    

    while True: # the main simulation loop
    
        f(timestep,particles) # apply force ( change velocity)
        for p,o in zip(particles,ovals):
            p.inertial_move(dt = timestep)
            bounding_box = p.bounding_box()
            move_oval_to(canvas,o,bounding_box[0],bounding_box[1])
        time_2 = time.time()
        if (time_2 - time_1) > 1/30:
            canvas.update()
            time_1 = time_2
            print(particles[0].velocity.norm())
        


