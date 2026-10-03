# Action Items — CASE-2025-014

Все задачи должны иметь владельца, срок и измеримый критерий завершения.

| # | Что | Owner | Due | Как проверим |
|---|---|---|---|---|
| 1 | Развернуть Sigma: LSASS access from non-standard parent | Detection Engineering | 7 дней | Rule deployed; synthetic test creates alert |
| 2 | Развернуть Sigma: hidden encoded PowerShell | Detection Engineering | 7 дней | Rule deployed; synthetic test creates alert |
| 3 | Добавить correlation: LSASS + impossible travel + large outbound transfer | SIEM / Detection Engineering | 30 дней | Один Critical case создается автоматически |
| 4 | Внедрить step-up MFA для `/v1/transactions/export` и аналогичных bulk endpoints | Backend / IAM | 30 дней | Bulk export без step-up невозможен |
| 5 | Ограничить egress по destination class и behavioral baseline | Network Security | 30 дней | Unapproved upload destination blocked; anomaly alert works |
| 6 | Внедрить verify-on-execute или hash allowlist для `SynthAgent` | Endpoint Engineering | 30 дней | Modified or unsigned agent blocked |
| 7 | Внедрить 24/7 L2/L3 on-call или contracted escalation | SOC Lead | 60 дней | Critical escalation SLA меньше 15 минут |
| 8 | Создать runbook «Compromised session / token response» | Incident Response | 14 дней | Runbook reviewed and tabletop tested |
| 9 | Провести tabletop: impossible travel detection unavailable | SOC Lead | 30 дней | Exercise completed; gaps documented |
| 10 | Внедрить DLP/CASB-контроль для bulk financial data export | Data Protection / App Security | 45 дней | Export above threshold requires approval |

## Правило качества

Плохой action item:

```text
Быть внимательнее при алертах.
```

Хороший action item:

```text
До 30 дней развернуть корреляцию LSASS access + impossible travel +
large outbound transfer; проверка — запуск synthetic telemetry должен создать
один Critical case в SIEM.
```
