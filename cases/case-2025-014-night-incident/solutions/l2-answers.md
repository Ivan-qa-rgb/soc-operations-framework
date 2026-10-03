# Solutions — L2 Answers

> Сначала самостоятельно заполните файлы в `04-investigation/`.

## Verified timeline

Ключевая подтвержденная последовательность:

1. `SynthAgent\agent.exe` запускается на `PAY-WKS-07`.
2. Из-под него запускаются `cmd.exe /c ver` и hidden encoded PowerShell.
3. PowerShell PID 4212 обращается к `lsass.exe` с `0x1010`.
4. `d.petrov` входит в `SynthPay-Admin` из новой географии.
5. Выполняются повторные Admin logins.
6. Выполняются запросы к `/v1/accounts`.
7. Выполняется экспорт транзакций за 90 дней.
8. На endpoint создается `cache.bin` размером около 1 GB.
9. Выполняется PUT на `uploads.synthetic.example`.
10. После этого фиксируются pastebin activity, новый encoded PowerShell и
    DNS к возможным C2/persistence destinations.

## Scope

### Confirmed

- Endpoint: `PAY-WKS-07`.
- User and identity: `d.petrov`.
- Application: `SynthPay-Admin`.
- Data event: transaction export for last 90 days.
- External destinations:
  - `uploads.synthetic.example`;
  - `pastebin.synthetic.example`;
  - `ctfmon.synthetic.example`;
  - `metric.synthetic.example`.

### Suspected

- `SynthAgent\agent.exe`.
- `wermgr.exe`.
- `ctfmon.exe`.
- Другие endpoints с похожим `SynthAgent` process tree.
- API tokens, OAuth grants, SSH keys и secrets пользователя.
- Другие учетные записи с доступом к Admin.

### Not confirmed

- Initial access vector.
- Binary replacement of `SynthAgent`.
- Domain Admin compromise.
- Полный состав утекших данных.
- Публикация credentials на pastebin.

## Primary hypothesis

Компрометация, подмена или злоупотребление `SynthAgent\agent.exe` на
`PAY-WKS-07` позволило выполнить hidden encoded PowerShell и access к LSASS.

Credential material, session tokens или другие identity artifacts могли быть
использованы для valid account access к `SynthPay-Admin`, после чего атакующий
экспортировал транзакционные данные и отправил их на внешний destination.

## Alternative hypotheses

1. Легитимный агент скомпрометирован или эксплуатируется через уязвимость.
2. Initial access получен через phishing или social engineering.
3. Активность является инсайдерской.
4. Часть telemetry ошибочно атрибутирована из-за proxy, NAT или EDR normalization.

## Что передать IR

- Полный timeline.
- Scope: confirmed, suspected и not confirmed.
- Priority list для evidence preservation.
- Список domains/IP для блокировки.
- Список sessions, refresh tokens, OAuth grants и API tokens для revoke.
- Список secrets для ротации.
- Информацию о чувствительном export данных.
