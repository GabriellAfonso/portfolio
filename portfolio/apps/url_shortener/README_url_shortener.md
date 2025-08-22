# 🔗 URL Shortener

Um encurtador de URLs simples e funcional, feito com Django, que permite aos usuários autenticados criar, visualizar e gerenciar links personalizados.


## 🚀 Funcionalidades

- Criação de URLs encurtadas
- Redirecionamento automático ao acessar o link curto
- Listagem de URLs do usuário logado
- Interface simples e funcional
- Restringido a usuários autenticados

## 🧩 Tecnologias Utilizadas

- Django
- HTML/CSS (com uso de templates)
- PostgreSQL 


## 📌 Como funciona

1. Usuário se autentica no sistema
2. Insere a URL original no formulário
3. O sistema gera um identificador único
4. O usuário recebe um link curto baseado no domínio do projeto
5. Ao acessar o link curto, é redirecionado para a URL original

## ✅ Exemplo de uso

| Long URL                                   | Short URL                        |
|--------------------------------------------|----------------------------------|
| `https://www.example.com/page/long-path`   | `https://seudominio.com/r/abc123` |

## 🔒 Requisitos de autenticação

Todas as funcionalidades são protegidas por login. Isso garante que cada usuário visualize apenas suas URLs.

## 🛠️ Observações Técnicas

- Validação de URL com `URLValidator`
- Redirecionamento com base no `slug` armazenado
- Integração com sistema de autenticação padrão do Django

## 📎 Possíveis melhorias futuras

- Contador de cliques por URL
- Expiração automática de links
- Dashboard de estatísticas

> Este projeto faz parte do meu [Portfólio](https://github.com/GabriellAfonso/portfolio), onde você pode conhecer outros projetos e detalhes do desenvolvedor.
