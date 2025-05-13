# 🗨️ WebChat

Sistema de chat desenvolvido com Django REST Framework e JavaScript, utilizando comunicação via HTTP ao invés de WebSockets.

Este projeto faz parte do meu portfólio e foi desenvolvido com o objetivo de explorar a criação de um sistema de mensagens assíncronas sem depender de WebSockets, aprendendo a lidar com pooling, estrutura de API REST e organização de um app completo de chat.

## 🎯 Funcionalidades

- Autenticação de usuários (registro e login)
- Criação automática de salas entre dois usuários
- Envio e recebimento de mensagens via requisições HTTP
- Atualização periódica das conversas (client-side pooling)
- Layout responsivo para mobile e desktop

## ⚙️ Tecnologias Utilizadas

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Comunicação**: HTTP (REST)
- **Armazenamento**: PostgreSQL 

## 📌 Observações

- Este projeto utiliza pooling (requisições periódicas via JavaScript) para simular mensagens em tempo real.
- O foco principal foi entender os limites e possibilidades do Django REST Framework para sistemas interativos.
- O WebChat é totalmente funcional e está embutido no portfólio principal. Ao rodar o portfólio, ele já estará disponível.