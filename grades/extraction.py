############ Análise de dados educacionais - TCC Fernanda e Luiz ############
# Autores: Fernanda Amaral Melo e Luiz Fernando Araújo 
# Contato: fernanda.amaral.melo@gmail.com e luizfna@gmail.com

# Script usado para extrair os dados dos arquivos .txt salvos na pasta
# "data" para inserção em um banco de dados SQL 

from os import listdir
from os.path import isfile, join
import re
import psycopg2
import json
import yaml
import json


class text(object):

    def __init__(self, mypath):

        with open("cred.yaml", 'r') as stream:
            self.yaml = yaml.load(stream, Loader=yaml.FullLoader)

        self.mypath = mypath
        self.dict = {
            'periodo': ('Período:', 'Dis'),
            'dis_data': ('Disciplina:', 'Turma:'),
            'turma': ('Turma:', 'MENÇÃO'),
            'SS': ('SS  -  SUPERIOR', 'MS'),
            'MS': ('MÉDIO SUPERIOR', 'MM'),
            'MM': ('MM  -  MÉDIO', 'MI'),
            'MI': ('MÉDIO INFERIOR', 'II'),
            'II': ('II  -  INFERIOR', 'SR'),
            'SR': ('SR  -  SEM RENDIMENTO', 'TR'),
            'TR': ('TR  -  TRANCAMENTO', 'TJ'),
            'TJ': ('TRANCAMENTO JUSTIFICADO', 'CC'),
            'CC': ('CRÉDITO CONCEDIDO', 'DP'),
            'DP': ('DISPENSADO', 'AP'),
            'AP': ('APROVADO', 'RP'),
            'RP': ('REPROVADO', 'TOTAL DE APROVAÇÕES'),
            'APROVAÇÕES': ('APROVAÇÕES', 'TOTAL DE REPROVAÇÕES'),
            'REPROVAÇÕES': ('REPROVAÇÕES', 'TOTAL DE TRANCAMENTOS'),
            'TRANCAMENTOS': ('TRANCAMENTOS', 'TOTAL DE MENÇÕES')
        }

        self.res = {}
        self.periodo = []
        self.files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    def build(self):

        with open('credentials.json') as json_file:
            data = json.load(json_file)

        conn = psycopg2.connect(
            host=data['host'],
            port=data['port'],
            user=data['user'],
            password=data['password']
        )

        cur = conn.cursor()
        mat_list = []
        mat_list.append('inicio')

        cur.execute("CREATE TABLE IF NOT EXISTS materias (id serial PRIMARY KEY, disciplina TEXT, tipo TEXT, codigo INTEGER, departamento TEXT);")
        cur.execute("CREATE TABLE IF NOT EXISTS mencoes (id serial PRIMARY KEY, fk_materia TEXT,ss_count INTEGER, ss_percent INTEGER, ms_count INTEGER, ms_percent INTEGER, mm_count INTEGER, mm_percent INTEGER, mi_count INTEGER, mi_percent INTEGER,ii_count INTEGER, ii_percent INTEGER, sr_count INTEGER, sr_percent INTEGER, tr_count INTEGER, tr_percent INTEGER, tj_count INTEGER, tj_percent INTEGER, cc_count INTEGER, cc_percent INTEGER, dp_count INTEGER, dp_percent INTEGER, ap_count INTEGER, ap_percent INTEGER, rp_count INTEGER, rp_percent INTEGER, aprova_count INTEGER, aprova_percent INTEGER, reprova_count INTEGER, reprova_percent INTEGER, tranca_count INTEGER, tranca_percent INTEGER, periodo_ano INTEGER, periodo_semestre INTEGER, turma TEXT);")

        cur.execute("SELECT MAX(id) FROM materias")
        id_mat = cur.fetchone()[0]
        for file in self.files:
            for key in self.dict:
                self.res[key] = self.read(self.mypath, file, self.dict[key])
            columns = ["disciplina", "tipo", "codigo", "departamento"]
            for i in range(len(self.res[key][0])):

                per_data = self.substitute(self.data('periodo', i, '/'))
                ss_data = self.substitute(self.data('SS', i, '           '))
                ms_data = self.substitute(self.data('MS', i, '           '))
                mm_data = self.substitute(self.data('MM', i, '           '))
                mi_data = self.substitute(self.data('MI', i, '           '))
                ii_data = self.substitute(self.data('II', i, '           '))
                sr_data = self.substitute(self.data('SR', i, '           '))
                tr_data = self.substitute(self.data('TR', i, '           '))
                tj_data = self.substitute(self.data('TJ', i, '           '))
                cc_data = self.substitute(self.data('CC', i, '           '))
                dp_data = self.substitute(self.data('DP', i, '           '))
                ap_data = self.substitute(self.data('AP', i, '           '))
                rp_data = self.substitute(self.data('RP', i, '           '))
                aprova_data = self.substitute(
                    self.data('APROVAÇÕES', i, '           '))
                reprova_data = self.substitute(
                    self.data('REPROVAÇÕES', i, '           '))
                tranca_data = self.substitute(
                    self.data('TRANCAMENTOS', i, '           '))
                turma_data = self.data('turma', i, '//')

                id_data = self.data('dis_data', i, '-')
                if not(id_data[3] in mat_list):
                    mat_list.append(id_data[3])

                index = mat_list.index(id_data[3]) + id_mat

                sql = "INSERT INTO materias (id,disciplina,tipo,codigo,departamento) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (disciplina) DO NOTHING;"
                cur.execute(
                    sql, (index, id_data[3], id_data[2], id_data[1], id_data[0]))
                conn.commit()

                sql2 = ("""INSERT INTO mencoes (fk_materia,ss_count,ss_percent,ms_count,
                      ms_percent,mm_count,mm_percent,mi_count,mi_percent,ii_count,
                      ii_percent,sr_count,sr_percent,tr_count,tr_percent,tj_count,
                      tj_percent,cc_count,cc_percent,dp_count,dp_percent,ap_count,
                      ap_percent,rp_count,rp_percent,aprova_count,aprova_percent,
                      reprova_count,reprova_percent,tranca_count,tranca_percent,
                      periodo_ano,periodo_semestre,turma) VALUES (%(fk_materia)s,
                      %(ss_count)s, %(ss_percent)s, %(ms_count)s, %(ms_percent)s,
                      %(mm_count)s, %(mm_percent)s, %(mi_count)s, %(mi_percent)s,
                      %(ii_count)s, %(ii_percent)s, %(sr_count)s, %(sr_percent)s,
                      %(tr_count)s, %(tr_percent)s, %(tj_count)s, %(tj_percent)s,
                      %(cc_count)s, %(cc_percent)s, %(dp_count)s, %(dp_percent)s,
                      %(ap_count)s, %(ap_percent)s, %(rp_count)s, %(rp_percent)s,
                      %(aprova_count)s, %(aprova_percent)s, %(reprova_count)s,
                      %(reprova_percent)s, %(tranca_count)s, %(tranca_percent)s,
                      %(periodo_ano)s, %(periodo_semestre)s, %(turma)s)""")

                values = {
                    'ss_count': int(ss_data[0]),
                    'ss_percent': float(ss_data[1]),
                    'ms_count': int(ms_data[0]),
                    'ms_percent': float(ms_data[1]),
                    'mm_count': int(mm_data[0]),
                    'mm_percent': float(mm_data[1]),
                    'mi_count': int(mi_data[0]),
                    'mi_percent': float(mi_data[1]),
                    'ii_count': int(ii_data[0]),
                    'ii_percent': float(ii_data[1]),
                    'sr_count': int(sr_data[0]),
                    'sr_percent': float(sr_data[1]),
                    'tr_count': int(tr_data[0]),
                    'tr_percent': float(tr_data[1]),
                    'tj_count': int(tj_data[0]),
                    'tj_percent': float(tj_data[1]),
                    'cc_count': int(cc_data[0]),
                    'cc_percent': float(cc_data[1]),
                    'dp_count': int(dp_data[0]),
                    'dp_percent': float(dp_data[1]),
                    'ap_count': int(ap_data[0]),
                    'ap_percent': float(ap_data[1]),
                    'rp_count': int(rp_data[0]),
                    'rp_percent': float(rp_data[1]),
                    'aprova_count': int(aprova_data[0]),
                    'aprova_percent': float(aprova_data[1]),
                    'reprova_count': int(reprova_data[0]),
                    'reprova_percent': float(reprova_data[1]),
                    'tranca_count': int(tranca_data[0]),
                    'tranca_percent': float(tranca_data[1]),
                    'periodo_ano': int(per_data[0]),
                    'periodo_semestre': int(per_data[1]),
                    'turma': turma_data[0]
                }

                cur.execute(sql2, values)

                conn.commit()
                cur.close()
                conn.close()

        return

    def substitute(self, list):

        list[1] = list[1].replace(",", ".")

        return list

    def data(self, key, n, sep):

        temp = [item for item in self.res[key][0]]
        ret = list(map(str.strip, temp[n].split(sep)))

        return ret

    def read(self, path, filename, values):
        temp = []
        with open(path+'/'+filename, 'rb') as f:
            fi = f.read()
            fi = str(fi)
            fi = fi.replace('\n', '').replace('\r', '').replace('\t', '')
            temp.append([tempp.strip() for tempp in re.findall(
                values[0]+'(.*?)'+values[1], str(fi), re.MULTILINE)])
        return temp


a = text('./data')
# a.build()
print("Done")
