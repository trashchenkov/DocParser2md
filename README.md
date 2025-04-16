# DocParser

DocParser — это CLI‑утилита на Python для сбора и конвертации документации с веб‑сайтов в формат Markdown.

## Функционал

- Рендеринг страниц с поддержкой JavaScript (Playwright + Chromium)
- Обход всех внутренних ссылок сайта (BFS)
- Извлечение основного блока контента (CSS‑селекторы: `.document`, `article`, `#main-content`, `#content`)
- Конвертация HTML в Markdown (`markdownify`)
- Сохранение каждой страницы в отдельный файл `.md`

## Требования

- Python 3.7+
- Виртуальное окружение (рекомендуется)
- Playwright (Chromium)
- BeautifulSoup4
- markdownify

## Установка

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Использование

```bash
python doc_parser.py --url <URL_документации> --out-dir <директория_вывода>
```

Например:

```bash
python doc_parser.py --url https://google.github.io/adk-docs/ --out-dir ./md_output
```

## Игнорируемые файлы

```gitignore
venv/
md_output/
```

Добавьте эти строки в файл `.gitignore` перед публикацией на GitHub.

## Лицензия

MIT
