# Solutions — IR Answers

> Сначала самостоятельно пройдите этапы `05-response/` и `06-recovery/`.

## Containment

1. Сохранить volatile evidence:
   - EDR telemetry;
   - process tree;
   - active network connections;
   - memory acquisition, если разрешено playbook;
   - копию `cache.bin` с SHA-256 и chain of custody.

2. Изолировать `PAY-WKS-07` через EDR:
   - сохранить management channel;
   - не перезагружать endpoint;
   - не удалять артефакты до копирования.

3. Заблокировать внешние destinations:
   - `uploads.synthetic.example`;
   - `pastebin.synthetic.example`;
   - `ctfmon.synthetic.example`;
   - `metric.synthetic.example`;
   - `192.0.2.77`.

4. Contain identity:
   - revoke SSO sessions;
   - revoke refresh tokens;
   - revoke device sessions;
   - revoke OAuth grants и API tokens;
   - временно disable `d.petrov`, не delete.

5. Ограничить доступ к данным:
   - заблокировать `d.petrov` в `SynthPay-Admin`;
   - временно приостановить bulk export;
   - проверить созданные API tokens, OAuth apps и service accounts.

6. Уведомить:
   - SOC Lead;
   - IR;
   - CISO;
   - IAM;
   - Endpoint;
   - Network;
   - Application owner;
   - Legal / DPO.

## Eradication

1. Проверить `SynthAgent\agent.exe`:
   - hash;
   - digital signature;
   - file version;
   - installation source;
   - update history;
   - distribution across fleet.

2. Проверить persistence:
   - scheduled tasks;
   - services;
   - Run/RunOnce keys;
   - WMI subscriptions;
   - startup folder;
   - OAuth applications;
   - API tokens.

3. Проверить `wermgr.exe` и `ctfmon.exe`:
   - path;
   - hash;
   - signature;
   - parent process;
   - network connections.

4. Выполнить fleet hunting:
   - тот же hash или путь `SynthAgent`;
   - PowerShell child processes от service-like parents;
   - соединения с identified destinations;
   - similar DNS activity.

5. Ротировать credentials:
   - API tokens;
   - OAuth client secrets;
   - SSH keys;
   - CI/CD credentials;
   - certificates;
   - service account credentials.

## Recovery

1. Развернуть `PAY-WKS-07` из trusted golden image.
2. Не использовать snapshot, созданный после начала подозрительной активности.
3. Установить endpoint agent из trusted source.
4. Выполнить MFA re-enrollment для `d.petrov`.
5. Вернуть доступы по least privilege.
6. Включить step-up MFA для sensitive admin functions.
7. Включить усиленный мониторинг минимум на 14 дней.

## Критерии закрытия

- Нет активных attacker sessions, refresh tokens или API tokens.
- Нет persistence.
- Нет C2 или upload traffic к identified destinations.
- Secrets ротированы.
- Endpoint восстановлен из trusted baseline.
- MFA re-enrolled.
- Доступы пересмотрены.
- Legal/DPO завершили оценку возможной утечки.
- PIR и action items созданы и имеют владельцев.
