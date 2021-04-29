from modules.getDataBase import *
from modules.sendEmail import *

db = GetDataBase()
sd = SendEmail()

class CheckSent():
    def __init__(self):
        pass

    def checkSent(self,empresa):
        body_email = ''
        envia_problem_email = 'N'
        directoryControl = 'sendEmailAlgarTech' if empresa == 'TECH' else 'sendEmailNinecon'
        equipeQualitor = 'TI - Infraestrutura Aplicações'if empresa == 'TECH' else 'TI - Infraestrutura DBA / ATG /CLOUD'

        # --------------------------- Lê arquivo de controle de chamados já enviados ---------------------------
        sendControl = open('C:/Automations/sendEmail/'+directoryControl+'/settings/sendControl.txt', 'r').readlines()

        # --------------------------- Lê arquivo de destinatários ---------------------------
        to_email = open('C:/Automations/sendEmail/'+directoryControl+'/settings/recipient.txt', 'r').readlines()

        list_sendControl = []
        for n in sendControl:
            list_sendControl.append(n.rstrip())

        json_output_tickets = db.chamados(equipeQualitor)

        cont = 0
        ticketsFounds = ''
        # --------------------------- Verifica se chamado já foi enviado ---------------------------
        for tck in json_output_tickets:
            if (str(tck[0]) not in list_sendControl):
                body_email += ("Chamado: " + str(tck[0]) + "\n")
                body_email += ("Data de Abertura: " + str(tck[1]) + "\n")
                body_email += ("Título: " + str(tck[2]) + "\n")
                body_email += ("Prioridade: " + str(tck[4]) + "\n")
                body_email += ("Previsão de encerramento: " + str(tck[7]) + "\n")
                body_email += ("\n")

                ticketsFounds += str(tck[0]) + ";"
                sendControl = open('C:/Automations/sendEmail/'+directoryControl+'/settings/sendControl.txt', 'a')
                sendControl.writelines(str(tck[0]) + "\n")
                sendControl.close()
                envia_problem_email = 'S'

        # ----------------------------- Enviando email aos interessados -----------------------------
        if (envia_problem_email == 'S'):
            sd.sendEmail(body_email,ticketsFounds,to_email,directoryControl)