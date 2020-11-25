#!/usr/bin/env python -i
import tkinter as tk

def handle_connect_to_db(event):
    #write the code to connect to db here
    print("Successfully connected to the database")

def handle_exit(event):
    print("Exiting...")
    exit(0)

if __name__=="__main__":
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
        master=frame2
    )
    
    button2.pack()
    
    button1.bind("<Button-1>",handle_connect_to_db)
    button2.bind("<Button-2>",handle_exit)


    #must be present at the end
    window.mainloop()
