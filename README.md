# Neko Café Bot

Um bot Discord personalizado para o servidor Neko Café com funcionalidades de moderação, sistema de tickets, formulários e muito mais.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Discord.py 2.0+
- SQLite3

## 🚀 Instalação

1. Clone ou baixe este repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o arquivo `config.json` com suas informações:
   ```json
   {
     "prefix": "st,",
     "token": "SEU_TOKEN_DO_BOT",
     "permissions": 8,
     "application_id": "ID_DA_APLICACAO",
     "sync_commands_globally": true,
     "owners": ["SEU_USER_ID"]
   }
   ```

## ⚙️ Configuração do Discord Developer Portal

Para que o bot funcione corretamente, você precisa habilitar os seguintes **Privileged Gateway Intents** no Discord Developer Portal:

1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Selecione sua aplicação
3. Vá para a aba "Bot"
4. Na seção "Privileged Gateway Intents", habilite:
   - ✅ **Presence Intent**
   - ✅ **Server Members Intent**
   - ✅ **Message Content Intent**

## 🎯 Funcionalidades

### 🎫 Sistema de Tickets
- Criação automática de tickets via dropdown
- Categorias: Comprar, Dúvidas, Denunciar, Parcerias, Patrocínio
- Sistema de fechamento de tickets
- Views persistentes (funcionam após restart do bot)

### 🛡️ Moderação
- Comandos de expulsão (`/expulsar`)
- Comandos de banimento (`/banir`)
- Sistema de avisos (`/avisar`)
- Verificação de blacklist
- Verificação de permissões

### 📝 Formulários
- Sistema de formulários personalizados
- Coleta de informações dos usuários

### 🚀 Boost
- Funcionalidades relacionadas ao boost do servidor

### 📜 Regras
- Sistema de exibição de regras
- Gerenciamento de regras do servidor

## 🗄️ Banco de Dados

O bot utiliza SQLite com as seguintes tabelas:

- `blacklist`: Usuários banidos do bot
- `warns`: Sistema de avisos/advertências

## 🔧 Estrutura do Projeto

```
├── main.py              # Arquivo principal do bot
├── config.json          # Configurações do bot
├── requirements.txt     # Dependências Python
├── database/
│   ├── database.db      # Banco de dados SQLite
│   └── schema.sql       # Schema do banco
├── cogs/                # Módulos do bot
│   ├── boost.py
│   ├── form.py
│   ├── moderation.py
│   ├── rules.py
│   ├── template.py
│   └── ticket.py
├── helpers/             # Funções auxiliares
│   ├── checks.py        # Verificações personalizadas
│   └── db_manager.py    # Gerenciador do banco
└── exceptions/          # Exceções personalizadas
    └── __init__.py
```

## 🚀 Executando o Bot

```bash
python main.py
```

## 📝 Logs

O bot gera logs detalhados incluindo:
- Carregamento de cogs
- Sincronização de comandos
- Erros e exceções
- Status de conexão

## ⚠️ Notas Importantes

1. **Intents**: Certifique-se de que todos os intents necessários estão habilitados no Discord Developer Portal
2. **Permissões**: O bot precisa das permissões adequadas no servidor para executar comandos de moderação
3. **Token**: Mantenha seu token seguro e nunca o compartilhe
4. **ID do Cargo**: Verifique se o ID do cargo de atendente no `ticket.py` está correto para seu servidor

## 🐛 Solução de Problemas

### Bot não responde a comandos
- Verifique se o `Message Content Intent` está habilitado
- Confirme se o prefixo está correto no `config.json`
- Verifique os logs para erros de carregamento de cogs

### Comandos de moderação não funcionam
- Verifique se o `Server Members Intent` está habilitado
- Confirme se o bot tem as permissões necessárias no servidor
- Verifique se o usuário não está na blacklist

### Sistema de tickets não funciona
- Verifique se as views persistentes foram carregadas corretamente
- Confirme se o ID do cargo de atendente está correto
- Verifique se o bot tem permissão para criar threads

## 📞 Suporte

Se você encontrar problemas, verifique:
1. Os logs do bot para erros específicos
2. Se todas as dependências estão instaladas
3. Se a configuração está correta
4. Se os intents estão habilitados no Discord Developer Portal
