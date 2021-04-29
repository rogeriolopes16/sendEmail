import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
from settings.credentials import *

class SendEmail():
    def __init__(self):
        pass

    def sendEmail(self,body_email,ticketsFounds,to_email,directoryControl):

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("" + CRD_EMAIL + "",
                     "" + CRD_PWD_EMAIL + "")
        body = "Informamos que o chamado abaixo foi aberto e está aguardando atendimento.\n\n" \
               + body_email + \
               "\n" \
               "Email automático."

        subject = "Novo chamado aberto no Qualitor"
        from_email = "" + CRD_EMAIL + ""
        to = to_email
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = Header(from_email, 'utf-8')
        # msg['To'] = Header(to, 'utf-8')
        text = msg.as_string()

        try:
            server.sendmail(from_email, to_email, text)
            log = open('C:/Automations/sendEmail/'+directoryControl+'/settings/logError.txt', 'a')
            log.writelines(
                str(datetime.now().strftime('%d/%m/%Y-%H:%M:%S') + ": Enviado com sucesso o chamaodo " + ticketsFounds + "\n"))
            log.close()
        except:
            log = open('C:/Automations/sendEmail/'+directoryControl+'/settings/logError.txt', 'a')
            log.writelines(str(datetime.now().strftime(
                '%d/%m/%Y-%H:%M:%S') + ": Erro no envio do email para o chamaodo " + ticketsFounds + "\n"))
            log.close()