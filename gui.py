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
        populateJobPostings = """INSERT INTO JobPostings VALUES 
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
                                'Maintain and research Deep Learning algorithms for healthcare;develop and deploy ML models in AWS')

                            INSERT INTO JobPostings VALUES 
                                (2,
                                'QA Tester',
                                'Massa Incorporated',
                                'UK',
                                'Alajuela',
                                '937-3241 Eget St.',
                                '584',
                                TO_DATE('23-01-22','DD-MM-YY'),
                                32093,
                                83732,
                                'PHP,
                                Python,
                                SQL,
                                Perl,
                                HTML,
                                CSS',
                                'Write automated tests for various software products; document all bugs and other issues encountered; debug legacy software; make SQL queries to receive necessary information from database')

                            INSERT INTO JobPostings VALUES 
                                (3,
                                'Data Engineer',
                                'Etiam Consulting',
                                'UK',
                                'Salzgitter',
                                'P.O. Box 267,
                                2552 Amet,
                                Avenue',
                                '500',
                                TO_DATE('20-10-21','DD-MM-YY'),
                                40948,
                                96836,
                                'AWS,
                                Bash,
                                Pytorch,
                                Tensorflow,
                                Python,
                                Numpy,
                                Pandas',
                                'Assess clients needs and insurance risks; develop software to detect insurance fraud using Machine Learning;Deploy and maintain model on AWS')

                            INSERT INTO JobPostings VALUES 
                                (4,
                                'Fullstack Developer',
                                'In Mi Pede Limited',
                                'Mexico',
                                'Isnes',
                                'P.O. Box 506,2785 Sit Street',
                                '253',
                                TO_DATE('09-12-21','DD-MM-YY'),
                                43317,
                                96028,
                                'HTML,
                                CSS,
                                React,
                                Javascript,
                                SQL',
                                'Maintain the database; write high-quality code for our clients')

                                INSERT INTO JobPostings VALUES 
                                (
                                    21,
                                    'UI/UX Engineer',
                                    'Automize',
                                    'Canada',
                                    'Toronto',
                                    'Bay St',
                                    '350',
                                    TO_DATE('09-12-21','DD-MM-YY'),
                                    150000,
                                    180000,
                                    'HTML, CSS, JavaScript, ReactJS',
                                    'Create, design and maintain frontend depending on user and business needs'
                                )

                                INSERT INTO JobPostings VALUES 
                                (
                                    22,
                                    'Backend Developer',
                                    'Automize',
                                    'Canada',
                                    'Toronto',
                                    'Bay St',
                                    '350',
                                    TO_DATE('09-12-21','DD-MM-YY'),
                                    160000,
                                    180000,
                                    'Python, PHP, SQL, Server Management',
                                    'Expand and maintain backend development'
                                )

                                INSERT INTO JobPostings VALUES 
                                (
                                    23,
                                    'Full Stack Developer',
                                    'Automize',
                                    'Canada',
                                    'Toronto',
                                    'Bay St',
                                    '350',
                                TO_DATE('09-12-21','DD-MM-YY'),
                                    170000,
                                    190000,
                                    'HTML, CSS, JavaScript, ReactJS, Python, PHP, SQL, Server Management',
                                    'Work across teams with engineers and designers'
                                )

                                INSERT INTO JobPostings VALUES
                                (
                                    111, 'Web Developer', 'BMO', 'Canada', 'Ontario', 'Toronto', NULL, NULL, NULL, 100000, 100000, 'Sample Skills', 'Sample Reqs') 

                                INSERT INTO JobPostings VALUES
                                (
                                    222, 'Software Engineer', 'Twitter', 'Canada', 'Saskatchewan', 'Saskatoon', NULL, NULL, NULL, 300000, 300000, 'Sample Skills', 'Sample Reqs')

                                INSERT INTO JobPostings VALUES
                                (
                                    333, 'Full Stack Developer', 'Big Company', 'Canada', 'Ontario', 'Ottawa', NULL, NULL, NULL, 50000, 50000, 'Sample Skills', 'Sample Reqs')"""
        
        populateRecruiters  = """INSERT INTO Recruiters VALUES 
                                (
                                    1,
                                    'Corporate Recruiter',
                                    'Pretium Neque Morbi Incorporated',
                                    'The auction house that sells a large collection of rare items including drawings,
                                    furniture,
                                    jewelry,
                                    and others',
                                    'Yuli',
                                    'Pierce',
                                    'neque@natoque.ca'
                                )

                                INSERT INTO Recruiters VALUES 
                                (
                                    2,
                                    'Career Advisor',
                                    'Bayes Incorporated',
                                    'IT company that prides itself on delivering the best ready-to-go server solutions for our clients',
                                    'Ruby',
                                    'Jacobs',
                                    'parturient.montes@placeratCrasdictum.co.uk'
                                )

                                INSERT INTO Recruiters VALUES 
                                (
                                    3,
                                    'Human Resources Officer',
                                    'Varius Incorporated',
                                    'One of the top 3 largest healthcare providers in US',
                                    'Meghan',
                                    'Francis',
                                    'turpis.Aliquam@nonhendreritid.co.uk'
                                )

                                INSERT INTO Recruiters VALUES 
                                (
                                    4,
                                    'Corporate Recruiter',
                                    'Maecenas Malesuada Fringilla Company',
                                    'The main importer of wine from all over Europe into Mexico.',
                                    'Oren',
                                    'Lane',
                                    'vulputate.nisi@Nam.ca'
                                )

                                INSERT INTO Recruiters VALUES 
                                (
                                    31,
                                    'Tech Lead',
                                    'Automize',
                                    'Automize technologies is the leader in automating your business needs and processes to introduce efficiencies and grow profits',
                                    'Bryce',
                                    'Larkin',
                                    'bryce.larkin@automize.com'
                                )

                                INSERT INTO Recruiters VALUES 
                                (
                                    32,
                                    'Business Analyst',
                                    'Automize',
                                    'Automize technologies is the leader in automating your business needs and processes to introduce efficiencies and grow profits',
                                    'Neill',
                                    'Caffrey',
                                    'neill.caffrey@automize.com'
                                )

                                INSERT INTO Recruiters VALUES
                                (
                                    1111111110, 'Recruiter', 'BMO', 'Sample Description', 'Bob', 'Smith', NULL, 'bobsmith@example.com'
                                )

                                INSERT INTO Recruiters VALUES
                                (
                                    2222222220, 'Recruitment Officer', 'Twitter', 'Sample Description', 'Jack', 'Jackson', 'J', 'jackjjackson@example.com'
                                )

                                INSERT INTO Recruiters VALUES
                                (
                                    3333333330, 'Super Recruiter', 'Big Company', 'Sample Description', 'Tony', 'Baloney', NULL, 'tbaloney@example.com'
                                )"""
        
        populateApplicants  = """INSERT INTO Applicants VALUES 
                                (
                                    5,
                                    'Daria',
                                    'Allison',
                                    To_DATE('20-09-85','DD-MM-YY'),
                                    'Virgin Islands,
                                    British',
                                    'Carleton',
                                    '170-3837 Tortor, Ave',
                                    '816',
                                    337,
                                    '39053-9090',
                                    'Cras.eget@sed.net',
                                    884,
                                    1631970315,
                                    'Work',
                                    'Manchester University',
                                    'Masters',
                                    'Computer Science',
                                    TO_DATE('01-09-10','DD-MM-YY'),
                                    TO_DATE('01-05-12','DD-MM-YY'),
                                    3.96,
                                    'Frontend Developer',
                                    'Sit Amet Associates',
                                    TO_DATE('01-06-12','DD-MM-YY'),
                                    NULL,
                                    'Japan',
                                    'Osaka',
                                    'Develop responsive websites for different platforms',
                                    'SQL,HTML,CSS,Swift,Bash',
                                    'Visual Studio Code,React',
                                    'English,Japanese',
                                    'Machine Learning,Linux',
                                    'dallison.test',
                                    'Personal Website'
                                )

                                INSERT INTO Applicants VALUES 
                                (
                                    6,
                                    'Desirae',
                                    'Kramer',
                                    TO_DATE('28-10-93','DD-MM-YY'),
                                    'Luxembourg',
                                    'Beringen',
                                    'P.O. Box 667,626 Sem Avenue',
                                    395,
                                    455,
                                    'Z7449',
                                    'nunc.est@pretiumet.co.uk',
                                    31,
                                    1283305781,
                                    'Main',
                                    'The University of Berlin',
                                    'Masters',
                                    'Computer Science',
                                    TO_DATE('01-09-08','DD-MM-YY'),
                                    TO_DATE('01-05-11','DD-MM-YY'),
                                    2,
                                    'Mobile Developer',
                                    'Ipsum Sodales LLC',
                                    TO_DATE('01-07-11','DD-MM-YY'),
                                    NULL,
                                    'UK',
                                    'Nelson',
                                    'Maintain and convert old Objective-C code into the Swift for IOS',
                                    'C++,
                                    Swift',
                                    'XCode,
                                    Visual Studio Code',
                                    'English,
                                    Russian',
                                    'Statistics,
                                    Machine Learning,
                                    DBMS',
                                    'github.com/kramer',
                                    'Github'
                                )

                                INSERT INTO Applicants VALUES 
                                (
                                    7,
                                    'Eliana',
                                    'Hoffman',
                                    TO_DATE('06-05-86','DD-MM-YY'),
                                    'Netherlands',
                                    'Millet',
                                    'Ap #540-2514 Orci,
                                    Road',
                                    952,
                                    355,
                                    'M46 3PP',
                                    'nisl.arcu@Praesenteudui.net',
                                    576,
                                    3135865588,
                                    'Main',
                                    'University of Amsterdam',
                                    'Phd',
                                    'Mathematics',
                                    TO_DATE('01-09-15','DD-MM-YY'),
                                    TO_DATE('01-05-17','DD-MM-YY'),
                                    4,
                                    'Data Engineer',
                                    'Dolor Company',
                                    TO_DATE('02-05-17','DD-MM-YY'),
                                    NULL,
                                    'Germany',
                                    'Frankfurt',
                                    'Creating Deep Learning models for healthcare',
                                    'C++,
                                    Python,
                                    SQL',
                                    'Visual Studio Code,
                                    Jupyter Notebook,
                                    Linux',
                                    'English,
                                    German,
                                    French',
                                    'CUDA Programming,
                                    Research Experience',
                                    'github.com/hoffman',
                                    'Github'
                                )

                                INSERT INTO Applicants VALUES 
                                (
                                    41,
                                    'Justin',
                                    'Uberti',
                                TO_DATE('09-12-89','DD-MM-YY'),
                                    'USA',
                                    'Seattle',
                                    'Downing St',
                                    '10',
                                    '11',
                                    'XYZXYZ',
                                    'justin.uberti@google.com',
                                    1,
                                    '123456789',
                                    'Business',
                                    'UC San Diego',
                                    'Bachelor of Science',
                                    'Math',
                                    TO_DATE('01-09-10','DD-MM-YY'),
                                    TO_DATE('01-05-12','DD-MM-YY'),
                                    3.8,
                                    'Tech Lead',
                                    'Google',
                                    TO_DATE('01-06-12','DD-MM-YY'),
                                    NULL,
                                    'USA',
                                    'Seattle',
                                    'I lead projects WebRTC and now I am leading Google Duo',
                                    'C++, Python, Java',
                                    'PyCharm, Chrome',
                                    'English',
                                    'Acting',
                                    'juberti.com',
                                    NULL
                                )

                                INSERT INTO Applicants VALUES 
                                (
                                    42,
                                    'Marissa',
                                    'Mayer',
                                    TO_DATE('01-12-74','DD-MM-YY'),
                                    'USA',
                                    'San Francisco',
                                    'Some St',
                                    '11',
                                    '12',
                                    'ABCABC',
                                    'marissa.mayer@yahoo.com',
                                    1,
                                    '987654321',
                                    'Business',
                                    'Stanford',
                                    'Bachelor of Arts',
                                    'Business Administration',
                                    TO_DATE('01-09-08','DD-MM-YY'),
                                    TO_DATE('01-05-11','DD-MM-YY'),
                                    3.95,
                                    'CEO',
                                    'Yahoo',
                                    TO_DATE('01-07-11','DD-MM-YY'),
                                    NULL,
                                    'USA',
                                    'San Francisco',
                                    'I was the CEO trying to save Yahoo',
                                    'C++, Python, Java',
                                    'None',
                                    'English',
                                    'Sword fighting',
                                    'mmayer.com',
                                    NULL
                                )

                                INSERT INTO Applicants VALUES 
                                (
                                    43,
                                    'Sheril',
                                    'Sandberg',
                                    TO_DATE('10-12-71','DD-MM-YY'),
                                    'USA',
                                    'San Francisco',
                                    'Crazy St',
                                    '13',
                                    '14',
                                    'IJKIJK',
                                    'sheril.sandberg@facebook.com',
                                    1,
                                    '987612345',
                                    'Business',
                                    'Harvard',
                                    'Bachelor of Arts',
                                    'Business Administration',
                                    TO_DATE('01-09-15','DD-MM-YY'),
                                    TO_DATE('01-05-17','DD-MM-YY'),
                                    3.5,
                                    'COO',
                                    'Facebook',
                                    TO_DATE('02-05-17','DD-MM-YY'),
                                    NULL,
                                    'USA',
                                    'San Francisco',
                                    'I am the COO trying to help Mark Zuckerburg stay alive',
                                    'None',
                                    'None',
                                    'English',
                                    'Painting',
                                    NULL,
                                    NULL
                                )

                                INSERT INTO Applicants VALUES
                                (
                                    1111111111, 'Kirill', 'Shmakov', NULL, TO_DATE('24/10/2000','DD/MM/YYYY'), 'Canada', 'Ontario', 'Toronto', 'Sample Street', '100', 'NULL', 'A1A 1A1', 'sample@sample.com', 1, 1234567890, 'mobile', 'Ryerson University', 'BSc', 'Computer Science', TO_DATE('07/07/2018','DD/MM/YYYY'), TO_DATE('04/10/2023','DD/MM/YYYY'), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Java, Python, C', 'Microsoft Office, Linux, Photoshop', 'English, Russian', 'Full Stack Development', 'Example Link', 'Example link name'
                                )

                                INSERT INTO Applicants VALUES
                                (
                                    2222222222, 'John', 'Lastname', NULL, TO_DATE('01/10/1990','DD/MM/YYYY'), 'Canada', 'Ontario', 'Ottawa', 'Sample Street', '50', '17', 'B2B 2B2', 'john@sample.com', 1, 2345678901, 'mobile', 'University of Toronto', 'BSc', 'Computer Science', TO_DATE('05/05/2008','DD/MM/YYYY'), TO_DATE('10/04/2016','DD/MM/YYYY'), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'JavaScript, HTML, CSS, PHP', 'Microsoft Office', 'English, Chinese', 'Web Development', 'Example Link', 'Example link name'
                                )
                                    
                                INSERT INTO Applicants VALUES
                                (
                                    3333333333, 'Experience', 'Man', NULL, TO_DATE('13/11/1980','DD/MM/YYYY'),'Canada','Quebec','Montreal','Sample Street', '1000', NULL, 'C3C 3C3', 'experienceman@sample.com', 1, 4545455555, 'mobile', 'University of Waterloo', 'BSc', 'Computer Science', TO_DATE('07/07/1998','DD/MM/YYYY'), TO_DATE('04/10/2003','DD/MM/YYYY'), 4.00, 'Software Developer', 'Google', TO_DATE('10/12/2003','DD/MM/YYYY'),NULL,'Canada','Toronto','Sample Description', 'Java,Python,C++, MySQL, Swift, Rust','Linux, Microsoft Office', 'English, French', 'Machine Learning, Web Development, Full Stack Development', 'Example link', 'Example link name'
                                )"""
        
        populateJobsApplied  = """INSERT INTO JobsApplied VALUES ('Applied',1,5)
                                    INSERT INTO JobsApplied VALUES ('Rejected',2,6)
                                    INSERT INTO JobsApplied VALUES ('Pending',3,7)
                                    INSERT INTO JobsApplied VALUES ('Applied',2,7)
                                    INSERT INTO JobsApplied VALUES ('Pending',23,43)
                                    INSERT INTO JobsApplied VALUES ('Applied',21,42)
                                    INSERT INTO JobsApplied VALUES ('Applied',111,1111111111)
                                    INSERT INTO JobsApplied VALUES ('Rejected',111,2222222222)
                                    INSERT INTO JobsApplied VALUES ('Pending',222,2222222222)
                                    INSERT INTO JobsApplied VALUES ('Accepted',222,3333333333)
                                    INSERT INTO JobsApplied VALUES ('Accepted',333,3333333333)"""
        
        populateJobsManaged = """INSERT INTO JobsManaged VALUES (1,1)
                                    INSERT INTO JobsManaged VALUES (2,2)
                                    INSERT INTO JobsManaged VALUES (3,3)
                                    INSERT INTO JobsManaged VALUES (4,4)
                                    INSERT INTO JobsManaged VALUES (21,31)
                                    INSERT INTO JobsManaged VALUES (22,32)
                                    INSERT INTO JobsManaged VALUES (23,31)
                                    INSERT INTO JobsManaged VALUES (21,32)
                                    INSERT INTO JobsManaged VALUES (111,1111111110)
                                    INSERT INTO JobsManaged VALUES (222,2222222220)
                                    INSERT INTO JobsManaged VALUES (333,3333333330)"""

        self.connection.cursor().execute(populateJobPostings)
        self.connection.cursor().execute(populateRecruiters)
        self.connection.cursor().execute(populateApplicants)
        self.connection.cursor().execute(populateJobsApplied)
        self.connection.cursor().execute(populateJobsManaged)

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
