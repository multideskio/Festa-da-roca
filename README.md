# Sistema de Gestão - Festa Junina

Um sistema web completo para gerenciar festas juninas, incluindo controle de vendas de fichas, gestão de barracas e relatórios financeiros.

## Funcionalidades

### 🎪 Gestão de Eventos
- Criação e edição de eventos
- Definição de objetivos e público-alvo
- Controle de status do evento

### 🏪 Gestão de Barracas
- Cadastro de barracas com responsáveis
- Gerenciamento de cardápio por barraca
- Controle de status (ativa/inativa)

### 💰 Sistema de Fichas
- Venda centralizada de fichas
- Registro de vendas por valor unitário
- Controle de estoque de fichas

### 📊 Relatórios Financeiros
- Dashboard com métricas em tempo real
- Relatórios por barraca
- Consolidação financeira geral
- Controle de fichas em circulação

## Tecnologias Utilizadas

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados
- **Flask-CORS** - Suporte a CORS

### Frontend
- **React** - Biblioteca JavaScript
- **Vite** - Build tool
- **Tailwind CSS** - Framework CSS
- **shadcn/ui** - Componentes UI
- **Lucide React** - Ícones

## Como Executar

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- pnpm

### Instalação e Execução

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd festa_junina_backend
   ```

2. **Configure o ambiente virtual Python**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências Python**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o servidor**
   ```bash
   python src/main.py
   ```

5. **Acesse o sistema**
   - Abra o navegador em: `http://localhost:5001`

## Estrutura do Projeto

```
festa_junina_backend/
├── src/
│   ├── models/
│   │   └── festa_junina.py      # Modelos do banco de dados
│   ├── routes/
│   │   ├── evento.py            # Rotas para eventos
│   │   ├── barraca.py           # Rotas para barracas
│   │   └── venda.py             # Rotas para vendas
│   ├── static/                  # Arquivos do frontend
│   ├── database/
│   │   └── app.db              # Banco de dados SQLite
│   └── main.py                 # Arquivo principal
├── venv/                       # Ambiente virtual
└── requirements.txt            # Dependências Python
```

## API Endpoints

### Eventos
- `GET /api/eventos` - Listar eventos
- `POST /api/eventos` - Criar evento
- `GET /api/eventos/{id}` - Obter evento específico
- `PUT /api/eventos/{id}` - Atualizar evento

### Barracas
- `GET /api/eventos/{id}/barracas` - Listar barracas do evento
- `POST /api/eventos/{id}/barracas` - Criar barraca
- `GET /api/barracas/{id}` - Obter barraca específica
- `PUT /api/barracas/{id}` - Atualizar barraca

### Vendas de Fichas
- `GET /api/eventos/{id}/vendas-fichas` - Listar vendas de fichas
- `POST /api/eventos/{id}/vendas-fichas` - Registrar venda de fichas
- `GET /api/eventos/{id}/relatorio-caixa` - Relatório do caixa central
- `GET /api/eventos/{id}/relatorio-geral` - Relatório geral do evento

## Como Usar o Sistema

### 1. Criando um Evento
1. Acesse a aba "Eventos"
2. Preencha os dados do evento (nome, data, local, etc.)
3. Clique em "Criar Evento"

### 2. Configurando Barracas
1. Com um evento selecionado, acesse a aba "Barracas"
2. Adicione as barracas necessárias
3. Defina responsáveis para cada barraca

### 3. Vendendo Fichas
1. Acesse a aba "Vendas de Fichas"
2. Registre cada venda informando:
   - Quantidade de fichas
   - Valor unitário
   - Responsável pela venda

### 4. Acompanhando Resultados
1. Use o "Dashboard" para visão geral em tempo real
2. Acesse "Relatórios" para análises detalhadas
3. Monitore fichas em circulação vs. vendidas

## Características do Sistema

### Controle Financeiro
- **Sistema de Fichas**: Todo pagamento é feito através de fichas compradas no caixa central
- **Rastreabilidade**: Cada venda é registrada com timestamp e responsável
- **Transparência**: Relatórios detalhados para prestação de contas

### Interface Intuitiva
- **Design Responsivo**: Funciona em desktop e mobile
- **Navegação por Abas**: Organização clara das funcionalidades
- **Feedback Visual**: Indicadores de status e métricas em tempo real

### Segurança e Confiabilidade
- **Banco de Dados Local**: Dados armazenados localmente
- **Backup Automático**: SQLite com backup automático
- **Validação de Dados**: Validação tanto no frontend quanto no backend

## Suporte

Para dúvidas ou problemas:
1. Verifique se todos os serviços estão rodando
2. Consulte os logs do servidor Flask
3. Verifique o console do navegador para erros do frontend

## Licença

Este projeto foi desenvolvido especificamente para gestão de festas juninas em igrejas e comunidades.

