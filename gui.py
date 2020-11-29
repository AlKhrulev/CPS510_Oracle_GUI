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
                          command=lambda: self.label.grid())
        self.buttonBottomLeft = tk.Button(self.root,
                          text = 'POPULATE TABLES',
                          command=lambda: self.label.grid_forget())
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
        createJobPostings = """CREATE TABLE JobPostings(
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

        createRecruiters = """CREATE TABLE Recruiters(
                                UserID NUMBER(10) PRIMARY KEY,
                                JobTitle VARCHAR2(40) NOT NULL,
                                CompanyName VARCHAR2(50) NOT NULL,
                                CompanyDescription VARCHAR2(300),
                                FirstName VARCHAR2(40) NOT NULL,
                                LastName VARCHAR2(40) NOT NULL,
                                MiddleName VARCHAR2(40),
                                Email VARCHAR2(320) UNIQUE)"""
        
        createApplicants = """CREATE TABLE Applicants(
                                UserID NUMBER(10) PRIMARY KEY,
                                FirstName VARCHAR2(40) NOT NULL,
                                LastName VARCHAR2(40) NOT NULL,
                                MiddleName VARCHAR2(40),
                                DateOfBirth DATE NOT NULL,
                                CurrentCountryName VARCHAR2(60) NOT NULL,
                                Province VARCHAR2(60) DEFAULT 'N/A',
                                CurrentCity VARCHAR2(90) NOT NULL,
                                StreetName VARCHAR2(50),
                                BuildingNumber VARCHAR2(5),
                                ApartmentNumber VARCHAR2(4) DEFAULT 'N/A',
                                PostalCode VARCHAR2(10),
                                Email VARCHAR2(320) UNIQUE NOT NULL,
                                CountryCode NUMBER(3) NOT NULL,
                                PhoneNumber NUMBER(10) NOT NULL,
                                Type VARCHAR2(20) NOT NULL,
                                InstitutionName VARCHAR2(100),
                                DegreeType VARCHAR2(50),
                                Major VARCHAR2(50),
                                MajorStartDate DATE,
                                MajorEndDate DATE,
                                CGPA NUMBER(3,2),
                                Title VARCHAR2(40),
                                CompanyName VARCHAR2(50),
                                JobStartDate DATE,
                                JobEndDate DATE,
                                JobCountryName VARCHAR2(60),
                                JobCity VARCHAR2(90),
                                Description VARCHAR2(300),
                                ProgrammingLanguages VARCHAR2(150) NOT NULL,
                                SoftwareTools VARCHAR2(300),
                                SpokenLanguages VARCHAR2(100),
                                OtherSkills VARCHAR2(300),
                                WebsiteLink VARCHAR2(300),
                                LinkName VARCHAR2(50))"""
        
        createJobsApplied = """CREATE TABLE JobsApplied(
                                ApplicationStatus VARCHAR(40) NOT NULL,
                                JobID NUMBER(10) REFERENCES JobPostings(JobID),
                                UserID NUMBER(10) REFERENCES Applicants(UserID),
                                PRIMARY KEY(UserID,JobID))"""
        
        createJobsManaged = """CREATE TABLE JobsManaged(
                                JobID NUMBER(10) REFERENCES JobPostings(JobID),
                                UserID NUMBER(10) REFERENCES Recruiters(UserID),
                                PRIMARY KEY(UserID,JobID))"""
        
        self.connection.cursor().execute(createJobPostings)
        self.connection.cursor().execute(createRecruiters)
        self.connection.cursor().execute(createApplicants)
        self.connection.cursor().execute(createJobsApplied)
        self.connection.cursor().execute(createJobsManaged)

    def populateTables(self):
        #TODO populate tables with INSERT INTO SQL Command
        populate = ""
        pass
    def dropTables(self):
        #TODO Drop tables with DROP TABLE SQL Command
        drop = ""
        pass
    def runCustomQuery(self):
        #TODO run a custiom query in a separate popup window
        
        query = simpledialog.askstring(title="Query", prompt=("Input Custom Query Here: " + " " * 100))
        self.connection.execute(query)
        
        result = self.connection.fetchall()
        
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
        self.buttonTopLeft.configure(text="CREATE TABLES")
        #return buttons to the window
        self.buttonTopRight.grid()
        self.buttonBottomLeft.grid()
        self.buttonBottomRight.grid()
        self.root.geometry("400x500")

if __name__=="__main__": 
    app = mainWindow()
