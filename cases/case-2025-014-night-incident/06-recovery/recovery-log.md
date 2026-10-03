# Recovery Log — CASE-2025-014

Цель recovery — безопасно вернуть сервисы, пользователя и endpoint в работу
только после containment, eradication и проверки остаточного риска.

## Действия восстановления

| Время UTC | Действие | Критерий возврата | Статус |
|---|---|---|---|
| 06:00 | Восстановить `PAY-WKS-07` из trusted golden image | Образ проверен, новее инцидента, EDR healthy | Pending |
| 06:30 | Установить `SynthAgent` из trusted source | Hash и signature verified; update channel validated | Pending |
| 07:00 | Выполнить MFA re-enrollment для `d.petrov` | Старые factors, sessions и tokens отозваны | Pending |
| 07:15 | Ротировать доступные пользователю API tokens, SSH keys и OAuth grants | Rotation completed and verified | Pending |
| 07:30 | Вернуть доступ `d.petrov` по least privilege | Identity review completed; device compliant | Pending |
| 08:00 | Вернуть доступ к `SynthPay-Admin` | Step-up MFA enabled; approval completed | Pending |
| 08:30 | Включить усиленный мониторинг | Monitoring for user, host and destinations enabled | Pending |

## Критерии возврата в production

- Нет известных persistence mechanisms.
- Нет соединений с C2, upload или pastebin destinations.
- EDR работает, обновлен и видит endpoint.
- Все потенциально скомпрометированные secrets ротированы.
- MFA повторно зарегистрирована.
- Доступы выданы по least privilege.
- Для `SynthPay-Admin` включены дополнительные проверки.
- Усиленный мониторинг включен минимум на 14 дней.

## Что нельзя делать

- Не восстанавливать хост из образа или snapshot, созданного после начала инцидента.
- Не возвращать учетную запись без revoke sessions/tokens и MFA re-enrollment.
- Не возвращать прежние admin privileges автоматически.
- Не завершать инцидент только потому, что хост снова работает.
