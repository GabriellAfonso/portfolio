# Portfólio — Gabriel Afonso

Site pessoal que vitrina meus projetos como desenvolvedor backend. Construído em **Django 6**, com PostgreSQL, deploy em VPS via Docker atrás de um Nginx reverse proxy.

Disponível em **[gabrielafonso.com.br](https://gabrielafonso.com.br)**.

---

## Sobre mim

Desenvolvedor backend com foco em **Django** e ecossistema Python. Trabalho com bancos relacionais, autenticação, APIs REST, WebSockets, filas assíncronas e deploy containerizado.

Gosto de backend porque é onde a lógica vive: modelar domínios, desenhar fluxos de dados e entender o que acontece por trás da interface. Esse interesse veio naturalmente do meu gosto por lógica, matemática e sistemas.

---

## Sobre este repositório

Este repositório contém **apenas o site do portfólio** — não os projetos em si. Cada projeto listado abaixo roda como uma aplicação independente, em seu próprio container, no mesmo VPS, exposto sob um subpath do domínio principal (ou domínio próprio, quando faz sentido).

O site em si é uma aplicação Django simples organizada em duas apps:

- `apps/home` — landing page e seções estáticas.
- `apps/content` — modelos de `Project`, `AboutMe` e `Resume` administráveis pelo Django Admin, sem precisar de redeploy para atualizar conteúdo. As thumbnails dos projetos são servidas a partir de `media/projects/<slug>.<ext>`, com nome estável (independe do upload).

---

## Projetos

### Dumcrown
<a href="https://dumcrown.com.br/"><img src="https://gabrielafonso.com.br/media/projects/dumcrown.png" alt="Dumcrown" width="480"></a>

Jogo de cartas PvP online com partidas em tempo real via WebSocket, matchmaking, criação/gerenciamento de decks e sistema ranqueado por tiers.

🔗 [dumcrown.com.br](https://dumcrown.com.br/)

---

### Shorter
<a href="https://gabrielafonso.com.br/shorter/"><img src="https://gabrielafonso.com.br/media/projects/shorter.png" alt="Shorter" width="480"></a>

Encurtador de URLs full-stack com redirecionamento otimizado via Redis, filas assíncronas com Celery e analytics detalhado.

🔗 [gabrielafonso.com.br/shorter](https://gabrielafonso.com.br/shorter/)

---

### IPBCB API
<a href="https://gabrielafonso.com.br/ipbcb/api/schema/swagger-ui/"><img src="https://gabrielafonso.com.br/media/projects/ipbcb-api.jpg" alt="IPBCB API" width="480"></a>

API REST para gestão de igreja com autenticação JWT/Google, repertório musical, escala mensal e galeria.

🔗 [Swagger UI](https://gabrielafonso.com.br/ipbcb/api/schema/swagger-ui/)

---

### IPBCB App
<a href="https://play.google.com/store/apps/details?id=com.ipb.castelobranco"><img src="https://gabrielafonso.com.br/media/projects/ipbcb-app.png" alt="IPBCB App" width="480"></a>

App oficial da IPB Castelo Branco. Escala mensal, hinário, ferramentas de louvor e área administrativa em um só lugar.

🔗 [Google Play](https://play.google.com/store/apps/details?id=com.ipb.castelobranco)

---

### Desafio PicPay
<a href="https://gabrielafonso.com.br/picpay/"><img src="https://gabrielafonso.com.br/media/projects/picpay-challenge.png" alt="Desafio PicPay" width="480"></a>

Back-end de carteira digital com transferências entre contas, validações de saldo/permissão e autorização externa, estruturado em camadas.

🔗 [gabrielafonso.com.br/picpay](https://gabrielafonso.com.br/picpay/)

---

## Stack

- **Linguagem:** Python 3.13
- **Framework:** Django 6
- **Banco:** PostgreSQL 16
- **Servidor:** Gunicorn
- **Infra:** Docker / Docker Compose
- **Qualidade:** Ruff, Bandit, MyPy, Pytest

---

## Deploy

Hospedado em VPS próprio. Cada projeto é um `docker compose` independente, em uma rede Docker compartilhada (`proxy-network`), com um **Nginx reverse proxy** central que roteia subpaths e subdomínios para o container correto.

Esse modelo permite deploys, rollbacks e dependências isoladas por projeto, sem acoplar o ciclo de vida do portfólio ao das aplicações que ele vitrina.

---

## Currículo

[Ver currículo](https://gabrielafonso.com.br/curriculo/)

---

## Contato

- **LinkedIn:** [linkedin.com/in/gabriellafonso](https://www.linkedin.com/in/gabriellafonso/)
- **GitHub:** [github.com/GabriellAfonso](https://github.com/GabriellAfonso)
- **Email:** gabriellafonso.dev@gmail.com
