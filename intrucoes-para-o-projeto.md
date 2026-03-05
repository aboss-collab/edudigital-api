# Intruções gerais para inicio do projeto

(Instale o git no seu computador https://git-scm.com/book/pt-br/v2/Come%C3%A7ando-Instalando-o-Git)

## 1 - Localize a pasta que você quer baixar o projeto e clone o repositório:

>git clone git@github.com:aboss-collab/edudigital-api.git

## 2 - Crie uma branch pessoal para as suas alterações:

Como boas praticas, você deve criar uma branch para identificar a sua seção,
caso julgue necessario, a partir da sua branch crie novas branchs para as etapas
das sua atividade.

>git checkout -b seu-nome-e-sobrenome-section

### 2.1 - Mantenha sempre seu código atualizado:

Antes de tomar qualquer ação para inciar sua parte do projeto, verifique se os códigos estão atualizados
em relação ao git.

Vá para branch main:

>git checkout main<br/>
>git pull

Com esses processos, você garante que estará atualizado com o nosso github, e não jogará fora qualquer progresso
que você já tiver feito, caso programe antes de fazer isso.

Para voltar para sua branch como tudo atualizado:

>git checkout seu-nome-e-sobrenome-section<br/>
>git merge main

### 2.2 - Caso divida sua branch em branches de etapas:

Para criar branches para etapas do projeto:

>git checkout -b etapa-exemplo-branch

Você pode commitar (seção 4.2) na branch de etapa, mas lembre-se que você deve fazer o pull request,
a partir da sua branch então, antes de utilizar o:

>git push

Faça:

>git checkout seu-nome-e-sobrenome-section<br/>
>git merge etapa-exemplo-branch

## 3 - Para iniciar sua parte:

Nosso projeto é focado nas 3 áreas cruciais para o funcionamento de um projeto:

- backend
- banco de dados
- frontend

a partir de agora as instruções serão separadas de acordo com a área a ser desenvolvida.

# Backend

## 1  Criando e ativando o .venv (ambiente virtual de desenvolvimento):

Dentro do nosso backend você precisará criar o ambiente virtual ".venv", onde vai ser necessário instalar as bibliotecas e depências que iremos usar,
para realizar a comunicacao com o frontend (para testar a comunitcacao, será usada a extensão thunder client)

Antes de tentar criar o ambiente virtual, verifique se já existe uma pasta chamada ".venv" na pasta do backend, e caso exista delete-a.

Para criar o ambiente virtual:

>python -m venv .venv

Agora você precisa ativá-lo:

>./.venv/Scripts/activate

Com o ambiente virtual ativo, você tera que instalar as bibliotecas, com os seguintes comandos:

>pip install -r requirements.txt

Para ativar o endereço de backend, depois de estar no ambiente virtual, utilize:

>flask --app ./src/app run --debug

Fazendo isso você vai habilitar o uso, terminando de programar, desative-a:

>deactivate

## 2 - Sobre o desenvolvimento:

Durante o desenvolvimento, todos os nossos códigos vão estar no caminho "backend/src/", lembre-se de criar os arquivos de código ".py" nele,
será importante para criarmos as rotas de comunicacão com o frontend que estão no arquivo "app.py" presente no mesmo caminho.

Não delete arquivos criado por outros colegas, e se for altera-los, lembre-se de informar e deixar o código anterior comentado para backup.

## 3 - Extensão thunder client:

Uma extensão útil para gente é o thunder client, onde podemos testar as requisições do projeto:

>GET POST PUT DELETE

Se você tiver iniciado o backend, o endereço dele será o:

>http://localhost:5000

Para testar um exemplo de funcionamento, voce pode utilizar o que já foi programado em:

>http://localhost:5000/register

No endereço do thunder client, selecione o metodo de POST, e envie um dado qualquer em JSON:

>{
>    "dado de teste": "teste"
>}

Se ele receber o dado e apresentar status de codigo 200, o backend estará recebendo a comunicação em JSON.

# 2 Frontend

## 1 - Atentar aos arquivos estarem alocados nas pastas corretas

Apenas o index.html deve estar na pasta base de frontend, sempre que for escrever um script deverá ser externo em um aquivo .js
e adicionado a pasta de scripts.

Os aquivos .css devem ser sempre adicionados a pasta de styles e os .html dentro dentro de pages.


