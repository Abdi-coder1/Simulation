from tkinter import *
from turtle import bgcolor, color, fill
from model import*
import random,time


root = Tk() # creat and setup the main graphical object

canvas = Canvas(root, bg="white", width=600, height=600) # setup window
canvas.pack()
#root.mainloop()  no need  if simulation loop is upp 

def p_vel_update(canvas,particle,p_vel):
    pos_vec = particle.position
    vel_vec = particle.velocity
    pos_canvas = to_canvas_coord(canvas,pos_vec)
    vel_canvas = (canvas.winfo_reqheight()/20) *  vel_vec
    canvas.coords(p_vel,pos_canvas[0],pos_canvas[1],
                       pos_canvas[0]+vel_canvas.x/5,pos_canvas[1]-vel_canvas.y/5)
    
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
def walls(canvas,r):
    r_c=(600/20) * r
    canvas.create_rectangle(0, 0, 600, 60-r_c, fill='red')
    canvas.create_rectangle(0, 0, 60-r_c, 600, fill='red')
    canvas.create_rectangle(0, 600-(60-r_c), 600, 600, fill='red')
    canvas.create_rectangle(600-(60-r_c), 0, 600, 600, fill='red')

def simulation_loop(f, timestep, particles):
    """
    The main simulation loop creats particles, applies forces and 
    then updtaes thei positions. All by calling diffrent inherent attributes
    of tthe particle class and model python file.
    """
    fps = 60
    ovals = []
    for particle in particles:
        ovals.append(create_oval(canvas,particle))


    canvas.itemconfig(ovals[0], fill="blue") # higlight one particle
    pos_vec = particles[0].position
    vel_vec = particles[0].velocity
    pos_canvas = to_canvas_coord(canvas,pos_vec)
    vel_canvas = (canvas.winfo_reqheight()/20) *  vel_vec

    p_vel = canvas.create_line(pos_canvas[0],pos_canvas[1],
                       pos_canvas[0]+vel_canvas.x/5,pos_canvas[1]+vel_canvas.y/5,
                       arrow=LAST,width=2,fill = 'red' )
    


    while True:
        time_ac = 0 # seconds that simulation has run
        while True:
            print(particles[0].velocity.norm())
            time_1 = time.time()
            f(timestep,particles) # apply force (change velocity)
            for p,o in zip(particles,ovals):
                p.inertial_move(dt = timestep) #  move particle
                bounding_box = p.bounding_box()
                move_oval_to(canvas,o,bounding_box[0],bounding_box[1]) # move particle on screen
                p_vel_update(canvas,particles[0],p_vel)
            time_ac += (time.time()-time_1)
            if time_ac > 1/fps: # time to update
                break
        canvas.update()
            
        


