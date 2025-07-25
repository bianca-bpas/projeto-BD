import sqlite3

conn = sqlite3.connect('biblioteca.db')

cursor = conn.cursor()

'''
codigo no if ja foi executado
mas achei melhor deixar pra todo mundo ver se ta coerente
e tbm pq é mais facil recriar quando preciso que alterar tabela
se vc baixou o biblioteca.db junto (no git) nao rode de novo
se nao mude a variavel e de run

os povoamentos colocados sao mais de exemplo dps a gente deixa mais completo
'''

rebooted = False

if rebooted:
    cursor.execute("""
    CREATE TABLE pessoa (
    cpf  CHAR(11)        NOT NULL,
    nome VARCHAR2(100)   NOT NULL,
    CONSTRAINT pk_pessoa PRIMARY KEY (cpf)
    );
    """)

    cursor.execute("""
    CREATE TABLE telefone (
    pessoa_fk CHAR(11)        NOT NULL,
    telefone  VARCHAR2(20)    NOT NULL,
    CONSTRAINT pk_telefone PRIMARY KEY (pessoa_fk, telefone),
    CONSTRAINT fk_telefone_pessoa FOREIGN KEY (pessoa_fk)
        REFERENCES pessoa (cpf)
        ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE socio (
    cpf  CHAR(11)      NOT NULL,
    cartao  VARCHAR2(16)  NOT NULL,
    CONSTRAINT pk_socio PRIMARY KEY (cpf),
    CONSTRAINT fk_socio_pessoa FOREIGN KEY (cpf)
        REFERENCES pessoa(cpf)
        ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE funcionario (
    cpf          CHAR(11)        NOT NULL,
    salario      NUMBER(12,2)    NOT NULL,
    cargo      VARCHAR(100)    NOT NULL,
    chefe_cpf  CHAR(11),
    CONSTRAINT pk_funcionario PRIMARY KEY (cpf),
    CONSTRAINT fk_func_pessoa FOREIGN KEY (cpf)
        REFERENCES pessoa(cpf)
        ON DELETE CASCADE,
    CONSTRAINT fk_chefia
        FOREIGN KEY (chefe_cpf)
        REFERENCES funcionario(cpf)
        ON DELETE SET NULL
    );
    """)

    pessoas = [
        ('11122233344', 'Ana Pereira'),
        ('22233344455', 'Bruno Santos'),
        ('33344455566', 'Carla Oliveira'),
        ('44455566677', 'Diego Costa')
    ]
    cursor.executemany("INSERT INTO pessoa (cpf, nome) VALUES (?, ?)", pessoas)

    telefones = [
        ('11122233344', '(21) 98765-4321'),
        ('11122233344', '(21) 91234-5678'),
        ('22233344455', '(31) 99876-5432'),
        ('33344455566', '(11) 93456-7890')
    ]
    cursor.executemany("INSERT INTO telefone (pessoa_fk, telefone) VALUES (?, ?)", telefones)

    socios = [
        ('22233344455', "1234567812345678"),
        ('44455566677', "8765432187654321")
    ]
    cursor.executemany("INSERT INTO socio (cpf, cartao) VALUES (?, ?)", socios)

    funcionarios = [
        ('11122233344', 5500.00, "Gerente", None),
        ('22233344455', 3800.00, "Chefe de Manutenção", '11122233344'),
        ('33344455566', 3200.00, "Faxineiro", '22233344455'),
        ('44455566677', 5000.00,  "Bibliotecário", '11122233344')
    ]
    cursor.executemany("INSERT INTO funcionario (cpf, salario, cargo, chefe_cpf) VALUES (?, ?, ?, ?)", funcionarios)

    conn.commit()

    cursor.execute("""
    CREATE TABLE biblioteca (
    id  VARCHAR2(10)        NOT NULL,
    local_estado VARCHAR2(100)   NOT NULL,
    local_cep VARCHAR2(8)   NOT NULL,
    local_numero NUMBER(5) NOT NULL,
    CONSTRAINT pk_biblioteca PRIMARY KEY (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE cargo_comissionado (
    cargo_comissionado VARCHAR2(100)  NOT NULL,
    gratificacao NUMBER(5, 2)   NOT NULL,
    CONSTRAINT pk_cargo_com PRIMARY KEY (cargo_comissionado)
    );
    """)

    bibs = [
        ("0000000123", "Pernambuco", "12345678", 100),
        ("4560010000", "Parauapebas", "12345999", 87),
        ("6097157000", "Sucupira do Riachão", "98426611", 901)
    ]
    cursor.executemany("INSERT INTO biblioteca (id, local_estado, local_cep, local_numero) VALUES (?, ?, ?, ?)", bibs)

    coms = [
        ("Consultor Técnico", 1000.00),
        ("Gerente Comercial", 400.50)
    ]

    cursor.executemany("INSERT INTO cargo_comissionado (cargo_comissionado, gratificacao) VALUES (?, ?)", coms)

    conn.commit()

    cursor.execute("""
    CREATE TABLE livro (
    ISBN  VARCHAR2(13)        NOT NULL,
    nome VARCHAR2(100)   NOT NULL,
    ano NUMBER(5)   NOT NULL,
    CONSTRAINT pk_livro PRIMARY KEY (ISBN)
    );
    """)

    livros = [
        ("9786584952003", "Moby Dick", 1851),
        ("9797138852114", "O Senhor dos Anéis: A Sociedade do Anel", 1954),
        ("1750094135220", "O Senhor dos Anéis: As Duas Torres", 1954),
        ("0965180092413", "O Senhor dos Anéis: O Retorno do Rei", 1955),
        ("1111111111111", "O Hobbit", 1937)
    ]
    cursor.executemany("INSERT INTO livro (ISBN, nome, ano) VALUES (?, ?, ?)", livros)

    conn.commit()

    cursor.execute("""
    CREATE TABLE autor (
    id  VARCHAR2(12)        NOT NULL,
    nome VARCHAR2(100)   NOT NULL,
    CONSTRAINT pk_autor PRIMARY KEY (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE colecao (
    id  VARCHAR2(12)        NOT NULL,
    nome VARCHAR2(100)   NOT NULL,
    CONSTRAINT pk_colecao PRIMARY KEY (id)
    );
    """)

    autores = [
        ("000000000001", "Herman Melville"),
        ("000000000002", "J. R. R. Tolkien"),
    ]
    cursor.executemany("INSERT INTO autor (id, nome) VALUES (?, ?)", autores)

    colecoes = [
        ("000000000001", "Clássicos Americanos"),
        ("000000000002", "Trilogia Senhor dos Anéis"),
        ("000000000003", "Coleção Terra Média"),
    ]
    cursor.executemany("INSERT INTO colecao (id, nome) VALUES (?, ?)", colecoes)

    conn.commit()

    cursor.execute("""
    CREATE TABLE pertence (
    ISBN  VARCHAR2(13)        NOT NULL,
    id  VARCHAR2(12)        NOT NULL,
    CONSTRAINT pk_pertence PRIMARY KEY (ISBN, id),
    CONSTRAINT fk_livro FOREIGN KEY (ISBN)
        REFERENCES livro (ISBN)
        ON DELETE CASCADE
    CONSTRAINT fk_colecao FOREIGN KEY (id)
        REFERENCES colecao (id)
        ON DELETE CASCADE
    );
    """)

    relacao_participa = [
        ("9786584952003", "000000000001"),
        ("9797138852114", "000000000002"),
        ("1750094135220", "000000000002"),
        ("0965180092413", "000000000002"),
        ("9797138852114", "000000000003"),
        ("1750094135220", "000000000003"),
        ("0965180092413", "000000000003"),
        ("1111111111111", "000000000003"),
    ]
    cursor.executemany("INSERT INTO pertence (ISBN, id) VALUES (?, ?)", relacao_participa)

    conn.commit()

    cursor.execute("""
    CREATE TABLE escreve (
    ISBN  VARCHAR2(13)        NOT NULL,
    id  VARCHAR2(12)        NOT NULL,
    CONSTRAINT pk_pertence PRIMARY KEY (ISBN, id),
    CONSTRAINT fk_livro FOREIGN KEY (ISBN)
        REFERENCES livro (ISBN)
        ON DELETE CASCADE
    CONSTRAINT fk_autor FOREIGN KEY (id)
        REFERENCES autor (id)
        ON DELETE CASCADE
    );
    """)

    relacao_escreve = [
        ("9786584952003", "000000000001"),
        ("9797138852114", "000000000002"),
        ("1750094135220", "000000000002"),
        ("0965180092413", "000000000002"),
        ("1111111111111", "000000000002"),
    ]
    cursor.executemany("INSERT INTO escreve (ISBN, id) VALUES (?, ?)", relacao_escreve)

    conn.commit()

    cursor.execute("""
    CREATE TABLE demanda (
    ISBN  VARCHAR2(13)        NOT NULL,
    id  VARCHAR2(10)        NOT NULL,
    cpf CHAR(11) NOT NULL,
    atendido NUMBER(1) NOT NULL,
    CONSTRAINT pk_demanda PRIMARY KEY (ISBN, id, cpf),
    CONSTRAINT fk_livro FOREIGN KEY (ISBN)
        REFERENCES livro (ISBN)
        ON DELETE CASCADE
    CONSTRAINT fk_biblioteca FOREIGN KEY (id)
        REFERENCES biblioteca (id)
        ON DELETE CASCADE
    CONSTRAINT fk_pessoa FOREIGN KEY (cpf)
        REFERENCES pessoa (cpf)
        ON DELETE CASCADE
    );
    """)

    relacao_demanda = [
        ("1111111111111", "0000000123", "33344455566", 0)
    ]
    cursor.executemany("INSERT INTO demanda (ISBN, id, cpf, atendido) VALUES (?, ?, ?, ?)", relacao_demanda)

    conn.commit()

    cursor.execute("""
        CREATE TABLE secao (
        id_biblioteca CHAR(10) NOT NULL,
        codigo CHAR(10) NOT NULL,
        descricao VARCHAR2(100) NOT NULL,
        CONSTRAINT pk_secao PRIMARY KEY (id_biblioteca, codigo),
        CONSTRAINT fk_biblioteca FOREIGN KEY (id_biblioteca)
            REFERENCES biblioteca (id)
            ON DELETE CASCADE
        );
    """)

    secao = [
        ("0000000123", "0000000001", "Fantasia"),
        ("0000000123", "0000000002", "Ficção Literária Americana"),
        ("0000000123", "0000000003", "Literatura Nacional Clássica"),
    ]
    cursor.executemany("INSERT INTO secao (id_biblioteca, codigo, descricao) VALUES (?, ?, ?)", secao)

    conn.commit()

conn.close()