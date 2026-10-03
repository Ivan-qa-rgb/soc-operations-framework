# Tuning Notes — CASE-2025-014

## Detection: impossible_travel_synthetic

### Проблема

Правило фиксирует географическую аномалию, но не учитывает чувствительность
приложения, повторные входы, смену ASN и корреляцию с endpoint/proxy.

### Что изменить

- Добавить risk boost при:
  - двух разных source IP в течение 180 минут;
  - разных ASN или географиях;
  - доступе к приложениям с меткой `sensitive`;
  - более трех успешных входов за 10 минут;
  - отсутствии соответствующей VPN-сессии.
- Повышать severity до High/Critical только при корреляции с endpoint
  или data-exfiltration сигналами.
- Автоматически обогащать кейс событиями EDR и proxy.

## Detection: large_outbound_transfer

### Проблема

Фиксированный порог `+640%` не учитывает роль хоста, класс destination,
время суток и характер передачи.

### Что изменить

- Строить baseline на 30 дней по хосту и классу destination.
- Использовать P95/P99 вместо среднего и процентного отклонения.
- Классифицировать destination:
  - internal service;
  - approved file transfer;
  - external file share;
  - developer or code-sharing service;
  - unknown or newly observed domain.
- Алертить при:
  - первом observed external upload domain для хоста;
  - превышении P99;
  - upload сразу после sensitive API export;
  - upload на `uploads.*`, `pastebin.*`, `transfer.*` или похожие категории.
- Temporary block применять только для high-confidence комбинаций.

## Egress policy

### Проблема

Allow-list домена фактически превращается в неограниченный канал исходящего
трафика.

### Что изменить

- Вести baseline `bytes_out` по домену, хосту, пользователю и URL path.
- Контролировать не только домен, но и:
  - HTTP method;
  - URL path;
  - content type;
  - пользователя;
  - роль хоста;
  - временной интервал.
- Для `uploads.*` требовать утвержденный business workflow.
- Алертить при превышении P99.
- Требовать approval выше заданного порога.
- Блокировать только high-confidence аномальные комбинации.

## Process

### Проблема

Отсутствие ночного L2/L3 замедляет эскалацию и containment.

### Что изменить

- Запустить пилотную ротацию L2 on-call.
- Установить SLA:
  - L1 acknowledges Critical alert за 5 минут;
  - L2 подключается за 15 минут.
- Через 60 дней оценить:
  - MTTA;
  - MTTD;
  - containment time;
  - false-page rate;
  - покрытие смен.
- Не отменять on-call только из-за отсутствия инцидентов.
