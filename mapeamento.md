# Mapeamento

## Entidades regulares

### Empréstimo

Emprestimo(<u>id</u>, prazo, data, devolvido, !cpf_socio, !codigo_exemplar)<br>
&nbsp;&nbsp;&nbsp;&nbsp;cpf_socio → Socio(cpf)<br>
&nbsp;&nbsp;&nbsp;&nbsp;codigo_exemplar → Exemplar(codigo)<br>

### Exemplar

Exemplar(<u>codigo</u>, edicao, !isbn_livro, !id_biblioteca, !codigo_secao)<br>
&nbsp;&nbsp;&nbsp;&nbsp;isbn_livro → Livro(isbn)<br>
&nbsp;&nbsp;&nbsp;&nbsp;id_biblioteca → Biblioteca(id)<br>
&nbsp;&nbsp;&nbsp;&nbsp;codigo_secao → Secao(codigo)<br>

### Livro

Livro(<u>isbn</u>, !nome, !ano)

Escreve(<u>isbn_livro, id_autor</u>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;isbn_livro → Livro(isbn)<br>
&nbsp;&nbsp;&nbsp;&nbsp;id_autor → Autor(id)<br>

Pertence(<u>isbn_livro, id_colecao</u>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;isbn_livro → Livro(isbn)<br>
&nbsp;&nbsp;&nbsp;&nbsp;id_colecao → Colecao(id)<br>

### Autor

Autor(<u>id</u>, !nome)

### Coleção

Colecao(<u>id</u>, !nome)

### Biblioteca

Biblioteca(<u>id</u>, !local_estado, !local_cep, !local_numero)

Demanda(<u>id_biblioteca, cpf_pessoa, isbn_livro</u>, !data, foi_atendido)<br>
&nbsp;&nbsp;&nbsp;&nbsp;id_biblioteca → Biblioteca(id)<br>
&nbsp;&nbsp;&nbsp;&nbsp;cpf_pessoa → Pessoa(cpf)<br>
&nbsp;&nbsp;&nbsp;&nbsp;isbn_livro → Livro(isbn)<br>

### Cargo Comissionado

Cargo_Comissionado(<u>cargo</u>, !valor)

## Entidades fracas

### Seção

Secao(<u>id_biblioteca, codigo</u>, descricao)<br>
&nbsp;&nbsp;&nbsp;&nbsp;id_biblioteca → Biblioteca(id)

## Super/subentidades

### Super-entidade Pessoa

Pessoa(<u>cpf</u>, !nome)

Telefone(<u>cpf_pessoa, telefone</u>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;cpf_pessoa → Pessoa(cpf)

### Sub-entidade Sócio

Socio(<u>cpf</u>, !cartao)<br>
&nbsp;&nbsp;&nbsp;&nbsp;cpf → Pessoa(cpf)

### Sub-entidade Funcionário

Funcionario(<u>cpf</u>, cpf_chefe)<br>
&nbsp;&nbsp;&nbsp;&nbsp;cpf → Pessoa(cpf)<br>
&nbsp;&nbsp;&nbsp;&nbsp;cpf_chefe → Funcionario(cpf)

## Entidades associativas

Trabalha(<u>cpf_funcionario, id_biblioteca</u>, !data, [cargo_comissionado])<br>
&nbsp;&nbsp;&nbsp;&nbsp;cpf_funcionario → Funcionario(cpf)<br>
&nbsp;&nbsp;&nbsp;&nbsp;id_biblioteca → Biblioteca(id)<br>
&nbsp;&nbsp;&nbsp;&nbsp;cargo_comissionado → CargoComissionado(cargo)
