# Eradication Log — CASE-2025-014

Цель eradication — устранить активный доступ атакующего, persistence,
скомпрометированные учетные данные и исходный вектор.

## Действия

| Время UTC | Действие | Проверка | Результат |
|---|---|---|---|
| 04:10 | Проверить `SynthAgent\agent.exe`: hash, signature, version, install source | Compare with known-good baseline | Pending |
| 04:20 | Найти тот же hash, path или process tree на других хостах | EDR fleet search | Pending |
| 04:30 | Проверить scheduled tasks, services, Run/RunOnce keys и WMI subscriptions | Endpoint and IR review | Pending |
| 04:40 | Проверить `wermgr.exe` и `ctfmon.exe`: path, hash, signature и network activity | EDR and forensic image review | Pending |
| 04:50 | Удалить подтвержденные persistence mechanisms | Before/after validation | Pending |
| 05:00 | Ротировать API tokens, OAuth grants, SSH keys и CI/CD secrets | Secrets inventory | Pending |
| 05:10 | Проверить pastebin publication и при необходимости запросить удаление | Legal and external service review | Pending |
| 05:20 | Проверить оставшиеся sessions, tokens и OAuth applications `d.petrov` | IAM audit | Pending |

## Критерии завершения eradication

- Нет активных sessions, refresh tokens и API tokens атакующего.
- Нет известных persistence mechanisms.
- Нет трафика к идентифицированным C2, upload и pastebin destinations.
- Секреты, доступные скомпрометированным системам, ротированы.
- `SynthAgent` проверен и либо восстановлен из trusted source, либо удален.
- Нет новых подозрительных событий по `PAY-WKS-07` и `d.petrov`.
