#!/usr/bin/env python -i
import tkinter as tk

def handle_connect_to_db(event):
    #write the code to connect to db here
    print("Successfully connected to the database")

def handle_exit(window,button1,button2):
    print("Exiting...")
    update_window(window,button1,button2)
    print("in handle exit")

def create_window():
    """
    Create an initial window with 2 buttons
    """
    window=tk.Tk()
    window.geometry("600x400") #widthxheight
    window.title("Database GUI Connector")

    text="""Welcome to the database.
    Please click the button to connect.
    """
    greeting=tk.Label(text=text)
    greeting.pack()

    #create 2 frames for 2 buttons
    frame1 = tk.Frame(master=window,width=200,height=50)
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    frame2=tk.Frame(master=window,width=200,height=50)
    frame2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

    button1 = tk.Button(
        text="Establish Connection",
        width=15,
        height=5,
        bg="red",
        fg="black",
        master=frame1
    )
    
    button1.pack()

    button2 = tk.Button(
        text="Exit",
        width=15,
        height=5,
        bg="red",
        fg="black",
        master=frame2,
        command=handle_exit(window,button1,button2)
    )
    
    button2.pack()
    
    button1.bind("<Button-1>",handle_connect_to_db)
    #button2.bind("<Button-2>",handle_exit)

    return window,button1,button2

def update_window(window,button1,button2):
    """
    Delete the previous 2 buttons and update the window
    """
    button1.destroy()
    button2.destroy()

    #the text to use for the buttons
    new_text="CREATE tables,DROP tables,POPULATE tables,RUN a custom query".split(",")
    new_text=[[new_text[0],new_text[1]],[new_text[2],new_text[3]]]

    for i in range(2):
        for j in range(2):
            frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1)

        frame.grid(row=i, column=j)
        label = tk.Label(master=frame, text=new_text[i][j])
        label.pack()

window,button1,button2=create_window()
print(f"here")
#run an event loop
window.mainloop()
