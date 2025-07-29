# Backend_Flask

## 🧩 Resumo do Projeto

Este projeto é um backend modular desenvolvido em **Python/Flask**, voltado para o gerenciamento, análise e visualização de indicadores logísticos e financeiros. Ele centraliza dashboards, relatórios e integrações de dados (WMS, financeiro, uploads), automatizando processos de análise e facilitando a tomada de decisão para áreas de **Logística, Transporte e Financeiro**.

O sistema permite:
- Importar planilhas Excel (.xlsx)
- Integrar dados de bancos **SQL Server**
- Calcular **KPIs logísticos e financeiros**
- Gerar relatórios dinâmicos
- Exportar dados em Excel
- Acessar todos os recursos via rotas web (Flask)

---

## ⚙️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Framework Web:** Flask, Flask-Admin
- **ORM e Banco de Dados:** SQLAlchemy, pyodbc, SQL Server
- **Manipulação de Dados:** pandas, openpyxl, scikit-learn
- **Ambiente:** virtualenv, python-dotenv
- **Templates:** Jinja2 (HTML)
- **Outros:** regex, urllib3, django-environ

---

## 🚀 Estratégia de Desenvolvimento

- **Modularização:** Uso de blueprints para separar funcionalidades
- **Reaproveitamento de Código:** Controllers centralizam lógica e dados
- **Integração Dinâmica:** Banco SQL Server + planilhas Excel
- **Tratamento de Erros:** Handlers personalizados
- **Segurança:** Variáveis de ambiente protegidas no `.env`
- **Exportação Inteligente:** Relatórios Excel sob demanda

---

## 📁 Estrutura de Pastas

```Bash
Backend_Flask/
├── app/
│ ├── Dash_Logistica/ # Dashboards e relatórios logísticos
│ ├── Dash_Financeiro/ # Dashboards e relatórios financeiros
│ ├── uploads/ # Upload e processamento de arquivos
│ ├── controllers/ # Lógica de negócio centralizada
│ ├── models/ # Modelos de dados auxiliares
│ ├── index/ # Página inicial e rotas base
│ ├── relatorios/ # Relatórios customizados
│ ├── admin_app/ # Administração do sistema
│ ├── login/ # Autenticação
│ └── ... # Outros módulos
├── resources/ # Recursos estáticos e arquivos auxiliares
├── uploadarquivos/ # Diretório de uploads de arquivos
├── requirements.txt # Dependências do projeto
├── config.py # Configurações e variáveis de ambiente
├── main.py # Inicialização da aplicação Flask
└── README.md # Este arquivo
```
---

## 🔄 Relacionamento dos Módulos

- **Dash_Logistica:** KPIs, integração WMS, performance logística, transporte
- **Dash_Financeiro:** Fluxo de caixa, contas a pagar/receber, vendas, inventário
- **uploads:** Importação de dados via planilhas
- **controllers/models:** Regras de negócio e integração de dados
- **relatorios/index/admin_app/login:** Navegação, autenticação e relatórios personalizados

---

## ▶️ Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/Backend_Flask.git
cd Backend_Flask
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo **.env** na raiz do projeto com:

```ini
driver=ODBC Driver 17 for SQL Server
server=SEU_SERVIDOR
database=SEU_BANCO
usuario=SEU_USUARIO
password=SUA_SENHA
```

### 5. Execute a aplicação
```bash
py main.py
```
Acesse no navegador: [http://localhost:8350]

📊 Exemplos de Uso
- Dashboard Logístico: `http://localhost:8350/dashboard/logistica`

- Dashboard Financeiro: `http://localhost:8350/dashboard/financeiro`

- Upload de Planilhas: Via aba `Upload`

- Exportação Excel: `Botões nas páginas de relatório`


🖼️ Prints de Tela
- Adicione aqui imagens de:

- Dashboard logístico

- Dashboard financeiro

- Tela de upload

- Relatórios gerados


☁️ Deploy em Produção
- Use **Gunicorn** ou **uWSGI**

- Configure um servidor reverso (ex: Nginx)

- Proteja variáveis sensíveis com `.env` externo ao repositório

- Habilite logs, monitoramento e backups regulares

- Crie jobs automáticos para importação periódica se necessário


📄 Licença
Este projeto está licenciado sob a [MIT License].

