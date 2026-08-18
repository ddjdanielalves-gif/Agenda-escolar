# Deploy — Escola Conecta

## Render
1. Conecte este repositório ao Render.
2. Use o `render.yaml` da raiz do projeto.
3. O backend deve ficar em um serviço Web e o frontend em um Static Site.
4. Confirme que `FRONTEND_ORIGIN` contém a URL pública do frontend.
5. Confirme que `VITE_API_URL` contém a URL pública do backend.
6. Depois de alterar variáveis `VITE_*`, faça um novo deploy do frontend.

## Teste rápido
- Backend: abra `/health` na URL da API.
- Login: use `professor@escola.com` / `123456` se esse usuário existir no banco de teste.
- No navegador, abra DevTools > Network e confirme que `/auth/login` está indo para a URL da API sem caracteres extras.
