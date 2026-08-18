# Escola Conecta

MVP de uma plataforma de comunicação e agenda escolar. O lançamento de aula feito pelo professor gera contexto para atividades, provas e prazos que aparecem automaticamente na agenda das famílias.

## O que já funciona

- Login com perfis de professor, responsável e administrador.
- Escolas, turmas e estudantes no modelo de dados.
- Dashboard com mural e próximos compromissos.
- Criação de atividades, trabalhos e provas com data de entrega.
- Calendário/agenda alimentado pelos lançamentos.
- API preparada para registros de aula, comunicados e notificações.
- Banco SQLite para desenvolvimento e PostgreSQL no Render.

## Executar localmente

Em dois terminais:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

```bash
cd frontend
npm install
npm run dev
```

Abra `http://localhost:5173`. A API fica em `http://localhost:8000` e a documentação interativa em `/docs`.

Usuários de demonstração (senha `123456`):

- `professor@escola.com`
- `responsavel@escola.com`
- `admin@escola.com`

## Implantação no Render

1. Envie este repositório para o GitHub.
2. No Render, escolha **New > Blueprint** e conecte o repositório.
3. O Render lê `render.yaml`, cria o banco PostgreSQL, a API e o site.
4. Depois da primeira implantação, confirme os domínios criados e atualize `FRONTEND_ORIGIN` e `VITE_API_URL` se os nomes forem diferentes.

Antes de produção, altere a chave secreta, configure um serviço de e-mail/push e substitua a criação automática de tabelas por migrações Alembic.

## Próximas evoluções recomendadas

Notificações agendadas por e-mail/push, associação de vários filhos a responsáveis, anexos, frequência, entrega de trabalhos, permissões mais granulares e auditoria.
