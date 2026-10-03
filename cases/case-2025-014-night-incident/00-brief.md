# Вводная

**Дата:** ночь с 14 на 15 января 2025  
**Контекст:** недавно завершился плановый релиз платежного сервиса.  
**Дежурный L1:** `analyst.synth.ok`  
**Смена:** 22:00–06:00 UTC

## Первичные алерты

| Время UTC | Источник | Алерт | Объект |
|---|---|---|---|
| 03:12:04 | EDR | Suspicious LSASS Access | `PAY-WKS-07` |
| 03:17:41 | IdP | Impossible Travel | `d.petrov` |
| 03:24:19 | NDR/Proxy | Large Outbound Transfer | `PAY-WKS-07` |

## Известный контекст

- `d.petrov` имеет доступ к `SynthPay-Admin` и `SynthPay-Backoffice`.
- `PAY-WKS-07` — рабочая станция инженера.
- `SynthAgent` — корпоративный endpoint agent.
- `uploads.synthetic.example` присутствует в proxy allow-list.
- Ночного L2/L3 в штате нет.
- MFA включен, но точный метод удовлетворения MFA в первичных алертах не указан.

## Задачи

### L1

- Определить TP/FP по каждому алерту.
- Назначить severity.
- Определить, связаны ли алерты.
- Эскалировать при необходимости.

### L2

- Построить verified timeline.
- Определить scope.
- Сформулировать primary и alternative hypotheses.
- Подготовить данные для IR.

### IR

- Сохранить evidence.
- Выполнить containment.
- Выполнить eradication.
- Начать recovery.
- Оценить влияние на бизнес и данные.

### SOC Lead / Detection Engineering

- Провести PIR.
- Сформулировать измеримые action items.
- Улучшить детекты и корреляции.
