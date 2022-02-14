# Deploy em nuvem

Um arquivo de configuração Kubernetes foi adicionado ao projeto, compatível com Kubernetes e AWS EKS.
É necessário atender alguns requisitos para iniciar como um serviço Kubernetes como DNS, Load Balancer e instância de banco de dados relacional.

OBSERVAÇÕES:

> Os arquivos são apenas um esboço;
> É preciso configurar um cluster SQL externo e alterar o arquivo de configuração;
> Pode-se utilizar o Kustomize para customizar ambientes de implantação;
> Não foram considerados arquivos de configuração, segredos e variáveis de ambiente.
