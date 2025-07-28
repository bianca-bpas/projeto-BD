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

rebooted = True

if rebooted:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  pessoa (
    cpf  CHAR(11)        NOT NULL,
    nome VARCHAR2(100)   NOT NULL,
    CONSTRAINT pk_pessoa PRIMARY KEY (cpf)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  telefone (
    pessoa_fk CHAR(11)        NOT NULL,
    telefone  VARCHAR2(20)    NOT NULL,
    CONSTRAINT pk_telefone PRIMARY KEY (pessoa_fk, telefone),
    CONSTRAINT fk_telefone_pessoa FOREIGN KEY (pessoa_fk)
        REFERENCES pessoa (cpf)
        ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  socio (
    cpf  CHAR(11)      NOT NULL,
    cartao  VARCHAR2(16)  NOT NULL,
    CONSTRAINT pk_socio PRIMARY KEY (cpf),
    CONSTRAINT fk_socio_pessoa FOREIGN KEY (cpf)
        REFERENCES pessoa(cpf)
        ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  funcionario (
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
    CREATE TABLE IF NOT EXISTS  biblioteca (
    id  VARCHAR2(10)        NOT NULL,
    local_estado VARCHAR2(100)   NOT NULL,
    local_cep VARCHAR2(8)   NOT NULL,
    local_numero NUMBER(5) NOT NULL,
    CONSTRAINT pk_biblioteca PRIMARY KEY (id)
    );
    """)


    bibs = [
        ("0000000123", "Pernambuco", "12345678", 100),
        ("4560010000", "Parauapebas", "12345999", 87),
        ("6097157000", "Sucupira do Riachão", "98426611", 901)
    ]
    cursor.executemany("INSERT INTO biblioteca (id, local_estado, local_cep, local_numero) VALUES (?, ?, ?, ?)", bibs)


    conn.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  livro (
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
    CREATE TABLE IF NOT EXISTS  autor (
    id  VARCHAR2(12)        NOT NULL,
    nome VARCHAR2(100)   NOT NULL,
    CONSTRAINT pk_autor PRIMARY KEY (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  colecao (
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
    CREATE TABLE IF NOT EXISTS  pertence (
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
    CREATE TABLE IF NOT EXISTS  escreve (
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
    CREATE TABLE IF NOT EXISTS  demanda (
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
        CREATE TABLE IF NOT EXISTS  secao (
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS  exemplar (
        id_biblioteca CHAR(10) NOT NULL,
        codigo NUMBER(10) NOT NULL,
        ISBN VARCHAR2(13) NOT NULL,
        id_biblioteca_from_secao CHAR(10),
        codigo_secao CHAR(10),
        CONSTRAINT pk_exemplar PRIMARY KEY (id_biblioteca, codigo),
        CONSTRAINT fk_biblioteca FOREIGN KEY (id_biblioteca)
            REFERENCES biblioteca (id)
            ON DELETE CASCADE,
        CONSTRAINT fk_secao FOREIGN KEY (id_biblioteca_from_secao, codigo_secao)
            REFERENCES secao (id_biblioteca, codigo)
            ON DELETE CASCADE
        CONSTRAINT fk_isbn FOREIGN KEY(ISBN)
            REFERENCES livro(ISBN)
            ON DELETE CASCADE
        );
    """)

    exemplares = [
        ("0000000123", 1, "9786584952003", "0000000123", "0000000002"),
        ("0000000123", 2, "9786584952003", "0000000123", "0000000002"),
        ("4560010000", 1, "9786584952003", None, None), 
        ("0000000123", 3, "9797138852114", "0000000123", "0000000001"),
        ("0000000123", 4, "9797138852114", None, None),
        ("0000000123", 5, "1750094135220", "0000000123", "0000000001"),
        ("0000000123", 6, "0965180092413", "0000000123", "0000000001")
    ]
    cursor.executemany("INSERT INTO exemplar (id_biblioteca, codigo, ISBN, id_biblioteca_from_secao, codigo_secao) VALUES (?, ?, ?, ?, ?)", exemplares)

    conn.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  emprestimo (
      id NUMBER(10) PRIMARY KEY,
      cpf_socio CHAR(11),
      data DATE,
      prazo DATE,
      id_biblioteca CHAR(10),
      codigo_exemplar NUMBER(10),
      CONSTRAINT fk_emprestimo_socio FOREIGN KEY (cpf_socio) REFERENCES SOCIO(CPF),
      CONSTRAINT fk_emprestimo_exemplar FOREIGN KEY (id_biblioteca, codigo_exemplar) REFERENCES EXEMPLAR(id_biblioteca, codigo)
    );
    """)

    emprestimos = [
        (1, "22233344455", "2024-06-01", "2024-06-16", "0000000123", 1),
        (2, "44455566677", "2024-06-02", "2024-06-12", "0000000123", 3)
    ]
    cursor.executemany("INSERT INTO EMPRESTIMO (id, cpf_socio, data, prazo, id_biblioteca, codigo_exemplar) VALUES (?, ?, ?, ?, ?, ?)", emprestimos)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  cargo_comissionado (
    cargo_comissionado VARCHAR(63)  NOT NULL,
    gratificacao NUMBER(5, 2)   NOT NULL,
    descricao VARCHAR(255),
    CONSTRAINT pk_cargo_com PRIMARY KEY (cargo_comissionado)
    );
    """)
    coms = [
        ("Assessor de business", 1000.00, "Alinha processos e integra o backbone com a lógica de negócios."),
    ]

    cursor.executemany("INSERT INTO cargo_comissionado (cargo_comissionado, gratificacao, descricao) VALUES (?, ?, ?)", coms)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trabalha(
        data DATE NOT NULL,
        cpf_socio CHAR(11) NOT NULL,
        id_biblioteca CHAR(10) NOT NULL,
        nome_cargo VARCHAR(63),

        CONSTRAINT fk_trabalha_cargo
            FOREIGN KEY(nome_cargo) REFERENCES cargo_comissionado(nome),
        CONSTRAINT uc_nome_cargo UNIQUE(nome_cargo),
        CONSTRAINT pk_trabalha PRIMARY KEY(data,cpf_socio,id_biblioteca),
        CONSTRAINT fk_trabalha_cpf
            FOREIGN KEY(cpf_socio) REFERENCES socio(cpf),
        CONSTRAINT fk_trablha_biblioteca
            FOREIGN KEY(id_biblioteca) REFERENCES biblioteca(id)
    )""")

    trabalha = [
        ("2024-06-01", "22233344455", "0000000123", "Assessor de business"),
        ("2024-06-02", "44455566677", "0000000123", None)
    ]

    cursor.executemany("INSERT INTO trabalha (data, cpf_socio, id_biblioteca, nome_cargo) VALUES (?, ?, ?, ?)", trabalha)

    conn.commit()

conn.close()