import cloudscraper
from bs4 import BeautifulSoup
import time

PAGES = [
    "https://freelancehunt.com/ua/projects/skill/javascript/28.html",
    "https://freelancehunt.com/ua/projects/skill/python/22.html",
    "https://freelancehunt.com/ua/projects/skill/veb-programuvannya/99.html",
    "https://freelancehunt.com/ua/projects/skill/rozrobka-botiv/180.html"
]


def get_page(url, max_retries=10):
    scraper = cloudscraper.create_scraper()
    for i in range(max_retries):
        response = scraper.get(url)
        if "<title>Just a moment" not in response.text:
            return response.text
        time.sleep(.5)
    raise Exception("😡 Не вдалося обійти Cloudflare після кількох спроб")


def parse_data(url):
    html = get_page(url)
    soup = BeautifulSoup(html, "html.parser")

    rows = soup.find_all("tr", attrs={"data-published": True})
    count = 0
    for row in rows:
        title_tag = row.find("a", class_="biggest")
        title = title_tag.text.strip() if title_tag else "Немає назви"
        url = title_tag['href'] if title_tag else "#"
        description_tag = row.find("p")
        description = description_tag.text.strip() if description_tag else "—"
        price_tag = row.find("div", class_="text-green price")
        price = price_tag.text.strip() if price_tag else "—"
        tags = [tag.text.strip() for tag in row.find_all("a") if '/projects/skill/' in tag['href']]

        if not price_tag: continue

        count += 1

        # print(f"Назва: {title}")
        # print(f"Посилання: {url}")
        # print(f"Опис: {description}")
        # print(f"Ціна: {price}")
        # print(f"Теги: {', '.join(tags)}")
        # print("-" * 60)
        print(f"{count}) {title} - {price} ({url})")


def main():
    for page in PAGES:
        print(f"Обробка сторінки: {page}\n")
        try:
            parse_data(page)
        except Exception as e:
            print(f"Помилка при обробці {page}: {e}")
        print("\n" + "=" * 80 + "\n")
        input("Натисніть Enter для продовження...")


if __name__ == "__main__":
    main()