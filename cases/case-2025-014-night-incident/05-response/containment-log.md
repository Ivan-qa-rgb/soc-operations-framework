# Containment Log — CASE-2025-014

Цель containment — остановить распространение инцидента и предотвратить
дальнейший ущерб, сохранив возможность расследования.

## Действия

| Время UTC | Действие | Исполнитель | Результат |
|---|---|---|---|
| 03:30 | Сохранить EDR telemetry, process tree и активные network connections | IR | Evidence preserved |
| 03:32 | Выполнить memory acquisition `PAY-WKS-07`, если разрешено playbook | IR | Pending |
| 03:34 | Скопировать `cache.bin` в evidence storage и зафиксировать SHA-256 | IR | Pending |
| 03:36 | Включить EDR network containment для `PAY-WKS-07`, сохранив management channel | IR / Endpoint | Pending |
| 03:38 | Заблокировать `uploads.synthetic.example`, `pastebin.synthetic.example`, `ctfmon.synthetic.example`, `metric.synthetic.example` и `192.0.2.77` | Network Security | Pending |
| 03:40 | Отозвать SSO sessions, refresh tokens и device sessions `d.petrov` | IAM | Pending |
| 03:42 | Временно disable `d.petrov`; не удалять учетную запись | IAM | Pending |
| 03:44 | Заблокировать доступ `d.petrov` к `SynthPay-Admin` | IAM / Application owner | Pending |
| 03:46 | Приостановить или ограничить bulk export для затронутой учетной записи | Application owner | Pending |
| 03:50 | Уведомить SOC Lead, IR, CISO, Legal / DPO | Incident Commander | Pending |

## Принципы

- Не перезагружать `PAY-WKS-07` до memory acquisition.
- Не удалять `cache.bin` до копирования в evidence storage.
- Не удалять учетную запись `d.petrov`: использовать disable.
- Не отключать весь SSO из-за одной скомпрометированной учетной записи.
- Не считать `SynthAgent\agent.exe` вредоносным до проверки hash, подписи,
  источника установки и распространенности на других хостах.
- Все действия фиксировать с точным временем UTC, исполнителем и результатом.
