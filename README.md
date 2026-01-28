# PDF Merge Web App

Este projeto é uma aplicação web simples para mesclar arquivos PDF. O usuário pode fazer upload de múltiplos arquivos PDF e baixar o resultado mesclado.

## Tecnologias
- Python 3
- Flask
- PyPDF2

## Como rodar
### Rodando localmente
1. Instale as dependências:
   ```bash
   pip install flask pypdf2 werkzeug
   ```
2. Execute o servidor:
   ```bash
   python app.py
   ```
3. Acesse `http://localhost:5000` no navegador.

### Deploy no Vercel
1. Instale o [Vercel CLI](https://vercel.com/docs/cli):
   ```bash
   npm i -g vercel
   ```
2. Faça login na Vercel:
   ```bash
   vercel login
   ```
3. Faça o deploy:
   ```bash
   vercel --prod
   ```
4. O projeto será publicado e você receberá uma URL pública.

## Estrutura
- app.py: aplicação principal Flask
- templates/: HTML da interface
- static/: arquivos estáticos (CSS, JS)

---

Este projeto foi gerado automaticamente.
