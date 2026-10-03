# Scope — CASE-2025-014

## Подтвержденно затронуто

| Объект | Тип | Основание |
|---|---|---|
| `PAY-WKS-07` | Endpoint | LSASS access, encoded PowerShell, staging и внешний upload |
| `d.petrov` | User / identity | Impossible travel, Admin access, sensitive API export |
| Transaction export | Data | `GET /v1/transactions/export?range=last_90d` |
| `uploads.synthetic.example` | External destination | PUT около 1 GB |
| `pastebin.synthetic.example` | External destination | POST после экспорта |
| `ctfmon.synthetic.example` | External destination | Possible C2 / persistence |
| `metric.synthetic.example` | External destination | Possible beaconing |

## Под подозрением

- `SynthAgent\agent.exe` — возможная подмена, компрометация или злоупотребление.
- `wermgr.exe` — нетипичная parent-child связь с PowerShell.
- `ctfmon.exe` — нетипичная parent-child связь с `agent.exe`.
- Другие хосты с тем же `SynthAgent` hash, path или process tree.
- Другие пользователи и service accounts с доступом к `SynthPay-Admin`.
- API tokens, OAuth grants, SSH keys и secrets, доступные `d.petrov` или `PAY-WKS-07`.

## Не подтверждено

- Первичный вектор компрометации.
- Фактическая подмена `SynthAgent\agent.exe`.
- Полное содержимое выгруженного архива.
- Публикация credentials или secrets на pastebin.
- Компрометация Domain Admin.
- Влияние на production payment services.

## Пользователи в monitoring scope

| Пользователь | Статус | Обоснование |
|---|---|---|
| `d.petrov` | Compromised / high confidence | Impossible travel, Admin access, API export |
| `a.sidorova` | Monitoring scope | Нормальный вход из обычной географии; полностью исключать нельзя |
| `m.orlov` | Monitoring scope | Нормальный git-трафик; полностью исключать нельзя |
