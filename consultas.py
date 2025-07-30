import sqlite3

conn = sqlite3.connect("biblioteca.db")
cursor = conn.cursor()

#subconsulta escalar e de tabela
#nome do livro e quantidade de emprestimos dele (motivação: analisar demanda)
query0 = """
SELECT nome,(
    SELECT COUNT(*)
    FROM emprestimo
    WHERE (id_biblioteca,codigo_exemplar) in (
                SELECT id_biblioteca,codigo
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
SELECT D.id,L.nome,EX.id_biblioteca,COUNT(*)
FROM demanda D
JOIN livro L ON L.ISBN = D.ISBN
JOIN exemplar EX ON EX.ISBN = D.ISBN
WHERE EX.id_biblioteca != D.id AND D.atendido = 0
GROUP BY EX.id_biblioteca,D.id,L.nome;
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

#descubra
query3 ="""
SELECT A.NOME
FROM AUTOR A
WHERE A.ID = '000000000007';
"""

cursor.execute(query3)
resultados = cursor.fetchall()

for nome in resultados:
    print(nome[0])

print('\n')

conn.close()