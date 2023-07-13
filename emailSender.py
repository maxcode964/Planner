from credentials import *
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = accDetails["EMAILID"]
EMAIL_PASSWORD = accDetails["APPPASSWORD"]


def taskEmail(reciversEmail, tTitle, tDescription, tDate, tTime, tPri):
    if(tPri == 1):
        tPriority = "Low"
    elif(tPri == 2):
        tPriority = "Medium"
    elif(tPri == 3):
        tPriority = "High"
    elif(tPri == 4):
        tPriority = "Very High"
    msg = EmailMessage()
    msg['Subject'] = 'Task Reminder'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = reciversEmail
    msg.set_content(f'''
    <!DOCTYPE html>
    <html>
        <style>
            table {{
                border:1px solid #b3adad;
                border-collapse:collapse;
                padding:5px;
            }}
            table th {{
                border:1px solid #b3adad;
                padding:5px;
                background: #313131;
                color: #d1d1d1;
            }}
            table td {{
                border:1px solid #b3adad;
                text-align:center;
                padding:5px;
                background: #d1d1d1;
                color: #313131;
            }}
        </style>
        <body style="background-color:#313131">
            <div style="background-color:#313131">
                <img src="https://github.com/adi1611/GUI-Planner/blob/main/images/Logo.png?raw=true" alt="Logo";left: 50%;>
            </div>
            <div style="background-color:#313131">
                <h1 style = "color: #D1D1D1;">
                    You have tasks!
                </h1>
            </div>
            <tbody style = "border: 1px solid #d1d1d1;border-collapse:collapse;padding:5px;">
                <h1 style = "font-size:25;">
                    <tr style = "border:1px solid #d1d1d1;padding:5px;background: #d1d1d1;color: #313131;font-size:200%;height:50px;">
                        <td><b>&nbsp;Task Title</b></td>
                        <td style = "width:50%;"><b>&nbsp;{tTitle}</b></td>
                    </tr>
                    <tr style = "border:10px;padding:5px;background: #313131;color: #d1d1d1;font-size:130%;height:50px;">
                        <td>&nbsp;Task Description</td>
                        <td style = "width:50%;">&nbsp;{tDescription}</td>
                    </tr>
                    <tr style = "border:10px;padding:5px;background: #313131;color: #d1d1d1;font-size:130%;height:50px;">
                        <td>&nbsp;Date</td>
                        <td style = "width:50%;">&nbsp;{tDate}</td>
                    </tr>
                    <tr style = "border:10px;padding:5px;background: #313131;color: #d1d1d1;font-size:130%;height:50px;">
                        <td>&nbsp;Time</td>
                        <td style = "width:50%;">&nbsp;{tTime}</td>
                    </tr>
                    <tr style = "border:10px;padding:5px;background: #313131;color: #d1d1d1;font-size:130%;height:50px;">
                        <td>&nbsp;Priority</td>
                        <td style = "width:50%;">&nbsp;{tPriority}</td>
                    </tr>
                </h1>
            </tbody>
        </body>
    </html>
    ''', subtype='html')




    

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
