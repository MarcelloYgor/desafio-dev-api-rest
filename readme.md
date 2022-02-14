
# Resolução

## API Restful em Python

Utilização do framework connexion (Flask e Swagger) para o webserver.
Utilização do framework Flask-SQLAlchemy como ORM.

A documentação da API pode ser consultada em *localhost:5000/ui*.

OBSERVAÇÕES:

> Ao inicializar o projeto, um arquivo de banco de dados SQL do SQLite é criado (test.db), talvez seja necessário alterar o caminho no *config.py*;
> A API foi escrita seguindo o padrão Restful, então as operações de depositar e sacar são acionadas na criação de uma transação (POST /operador/{operador_id}/conta/{conta_id}/transacao) com o tipo de transação enviada no body (transacao: DEPOSITO | SAQUE);
> Foi adicionada uma tabela de usuários para autenticação com JWT;
> As rotas que precisam de um token estão marcadas na documentação Swagger e o token deve ser passado no header como um _**'Bearer <token>'**_;
> A função de fechar a conta pelo portador foi interpretada como exclusão de conta;
> O bloqueio e ativação de contas é permitido somente por usuários administradores (parâmetro admin) e um Design Pattern **Decorator** valida a permissão (PATCH /portador/{portador_id}/conta/{id}).

### Inicializando o projeto:

#### Para iniciar localmente:

> Execute na pasta _**src**_.

~~~ssh
flask run
~~~

#### Para rodar os testes automatizados:

> Execute na pasta _**src**_.

~~~ssh
pytest
~~~

#### Para iniciar em uma imagem docker:

> Execute na pasta principal, onde está o _**Dockerfile**_.

~~~ssh
docker build -t flask-dock:latest .
docker run -d -p 5000:5000 flask-dock
~~~

### Deploy em nuvem

Um arquivo de configuração Kubernetes foi adicionado ao projeto, compatível com Kubernetes e AWS EKS.
É necessário atender alguns requisitos para iniciar como um serviço Kubernetes como DNS, Load Balancer e instância de banco de dados relacional.

OBSERVAÇÕES:

> Os arquivos são apenas um esboço;
> Pode-se utilizar o Kustomize para customizar ambientes de implantação;
> Não foram considerados arquivos de configuração, segredos e variáveis de ambiente.

### Considerações

Pelo tamanho da API, a construção de um único serviço com acesso a um banco de dados relacional bem definido pode atender a certos escopos de negócio.
Pensando em escalabilidade ilimitada e integração com diversos outros serviços, pode-se considerar construir a API com uma divisão maior e mais específica para um ambiente de microsserviços, utilizar bancos de dados relacionacionais com abordagem de fragmentação e federação ou bancos não-relacionais e utilizar ferramentas específicas para algumas funcionalidades, como a autenticação de usuários.

# Cenário

A Dock está crescendo e expandindo seus negócios, gerando novas oportunidades de revolucionar o mercado financeiro e criar produtos diferenciados.
Nossa próxima missão é construir uma nova conta digital Dock para nossos clientes utilizarem através de endpoints, onde receberemos requisições em um novo backend que deverá gerenciar as contas e seus portadores (os donos das contas digitais).

## Requisitos

- Deve ser possível criar e remover **portadores**
    - Um **portador** deve conter apenas seu *nome completo* e *CPF*
    - O *CPF* deve ser válido e único no cadastro de **portadores**
- As **contas digital Dock** devem conter as seguintes funcionalidades:
    - A conta deve ser criada utilizando o *CPF* do **portador**
    - Uma conta deve ter seu *saldo*, *número* e *agência* disponíveis para consulta
    - Necessário ter funcionalidade para fazer a *consulta de extrato* da conta *por período*
    - Um **portador** pode fechar a **conta digital Dock** a qualquer instante
    - Executar as operações de *saque* e *depósito*
        - *Depósito* é liberado para todas as *contas ativas* e *desbloqueadas*
        - *Saque* é permitido para todas as *contas ativas* e *desbloqueadas* desde que haja *saldo disponível* e não ultrapasse o limite diário de *2 mil reais*

### Regulação obrigatória

- Precisamos *bloquear* e *desbloquear* a **conta digital Dock** a qualquer momento
- A **conta digital Dock** nunca poderá ter o *saldo negativo*


## Orientações

Utilize qualquer uma das linguagens de programação:
- Java
- Javascript
- Typescript
- Python
- Kotlin
- Golang

Desenvolva o case seguindo as melhores práticas que julgar necessário, aplique todos os conceitos, se atente a qualidade, utilize toda e qualquer forma de governança de código válido. Vamos considerar toda e qualquer implementação, trecho de código, documentação e/ou intenção compartilhada conosco. Esperamos também que o desafio seja feito dentro do tempo disponibilizado e que esteja condizente com a posição pretendida.

É necessário ter o desafio 100% funcional contendo informações e detalhes sobre: como iniciar a aplicação, interagir com as funcionalidades disponíveis e qualquer outro ponto adicional.

## Diferenciais

- Práticas, padrões e conceitos de microservices será considerado um diferencial para nós por existir uma variedade de produtos e serviços dentro da Dock.
- Temos 100% das nossas aplicações e infraestrutura na nuvem, consideramos um diferencial, caso o desafio seja projeto para ser executado na nuvem.
- Nossos times são autônomos e têm liberdade para definir arquiteturas e soluções. Por este motivo será considerado diferencial toda: arquitetura, design, paradigma e documentação detalhando a sua abordagem.

### Instruções

    1. Faça o fork do desafio;
    2. Crie um repositório privado no seu github para o projeto e adicione como colaborador, os usuários informados no email pelo time de recrutameto ;
    3. Após concluir seu trabalho faça um push; 
    4. Envie um e-mail à pessoa que está mantendo o contato com você durante o processo notificando a finalização do desafio para validação.
