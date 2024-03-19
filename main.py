import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os

def fetch_and_save_articles(url):
    # Отправляем GET-запрос к сайту
    response = requests.get(url)
    response.raise_for_status()  # проверяем на ошибки

    # Парсим HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Поиск всех статей или нужных элементов на странице
    articles = soup.findAll('article') # Нужно адаптировать под структуру сайта

    for article in articles:
        # Извлекаем заголовок статьи и текст (это пример, нужно адаптировать под структуру сайта)
        title = article.find('h2').text.strip()
        content_html = str(article.find('div', class_='content'))  # Нужно уточнить класс для контента

        # Конвертируем HTML в Markdown
        content_md = md(content_html)

        # Создаем или открываем файл для сохранения статьи
        # Используем заголовок статьи как название файла (обязательно проверьте на валидность и уникальность!)
        file_path = f'articles/{title}.md'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f'# {title}\n\n{content_md}')

# Пример использования
url = 'https://exil-solidaire.fr'
fetch_and_save_articles(url)
