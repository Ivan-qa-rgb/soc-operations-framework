# Hypothesis — CASE-2025-014

## Primary hypothesis

Компрометация, подмена или злоупотребление `SynthAgent\agent.exe` на
`PAY-WKS-07` позволило выполнить reconnaissance, hidden encoded PowerShell
и подозрительный доступ к LSASS.

Полученный доступ к credential material, session tokens или активным сессиям
мог использоваться для входа в `SynthPay-Admin`, экспорта транзакций за 90 дней
и выгрузки данных на внешний endpoint.

## Предполагаемая цепочка

1. Возможная компрометация или злоупотребление `SynthAgent\agent.exe`.
2. Запуск `cmd.exe /c ver` для reconnaissance.
3. Запуск hidden encoded PowerShell.
4. Доступ к `lsass.exe` с `granted_access=0x1010`.
5. Возможное извлечение credentials, tokens или session material.
6. Вход в `SynthPay-Admin` из новой геолокации.
7. Account discovery через `/v1/accounts`.
8. Экспорт транзакций за 90 дней.
9. Staging данных в `cache.bin`.
10. Выгрузка около 1 GB на `uploads.synthetic.example`.
11. POST на `pastebin.synthetic.example`.
12. Возможное закрепление или C2 через `ctfmon.synthetic.example` и
    `metric.synthetic.example`.

## Alternative hypotheses

1. **Легитимный `SynthAgent` был скомпрометирован или эксплуатируется через уязвимость.**  
   Требуется проверка подписи, версии, update channel и известных уязвимостей.

2. **Initial access получен через phishing или social engineering.**  
   Не подтверждено, но не исключено: первый подозрительный вход сопровождается
   MFA push approval.

3. **Инсайдерская активность.**  
   Возможна, но не подтверждена; требуется coordination с HR и Legal.

4. **Ошибка нормализации или атрибуции telemetry.**  
   Контекст `SYSTEM` и часть IP-атрибуции могут быть следствием работы proxy,
   NAT или особенностей EDR.

## ATT&CK mapping

| Техника | Уверенность | Обоснование |
|---|---|---|
| T1059.001 — PowerShell | High | Несколько hidden encoded PowerShell processes |
| T1003.001 — LSASS Memory | High, требует валидации | Access `0x1010` к `lsass.exe` |
| T1078 — Valid Accounts | High | Повторные успешные входы в Admin |
| T1087 — Account Discovery | Medium | Запросы к `/v1/accounts` |
| T1567 — Exfiltration Over Web Service | High | Большой PUT на внешний upload endpoint |
| T1102 — Web Service | Medium | POST на pastebin |
| T1218 — System Binary Proxy Execution | Low / hypothesis | `wermgr.exe` и `ctfmon.exe` в нетипичном process tree |
| T1547 / T1543 — Persistence | Low / hypothesis | C2-like DNS и повторные процессы требуют проверки |
