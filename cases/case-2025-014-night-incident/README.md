# Case 2025-014 — «Ночной инцидент в финтех-стартапе»

**Уровень:** средний, L1 → L2 → IR  
**Время прохождения:** 2–4 часа  
**Данные:** полностью синтетические  
**Формат:** самостоятельная работа с самопроверкой

## Легенда

SynthPay — финтех-стартап на ~200 сотрудников. Используются IdP с MFA, EDR,
прокси с TLS-inspection, DNS logging и SIEM.

Ночью 15 января 2025 года в 03:12 UTC приходят три алерта:

1. EDR: `Suspicious LSASS Access` на `PAY-WKS-07`.
2. IdP: `Impossible Travel` для `d.petrov`.
3. NDR/Proxy: `Large Outbound Transfer` с `PAY-WKS-07`.

## Что тренируем

- Корреляцию слабых сигналов из разных источников.
- Построение timeline по неполным данным.
- Различение факта, оценки и гипотезы.
- Containment без уничтожения evidence.
- Eradication, recovery, PIR и улучшение детектов.

## Как работать

1. Прочитайте `00-brief.md`.
2. Откройте `01-alerts/`.
3. Изучите `02-telemetry/`.
4. Заполните `03-triage/triage-notes.md`.
5. Постройте timeline и scope в `04-investigation/`.
6. Пройдите containment, eradication и recovery.
7. Составьте PIR и action items.
8. Сверьтесь с `solutions/` только после собственных выводов.

## Важно

Кейс не утверждает, что `SynthAgent\agent.exe` точно подменен. Это primary
hypothesis, которую нужно проверить по hash, подписи, источнику установки,
process tree и распространенности на других хостах.
