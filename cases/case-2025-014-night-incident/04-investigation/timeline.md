# Timeline — CASE-2025-014

Все времена указаны в UTC.

| Время | Источник | Событие | Оценка |
|---|---|---|---|
| 2025-01-14 22:40:11 | IdP | `d.petrov` входит в `SynthPay-Admin` из `SynthCity-A` | Baseline |
| 2025-01-15 01:05:12 | IdP | `d.petrov` входит в `SynthPay-Backoffice` из `SynthCity-A` | Baseline |
| 02:58:11 | EDR | Запуск `SynthAgent\agent.exe`, PID 1180 | Требует проверки |
| 02:58:14 | EDR | `agent.exe` запускает `cmd.exe /c ver` | Reconnaissance |
| 03:04:02 | EDR | Hidden encoded PowerShell, PID 3555 | Execution |
| 03:11:52 | EDR | Hidden encoded PowerShell, PID 4212 | Preparation for credential access |
| 03:12:04 | EDR | PID 4212 получает доступ к `lsass.exe`, `0x1010` | Suspected credential dumping |
| 03:12:37 | EDR | `wermgr.exe -manual` от PID 4212 | Possible LOLBin / masquerading |
| 03:17:02 | IdP | `d.petrov` входит в Admin из `SynthCity-B`, MFA push approved | Account compromise indicator |
| 03:17:33–03:22:45 | IdP | Повторные входы в Admin | Possible session/token reuse |
| 03:18:42 | DNS | `PAY-WKS-07` резолвит `api.synthetic.example` | API access preparation |
| 03:20:11–03:21:02 | Proxy | Два запроса к `/v1/accounts` | Account discovery |
| 03:22:18 | Proxy | `GET /v1/transactions/export?range=last_90d` | Sensitive data export |
| 03:23:41 | EDR | Создан `cache.bin`, около 1 GB | Data staging |
| 03:24:02 | Proxy / EDR | `PUT` около 1 GB на `uploads.synthetic.example` | Suspected exfiltration |
| 03:31:00–03:31:22 | DNS | Три DNS-запроса к `pastebin.synthetic.example` | Possible publication / C2 |
| 03:31:12 | Proxy | `POST` на pastebin | Possible secret or data publication |
| 03:31:50 | EDR | Еще один hidden encoded PowerShell | Continued activity |
| 04:02:10 | DNS | Запрос `ctfmon.synthetic.example` | Possible C2 / persistence |
| 04:02:13 | EDR | `ctfmon.exe` запущен от `agent.exe` | Possible masquerading / persistence |
| 04:02:14 | IdP | Повторный вход в Admin | Continued account access |
| 04:15:00 | EDR | Session idle 45 minutes | Activity paused; remediation not confirmed |
| 04:15:03 | DNS | Запрос `metric.synthetic.example` | Possible beaconing |
| 04:15:33 | IdP | Последний успешный вход в Admin | Continued account access |
