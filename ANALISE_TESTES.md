# Análise de Cobertura de Testes — Portfólio

> Gerado em 2026-04-14. Revisar e executar amanhã.

---

## Resumo

**126 testes** em **19 arquivos** — cobertura geral estimada em ~70%, com lacunas importantes em integração, segurança e alguns fluxos críticos.

---

## Mapa de Cobertura por Componente

| Componente | Unit | Integração | Cobertura | Estado |
|---|---|---|---|---|
| Forms (PicPayRegisterForm) | 23 | 1 (mock) | 85% | Bom |
| Models | 11 | 0 | 60% | Raso |
| Views tradicionais | 0 | 17 | 70% | Conteúdo não verificado |
| REST API Views | 0 | 7 | 60% | Autenticação não testada |
| Serializers | 10 | 0 | 80% | Ok |
| Service: Register | 8 | 0 | 70% | Role assignment mockado |
| Service: Transaction | 13 | 0 | 65% | Sem fluxo end-to-end |
| Service: Profile | 17 | 0 | 75% | Ok |
| Validators | 8 | 0 | 80% | Ok |
| Exceptions | 12 | 0 | 90% | Ok |
| Auth Backend | 5 | 0 | 90% | Ok |
| Home Views (guest_login) | — | — | — | **Remover** (ver abaixo) |

---

## Tarefas

### Urgente

- [ ] **Remover `guest_login`** — a função não tem testes, não tem justificativa de negócio clara e acopla lógica de conta PicPay à home app. Remover a view, a URL e qualquer referência antes de escrever qualquer teste para ela.

- [ ] **Teste end-to-end de transação** — os testes atuais de `TransactionAPIView` mocam o service inteiro. Criar um teste de integração real: POST na API → validação → saldo deduzido do sender → saldo creditado no receiver → Transaction salva no banco.

- [ ] **Autenticação na REST API** — nenhum teste verifica que um usuário não autenticado recebe 401. `force_authenticate()` é usado em todos os testes, mascarando o problema.

- [ ] **Conteúdo do `YourProfile`** — o teste atual só verifica `status_code == 200`. Verificar que saldo, nome e transações recentes aparecem corretamente no template.

### Importante

- [ ] **Extrair helpers de teste** — `make_user()` e `make_account()` estão duplicados em praticamente todo arquivo de teste. Centralizar em `conftest.py` ou em um módulo `tests/factories.py`.

- [ ] **Role assignment sem mock** — `test_register_picpay_user.py` mocka `assign_role()`. Criar um teste que verifica que a role foi de fato atribuída no banco após o registro.

- [ ] **Merchant não consegue iniciar transação pela API** — a restrição é testada só no validator isolado. Criar um teste de integração: merchant faz POST em `/api/transaction/` e recebe 403.

- [ ] **Autorização entre usuários** — nenhum teste verifica que usuário A não consegue ver o perfil do usuário B nem iniciar transação em nome dele.

### Lacunas de Qualidade

- [ ] **Assertions fracas nas views** — muitos testes verificam apenas `status_code`. Complementar com verificações de conteúdo onde relevante.

- [ ] **Persistência dos models** — `pay()` e `receive()` não chamam `save()`. Os testes verificam apenas mutação em memória. Adicionar teste que confirma persistência no banco após chamada + save.

- [ ] **Edge cases nos forms** — campo `sex` não é validado nos testes. Nome com só espaços, documento com só letras, senha com espaços — nenhum desses casos é coberto.

- [ ] **Mensagens de erro** — testes verificam que erros existem, mas não o conteúdo. Há um typo em produção: `"ultilizado"` em vez de `"utilizado"` no erro de email duplicado.

- [ ] **CSRF na REST API** — `TransactionAPIView` tem `@csrf_protect` mas todos os testes usam `enforce_csrf_checks=False`. O decorator efetivamente nunca foi testado.

### Baixa Prioridade

- [ ] **Cascade delete** — deletar um `User` deleta o `PicPayAccount` (CASCADE), mas as `Transactions` ficam com sender/receiver `None` (SET_NULL). Esse comportamento nunca foi verificado.

- [ ] **Timezone em `humanize_date()`** — a função usa `now()` mas não há teste com mudança de horário de verão.

- [ ] **Arquivo de currículo** — o teste verifica `Content-Type` mas não verifica o que acontece se o arquivo não existir.

---

## Notas

- O `TESTES_PENDENTES.md` original pode ser apagado após este arquivo ser revisado — as informações foram consolidadas aqui.
- Priorizar remoção do `guest_login` antes de qualquer nova escrita de teste na home app.
