# Projeto de Controle Estatístico de Processos

Este projeto visa implementar um sistema de monitoramento e análise de processos utilizando **Controle Estatístico de Processos (CEP)**. Através de gráficos e cálculos estatísticos, ele permite verificar a capacidade do processo de atender às especificações e identificar potenciais problemas, como a violação das regras de controle. O projeto é baseado em **Python** e utiliza o **Telegram Bot** para enviar feedback sobre o status do processo.

Este é um trabalho da disciplina **Tópicos Especiais em Eletrônica**, lecionada pelo professor **Henrique Moura** na **Universidade de Brasília**.

## Funcionalidades

O menu de monitoramento do sistema oferece as seguintes opções:

1. **Visualizar dados**: Exibe os dados atuais no arquivo CSV.
2. **Calcular limites de controle**: Calcula os limites de controle superior e inferior baseados nas amostras fornecidas.
3. **Gerar gráfico X-barra e identificar os outliers**: Gera o gráfico de controle X-barra, identifica os pontos fora dos limites de controle e envia um alerta via bot do Telegram se houver violação das regras.
4. **Gerar gráfico R e identificar os outliers**: Gera o gráfico de controle R, identifica os pontos fora dos limites de controle e envia um alerta via bot do Telegram.
5. **Calcular Cp e Cpk**: Calcula e exibe os índices de capacidade do processo (Cp e Cpk).
6. **Sair**: Encerra o programa.

Este projeto utiliza técnicas do controle estatístico de processos para detectar desvios e falhas nos processos de produção, garantindo que os produtos atendam aos padrões de qualidade.

## Requisitos

- **Python 3.x** (recomenda-se usar um ambiente virtual `venv`).
- **Bibliotecas Python**:
  - `matplotlib`: Para geração de gráficos.
  - `numpy`: Para cálculos estatísticos.
  - `requests`: Para enviar mensagens através do Telegram Bot.
  - `pandas`: Para manipulação de dados.

Você pode instalar todas as dependências do projeto utilizando o arquivo `requirements.txt` fornecido.

## Como Baixar e Rodar o Projeto

### 1. Clonando o Repositório

Primeiro, clone o repositório para sua máquina local:

```bash
git clone 
cd lista_exercicios
```

### 2. Criando um Ambiente Virtual

Recomenda-se usar um ambiente virtual (venv) para isolar as dependências do projeto:

```bash
python -m venv venv
```

### 3. Instalando as Dependências

Ative o ambiente virtual e instale as dependências necessárias:

No Windows:
```bash
venv\Scripts\activate
```

No Linux/Mac:

```bash
source venv/bin/activate
```

Depois, instale as dependências com o pip:

```bash
pip install -r requirements.txt
```

### 4. Configurando as Variáveis de Ambiente do Telegram
Este projeto utiliza um bot do Telegram para enviar alertas. Para configurar o bot, siga os seguintes passos:

1. Crie seu bot no Telegram:
No Telegram, procure por BotFather e crie um novo bot. Você receberá um token que será utilizado para autenticar o bot.

2. Obtenha seu chat_id:
Para identificar o chat que o bot deve enviar as mensagens, você pode usar a API do Telegram para descobrir seu chat_id. Uma maneira simples de obter o chat_id é conversar com o bot, acessar a URL abaixo (substituindo TOKEN pelo token do seu bot) e enviar uma mensagem:
```bash
https://api.telegram.org/botTOKEN/getUpdates
```
O chat_id aparecerá na resposta JSON, e você poderá usá-lo para enviar as mensagens.

3. Defina as variáveis de ambiente:
    - No diretório principal, crie um arquivo chamado `.env` e insira o seguinte:
```python
TELEGRAM_TOKEN=seu_token_aqui
CHAT_ID=seu_chat_id_aqui
```
    - Substituia `seu_token_aqui` e `seu_chat_id_aqui` pelos respectivos do seu chat com o bot

5. Rodando o Código
Agora, execute o arquivo principal main.py para iniciar o menu interativo e utilizar as funcionalidades:

```bash
python main.py
```

6. Testando Dados Diferentes
Para testar dados diferentes, você pode alterar o arquivo CSV que o projeto utiliza. O caminho do arquivo está configurado no código da seguinte forma:

```python
file_path = f'data/<nomedoarquivo>.csv'
```
Se quiser usar outro arquivo CSV, basta modificar o nome no código para o novo arquivo que você deseja utilizar.

As opções são:
    - **amostras_perfeitas**: Para amostras em que todas as regras são atendidas e não há alerta de erro
    - **amostras_violando_regras**: Para amostras que violam regras do Western Handbook e são enviados alertas vermelho e amarelo 
    - **data_lista**: Para os dados fornecidos pela lista de exercícios 
    - **data**: Para dados aleatórios gerados por IA