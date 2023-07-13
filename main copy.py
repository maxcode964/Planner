from dis import show_code
import tkinter.messagebox as tmsg
from dataclasses import field
from re import T
from select import select
from tkinter import *
from tkinter import font
from tkinter.ttk import Style
from turtle import bgcolor, width
from xml.dom.minidom import TypeInfo
from tkcalendar import *
from PIL import ImageTk, Image
from tktimepicker import *
import datetime as dt
from time import sleep
import smtplib
import sqlite3
from emailSender import *
def main():   
    conn = sqlite3.connect('PlannerDataBase.db')
    c = conn.cursor()
    # create a table
    #c.execute("DROP TABLE IF EXISTS REGISTRATIONINFO")
    c.execute('''CREATE TABLE IF NOT EXISTS REGISTRATIONINFO(register_Name TEXT,
                register_UserName TEXT,register_Gender TEXT, register_Password TEXT,register_DOB TEXT,register_Email TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS TASKSTODO(userName TEXT,taskTitle TEXT,
                taskDes TEXT,taskDate TEXT, taskTime TEXT,taskPriority TEXT,taskOrder TEXT)''')
    conn.commit()
    date = dt.datetime.now()

    def resetRegistration():
        registerNameEntry.delete(0, 'end')
        registerUserNameEntry.delete(0, 'end')
        registerPasswordEntry.delete(0, 'end')
        registerRePasswordEntry.delete(0, 'end')
        registerGenderMenu.set("Select Gender")
        registerDatePicker.set_date(dt.date.today())
        registerEmailEntry.delete(0, 'end')
        
    def registrationInfo():
        try:
            sts = 1
            register_Name = registerNameEntry.get()
            register_UserName = registerUserNameEntry.get()
            register_Gender = registerGenderMenu.get()
            register_Password = registerPasswordEntry.get()
            register_Repassword = registerRePasswordEntry.get()
            register_DOB = registerDOB.get()
            register_Email = registerEmailEntry.get()
            c.execute("SELECT * FROM REGISTRATIONINFO ")
            r = c.fetchall()
            if(register_Name == "" or register_UserName == "" or register_Gender == "" or register_Password == "" or register_DOB == "" or register_Email == ""):
                tmsg.showinfo("NOTE", "Please fill all the information")
            else:
                for i in r:
                    if(i[1] == register_UserName):
                        sts = 0
                        break
                if(sts == 0):
                    tmsg.showinfo("NOTE", "Username already exist")
                elif(len(register_Password) < 5):
                    tmsg.showinfo(
                        "NOTE", "Password should contain atleast 5 characters")
                elif(register_Repassword!=register_Password):
                    tmsg.showinfo(
                        "NOTE", "Passwords donot match")
                else:
                    c.execute("INSERT INTO REGISTRATIONINFO VALUES (?,?,?,?,?,?)", (register_Name,
                                                                                    register_UserName, register_Gender, register_Password, register_DOB, register_Email))
                    conn.commit()
                    tmsg.showinfo(
                        "STATUS", f"{register_Name} registered successfully")
                    resetRegistration()
                    registerFrame.forget()
                    loginFrame.pack(fill=BOTH, expand=True)

        except sqlite3.Error as er:
            tmsg.showinfo("STATUS", er)

    def deleteAcc():
        try:
            c.execute("DELETE FROM REGISTRATIONINFO where register_UserName=?",(userNameSecLabel.cget("text"),))
            conn.commit()
            c.execute("DELETE FROM TASKSTODO where UserName=?",(userNameSecLabel.cget("text"),))
            conn.commit()
            tmsg.showinfo("STATUS","Account deleted successfully")
            signOut()
        except sqlite3.Error as er:
            tmsg.showinfo("STATUS",er)

    def login1():
        changeToMain()

    def isOne(num):
        if num==1:
            return 0
        else:
            return 1

    def login():
        try:
            login.login_UserName = loginUserName.get()
            login.login_Password = loginPassword.get()
            c.execute("VACUUM") 
            c.execute("SELECT rowid,* FROM TASKSTODO where UserName=?",
                      (login.login_UserName,))
            r1 = c.fetchall()
            login.NoOfTasks=len(r1)

            c.execute("SELECT * FROM REGISTRATIONINFO where register_UserName=?",
                      (login.login_UserName,))
            r = c.fetchall()
            if(login.login_UserName == "" or login.login_Password == ""):
                tmsg.showinfo("NOTE", "Please fill all the information")
            elif(r == []):
                tmsg.showinfo("STATUS", "Details not found")
            elif(login.login_Password != r[0][3]):
                tmsg.showinfo("STATUS", "Wrong Password")
            else:
                changeToMain()
                loginUserName.delete(0, 'end')
                loginPassword.delete(0, 'end')
                # AccountSet
                namesetLabel.config(text=r[0][0])
                genderSetLabel.config(text=r[0][2])
                DOBSetLabel.config(text=r[0][4])
                # SecuritySet
                namesecLabel.config(text=r[0][0])
                userNameSecLabel.config(text=r[0][1])
                passSecLabel.config(text="*******")
                #TaskInMainWin
                j=1
                for i in r1:
                    Task.task(i[2],i[3],i[4],i[5],int(i[6]),isOne(int(j)),j)
                    j=j+1
                    #Task.task("Hello", "Hello World", 16, "22:00", 4, 1, 3)

        except sqlite3.Error as er:
            tmsg.showinfo("STATUS", er)


    def recoveryPass():
        try:
            recovery_UserName = forgotPass.recoveryUserName.get()
            recovery_Email = forgotPass.recoveryEmail.get()
            recovery_DOB = forgotPass.recoveryDOB.get()

            c.execute("SELECT * FROM REGISTRATIONINFO where register_UserName=?", (recovery_UserName,))
            r = c.fetchall()
            if(recovery_UserName == "" or recovery_Email == "" or recovery_DOB == ""):
                tmsg.showinfo("NOTE", "Please fill all the information")
            elif(r == []):
                tmsg.showinfo("STATUS", "Username not found")
            elif(recovery_Email != r[0][5]):
                tmsg.showinfo("STATUS", "Please enter the registered Email")
            elif(recovery_DOB != r[0][4]):
                tmsg.showinfo("STATUS", "Wrong DOB")
            else:
                sender_mail = 'plannerbypce@gmail.com'
                receivers_mail = [recovery_Email]
                message = f"""
                Username  :- {r[0][1]}
                Passoword :- {r[0][3]}
                """
                try:
                    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
                    smtpObj.starttls()
                    smtpObj.login(sender_mail, "imamagqvdsngofrl")
                    smtpObj.sendmail(sender_mail, receivers_mail, message)
                    smtpObj.quit()
                    forgotPass.recoveryUserName.delete(0, 'end')
                    forgotPass.recoveryEmail.delete(0, 'end')
                    forgotPass.recoveryDOB.delete(0, 'end')
                    print("Successfully sent email")
                    tmsg.showinfo(
                        "STATUS", "Please read the Email send to your registered Email-ID")

                except Exception:
                    print("Error: unable to send email")

        except sqlite3.Error as er:
            tmsg.showinfo("STATUS", er)

    

    def passShow():
        passShowButton.forget()
        # passHide.passShowButton.forget()
        passHideImg1 = Image.open('images\\hide.png')
        passHideImg = passHideImg1.resize((32, 32))
        photo = ImageTk.PhotoImage(passHideImg)
        passShow.passHideButton = Button(
            loginFrame, image=photo, bg='#d1d1d1', borderwidth=0, activebackground='#d1d1d1', command=passHide)
        passShow.passHideButton.image = photo
        passShow.passHideButton.place(x=1172, y=368)
        loginPassword.config(show='')
    def passHide():
        passShow.passHideButton.forget()
        passShowImg1 = Image.open('images\\show.png')
        passShowImg = passShowImg1.resize((32, 32))
        photo = ImageTk.PhotoImage(passShowImg)
        passHide.passShowButton = Button(
            loginFrame, image=photo, bg='#d1d1d1', borderwidth=0, activebackground='#d1d1d1', command=passShow)
        passHide.passShowButton.image = photo
        passHide.passShowButton.place(x=1172, y=368)
        loginPassword.config(show='*')

    def passShowsec():
        passShowButtonsec.forget()
        # passHide.passShowButton.forget()
        passHideImg1sec = Image.open('images\\hide1.png')
        passHideImgsec = passHideImg1sec.resize((32, 32))
        photo = ImageTk.PhotoImage(passHideImgsec)
        passShowsec.passHideButtonsec = Button(
            securitySettingWinFrame, image=photo, bg='#313131', borderwidth=0, activebackground='#313131', command=passHidesec)
        passShowsec.passHideButtonsec.image = photo
        passShowsec.passHideButtonsec.place(x=830, y=395)
        c.execute("SELECT * FROM REGISTRATIONINFO where register_UserName=?",
                       (userNameSecLabel.cget("text"),))
        r = c.fetchall()
        passSecLabel.config(text=r[0][3]) 
    def passHidesec():
        passShowsec.passHideButtonsec.forget()
        passShowImg1sec = Image.open('images\\show1.png')
        passShowImgsec = passShowImg1sec.resize((32, 32))
        photo = ImageTk.PhotoImage(passShowImgsec)
        passHidesec.passShowButtonsec = Button(
            securitySettingWinFrame, image=photo, bg='#313131', borderwidth=0, activebackground='#313131', command=passShowsec)
        passHidesec.passShowButtonsec.image = photo
        passHidesec.passShowButtonsec.place(x=830, y=395)
        passSecLabel.config(text='*******')

    def changeToSet():
        mainFrame1.forget()
        settingWinMain.pack(fill=BOTH, expand=True)


    def changeToMain():
        mainFrame1.pack(fill=BOTH, expand=True)
        loginFrame.forget()
        settingWinMain.forget()
        accSettingWinFrame.pack(fill=BOTH, expand=True)
        securitySettingWinFrame.forget()


    def changeToRegistration():
        registerFrame.pack(fill=BOTH, expand=True)
        loginFrame.forget()

    def signOut():
        root.destroy()
        main()

    def changeToLogin():
        registerFrame.forget()
        settingWinMain.forget()
        accSettingWinFrame.forget()
        loginFrame.pack(fill=BOTH, expand=True)


    def changeToLoginByRegister():

        settingWinMain.forget()
        accSettingWinFrame.forget()

        registrationInfo()


    def changeToSecuritySettingWin():
        securitySettingWinFrame.pack(fill=BOTH, expand=True)
        accSettingWinFrame.forget()


    def changeToAccSetting():
        accSettingWinFrame.pack(fill=BOTH, expand=True)
        securitySettingWinFrame.forget()
        # settingAccWin.forget()


    def forgotPass1():
        login_UserName = loginUserName.get()
        login_Password = loginPassword.get()
        if(login_UserName == ""):
            tmsg.showinfo("Note", "Please enter Username")
        else:
            forgotPass()


    def forgotPass():
        root2 = Toplevel()
        root2.geometry("605x400")
        root2.maxsize(605,400)
        root2.title("Forgot Password")
        # frame
        inFrame3 = Frame(root2, bg='#313131', width='605', height=400)
        inFrame3.place(x=0, y=0)
        # img
        inImg3 = Image.open('images\\forgotPasswordWin.png')
        # createTaskImg=inImg1.resize((,674))
        photo = ImageTk.PhotoImage(inImg3)
        forgotPassImageLabel = Label(inFrame3, image=photo, bg='#313131')
        forgotPassImageLabel.image = photo
        forgotPassImageLabel.place(x=0, y=0)
        forgotPass.recoveryUserName = Entry(inFrame3, width='30', font=(
            'Times', 17), bg='#313131', borderwidth=0, fg='#d1d1d1', insertbackground='#d1d1d1')
        forgotPass.recoveryUserName.place(x=30, y=100)
        forgotPass.recoveryEmail = Entry(inFrame3, width='30', font=(
            'Times', 17), bg='#313131', borderwidth=0, fg='#d1d1d1', insertbackground='#d1d1d1')
        forgotPass.recoveryEmail.place(x=30, y=174)
        forgotPass.recoveryDOB = Entry(inFrame3, width='30', font=(
            'Times', 17), bg='#313131', borderwidth=0, fg='#d1d1d1', insertbackground='#d1d1d1')
        forgotPass.recoveryDOB.place(x=30, y=248)
        # Submit Button
        recoverySubmitButtonImg = Image.open('images\\submitButton.png')
        photo = ImageTk.PhotoImage(recoverySubmitButtonImg)
        recoverySubmitButton = Button(inFrame3, image=photo, bg='#313131',
                                      borderwidth=0, activebackground='#313131', command=recoveryPass)
        recoverySubmitButton.image = photo
        recoverySubmitButton.place(x=463, y=333)
        # Cancel Button
        recoveryCancelButtonImg = Image.open('images\\cancelButton.png')
        photo = ImageTk.PhotoImage(recoveryCancelButtonImg)
        recoveryCancelButton = Button(inFrame3, image=photo, bg='#313131',
                                      command=root2.destroy, borderwidth=0, activebackground='#313131')
        recoveryCancelButton.image = photo
        recoveryCancelButton.place(x=342, y=333)
        root2.mainloop()


    def deleteTaskWin():
        delWin=Toplevel()
        delWin.geometry("605x400")
        delWin.maxsize(605,400)
        delWin.title("Delete Task")

        delWinFrame=Frame(delWin, bg='#313131', width='605', height=400)
        delWinFrame.place(x=0, y=0)
        # image
        inImg1 = Image.open('images\\deleteTask.png')
       # createTaskImg=inImg1.resize((,674))
        photo = ImageTk.PhotoImage(inImg1)
        deleteTaskImageLabel = Label(delWinFrame, image=photo, bg='#313131')
        deleteTaskImageLabel.image = photo
        deleteTaskImageLabel.place(x=0, y=0)

        TaskTitleEntry= Entry(delWinFrame, width='17', font=(
            'Times', 20), bg='#313131', borderwidth=0, fg='white', insertbackground='white')
        TaskTitleEntry.place(x=325, y=150)
        def deleteTask():
            c.execute("DELETE FROM TASKSTODO where  taskTitle=?  and userName=?",(TaskTitleEntry.get(),userNameSecLabel.cget("text")))
            conn.commit()

            c.execute("VACUUM")
            c.execute("SELECT rowid,* FROM TASKSTODO where UserName=?",
                      (userNameSecLabel.cget("text"),))
            r1 = c.fetchall()
            j=1
            for i in r1:
                Task.task(i[2],i[3],i[4],i[5],int(i[6]),isOne(int(j)),j)
                j=j+1
            delWin.destroy()
        # Submit Button
        submitbtn = Image.open('images\\submitButton.png')
        # subImg=img4.resize((43,43))
        photo = ImageTk.PhotoImage(submitbtn)
        subImageButton = Button(delWinFrame, image=photo, bg='#313131', borderwidth=0, activebackground='#313131',command=deleteTask)
        subImageButton.image = photo
        subImageButton.place(x=463, y=333)
        # Cancel Button
        cancel = Image.open('images\\cancelButton.png')
        # cancelImg=img4.resize((43,43))
        photo = ImageTk.PhotoImage(cancel)
        cancelImageButton = Button(delWinFrame, image=photo, bg='#313131',
                                   command=delWin.destroy, borderwidth=0, activebackground='#313131')
        cancelImageButton.image = photo
        cancelImageButton.place(x=342, y=333)

        delWin.mainloop()

    def creatTaskWin():
        creatTaskWin.root1 = Toplevel()
        creatTaskWin.root1.geometry("535x674")
        creatTaskWin.root1.title("Create Task")
        # Frame
        inFrame1 = Frame(creatTaskWin.root1, bg='#313131', width='535', height=674)
        inFrame1.place(x=0, y=0)
        # image
        inImg1 = Image.open('images\\createtask1.png')
       # createTaskImg=inImg1.resize((,674))
        photo = ImageTk.PhotoImage(inImg1)
        createTaskImageLabel = Label(inFrame1, image=photo, bg='#313131')
        createTaskImageLabel.image = photo
        createTaskImageLabel.place(x=0, y=0)
        # inLabel1=Label(inFrame1,text='Create Task',font=('yu gothic ui',25,'bold'),bg='#313131')
        # inLabel1.place(x=60,y=5)
        creatTaskWin.createTaskTitleEntry= Entry(inFrame1, width='30', font=(
            'Times', 20), bg='#313131', borderwidth=0, fg='white', insertbackground='white')
        creatTaskWin.createTaskTitleEntry.place(x=21, y=117)

        creatTaskWin.createTaskDesEntry= Text(inFrame1, width='35', height=5, font=(
            'Times', 20), fg='white', insertbackground='white', bg='#313131', borderwidth=0)
        creatTaskWin.createTaskDesEntry.place(x=20, y=192)
        # Datepicker
        creatTaskWin.dateSelected=StringVar()
        creatTaskWin.datePicker = DateEntry(inFrame1,textvariable=creatTaskWin.dateSelected, width=10, font=('Times', 15), fg='white', date_pattern="dd-mm-y")
        creatTaskWin.datePicker.set_date(dt.datetime.today())
        creatTaskWin.datePicker.place(x=25, y=400)
        # TimePicker 
        creatTaskWin.timeSelected=StringVar()    
        
        creatTaskWin.timePicker = Entry(inFrame1, width='10', font=(
                                    'Times', 20), bg='#313131',validate='key', borderwidth=0, fg='white', insertbackground='white')
        creatTaskWin.timePicker.insert(0,current_time)
        creatTaskWin.timePicker.place(x=245, y=400)
        '''
        creatTaskWin.timeSelected=StringVar()
        creatTaskWin.timePicker = SpinTimePickerModern(inFrame1)
        creatTaskWin.timePicker.addAll(constants.HOURS24)
        creatTaskWin.timePicker.configureAll(bg="#313131", height=1, width=2, fg="white", font=("Times", 16), hoverbg="#313131",
                                hovercolor="#313131", clickedbg="#313131", clickedcolor="white")
        creatTaskWin.timePicker.configure_separator(bg="#313131", fg="#ffffff")
        creatTaskWin.timePicker.place(x=245, y=400)'''
        # Setpriority
        creatTaskWin.taskMenu = StringVar()
        creatTaskWin.taskMenu.set("Set Priority")
        creatTaskWin.setPriority = OptionMenu(inFrame1, creatTaskWin.taskMenu, "Low", "Medium", "High","Very High")
        creatTaskWin.setPriority.config(bg="#313131", border=0, fg="WHITE",
                           font=('Times', 15), highlightthickness=0)

        creatTaskWin.setPriority["menu"].config(bg="#313131", fg='white')
        creatTaskWin.setPriority.place(x=25, y=473)

        # Submit Button
        img4 = Image.open('images\\submitButton.png')
        # subImg=img4.resize((43,43))
        photo = ImageTk.PhotoImage(img4)
        subImageButton = Button(inFrame1, image=photo, bg='#313131', borderwidth=0, activebackground='#313131',command=addTask)
        subImageButton.image = photo
        subImageButton.place(x=415, y=598)
        # Cancel Button
        img5 = Image.open('images\\cancelButton.png')
        # cancelImg=img4.resize((43,43))
        photo = ImageTk.PhotoImage(img5)
        cancelImageButton = Button(inFrame1, image=photo, bg='#313131',
                                   command=creatTaskWin.root1.destroy, borderwidth=0, activebackground='#313131')
        cancelImageButton.image = photo
        cancelImageButton.place(x=294, y=598)
        creatTaskWin.root1.mainloop()

    def addTask():
        c.execute("SELECT rowid,* FROM TASKSTODO where UserName=?",
                      (userNameSecLabel.cget("text"),))
        r1 = c.fetchall()

        c.execute("SELECT * FROM REGISTRATIONINFO where register_UserName=?",
                      (userNameSecLabel.cget("text"),))
        r2 = c.fetchall()
        if(r1==[]):
            firstcall=1
        else:
            firstcall=0
        login.NoOfTasks=login.NoOfTasks+1
        taskTitle= creatTaskWin.createTaskTitleEntry.get()
        taskDes=creatTaskWin.createTaskDesEntry.get("1.0","end-1c")
        taskDate=creatTaskWin.dateSelected.get()
        taskTime=creatTaskWin.timePicker.get()
        taskPriority=creatTaskWin.taskMenu.get()
        if(taskTitle=="" or taskDes=="" or taskDate=="" or taskTime=="" or taskPriority==""):
            tmsg.showwarning("Warinig","Fill all the fields")
        else:
            if(taskPriority=="Low"):
                priNo=1
            elif(taskPriority=="Medium"):
                priNo=2
            elif(taskPriority=="High"):
                priNo=3
            elif(taskPriority=="Very High"):
                priNo=4
            if(firstcall==1):
                Task.task(taskTitle, taskDes, taskDate, taskTime, priNo, 0, login.NoOfTasks)
            else:
                Task.task(taskTitle, taskDes, taskDate, taskTime, priNo, 1, login.NoOfTasks)
            c.execute("INSERT INTO TASKSTODO VALUES (?,?,?,?,?,?,?)",(userNameSecLabel.cget("text"),taskTitle,taskDes,taskDate, taskTime,priNo,login.NoOfTasks))
            conn.commit()
            taskEmail(r2[0][5], taskTitle,taskDes, taskDate,taskTime,priNo)
            creatTaskWin.root1.destroy()

    root = Tk()
    root.geometry("1280x720")
    root.title("Planner")


    # loginFrame
    loginFrame = Frame(root)
    loginFrame.pack(fill=BOTH, expand=True)
    # Giving Dimensions and background image
    loginImg = PhotoImage(file='images//loginWin.png', master=loginFrame)
    loginImg_label = Label(loginFrame, image=loginImg)
    loginImg_label.place(x=-1, y=0)
    # Placing Submit Button
    loginSubmitButtonImg = PhotoImage(
        file="images//loginSubmitButton.png", master=loginFrame)
    loginSubmitButton = Button(loginFrame, image=loginSubmitButtonImg, border=0,
                               background="#d1d1d1", activebackground="#d1d1d1", command=login)
    loginSubmitButton.place(x=1113, y=449)
    # Placing forgotPassword Button
    forgotPasswordButton = PhotoImage(
        file="images//forgotPasswordButton.png", master=loginFrame)
    forgotPassword = Button(loginFrame, image=forgotPasswordButton, border=0,
                            background="#d1d1d1", activebackground="#d1d1d1", command=forgotPass1)
    forgotPassword.place(x=1111, y=508)
    # Placing register Button
    registerButton = PhotoImage(file="images//registerButton.png")
    register = Button(loginFrame, image=registerButton, border=0,
                      background="#d1d1d1", activebackground="#d1d1d1", command=changeToRegistration)
    register.place(x=821, y=671)
    # Placing Text Entry of Username
    loginUserName = Entry(loginFrame, background="#d1d1d1",
                          border=0, width=40, font=("Inter", 15))
    loginUserName.place(x=764, y=290, height=43)
    # Placing Text Entry of Password
    loginPassword = Entry(loginFrame, background="#d1d1d1", border=0,
                          width=40, show="*", font=("Inter", 15))
    loginPassword.place(x=764, y=363, height=43)
    # Placing show hide Password button
    passShowImg1 = Image.open('images\\show.png')
    passShowImg = passShowImg1.resize((32, 32))
    photo = ImageTk.PhotoImage(passShowImg)
    passShowButton = Button(loginFrame, image=photo, bg='#d1d1d1',
                            borderwidth=0, activebackground='#d1d1d1', command=passShow)
    passShowButton.image = photo
    passShowButton.place(x=1172, y=368)


    # registrationWindow Frame
    registerFrame = Frame(root)
    # registerFrame.pack(fill=BOTH,expand=True)
    # registrationImage
    registrationWinImg = Image.open('images\\registrationWin.png')
    photo = ImageTk.PhotoImage(registrationWinImg)
    registrationWinLabel = Label(registerFrame, image=photo, bg='#313131')
    registrationWinLabel.image = photo
    registrationWinLabel.place(x=-2, y=-2)
    # registrationName
    registerNameEntry = Entry(registerFrame, width='31', bg='#D1D1D1', fg='#313131',
                              borderwidth=0, insertbackground='black', font=("Inter", 18))
    registerNameEntry.place(x=100, y=162)
    # registrationUserName
    registerUserNameEntry = Entry(registerFrame, width='31', bg='#D1D1D1',
                                  fg='#313131', borderwidth=0, insertbackground='black', font=("Inter", 18))
    registerUserNameEntry.place(x=100, y=235)
    # SetGender
    registerGenderMenu = StringVar()
    registerGenderMenu.set("Select Gender")
    setRegisterGender = OptionMenu(
        registerFrame, registerGenderMenu, "Male", "Female", "Other")
    setRegisterGender.config(bg="#D1D1D1", border=0, fg="#313131", font=(
        'Times', 15), highlightthickness=0)
    setRegisterGender["menu"].config(bg="#D1D1D1", fg='#313131')
    setRegisterGender.place(x=100, y=306)
    # registrationPassword
    registerPasswordEntry = Entry(registerFrame, width='31', bg='#D1D1D1', fg='#313131',
                                  show='*', borderwidth=0, insertbackground='black', font=("Inter", 18))
    registerPasswordEntry.place(x=100, y=381)
    # registrationRePassword
    registerRePasswordEntry = Entry(registerFrame, width='31', bg='#D1D1D1', fg='#313131',
                                    show='*', borderwidth=0, insertbackground='black', font=("Inter", 18))
    registerRePasswordEntry.place(x=100, y=454)
    # registerDOBpicker
    registerDOB = StringVar()
    registerDatePicker = DateEntry(registerFrame, width=10, font=(
        'Times', 15), fg='white', textvariable=registerDOB, date_pattern="dd-mm-y")
    registerDatePicker.set_date(date.today())
    registerDatePicker.place(x=100, y=527)
    # registration-loginbackbutton
    registrationLoginBackButtonImg = Image.open(
        'images\\registrationBackButton.png')
    photo = ImageTk.PhotoImage(registrationLoginBackButtonImg)
    registrationLoginBackButton = Button(
        registerFrame, image=photo, bg='#D1D1D1', borderwidth=0, activebackground='#D1D1D1', command=changeToLogin)
    registrationLoginBackButton.image = photo
    registrationLoginBackButton.place(x=0, y=0)
    # registrationEmail
    registerEmailEntry = Entry(registerFrame, width='31', bg='#D1D1D1',
                               fg='#313131', borderwidth=0, insertbackground='black', font=("Inter", 18))
    registerEmailEntry.place(x=100, y=600)
    # registrationSubmitButton
    registrationSubmitButtonImg = Image.open('images\\registerSubmitButton.png')
    photo = ImageTk.PhotoImage(registrationSubmitButtonImg)
    registrationSubmitButton = Button(registerFrame, image=photo, bg='#D1D1D1',
                                      borderwidth=0, activebackground='#D1D1D1', command=changeToLoginByRegister)
    registrationSubmitButton.image = photo
    registrationSubmitButton.place(x=444, y=652)


    # ShowTaskWindow
    mainFrame1 = Frame(root)
    # mainFrame1.pack(fill=BOTH,expand=True)
    # ShowTaskWindowImg
    mainImg1 = Image.open('images\\planner.png')
    photo = ImageTk.PhotoImage(mainImg1)
    mainImg1Label = Label(mainFrame1, image=photo, bg='#313131')
    mainImg1Label.image = photo
    mainImg1Label.place(x=0, y=0)
    # AddTaskImg
    img1 = Image.open('images\\add.png')
    addTaskImg = img1.resize((48, 48))
    photo = ImageTk.PhotoImage(addTaskImg)
    addImgButton = Button(mainFrame1, image=photo, bg='#313131',
                          command=creatTaskWin, borderwidth=0, activebackground='#313131')
    addImgButton.image = photo
    addImgButton.place(x=12, y=15)
    # RemoveTaskImg
    img1 = Image.open('images\\delete.png')
    addTaskImg = img1.resize((65, 65))
    photo = ImageTk.PhotoImage(addTaskImg)
    addImgButton = Button(mainFrame1, image=photo, bg='#313131',
                          command=deleteTaskWin, borderwidth=0, activebackground='#313131')
    addImgButton.image = photo
    addImgButton.place(x=75, y=10)
   
    # SettingImg
    img2 = Image.open('images\\settingsButton.png')
    photo = ImageTk.PhotoImage(img2)
    settingImageButton = Button(mainFrame1, image=photo, bg='#313131',
                                command=changeToSet, borderwidth=0, activebackground='#313131')
    settingImageButton.image = photo
    settingImageButton.place(x=1205, y=1)
    # calendar
    frame2 = Frame(mainFrame1, bg='#313131', width=864, height=645)
    frame2.place(x=2, y=80)
    cal = Calendar(frame2, font="Times 35", selectmode='day',
                   year=2022, month=1, day=1, bgcolor='#313131')
    cal.pack(fill="both", expand=True)
    # taskImg
    img3 = Image.open('images\\todotask.png')
    taskImg = img3.resize((32, 32))
    photo = ImageTk.PhotoImage(taskImg)
    taskImageLabel = Label(mainFrame1, image=photo, bg='#313131')
    taskImageLabel.image = photo
    taskImageLabel.place(x=880, y=90)
    # taskLabel
    # label1 = Label(mainFrame1, text='Task to do', fg='white',
    #                bg='#313131', font=('Sans-serif', 27))
    # label1.place(x=930, y=85)
    # label2 = Label(mainFrame1, text='Nothing to do..', fg='white',
    #                bg='#313131', font=('yu gothic ui', 20,))
    # label2.place(x=950, y=150)

    # Tasks
    frame3 = Frame(mainFrame1, background="#313131", width=418, height=664)
    frame3.place(x=865, y=79)
    today = dt.datetime.today()
    t = today.strftime("%d %b")
    date = Label(frame3, text=t, font=("Inter", 20), background="#313131",
                 foreground="#d1d1d1")
    date.place(relx=0.1, rely=0.1)
    timeNow = dt.datetime.now()
    current_time = timeNow.strftime("%H  %M")
    container = Frame(frame3)
    canvas = Canvas(container)
    canvas.configure(height=664, width=408)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame.configure(height=664, width=408)

    class Task:

        def __init__(self, title, description, date, time, priority, type, order):
            self.title = title
            self.description = description
            self.date = date
            self.time = time
            self.priority = priority
            self.type = type
            self.order = order

        def task(title, description, date, time, priority, type, order):
            if(type == 0):
                cb = Checkbutton(scrollable_frame, text=title, font=("Inter", 15), image=offImg, compound='left', padx=20,
                                selectimage=onImg, indicatoron=False, background="#313131", activebackground="#313131", selectcolor="#313131", foreground="#d1d1d1", activeforeground="#d1d1d1", border=0)
                cb.place(x=42, y=133+(153*(order-1)))
                time = Label(scrollable_frame, text=time, font=("Inter", 10),
                            background="#313131", foreground="#d1d1d1")
                time.place(x=145, y=179)
                if(priority == 1):
                    pri = Label(scrollable_frame, image=priority1img,
                                background="#313131")
                    pri.place(x=188, y=181)
                elif(priority == 2):
                    pri = Label(scrollable_frame, image=priority2img,
                                background="#313131")
                    pri.place(x=188, y=181)
                elif(priority == 3):
                    pri = Label(scrollable_frame, image=priority3img,
                                background="#313131")
                    pri.place(x=188, y=181)
                elif(priority == 4):
                    pri = Label(scrollable_frame, image=priority4img,
                                background="#313131")
                    pri.place(x=188, y=181)

                des = Label(scrollable_frame, text=description, font=("Inter", 10),
                            background="#313131", foreground="#d1d1d1")
                des.place(x=145, y=199)
                d = Label(scrollable_frame, text=date, background="#313131",
                        foreground="#d1d1d1", font=("Inter", 10))
                d.place(x=145, y=219)
            else:
                cv = Canvas(scrollable_frame, width=60, height=100,
                            background="#313131", highlightthickness=0)
                cv.place(relx=0.153, y=46+(153*(order-1)))
                cv.create_line(30, 0, 30, 100, fill="#d1d1d1", width=2)
                cb = Checkbutton(scrollable_frame, text=title, font=("Inter", 15), image=offImg, compound='left', padx=20,
                                selectimage=onImg, indicatoron=False, background="#313131", activebackground="#313131", selectcolor="#313131", foreground="#d1d1d1", activeforeground="#d1d1d1", border=0)
                cb.place(relx=0.1, y=133+(153*(order-1)))
                time = Label(scrollable_frame, text=time, font=("Inter", 10),
                            background="#313131", foreground="#d1d1d1")
                time.place(x=140, y=27.5+(152.5*(order)))
                if(priority == 1):
                    pri = Label(scrollable_frame, image=priority1img,
                                background="#313131")
                    pri.place(x=188, y=29.5+(152.5*(order)))
                elif(priority == 2):
                    pri = Label(scrollable_frame, image=priority2img,
                                background="#313131")
                    pri.place(x=188, y=29.5+(152.5*(order)))
                elif(priority == 3):
                    pri = Label(scrollable_frame, image=priority3img,
                                background="#313131")
                    pri.place(x=188, y=29.5+(152.5*(order)))
                elif(priority == 4):
                    pri = Label(scrollable_frame, image=priority4img,
                                background="#313131")
                    pri.place(x=188, y=29.5+(152.5*(order)))

                des = Label(scrollable_frame, text=description, font=("Inter", 10),
                            background="#313131", foreground="#d1d1d1")
                des.place(x=140, y=46.5+(152.5*(order)))
                d = Label(scrollable_frame, text=date, background="#313131",
                        foreground="#d1d1d1", font=("Inter", 10))
                d.place(x=140, y=66.5+(152.5*(order)))
                if(order > 3):
                    scrollable_frame.configure(
                        height=664+(180*(order-3)), width=400)
    onImg = PhotoImage(file='images//OnButton.png', master=frame3)
    offImg = PhotoImage(file='images//OffButton.png', master=frame3)
    priority1img = PhotoImage(file='images//Priority1.png', master=frame3)
    priority2img = PhotoImage(file='images//Priority2.png', master=frame3)
    priority3img = PhotoImage(file='images//Priority3.png', master=frame3)
    priority4img = PhotoImage(file='images//Priority4.png', master=frame3)
    dropImg = PhotoImage(file='images//dropDownButton.png', master=frame3)
    firstcall=1
    order=1
    scrollable_frame.configure(background="#313131")
    date = Label(scrollable_frame, text=t, font=("Inter", 20), background="#313131",
                foreground="#d1d1d1")
    date.place(relx=0.1, y=66)

    container.pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.place(x=393,height=645)
    #Task.task("Spam", "I Am Spamming", 16, "20:00", 1, 0, 1)
    #Task.task("Hi", "Hey Everyone", 16, "21:00", 2, 1, 2)
    #Task.task("Hello", "Hello World", 16, "22:00", 4, 1, 3)
    def updateNameWin():
        root3 = Toplevel()
        root3.geometry('605x400')
        root3.maxsize(605,400)
        root3.title("Forgot Password")
        #frame
        inFrame4 = Frame(root3, bg='#313131', width='605', height=400)
        inFrame4.place(x=0, y=0)
        # img
        updateNameFrameImg = Image.open('images\\updateNameWin.png')
        photo = ImageTk.PhotoImage(updateNameFrameImg)
        updateNameFrameImgLabel = Label(inFrame4, image=photo, bg='#313131')
        updateNameFrameImgLabel.image = photo
        updateNameFrameImgLabel.place(x=0, y=0)
        #Entry
        nameUpdateEntry=Entry(root3, width='35', font=(
            'Times', 20), bg='#313131', borderwidth=0, fg='white', insertbackground='white')
        nameUpdateEntry.place(x=25,y=125)

        passFornameUpdateEntry=Entry(root3, width='35',show='*', font=(
            'Times', 20), bg='#313131', borderwidth=0, fg='white', insertbackground='white')
        passFornameUpdateEntry.place(x=25,y=212)
        
        def updateName():
            c.execute("SELECT * FROM REGISTRATIONINFO where register_UserName=?",
                      (userNameSecLabel.cget("text"),))
            r = c.fetchall()
            updatedName=nameUpdateEntry.get()
            if(passFornameUpdateEntry.get()==r[0][3]):
                
                c.execute("UPDATE REGISTRATIONINFO SET register_Name=? where register_UserName=?",
                       (updatedName,userNameSecLabel.cget("text"),))
                conn.commit()
                #refreshWin
                c.execute("SELECT * FROM REGISTRATIONINFO where register_UserName=?",
                       (userNameSecLabel.cget("text"),))
                r1 = c.fetchall()
                print(r)
                # AccountSet
                namesetLabel.config(text=r1[0][0])
                genderSetLabel.config(text=r1[0][2])
                DOBSetLabel.config(text=r1[0][4])
                # SecuritySet
                namesecLabel.config(text=r1[0][0])
                userNameSecLabel.config(text=r1[0][1])
                passSecLabel.config(text="*******")
                tmsg.showinfo("STATUS","Name updated successfully")
                root3.destroy()
            else:
                tmsg.showinfo("Note","Please enter correct password")
        # Submit Button
        updateSubmitButtonImg = Image.open('images\\submitButton.png')
        photo = ImageTk.PhotoImage(updateSubmitButtonImg)
        updateSubmitButton = Button(inFrame4, image=photo, bg='#313131',
                                      borderwidth=0, activebackground='#313131',command=updateName)
        updateSubmitButton.image = photo
        updateSubmitButton.place(x=463, y=333)
        # Cancel Button
        updateCancelButtonImg = Image.open('images\\cancelButton.png')
        photo = ImageTk.PhotoImage(updateCancelButtonImg)
        updateCancelButton = Button(inFrame4, image=photo, bg='#313131',
                                      command=root3.destroy, borderwidth=0, activebackground='#313131')
        updateCancelButton.image = photo
        updateCancelButton.place(x=342, y=333)
        root3.mainloop()

    
    def updateUserNameWin():
        root3 = Toplevel()
        root3.geometry('605x400')
        root3.maxsize(605,400)
        root3.title("Update UserName")
        #frame
        inFrame4 = Frame(root3, bg='#313131', width='605', height=400)
        inFrame4.place(x=0, y=0)
        # img
        updateNameFrameImg = Image.open('images\\updateUserNameWin.png')
        # createTaskImg=inImg1.resize((,674))
        photo = ImageTk.PhotoImage(updateNameFrameImg)
        updateNameFrameImgLabel = Label(inFrame4, image=photo, bg='#313131')
        updateNameFrameImgLabel.image = photo
        updateNameFrameImgLabel.place(x=0, y=0)

        #Entry
        userNameEntry=Entry(root3, width='35', font=(
            'Times', 20), bg='#313131', borderwidth=0, fg='white', insertbackground='white')
        userNameEntry.place(x=25,y=110)

        newUserNameEntry=Entry(root3, width='35', font=(
            'Times', 20), bg='#313131', borderwidth=0, fg='white', insertbackground='white')
        newUserNameEntry.place(x=25,y=185)

        passForUsernameUpdateEntry=Entry(root3, width='35',show='*', font=(
            'Times', 20), bg='#313131', borderwidth=0, fg='white', insertbackground='white')
        passForUsernameUpdateEntry.place(x=25,y=260)


        def updateUserName():
            c.execute("SELECT * FROM REGISTRATIONINFO where register_UserName=?",
                      (userNameSecLabel.cget("text"),))
            r = c.fetchall()
            userName=userNameEntry.get()
            updatedUserName=newUserNameEntry.get()
            if(userName!=userNameSecLabel.cget("text")):
                tmsg.showinfo("Note","Enter correct old username")
            elif(passForUsernameUpdateEntry.get()==r[0][3]):
                c.execute("UPDATE TASKSTODO SET userName=? where userName=?",(updatedUserName, userNameSecLabel.cget("text"),))
                conn.commit()
                c.execute("UPDATE REGISTRATIONINFO SET register_UserName=? where register_UserName=?",
                       (updatedUserName, userNameSecLabel.cget("text"),))
                conn.commit()
                #refreshWin
                c.execute("SELECT * FROM REGISTRATIONINFO where register_Name=?",
                       (namesetLabel.cget("text"),))
                r1 = c.fetchall()
                print(r1)
                # AccountSet
                namesetLabel.config(text=r1[0][0])
                genderSetLabel.config(text=r1[0][2])
                DOBSetLabel.config(text=r1[0][4])
                # SecuritySet
                namesecLabel.config(text=r1[0][0])
                userNameSecLabel.config(text=r1[0][1])
                passSecLabel.config(text="*******")
                tmsg.showinfo("STATUS","Username updated successfully")
                root3.destroy()
            else:
                tmsg.showinfo("Note","Please enter correct password")

        # Submit Button
        updateSubmitButtonImg = Image.open('images\\submitButton.png')
        photo = ImageTk.PhotoImage(updateSubmitButtonImg)
        updateSubmitButton = Button(inFrame4, image=photo, bg='#313131',
                                      borderwidth=0, activebackground='#313131',command=updateUserName)
        updateSubmitButton.image = photo
        updateSubmitButton.place(x=463, y=333)
        # Cancel Button
        updateCancelButtonImg = Image.open('images\\cancelButton.png')
        photo = ImageTk.PhotoImage(updateCancelButtonImg)
        updateCancelButton = Button(inFrame4, image=photo, bg='#313131',
                                      command=root3.destroy, borderwidth=0, activebackground='#313131')
        updateCancelButton.image = photo
        updateCancelButton.place(x=342, y=333)
        root3.mainloop()

    def updatePassWin():
        root3 = Toplevel()
        root3.geometry('605x400')
        root3.maxsize(605,400)
        root3.title("Update Password")
        #frame
        inFrame4 = Frame(root3, bg='#313131', width='605', height=400)
        inFrame4.place(x=0, y=0)
        # img
        updateNameFrameImg = Image.open('images\\updatePassWin.png')
        # createTaskImg=inImg1.resize((,674))
        photo = ImageTk.PhotoImage(updateNameFrameImg)
        updateNameFrameImgLabel = Label(inFrame4, image=photo, bg='#313131')
        updateNameFrameImgLabel.image = photo
        updateNameFrameImgLabel.place(x=0, y=0)

        #Entry
        passUpdateEntry=Entry(root3, width='35',show='*', font=(
            'Times', 20), bg='#313131', borderwidth=0, fg='white', insertbackground='white')
        passUpdateEntry.place(x=25,y=125)

        newPassUpdateEntry=Entry(root3, width='35',show='*', font=(
            'Times', 20), bg='#313131', borderwidth=0, fg='white', insertbackground='white')
        newPassUpdateEntry.place(x=25,y=212)

        def updatePass():
            c.execute("SELECT * FROM REGISTRATIONINFO where register_UserName=?",
                      (userNameSecLabel.cget("text"),))
            r = c.fetchall()
            prePass=passUpdateEntry.get()
            updatedPass=newPassUpdateEntry.get()
            if(prePass!=r[0][3]):
                tmsg.showinfo("Note","Enter correct old password ")
            elif(len(updatedPass)<5):
                tmsg.showinfo("Note","Password should have atleast 5 characters")
            elif(prePass==updatedPass):
                tmsg.showinfo("Note","Your password cannot be same old one")
            else:
                c.execute("UPDATE REGISTRATIONINFO SET register_Password=? where register_UserName=?",
                       (updatedPass, userNameSecLabel.cget("text"),))
                conn.commit()
                #refreshWin
                c.execute("SELECT * FROM REGISTRATIONINFO where register_Name=?",
                       (namesetLabel.cget("text"),))
                r1 = c.fetchall()
                print(r1)
                # AccountSet
                namesetLabel.config(text=r1[0][0])
                genderSetLabel.config(text=r1[0][2])
                DOBSetLabel.config(text=r1[0][4])
                # SecuritySet
                namesecLabel.config(text=r1[0][0])
                userNameSecLabel.config(text=r1[0][1])
                passSecLabel.config(text="*******")
                tmsg.showinfo("STATUS","Password updated successfully")
                root3.destroy()

        # Submit Button
        updateSubmitButtonImg = Image.open('images\\submitButton.png')
        photo = ImageTk.PhotoImage(updateSubmitButtonImg)
        updateSubmitButton = Button(inFrame4, image=photo, bg='#313131',
                                      borderwidth=0, activebackground='#313131',command=updatePass)
        updateSubmitButton.image = photo
        updateSubmitButton.place(x=463, y=333)
        # Cancel Button
        updateCancelButtonImg = Image.open('images\\cancelButton.png')
        photo = ImageTk.PhotoImage(updateCancelButtonImg)
        updateCancelButton = Button(inFrame4, image=photo, bg='#313131',
                                      command=root3.destroy, borderwidth=0, activebackground='#313131')
        updateCancelButton.image = photo
        updateCancelButton.place(x=342, y=333)
        root3.mainloop()

    # SettingWinMainFrame
    settingWinMain = Frame(root, bg='#313131', width='1280', height=720)
    # SettingWinImg
    settingWinMainImg = Image.open('images\\settingWinMain.png')
    photo = ImageTk.PhotoImage(settingWinMainImg)
    settingWinMainImageLabel = Label(settingWinMain, image=photo, bg='#313131')
    settingWinMainImageLabel.image = photo
    settingWinMainImageLabel.place(x=0, y=0)


    # accSettingWinFrame
    accSettingWinFrame = Frame(settingWinMain)
    accSettingWinFrame.pack(fill=BOTH, expand=True)
    accSettingWinImg = Image.open('images\\accSettingWin.png')
    photo = ImageTk.PhotoImage(accSettingWinImg)
    accSettingWinLabel = Label(accSettingWinFrame, image=photo, bg='#313131')
    accSettingWinLabel.image = photo
    accSettingWinLabel.place(x=0, y=0)

    # accountsettingButton
    accSettingImg = Image.open('images\\accountSettingsButton.png')
    photo = ImageTk.PhotoImage(accSettingImg)
    accsetImageButton = Button(accSettingWinFrame, image=photo, bg='#313131', borderwidth=0,
                               activebackground='#313131', command=changeToAccSetting)
    accsetImageButton.image = photo
    accsetImageButton.place(x=0, y=177)
    # securitySettingsButton
    securitySettingImg = Image.open('images\\securitySettingsButton.png')
    photo = ImageTk.PhotoImage(securitySettingImg)
    secsetImageButton = Button(accSettingWinFrame, image=photo, bg='#313131', borderwidth=0,
                               activebackground='#313131', command=changeToSecuritySettingWin)
    secsetImageButton.image = photo
    secsetImageButton.place(x=0, y=236)
    # BackButton
    settingBackButtonImg = Image.open('images\\backButton.png')
    photo = ImageTk.PhotoImage(settingBackButtonImg)
    settingBackButton = Button(accSettingWinFrame, image=photo, bg='#313131',
                               borderwidth=0, command=changeToMain, activebackground='#313131')
    settingBackButton.image = photo
    settingBackButton.place(x=0, y=-1)

    # nameLabel
    namesetLabel = Label(accSettingWinFrame, font=(
        'Times', 17), fg='#d1d1d1', bg='#313131', width=30, borderwidth=0, anchor=W)
    namesetLabel.place(x=470, y=439)
    #nameUpdate
    nameUpdateImg = Image.open('images\\updateButton.png')
    photo = ImageTk.PhotoImage(nameUpdateImg)
    nameUpdateImgButton = Button(accSettingWinFrame, image=photo, bg='#313131', borderwidth=0,
                               activebackground='#313131', command=updateNameWin)
    nameUpdateImgButton.image = photo
    nameUpdateImgButton.place(x=887, y=444)
    
    # genderLabel
    genderSetLabel = Label(accSettingWinFrame, font=(
        'Times', 17), fg='#d1d1d1', bg='#313131', width=30, borderwidth=0, anchor=W)
    genderSetLabel.place(x=478, y=499)
   
    # DOBLabel
    DOBSetLabel = Label(accSettingWinFrame, font=(
        'Times', 17), fg='#d1d1d1', bg='#313131', width=30, borderwidth=0, anchor=W)
    DOBSetLabel.place(x=535, y=559)
 
    # SignOutButton
    signOutButtonImg = Image.open('images\\signOutButton.png')
    photo = ImageTk.PhotoImage(signOutButtonImg)
    signOutButton = Button(accSettingWinFrame, image=photo, bg='#313131',
                           borderwidth=0, command=signOut, activebackground='#313131')
    signOutButton.image = photo
    signOutButton.place(x=394, y=648)
    #DeleteMyAccButton
    deleteMyAccButtonImg = Image.open('images\\deleteMyAcc.png')
    photo = ImageTk.PhotoImage(deleteMyAccButtonImg)
    deleteMyAccButton = Button(accSettingWinFrame, image=photo, bg='#313131',
                           borderwidth=0, command=deleteAcc, activebackground='#313131')
    deleteMyAccButton.image = photo
    deleteMyAccButton.place(x=539, y=648)


    # securitySettingWinFrame
    securitySettingWinFrame = Frame(settingWinMain)
    securitySettingWinImg = Image.open('images\\securitySettingWin.png')
    photo = ImageTk.PhotoImage(securitySettingWinImg)
    securitySettingWinLabel = Label(
        securitySettingWinFrame, image=photo, bg='#313131')
    securitySettingWinLabel.image = photo
    securitySettingWinLabel.place(x=0, y=0)
    # accountsettingButton
    accSettingImg = Image.open('images\\accountSettingsButton.png')
    photo = ImageTk.PhotoImage(accSettingImg)
    accsetImageButton = Button(securitySettingWinFrame, image=photo, bg='#313131', borderwidth=0,
                               activebackground='#313131', command=changeToAccSetting)
    accsetImageButton.image = photo
    accsetImageButton.place(x=0, y=177)
    # securitySettingsButton
    securitySettingImg = Image.open('images\\securitySettingsButton.png')
    photo = ImageTk.PhotoImage(securitySettingImg)
    secsetImageButton = Button(securitySettingWinFrame, image=photo, bg='#313131', borderwidth=0,
                               activebackground='#313131', command=changeToSecuritySettingWin)
    secsetImageButton.image = photo
    secsetImageButton.place(x=0, y=236)
    # BackButton
    settingBackButtonImg = Image.open('images\\backButton.png')
    photo = ImageTk.PhotoImage(settingBackButtonImg)
    settingBackButton = Button(securitySettingWinFrame, image=photo, bg='#313131',
                               borderwidth=0, command=changeToMain, activebackground='#313131')
    settingBackButton.image = photo
    settingBackButton.place(x=0, y=-1)
    # nameLabel
    namesecLabel = Label(securitySettingWinFrame, font=(
        'Times', 17), fg='#d1d1d1', bg='#313131', width=30, borderwidth=0, anchor=W)
    namesecLabel.place(x=470, y=283)
    # UsernameLabel
    userNameSecLabel = Label(securitySettingWinFrame, font=(
        'Times', 17), fg='#d1d1d1', bg='#313131', width=25, borderwidth=0, anchor=W)
    userNameSecLabel.place(x=515, y=343)
    # UsernameUpdate
    userNameUpdateImg = Image.open('images\\updateButton.png')
    photo = ImageTk.PhotoImage(nameUpdateImg)
    userNameUpdateImgButton = Button(securitySettingWinFrame, image=photo, bg='#313131', borderwidth=0,
                               activebackground='#313131', command=updateUserNameWin)
    userNameUpdateImgButton.image = photo
    userNameUpdateImgButton.place(x=889, y=348)
    # passwordLabel
    passSecLabel = Label(securitySettingWinFrame, font=(
        'Times', 17), fg='#d1d1d1', bg='#313131', width=25, borderwidth=0, anchor=W)
    passSecLabel.place(x=515, y=403)
    # PasswordUpdate
    passUpdateImg = Image.open('images\\updateButton.png')
    photo = ImageTk.PhotoImage(passUpdateImg)
    passUpdateImgButton = Button(securitySettingWinFrame, image=photo, bg='#313131', borderwidth=0,
                               activebackground='#313131', command=updatePassWin)
    passUpdateImgButton.image = photo
    passUpdateImgButton.place(x=889, y=408)
    # Placing show hide Password button In securityWindow
    passShowImg1sec = Image.open('images\\show1.png')
    passShowImgsec = passShowImg1sec.resize((32, 32))
    photo = ImageTk.PhotoImage(passShowImgsec)
    passShowButtonsec = Button(securitySettingWinFrame, image=photo, bg='#313131',
                            borderwidth=0, activebackground='#313131', command=passShowsec)
    passShowButtonsec.image = photo
    passShowButtonsec.place(x=830, y=395)
    root.mainloop()



'''
def task():
    sleep(3) # Replace this with the code you want to run
    Loading.destroy()
    main()

Loading = Tk()
Loading.geometry("1280x720")
Loading.title("Planner")
loading = Image.open('images\\loadingPage.png')
photo = ImageTk.PhotoImage(loading)
mainImg1Label = Label(Loading, image=photo, bg='#313131')
mainImg1Label.image = photo
mainImg1Label.place(x=0, y=0)


Loading.after(200, task)
Loading.mainloop()

print("Main loop is now over and we can do other stuff.")
'''
main()