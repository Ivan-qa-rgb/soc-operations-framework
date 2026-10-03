# L1 Decisions — CASE-2025-014

> Этот файл — эталон для самопроверки. Сначала заполни `triage-notes.md`
> самостоятельно, затем сравни свои выводы с этим документом.

## SYNTH-ALERT-0001 — LSASS access

**Классификация:** True Positive  
**Severity:** Critical после корреляции

**Обоснование:**

- Hidden encoded PowerShell обращается к `lsass.exe`.
- `granted_access=0x1010` соответствует подозрительному доступу к памяти процесса.
- Родительский процесс — `SynthAgent\agent.exe`, что нетипично для интерактивного пользователя.
- Контекст `NT AUTHORITY\SYSTEM` требует проверки: это может быть service context,
  token manipulation или ошибка атрибуции в telemetry.
- Перед LSASS access были запущены два hidden encoded PowerShell-процесса.
- После LSASS access создается `cache.bin` и наблюдается внешняя передача данных.

**Что проверить дальше:**

- Все EDR-события по `PAY-WKS-07` за 02:30–04:30 UTC.
- Полные command line для PowerShell PID 3555, 4212 и 6301.
- Hash, подпись, версию и источник установки `SynthAgent\agent.exe`.
- Process tree: `agent.exe → powershell.exe → wermgr.exe`.
- Наличие `cache.bin`, других временных файлов и артефактов persistence.
- Другие хосты с тем же `SynthAgent` hash, path или process tree.

**Кому эскалировать:**

- L2 / IR on-call — немедленно.
- SOC Lead / Incident Commander.
- Endpoint team для изоляции и forensic support.

## SYNTH-ALERT-0002 — Impossible Travel

**Классификация:** True Positive  
**Severity:** Critical после корреляции

**Обоснование:**

- `d.petrov` ранее успешно аутентифицировался из `SynthCity-A`.
- В 03:17 UTC происходит успешный вход из `SynthCity-B` при расстоянии 8700 км.
- Первый подозрительный вход использует MFA push approval.
- Затем следуют повторные входы в `SynthPay-Admin`, вероятно через session
  или refresh token reuse.
- Пользователь получает доступ к чувствительному административному приложению.
- После входа выполняются запросы к `/v1/accounts` и экспорт транзакций за 90 дней.

**Что проверить дальше:**

- Тип MFA: push, number matching, WebAuthn, OTP, remembered device.
- Все MFA challenges, push-уведомления и их одобрения.
- Session IDs, refresh tokens, device IDs и OAuth grants.
- Новые устройства, recovery methods и изменения MFA factors.
- Историю входов `d.petrov` за 7–30 дней.
- Действия в `SynthPay-Admin` и API audit logs.
- Подтверждение у пользователя через защищенный out-of-band канал.

**Кому эскалировать:**

- L2 / IR on-call — немедленно.
- IAM / IdP administrator.
- Application owner `SynthPay-Admin`.
- Руководитель пользователя через HR или другой защищенный канал.

## SYNTH-ALERT-0003 — Large outbound transfer

**Классификация:** True Positive после корреляции  
**Severity:** Critical после корреляции

**Обоснование:**

- С `PAY-WKS-07` передается около 1 GB по TLS на `uploads.synthetic.example`.
- Используется метод `PUT`, что соответствует загрузке файла или набора данных.
- Объем превышает P99 baseline для хоста и destination class.
- Передача происходит сразу после `GET /v1/transactions/export?range=last_90d`.
- На хосте создается `cache.bin` размером около 1 GB.
- Destination совпадает с внешней активностью, связанной с тем же пользователем и хостом.

**Что проверить дальше:**

- Полный URL, SNI, certificate metadata, user agent и content type.
- Все обращения к `uploads.synthetic.example` за 30 дней.
- Другие хосты и пользователи, связанные с этим destination.
- API audit trail: состав и объем результата transaction export.
- Содержимое и происхождение `cache.bin`.
- Возможность блокировки или удаления опубликованных данных.
- DLP, CASB, mail gateway и cloud audit logs.

**Кому эскалировать:**

- L2 / IR on-call — немедленно.
- Network Security для блокировки destination.
- Application owner и Data Protection / Legal / DPO.
- DevOps / API team для проверки export-функции и токенов.

## Объединенный инцидент

**CASE-2025-014**  
**Severity:** Critical  
**Owner:** L2 / IR on-call  
**Status:** Open, active investigation

### Основание для объединения

- Общий пользователь: `d.petrov`.
- Общий endpoint: `PAY-WKS-07`.
- Связная временная последовательность: LSASS access → Admin SSO activity →
  transaction export → large outbound upload.
- Endpoint, identity и data signals указывают на один вероятный инцидент.

### Первичная гипотеза

Компрометация, подмена или злоупотребление `SynthAgent\agent.exe` на
`PAY-WKS-07` позволило выполнить reconnaissance, encoded PowerShell, LSASS access,
а затем использовать украденные сессии или токены `d.petrov` для доступа к
`SynthPay-Admin`, экспорта транзакций и выгрузки данных.

### Альтернативные гипотезы

1. Легитимный `SynthAgent` был скомпрометирован или эксплуатируется через уязвимость.
2. Initial access — phishing или social engineering.
3. Инсайдерская активность.
4. Telemetry attribution error.

### Что не подтверждено

- Initial access vector.
- Фактическая подмена `SynthAgent\agent.exe`.
- Полный состав выгруженных данных.
- Публикация credentials или secrets на pastebin.
- Компрометация Domain Admin.
- Влияние на production payment services.

### Рекомендация L1

Немедленно эскалировать все три алерта как один Critical incident.
Не закрывать алерты независимо друг от друга.
