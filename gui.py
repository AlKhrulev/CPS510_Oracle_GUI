#!/usr/bin/env python
import tkinter as tk
import cx_Oracle
import config
from tkinter import N,S,W,E, simpledialog

class mainWindow():
    def __init__(self):
        self.root = tk.Tk()
        #self.label=tk.Label(self.root,
        #                   text = "Welcome to the database.\nPlease click the button to connect.")

        self.root.geometry("200x100")
        self.label=tk.Label(self.root)        
    
        #TODO change the button command once they are written
        self.buttonTopLeft = tk.Button(self.root,
                          text = 'Establish connection',
                          command=self.connect_to_db)
        self.buttonTopRight = tk.Button(self.root,
                          text = 'DROP TABLES',
                          command=self.dropTables)
        self.buttonBottomLeft = tk.Button(self.root,
                          text = 'POPULATE TABLES',
                          command=self.populateTables)
        self.buttonBottomRight = tk.Button(self.root,
                          text = 'RUN A CUSTOM QUERY',
                          command=self.runCustomQuery)
                          #command=lambda: self.label.grid())                     
       
        #for reference, don't delete yet padx=10, pady=10
        #
        self.buttonTopLeft.grid(column=0, row=0,sticky=N+S+E+W)
        self.buttonTopRight.grid(column=1, row=0,sticky=N+S+E+W)
        self.buttonBottomLeft.grid(column=0, row=1,sticky=N+S+E+W)
        self.buttonBottomRight.grid(column=1, row=1,sticky=N+S+E+W)
        self.label.grid(column=2, row=2,sticky=N+S+E+W)

        #set weight to make the window responsive
        for i in range(2):
            self.root.grid_rowconfigure(i,  weight =1)
        for i in range(2):
            self.root.grid_columnconfigure(i,  weight =1)

        #temporary hide the 3 other buttons
        self.buttonTopRight.grid_remove()
        self.buttonBottomLeft.grid_remove()
        self.buttonBottomRight.grid_remove()

        #run the mainloop
        self.root.mainloop()
    
    def quit(self):
        self.root.destroy()
    
    def createTables(self):
        #TODO Create tables through CREATE TABLE SQL Command
        # createTablesString = " ".join(open("createTables.txt", "r").read().split('\n'))
        createTablesString = """CREATE TABLE JobPostings(
                                JobID NUMBER(10) PRIMARY KEY,
                                JobTitle VARCHAR2(40) NOT NULL,
                                CompanyName VARCHAR2(50) NOT NULL,
                                CountryName VARCHAR2(50) NOT NULL,
                                Province VARCHAR2(60) DEFAULT 'N/A',
                                City VARCHAR2(90) NOT NULL,
                                StreetName VARCHAR2(50),
                                BuildingNumber VARCHAR2(5),
                                StartDate DATE,
                                SalaryStartRange NUMBER(7) ,
                                SalaryEndRange NUMBER(7),
                                RequiredSkills VARCHAR2(300) NOT NULL,
                                Responsibilities VARCHAR2(300) NOT NULL)"""

        self.connection.cursor().execute(createTablesString)


    def populateTables(self):
        #TODO populate tables with INSERT INTO SQL Command
        # populateTablesString = " ".join(open("populateTables.txt", "r").read().split('\n'))
        populateTablesString = """INSERT INTO JobPostings VALUES 
                                    (1,
                                    'Data Scientist',
                                    'Sapien Cras Incorporated',
                                    'Germany',
                                    'De Haan',
                                    '636-962 Cursus. Road',
                                    '247',
                                    TO_DATE('11-01-22','DD-MM-YY'),
                                    40971,
                                    57383,
                                    'Linux,
                                    Tensorflow,
                                    Python,
                                    Bash,
                                    Pandas,
                                    Numpy,
                                    Git',
                                    'Maintain and research Deep Learning algorithms for healthcare;develop and deploy ML models in AWS')"""

        self.connection.cursor().execute(populateTablesString)

    def dropTables(self):
        #TODO Drop tables with DROP TABLE SQL Command
        dropJobPostings = "DROP TABLE JobPostings CASCADE Constraints"
        dropRecruiters = "DROP TABLE Recruiters CASCADE Constraints"
        dropApplicants = "DROP TABLE Applicants CASCADE Constraints"
        dropJobsApplied = "DROP TABLE JobsApplied CASCADE Constraints"
        dropJobsManaged = "DROP TABLE JobsManaged CASCADE Constraints"

        self.connection.cursor().execute(dropJobPostings)
        self.connection.cursor().execute(dropRecruiters)
        self.connection.cursor().execute(dropApplicants)
        self.connection.cursor().execute(dropJobsApplied)
        self.connection.cursor().execute(dropJobsManaged)

    def runCustomQuery(self):
        #TODO run a custiom query in a separate popup window
        
        query = simpledialog.askstring(title="Query", prompt=("Input Custom Query Here: " + " " * 100))
        self.cursor.execute(query)
        
        result = self.cursor.fetchall()
        
        for x in result:
            print(x)
        pass

    def connect_to_db(self):
        """
        Connect to the Oracle DMBS and restore the right layout through
        self.restore_layout()
        """
        #TODO paste the db connect code here
        self.connection = None
        try:
            self.connection = cx_Oracle.connect(
                config.username,
                config.password,
                config.dsn,
                encoding=config.encoding)
            self.cursor = self.connection.cursor()
        
            # show the version of the Oracle Database
            print(self.connection.version)
        except cx_Oracle.Error as error:
            print(error)
        #restore the layout to the correct one
        self.restore_layout()

    def restore_layout(self):
        """
        Change the text on the right button and restore the other 3 buttons in the grid
        """
        #change the text on the top left button
        self.buttonTopLeft.configure(text="CREATE TABLES",command=self.createTables)
        #return buttons to the window
        self.buttonTopRight.grid()
        self.buttonBottomLeft.grid()
        self.buttonBottomRight.grid()
        self.root.geometry("400x500")

if __name__=="__main__": 
    app = mainWindow()
