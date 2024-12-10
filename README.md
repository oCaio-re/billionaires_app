# Projeto de BD
## Bases de Dados (CC2005)

# Para executar:
## Com ambiente virtual(virtual environment):
### Criar um virtual environment:
``` shell
    python3 -m venv .venv
```
### Ativar o python path com o script 'activate':
``` shell
  source .venv/bin/activate
```
### Instalar as dependências:
``` shell
  pip install -r requirements.txt
```
### Executar a aplicação:
``` shell
  python3 app.py
```

## Sem ambiente virtual(virtual environment):
### Instalar as dependências:
``` shell
  pip install -r requirements.txt
```

### Executar a aplicação:
``` shell
  python3 app.py
```

# Objetivo
O projeto pretende constituir uma oportunidade de experimentação das matérias expostas na unidade curricular, em particular a especificação de um modelo UML e respetiva tradução para um modelo relacional e a criação, o povoamento e a interrogação de BD utilizando a linguagem SQL.

# Método
## Trabalho em grupo
O trabalho deverá ser realizado em grupos de 2 ou 3 alunos registados via Moodle. São permitidos também grupos de 1 só aluno em casos especiais.

# Atividades
O projeto é constituído pelos 12 passos abaixo, sendo que o passo 6 é um ponto de controlo que requer a validação pelo docente das práticas.

## Constituição dos grupos;
atribuição de um tema a cada grupo, baseado num dataset com dados reais;
descrição do universo em causa;
elaboração de um diagrama de classes UML correspondente;
mapeamento do modelo de classes UML num modelo relacional;
[wait]-> validação pelo docente das práticas;
criação do esquema da BD no SGBD escolhido (pode ser em SQLite);
povoamento da BD com a totalidade dos dados do dataset;
elaboração de 10+ interrogações em SQL de complexidade variável, extraindo conteúdo relevante do dataset e ilustrando as técnicas de interrogação estudadas;
construção de uma interface em Python com acesso à BD;
escrita do relatório e entrega no Moodle até 2024-12-09;
apresentação do trabalho na aula prática da semana de 2024-12-12/18.
Resultado
Deverá entregar um relatório em formato Word ou PDF, podendo inspirar-se no modelo do documento disponibilizado aqui. A entrega deverá ser feita até 2024-12-09 via Moodle, na presente atividade.

## Restrições
Universo da BD
O universo da BD deverá corresponder a dados reais. O tema do trabalho e o respetivo conjunto de dados serão atribuídos pelos docentes das práticas.

Os modelos de dados elaborados devem captar todo o conteúdo do conjunto de dados e evitar redundâncias, procurando registar cada facto apenas uma vez.

## Modelo relacional
O modelo relacional deverá corresponder a um mapeamento bem feito do diagrama de classes UML e ter chaves primárias e externas bem definidas.

## Povoamento da BD
A implementação do esquema deverá ser realizada em SQLite. As tabelas devem ser povoadas com os dados obtidos do conjunto de dados fornecido, evitando perda de informação.

## Extração de informação
As interrogações SQL, 10 ou mais de complexidade variável, visam ilustrar conteúdos relevantes da BD e, ao mesmo tempo, demonstrar as técnicas de interrogação estudadas.

## Interface
A interface, construída em Python, deverá permitir navegar pelas tabelas e executar as interrogações SQL elaboradas no ponto anterior.
