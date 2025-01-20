# Projeto de Automação Google Sheets e Google Docs
Este projeto visa automatizar a criação de documentos no Google Docs a partir de dados extraídos de uma planilha do Google Sheets. O fluxo de trabalho inclui ler os dados de uma planilha, formatá-los de acordo com certos critérios (como status dos projetos) e gerar um documento no Google Docs, onde as informações são organizadas e visualmente destacadas, criando um briefing de projetos.

obs: para criar uma conta no google cloud para acessar as API's necessarias demora menos de 10 minutos e seu uso é 100% gratuito,  [tutorial](https://www.youtube.com/watch?v=j7JlI6IAdQ0)

## Escolha da Ferramenta

**Python:** Escolhido pela sua facilidade de uso e pela grande disponibilidade de bibliotecas que facilitam a automação e integração com APIs. 

**API do Google Docs e Google Sheets:** Utilizadas para acessar e manipular documentos e planilhas diretamente. Elas são altamente escaláveis, seguras e oferecem integração fácil com o ecossistema do Google. Assim como são gratuitas, facéis de serem utilizadas e aumentam drasticamente a automatização, pois sem elas não é possivel criar documentos diretamente no google docs por python.

## Passo a Passo da Implementação

### 1. **Autenticação do Google API**
   - O script usa a biblioteca `google_auth_oauthlib` para autenticação.
   - O arquivo de credenciais (`credentials.json`) é necessário, e ele pode ser obtido a partir do [Google Cloud Console](https://console.cloud.google.com/).

### 2. **Leitura da Planilha do Google Sheets**
   - A função `le_sheets()` é responsável por ler uma planilha a partir do link fornecido.
   - A URL do Google Sheets é processada pela função `extrai_ID()`, que extrai o ID da planilha do link.
   - O conteúdo da planilha é lido e convertido em um DataFrame do `pandas`.

### 3. **Processamento e Formatação dos Dados**
   - Os dados são organizados e formatados de acordo com o status dos projetos: "Em andamento", "Pendente" ou "Concluído".
   - Cada status recebe uma cor específica e o projeto é detalhado com informações como nome, responsável, prazo e descrição.

### 4. **Criação do Documento no Google Docs**
   - Um novo documento é criado no Google Docs usando a função `criar_documento()`.
   - O nome do documento é gerado dinamicamente com base na data atual.

### 5. **Inserção de Dados e Formatação no Documento**
   - A função `adicionar_texto()` insere os dados formatados no documento do Google Docs.
   - Estilos de texto (negrito, cor e tamanho da fonte) são aplicados aos dados para destacar as informações importantes.

### 6. **Execução Completa**
   - O script principal (`main.py`) chama a função `sheets_to_docs()` do módulo `functions.py`, que realiza todo o processo desde a leitura da planilha até a criação e formatação do documento.


## Requisitos

- Python 3.x
- Bibliotecas: `pandas`, `re`, `google-auth`, `google-auth-oauthlib`, `google-api-python-client`
- Google Cloud Project com as APIs do Google Docs e Google Sheets habilitadas
- Arquivo de credenciais (`credentials.json`) obtido no Google Cloud Console

## Como Usar

### 1. **Obter as Credenciais**
   - Acesse o [Google Cloud Console](https://console.cloud.google.com/), crie um projeto e habilite as APIs do Google Docs e Sheets.
   - Gere o arquivo de credenciais `credentials.json` e faça o download.

### 2. **Instalar Dependências**
   - Instale as bibliotecas necessárias executando:
   pip install pandas google-auth google-auth-oauthlib google-api-python-client

### 3. **Executar código**
  - Mude as variaveis sheets_link (que contém o link para o arquivo do google sheets) e credentials_path (que contém o diretorio do seu arquivo de credencias google cloud) no arquivo `main.py`
  - Execute o `main.py`
  - O script irá abrir uma página para poder fazer o login na conta do google
  - Sera gerado um arquivo no google docs com o nome Project Briefing {data atual}, caso deseje mudar o nome, adicione mais um argumento a função `sheets_to_docs()` com o nome desejado
  - 
## Limitações

- **Estrutura da Planilha**: O código assume que a planilha tem uma estrutura pré-definida. Alterações nas colunas ou na organização dos dados podem exigir ajustes no código.
- **Autenticação Manual**: A autenticação exige interação do usuário. Para uso em servidores ou de forma automatizada, seria necessário modificar o processo de autenticação.

## Melhorias Futuras

- **Automatizar a Autenticação**: Implementar um processo de autenticação sem a necessidade de interação do usuário, adequado para uso em servidores ou execução em segundo plano.
- **Customização de Formatação**: Permitir que o usuário defina as cores e os estilos diretamente no script ou em um arquivo de configuração.


## Refêrencias

  - https://developers.google.com/docs/api/quickstart/python?hl=pt-br
  - https://www.youtube.com/watch?v=j7JlI6IAdQ0


