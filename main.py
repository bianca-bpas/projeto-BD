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
    cpf_chefe  CHAR(11),
    CONSTRAINT pk_funcionario PRIMARY KEY (cpf),
    CONSTRAINT fk_func_pessoa FOREIGN KEY (cpf)
        REFERENCES pessoa(cpf)
        ON DELETE CASCADE,
    CONSTRAINT fk_chefia
        FOREIGN KEY (cpf_chefe)
        REFERENCES funcionario(cpf)
        ON DELETE SET NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  biblioteca (
    id  VARCHAR2(10)        NOT NULL,
    local_estado VARCHAR2(100)   NOT NULL,
    local_cep VARCHAR2(8)   NOT NULL,
    local_numero NUMBER(5) NOT NULL,
    CONSTRAINT pk_biblioteca PRIMARY KEY (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  livro (
    ISBN  VARCHAR2(13)        NOT NULL,
    nome VARCHAR2(100)   NOT NULL,
    ano NUMBER(5)   NOT NULL,
    CONSTRAINT pk_livro PRIMARY KEY (ISBN)
    );
    """)

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

    conn.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  demanda (
    ISBN  VARCHAR2(13)        NOT NULL,
    id  VARCHAR2(10)        NOT NULL,
    cpf CHAR(11) NOT NULL,
    atendido NUMBER(1) NOT NULL,
    data DATE NOT NULL,
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


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS  secao (
        id_biblioteca CHAR(10) NOT NULL,
        codigo CHAR(10) NOT NULL,
        descricao VARCHAR2(100),
        CONSTRAINT pk_secao PRIMARY KEY (id_biblioteca, codigo),
        CONSTRAINT fk_biblioteca FOREIGN KEY (id_biblioteca)
            REFERENCES biblioteca (id)
            ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS  exemplar (
        codigo NUMBER(10) NOT NULL,
        ISBN VARCHAR2(13) NOT NULL,
        id_biblioteca_from_secao CHAR(10) NOT NULL, 
        codigo_secao CHAR(10) NOT NULL,
        CONSTRAINT pk_exemplar PRIMARY KEY (codigo),
        CONSTRAINT fk_secao FOREIGN KEY (id_biblioteca_from_secao, codigo_secao)
            REFERENCES secao (id_biblioteca, codigo)
            ON DELETE CASCADE
        CONSTRAINT fk_isbn FOREIGN KEY(ISBN)
            REFERENCES livro(ISBN)
            ON DELETE CASCADE
        );
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  emprestimo (
      id NUMBER(10) PRIMARY KEY,
      cpf_socio CHAR(11) NOT NULL,
      data DATE,
      prazo DATE,
      codigo_exemplar NUMBER(10) NOT NULL,
      devolvido NUMBER(1),
      CONSTRAINT fk_emprestimo_socio FOREIGN KEY (cpf_socio) REFERENCES SOCIO(CPF),
      CONSTRAINT fk_emprestimo_exemplar FOREIGN KEY (codigo_exemplar) REFERENCES EXEMPLAR(codigo)
    );
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  cargo_comissionado (
    cargo VARCHAR(63)  NOT NULL,
    valor NUMBER(5, 2)   NOT NULL,
    CONSTRAINT pk_cargo_com PRIMARY KEY (cargo)
    );
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trabalha(
        data DATE NOT NULL,
        cpf_funcionario CHAR(11) NOT NULL,
        id_biblioteca CHAR(10) NOT NULL,
        cargo_comissionado VARCHAR(63) UNIQUE,

        CONSTRAINT fk_trabalha_cargo
            FOREIGN KEY(cargo_comissionado) REFERENCES cargo_comissionado(cargo),
        CONSTRAINT uc_cargo_comissionado UNIQUE(cargo_comissionado),
        CONSTRAINT pk_trabalha PRIMARY KEY(data,cpf_funcionario,id_biblioteca),
        CONSTRAINT fk_trabalha_cpf
            FOREIGN KEY(cpf_funcionario) REFERENCES funcionario(cpf),
        CONSTRAINT fk_trabalha_biblioteca
            FOREIGN KEY(id_biblioteca) REFERENCES biblioteca(id)
    )""")


conn.close()