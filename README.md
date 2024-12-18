# Сервис мониторинга сайта

Сервис для мониторинга работоспособности веб-сайта с автоматическим обновлением записей при обнаружении проблем.

## Описание

Этот сервис выполняет следующие функции:
- Периодически проверяет доступность указанного веб-сайта
- Проверяет корректность JSON-ответов
- Отслеживает количество последовательных ошибок
- Автоматически обновляет записи при достижении определенного порога ошибок
- Ведет подробное логирование всех операций

## Требования

- Python 3.7+
- Poetry (опционально)

## Установка

1. Клонируйте репозиторий и перейдите в директорию проекта:
```bash
git clone <url-репозитория>
cd service-monitoring-site
```

2. Установите зависимости с помощью Poetry:
```bash
poetry install
```

3. Создайте файл .env в корневой директории проекта и добавьте следующие настройки:
```env
MONITORED_SITE_URL=https://ваш-сайт.ru
CHECK_INTERVAL_SECONDS=5
```

## Запуск

Для запуска сервиса выполните команду:
```bash
python src/monitor.py
```

## Настройка

Сервис настраивается через переменные окружения:

- `MONITORED_SITE_URL`: Адрес сайта для мониторинга
- `CHECK_INTERVAL_SECONDS`: Интервал между проверками в секундах (по умолчанию: 5)

## Логирование

Сервис ведет подробное логирование всех операций. В логах содержится:
- Метка времени каждого события
- Уровень важности сообщения
- Результаты проверок сайта
- Информация об ошибках и предупреждениях

## Обработка ошибок

- Сервис подсчитывает количество последовательных ошибок
- После двух последовательных ошибок происходит автоматическое обновление записи
- Счетчик ошибок сбрасывается после успешной проверки или обновления записи

## Структура проекта

```
service-monitoring-site/
├── src                    # Код проекта
│   ├── routes             # Маршруты
│   ├──   |── records.py   # Маршрут для работы с записями
│   ├──   |── zones.py     # Маршрут для работы с зонами
│   ├── main.py            # Запуск FastAPI приложения
│   ├── monitor.py         # Скрипт мониторинга сайта
│   ├── utils.py           # Вспомогательные функции
├── pyproject.toml         # Конфигурация Poetry и зависимости проекта
├── poetry.lock            # Фиксация версий зависимостей
├── .env                   # Файл с env
└── README.md              # Документация
```

## Зависимости

- requests: Библиотека для HTTP-запросов
- python-dotenv: Работа с переменными окружения
- logging: Система логирования
- asyncio: Асинхронное выполнение операций

## Для разработчиков

При внесении изменений в код убедитесь, что:
1. Все значимые действия фиксируются в логах
2. Правильно обрабатываются исключения

## Лицензия
см. файл LICENSE.txt
