# Post-Incident Review — CASE-2025-014

**Severity:** Critical  
**Detection:** 03:12 UTC  
**Containment:** после evidence preservation  
**Recovery:** поэтапный  
**PIR:** в течение 3 рабочих дней  
**Формат:** blameless

## Что сработало

- EDR обнаружил подозрительный LSASS access.
- IdP зафиксировал impossible travel и серию входов в Admin.
- Proxy и DNS позволили связать export, upload и последующую активность.
- L1 объединил три алерта в один инцидент.
- Были сохранены ключевые артефакты до возможной переустановки endpoint.

## Что не сработало

- Нет круглосуточного L2/L3 on-call.
- LSASS detection имел severity `high`, но не был автоматически повышен до
  Critical при корреляции с identity и data signals.
- Отзыв sessions и refresh tokens был выполнен с задержкой.
- Для bulk transaction export не требовалась step-up authentication.
- Proxy allow-list разрешал большой исходящий объем на внешний upload endpoint.
- Binary integrity `SynthAgent` не контролировалась на каждом запуске.
- Не было автоматической корреляции LSASS + impossible travel + large outbound transfer.

## Root cause analysis

**Primary hypothesis:** компрометация, подмена или злоупотребление
`SynthAgent\agent.exe` на `PAY-WKS-07`.

Текущая telemetry подтверждает аномальное поведение `SynthAgent`, но сама по
себе не доказывает подмену бинарника. Для подтверждения нужны hash, signature,
install source, update history и сравнение с known-good baseline.

## Contributing factors

- Недостаточная behavioral detection для encoded PowerShell от service-like parent.
- Отсутствие step-up MFA для bulk export.
- Отсутствие 24/7 L2/L3.
- Избыточный egress для endpoint.
- Отсутствие continuous binary integrity monitoring.
- Отсутствие автоматической блокировки подозрительных external destinations.
- Недостаточное разделение прав доступа к административному API.

## Lessons learned

- Один отдельный алерт может быть неоднозначным; критична корреляция EDR, IdP,
  proxy и DNS.
- MFA-событие `satisfied` не означает, что доступ легитимен: нужно учитывать
  MFA method, device, session reuse и контекст.
- Allow-list домена не должен означать unlimited egress.
- Массовый экспорт чувствительных данных должен требовать дополнительного
  подтверждения и фиксироваться в audit log.
- Гипотезы должны быть отделены от подтвержденных фактов.
