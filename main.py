import sqlite3

conn = sqlite3.connect('biblioteca.db')

cursor = conn.cursor()

'''
codigo comentado ja foi executado
se vc baixou o biblioteca.db junto (no git) nao rode de novo
se nao descomente e de run
'''

# cursor.execute("""
# CREATE TABLE pessoa (
#   cpf  CHAR(11)        NOT NULL,
#   nome VARCHAR2(100)   NOT NULL,
#   CONSTRAINT pk_pessoa PRIMARY KEY (cpf)
# );
# """)

# cursor.execute("""
# CREATE TABLE telefone (
#   pessoa_fk CHAR(11)        NOT NULL,
#   telefone  VARCHAR2(20)    NOT NULL,
#   CONSTRAINT pk_telefone PRIMARY KEY (pessoa_fk, telefone),
#   CONSTRAINT fk_telefone_pessoa FOREIGN KEY (pessoa_fk)
#     REFERENCES pessoa (cpf)
#     ON DELETE CASCADE
# );
# """)

# cursor.execute("""
# CREATE TABLE socio (
#   cpf  CHAR(11)      NOT NULL,
#   cartao  NUMBER(16)  NOT NULL,
#   CONSTRAINT pk_socio PRIMARY KEY (cpf),
#   CONSTRAINT fk_socio_pessoa FOREIGN KEY (cpf)
#     REFERENCES pessoa(cpf)
#     ON DELETE CASCADE
# );
# """)

# cursor.execute("""
# CREATE TABLE funcionario (
#   cpf          CHAR(11)        NOT NULL,
#   salario      NUMBER(12,2)    NOT NULL,
#   chefe_cpf  CHAR(11),
#   CONSTRAINT pk_funcionario PRIMARY KEY (cpf),
#   CONSTRAINT fk_func_pessoa FOREIGN KEY (cpf)
#     REFERENCES pessoa(cpf)
#     ON DELETE CASCADE,
#   CONSTRAINT fk_chefia
#     FOREIGN KEY (chefe_cpf)
#     REFERENCES funcionario(cpf)
#     ON DELETE SET NULL
# );
# """)

# pessoas = [
#     ('11122233344', 'Ana Pereira'),
#     ('22233344455', 'Bruno Santos'),
#     ('33344455566', 'Carla Oliveira'),
#     ('44455566677', 'Diego Costa')
# ]
# cursor.executemany("INSERT INTO pessoa (cpf, nome) VALUES (?, ?)", pessoas)

# telefones = [
#     ('11122233344', '(21) 98765-4321'),
#     ('11122233344', '(21) 91234-5678'),
#     ('22233344455', '(31) 99876-5432'),
#     ('33344455566', '(11) 93456-7890')
# ]
# cursor.executemany("INSERT INTO telefone (pessoa_fk, telefone) VALUES (?, ?)", telefones)

# socios = [
#     ('22233344455', 1234567812345678),
#     ('44455566677', 8765432187654321)
# ]
# cursor.executemany("INSERT INTO socio (cpf, cartao) VALUES (?, ?)", socios)

# funcionarios = [
#     ('11122233344', 4500.00, None),
#     ('22233344455', 3800.00, '11122233344'),
#     ('33344455566', 3200.00, '22233344455'),
#     ('44455566677', 5000.00, '11122233344')
# ]
# cursor.executemany("INSERT INTO funcionario (cpf, salario, chefe_cpf) VALUES (?, ?, ?)", funcionarios)

# conn.commit()

conn.close()