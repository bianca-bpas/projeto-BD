import sqlite3

conn = sqlite3.connect("biblioteca.db")
cursor = conn.cursor()

#subconsulta escalar
#nome do livro e quantidade de emprestimos dele (motivação: analisar demanda)
query0 = """
SELECT nome,(
    SELECT COUNT(*)
    FROM emprestimo
    WHERE (codigo_exemplar) in (
                SELECT codigo
                FROM exemplar E
                WHERE E.ISBN = L.ISBN
                )
)
FROM livro L;
"""

cursor.execute(query0)
resultados = cursor.fetchall()

for nome,qtd in resultados:
    print(f"{nome} - qtd demanda: {qtd}")

print('\n')

#juncao interna e group by
#livros que tem demanda na bilioteca A e existem em outra (motivação: possivel transferência de livros para evitar compra)
query1 = """
SELECT D.id,L.nome,EX.id_biblioteca_from_secao,COUNT(*)
FROM demanda D
JOIN livro L ON L.ISBN = D.ISBN
JOIN exemplar EX ON EX.ISBN = D.ISBN
WHERE EX.id_biblioteca_from_secao != D.id AND D.atendido = 0
GROUP BY EX.id_biblioteca_from_secao,D.id,L.nome;
"""

cursor.execute(query1)
resultados = cursor.fetchall()

for id1,nome,id2,qtd in resultados:
    print(f"ID_falta: {id1} - Nome livro: {nome} - ID_tem e qtd: {id2} - {qtd}")

print('\n')

#semijoin
#demandas de pessoas que são socios (motivação: priorizar pedidos de clientes)
query2 ="""
SELECT D.cpf,D.id,D.ISBN
FROM demanda D
WHERE D.cpf in (
            SELECT P.cpf
            FROM pessoa P
            WHERE EXISTS (
                    SELECT 1
                    FROM socio S
                    WHERE S.cpf = P.cpf
                    )
        );
"""

cursor.execute(query2)
resultados = cursor.fetchall()

for cpf,id,isbn in resultados:
    print(f"CPF:{cpf} - ID_lib: {id} - ISBN: {isbn}")

print('\n')

#nome e telefone de todos os sócios com livros atrasados
query3 ="""
SELECT P1.NOME, P1.TELEFONE, P2.PRAZO
FROM 
    (SELECT E.CPF_SOCIO, E.PRAZO
     FROM EMPRESTIMO E
     WHERE E.DEVOLVIDO = 0 AND E.PRAZO < '2024-07-01') P2,
    (SELECT P.NOME, P.CPF, T.TELEFONE
     FROM PESSOA P, TELEFONE T
     WHERE P.CPF = T.PESSOA_FK) P1
WHERE P1.CPF = P2.CPF_SOCIO
"""

cursor.execute(query3)
resultados = cursor.fetchall()

for nome in resultados:
    print(nome)

print('\n')

#autores com mais livros emprestados
query4 ="""
SELECT A.NOME, COUNT(*)
FROM AUTOR A, (SELECT EX.ISBN
                FROM EMPRESTIMO E, EXEMPLAR EX
                WHERE E.CODIGO_EXEMPLAR = EX.CODIGO) P1
WHERE A.ID IN (SELECT ESC.ID
                FROM ESCREVE ESC
                WHERE ESC.ISBN = P1.ISBN)
GROUP BY A.NOME
ORDER BY COUNT(*) DESC;
"""

cursor.execute(query4)
resultados = cursor.fetchall()

for nome in resultados:
    print(nome)

print('\n')

#funcionarios que sao socios
query5 ="""
SELECT P.NOME
FROM PESSOA P, (SELECT F.CPF
                FROM FUNCIONARIO F, SOCIO S
                WHERE F.CPF = S.CPF) P2
WHERE P.CPF = P2.CPF;
"""

cursor.execute(query5)
resultados = cursor.fetchall()

for nome in resultados:
    print(nome)

print('\n')

#quantas coleções cada autor participa
query6 ="""
SELECT A.NOME, COUNT(*)
FROM AUTOR A, (SELECT DISTINCT ESC.ID as ID_AUT, C1.ID as ID_COL
                FROM ESCREVE ESC, (SELECT P.ISBN, P.ID 
                                    FROM PERTENCE P) C1
                WHERE ESC.ISBN = C1.ISBN) C2
WHERE A.ID = C2.ID_AUT
GROUP BY A.NOME
"""

