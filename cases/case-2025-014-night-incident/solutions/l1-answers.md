# Solutions — L1 Answers

> Сначала самостоятельно заполните `03-triage/triage-notes.md`.
> Этот файл используйте только для самопроверки.

## SYNTH-ALERT-0001 — LSASS access

**Вердикт:** True Positive  
**Severity:** High отдельно; Critical после корреляции

### Почему

- Hidden encoded PowerShell обращается к `lsass.exe`.
- `granted_access=0x1010` соответствует подозрительному доступу к памяти процесса.
- Родительский процесс — `SynthAgent\agent.exe`; это нетипичный parent для PowerShell.
- Контекст `NT AUTHORITY\SYSTEM` требует проверки: возможны service context,
  token manipulation или ошибка telemetry attribution.
- Перед LSASS access наблюдаются два hidden encoded PowerShell-процесса.
- После LSASS access происходит staging и внешняя передача около 1 GB.

### Действия L1

- Сохранить alert context и process tree.
- Эскалировать L2/IR.
- Не перезагружать endpoint.
- Подготовить `PAY-WKS-07` к containment с сохранением management channel.

## SYNTH-ALERT-0002 — Impossible Travel

**Вердикт:** True Positive  
**Severity:** High отдельно; Critical после корреляции

### Почему

- `d.petrov` ранее входил из `SynthCity-A`.
- В 03:17 происходит успешный вход из `SynthCity-B` на расстоянии 8700 км.
- Первый подозрительный login использует MFA push approval.
- Затем фиксируется серия входов в `SynthPay-Admin`.
- Возможны session reuse, refresh token reuse или MFA social engineering.
- После IdP activity начинаются sensitive API calls и transaction export.

### Действия L1

- Эскалировать L2/IR.
- Передать в IAM данные о пользователе, времени, IP, ASN, MFA и приложении.
- Запросить revoke sessions, refresh tokens и device sessions.
- Не удалять учетную запись; требуется временный disable.

## SYNTH-ALERT-0003 — Large outbound transfer

**Вердикт:** True Positive после корреляции  
**Severity:** Medium отдельно; Critical после корреляции

### Почему

- С `PAY-WKS-07` выполнен PUT примерно 1 GB на внешний upload endpoint.
- Перед этим выполнен API export транзакций за 90 дней.
- `cache.bin` по размеру соответствует объему передаваемых данных.
- Destination не относится к внутренним сервисам компании.
- Событие совпадает по времени, хосту и пользователю с LSASS access и
  suspicious Admin SSO activity.

### Действия L1

- Эскалировать L2/IR одним объединенным кейсом.
- Передать destination domain, IP, объем, HTTP method и время передачи.
- Запросить блокировку destination.
- Запросить проверку состава выгруженного transaction export.

## Объединенный вердикт

**Incident ID:** CASE-2025-014  
**Severity:** Critical  
**Статус:** Active investigation  
**Owner:** L2 / IR on-call

### Основание

```text
Encoded PowerShell
→ LSASS access
→ Impossible Travel / Admin SSO
→ API account discovery
→ Transaction export
→ External PUT upload
→ Possible pastebin publication / C2
```

### Что остается гипотезой

- Подмена `SynthAgent\agent.exe`.
- Initial access vector.
- Фактическое содержание выгруженного архива.
- Публикация secrets на pastebin.
- Persistence через `ctfmon.exe`.
