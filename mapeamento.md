# Mapeamento

## Entidades regulares

### Empréstimo

Emprestimo(<u>id</u>, prazo, data, devolvido)

### Exemplar

Exemplar(<u>codigo</u>, edicao)

### Livro

Livro(<u>isbn</u>, nome, ano)

### Autor

Autor(<u>id</u>, nome)

### Coleção

Colecao(<u>id</u>, nome)

### Biblioteca

Biblioteca(<u>id</u>, local_estado, local_cep, local_numero)

### Cargo Comissionado

CargoComissionado(<u>cargo</u>, valor)

## Entidades fracas

### Seção

Secao(<u>id_biblioteca, codigo</u>, descricao)<br>
&nbsp;&nbsp;&nbsp;&nbsp;id_biblioteca → Biblioteca(id)

## Super/subentidades

### Super-entidade Pessoa

Pessoa(<u>cpf</u>, nome)

Telefone(<u>cpf_pessoa, telefone</u>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;cpf_pessoa → Pessoa(cpf)

### Sub-entidade Sócio

Socio(<u>cpf_pessoa</u>, cartao)<br>
&nbsp;&nbsp;&nbsp;&nbsp;cpf_pessoa → Pessoa(cpf)

### Sub-entidade Funcionário

Funcionario(<u>cpf_pessoa</u>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;cpf_pessoa → Pessoa(cpf)

## Entidades associativas

Trabalha(<u>cpf_funcionario, id_biblioteca</u>, data, cargo_comissionado)<br>
&nbsp;&nbsp;&nbsp;&nbsp;cpf_funcionario → Funcionario(cpf)<br>
&nbsp;&nbsp;&nbsp;&nbsp;id_biblioteca → Biblioteca(id)<br>
&nbsp;&nbsp;&nbsp;&nbsp;cargo_comissionado → CargoComissionado(cargo)

## Relacionamentos