cursor.execute(query6)
resultados = cursor.fetchall()

for nome in resultados:
    print(nome)

print('\n')

#funcionarios que trabalharam em mais de uma filial
query7 ="""
SELECT P.NOME, COUNT(*)
FROM PESSOA P, (SELECT DISTINCT T.CPF_FUNCIONARIO, T.ID_BIBLIOTECA
                FROM TRABALHA T) P1
WHERE P.CPF = P1.CPF_FUNCIONARIO
GROUP BY P.NOME
HAVING COUNT(*) >= 2
"""

cursor.execute(query7)
resultados = cursor.fetchall()
print()

# juncao externa
# Bibliotecas sem seção
query8 ="""
select id from biblioteca left join secao s on s.id_biblioteca = id where s.id_biblioteca is null;
"""

cursor.execute(query8)
resultados = cursor.fetchall()
for nome in resultados:
    print(nome)
print()


# anti join, subconsulta relacionada de tabela
# Livros nunca emprestados
query9 ="""
select nome,isbn from livro l where not exists (select 1 from emprestimo where codigo_exemplar IN (select codigo from exemplar e where e.isbn = l.isbn));

"""

cursor.execute(query9)
resultados = cursor.fetchall()
for nome in resultados:
    print(nome)
print()


# operacao de conjunto (union)
# livros mais demandados ou com muitos emprestimos: livros em destaque
query10 = """
SELECT l.nome,'Emprestimos' as ocorrencia, count(e.codigo) AS emp FROM livro l JOIN exemplar e ON l.isbn = e.isbn GROUP BY l.nome UNION
SELECT l1.nome,'Demandas',count(*) as emp2 from livro l1 JOIN demanda d ON d.isbn = l1.isbn GROUP BY l1.nome ORDER BY emp DESC;
"""
cursor.execute(query10)
resultados = cursor.fetchall()
for nome in resultados:
    print(nome)
print()


print('\n')


#quantas vezes cada coleção foi concluída (todos os livros emprestados por uma pessoa)
query11 ="""
SELECT C.NOME, COUNT(*)
FROM COLECAO C, (SELECT P2.ID, P2.CPF_SOCIO
                FROM (SELECT P.ID, P1.CPF_SOCIO, COUNT(*) as CONT
                    FROM PERTENCE P, (SELECT DISTINCT E.CPF_SOCIO, EX.ISBN 
                                    FROM EMPRESTIMO E, EXEMPLAR EX
                                    WHERE E.CODIGO_EXEMPLAR = EX.CODIGO) P1
                    WHERE P.ISBN = P1.ISBN
                    GROUP BY P.ID, P1.CPF_SOCIO) P2
                WHERE CONT = (SELECT COUNT(*)
                                FROM PERTENCE PE
                                WHERE PE.ID = P2.ID
                                GROUP BY PE.ID)) P3
WHERE C.ID = P3.ID
GROUP BY C.NOME
"""

cursor.execute(query11)
resultados = cursor.fetchall()

for nome in resultados:
    print(nome)

print('\n')

#pessoas que nao sao socios nem funcionarios (antijoin + union)
query12 ="""
SELECT P.NOME
FROM PESSOA P
WHERE P.CPF NOT IN (
    SELECT CPF FROM SOCIO
    UNION
    SELECT CPF FROM FUNCIONARIO
);
"""

cursor.execute(query12)
resultados = cursor.fetchall()

#autor com mais livros emprestados 
query13 ="""
SELECT nome, total_emprestimos
FROM (
    SELECT A.nome, COUNT(*) AS total_emprestimos
    FROM emprestimo E
    JOIN exemplar EX ON E.codigo_exemplar = EX.codigo
    JOIN escreve ESC ON EX.ISBN = ESC.ISBN
    JOIN autor A ON ESC.id = A.id
    GROUP BY A.nome
    ORDER BY total_emprestimos DESC
    LIMIT 1
) AS top_autor;
"""

cursor.execute(query13)
resultados = cursor.fetchall()

for nome in resultados:
    print(nome)

print('\n')

conn.close()

