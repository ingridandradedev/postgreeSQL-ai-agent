# Chatbot de Consultas em PostgreSQL usando OpenAI e LangChain

Este projeto apresenta um **chatbot** que utiliza [LangChain](https://github.com/hwchase17/langchain) para orquestrar interações com a API da **OpenAI** (GPT-4, GPT-3.5, etc.) e executar consultas em um banco de dados **PostgreSQL**. A interface de usuário foi desenvolvida em **Streamlit** e a aplicação backend em **FastAPI**.

---
## Tecnologias utilizadas

- **Python 3.8+**  
- **[LangChain](https://github.com/hwchase17/langchain)**: Framework que facilita a integração de LLMs (Large Language Models) com fontes de dados e ferramentas, permitindo a criação de agentes inteligentes.  
- **[OpenAI API](https://platform.openai.com/docs/introduction)**: Fornece acesso aos modelos de linguagem como GPT-4.  
- **[PostgreSQL](https://www.postgresql.org/)**: Banco de dados relacional utilizado para armazenamento e consulta.  
- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web e de APIs para Python, simples e eficiente.  
- **[Streamlit](https://streamlit.io/)**: Framework para criação de aplicações web interativas e orientadas a dados.  

---
## Visão Geral do Projeto

### Fluxo de funcionamento

1. O usuário acessa a interface **Streamlit** (`streamlit_app.py`):
   - Informa a **OpenAI API Key** (chave secreta).
   - Preenche as credenciais do banco PostgreSQL (host, banco, usuário, senha, porta).
   - Digita perguntas em linguagem natural ou consultas SQL.
2. O **Streamlit** envia as requisições para o **FastAPI** (`main.py`):
   - A chave de API é enviada via cabeçalho HTTP (`Authorization: Bearer <sua_chave>`).
   - As credenciais do PostgreSQL e a mensagem do usuário são enviadas no corpo da requisição.
3. O **FastAPI** (por meio do LangChain):
   - Recebe a chave da OpenAI do cabeçalho.
   - Configura um objeto `ChatOpenAI`.
   - Cria uma ferramenta (Tool) que faz as consultas ao PostgreSQL via `psycopg2`.
   - Interage com o modelo da OpenAI para interpretar a pergunta e, se necessário, executar a consulta no banco.
   - Retorna a resposta ao Streamlit.
4. O **Streamlit** exibe a resposta no chat, simulando uma conversa.

---

## Como Instalar e Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/sua-org/sua-repo.git
cd sua-repo
```

### 2. Criar e ativar um ambiente virtual (opcional, mas recomendado)

No Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

No Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o backend (FastAPI)

Abra um terminal na raiz do projeto e execute:

```bash
uvicorn main:app --reload
```

Por padrão, o servidor ficará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 5. Executar o frontend (Streamlit)

Em outro terminal (continuando no diretório do projeto):

```bash
streamlit run streamlit_app.py
```

O Streamlit abrirá no navegador (geralmente [http://localhost:8501](http://localhost:8501)).

---

## Exemplo de Uso

1. Acesse a página do Streamlit.
2. Digite sua **OpenAI API Key** (ex.: `sk-xxxxx...`).
3. Preencha as credenciais do banco **PostgreSQL**:
   - **Host** (ex.: `localhost`)
   - **Database** (ex.: `meu_banco`)
   - **User** (ex.: `postgres`)
   - **Password** (a senha do seu usuário do PostgreSQL)
   - **Port** (padrão `5432`)
4. Digite um comando ou pergunta, por exemplo:
   ```
   Me mostre os 5 primeiros clientes cadastrados no banco.
   ```
   ou
   ```
   SELECT * FROM clientes LIMIT 5;
   ```
5. Observe a resposta do **chatbot** com os resultados da consulta no PostgreSQL ou uma resposta em linguagem natural.

---

## Estrutura de Arquivos

```
.
├── main.py             # Arquivo com a aplicação FastAPI
├── streamlit_app.py    # Arquivo com a aplicação Streamlit
├── requirements.txt    # Lista de dependências do projeto
└── README.md           # Este arquivo de documentação
```

---

## Personalização

- **Modelo GPT**: Você pode ajustar o parâmetro `model` em `ChatOpenAI` (no `main.py`) para usar `gpt-3.5-turbo`, `gpt-4` ou outro modelo disponível.
- **Temperatura**: Ajuste o nível de criatividade (parâmetro `temperature`), indo de 0 a 1.
- **Variáveis de ambiente**: Se preferir, defina `OPENAI_API_KEY` como variável de ambiente para evitar envio via cabeçalho HTTP.

---

## Dúvidas Frequentes

1. **Por que recebo o erro `Did not find openai_api_key`?**  
   Certifique-se de estar enviando corretamente a chave no cabeçalho (ex.: `Authorization: Bearer sk-xxxx`). Caso esteja usando variáveis de ambiente, verifique se a variável `OPENAI_API_KEY` está realmente definida no ambiente em que o FastAPI roda.

2. **Por que recebo `connection refused` ao tentar consultar o banco?**  
   - Verifique se o servidor PostgreSQL está ativo no host/porta especificados.  
   - Confirme se as credenciais (usuário/senha) estão corretas.

3. **Posso rodar o projeto em produção?**  
   - Sim, porém recomenda-se configurar HTTPS e um servidor mais robusto para o Streamlit, além de configurar logs e segurança adicionais no FastAPI.

---

## Contribuindo

Sinta-se à vontade para abrir [issues](https://github.com/sua-org/sua-repo/issues) ou enviar [pull requests](https://github.com/sua-org/sua-repo/pulls). Qualquer sugestão, correção ou melhoria é bem-vinda.

---

## Licença

Este projeto é distribuído sob a licença [MIT](https://opensource.org/licenses/MIT). Caso necessário, revise o arquivo LICENSE (se existir) ou insira a licença no seu repositório.