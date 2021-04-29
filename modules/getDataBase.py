import cx_Oracle
import json
from settings.credentials import *
from settings.parameters import *

#--------------------------- Abrindo conexão com Oracle ---------------------------
conn = cx_Oracle.connect(user=CRD_USER_DB_QUALITOR, password=CRD_PWD_DB_QUALITOR, dsn=PAR_QUALITOR_TNS)
c = conn.cursor()

class GetDataBase():
    def __init__(self):
        pass

    def chamados(self,equipe):
        #----------------- fazendo select e buscando chamados abertos -----------------
        c.execute("select hd_chamado.cdchamado as chamado, to_char(hd_chamado.dtchamado,'DD/MM/YYYY') as abertura, hd_chamado.nmtitulochamado as titulo, hd_equipe.nmequipe as equipe, c3.nmcategoria as categoria_3, "
                    "hd_situacao.nmsituacao as situacao, case when hd_chamado.dttermino > hd_chamado.dtprevisaotermino then 'SIM' when sysdate > hd_chamado.dtprevisaotermino and "
                    "hd_chamado.dttermino is null then 'SIM' else 'NAO' end as atraso_servico, to_char(hd_chamado.dtprevisaotermino,'DD/MM/YYYY') previsao_termino, hd_chamado.dttermino as data_solucao, to_char(hd_chamado.dschamado) as descricao "
                    "from hd_chamado "
                    "left outer join hd_situacao "
                    "on hd_situacao.cdsituacao = hd_chamado.cdsituacao "
                    "left outer join ad_contato "
                    "on ad_contato.cdcliente = hd_chamado.cdcliente "
                    "and ad_contato.cdcontato = hd_chamado.cdcontato "
                    "left outer join hd_equipe "
                    "on hd_equipe.cdequipe = hd_chamado.cdequipe "
                    "left outer join hd_categoria C3 "
                    "on C3.cdcategoria = hd_chamado.cdcategoria "
                    "left outer join hd_estruturasubsituacaoitem "
                    "on hd_estruturasubsituacaoitem.cdestrutura = hd_chamado.cdestrutura "
                    "and hd_estruturasubsituacaoitem.nrsequencia = hd_chamado.cdsubsituacao "
                    "left outer join hd_severidade "
                    "on hd_severidade.cdseveridade = hd_chamado.cdseveridade "
                    "left outer join hd_origem "
                    "on hd_origem.cdorigem = hd_chamado.cdorigem "
                    "left outer join hd_localidade "
                    "on hd_localidade.cdlocalidade = hd_chamado.cdlocalidade "
                    "left outer join hd_estruturasubsituacaoitem "
                    "on hd_estruturasubsituacaoitem.cdestrutura = hd_chamado.cdestrutura "
                    "and hd_estruturasubsituacaoitem.nrsequencia = hd_chamado.cdsubsituacao "
                    "left outer join hd_causa causa3 "
                    "on causa3.cdcausa = hd_chamado.cdcausa "
                    "left outer join hd_causa causa2 "
                    "on causa2.cdcausa = causa3.cdcausa "
                    "left outer join hd_causa causa1 "
                    "on causa1.cdcausa = causa2.cdcausa "
                    "where hd_chamado.Dttermino IS NULL "
                    "and hd_equipe.nmequipe like '"+equipe+"' "
                    "order by hd_chamado.dtchamado")

        tickets = c.fetchall()
        return json.loads(json.dumps(tickets))