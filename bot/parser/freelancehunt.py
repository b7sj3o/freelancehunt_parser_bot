import time
import re

import cloudscraper
from bs4 import BeautifulSoup

from bot.db.models import User
from dataclasses import dataclass
from typing import List

@dataclass
class Project:
    title: str
    link: str
    description: str
    price: int
    tags: List[str]
    bets: int

def get_page(url, max_retries=10):
    scraper = cloudscraper.create_scraper()
    for i in range(max_retries):
        response = scraper.get(url)
        if "<title>Just a moment" not in response.text:
            return response.text
        time.sleep(.5)
    raise Exception("😡 Не вдалося обійти Cloudflare після кількох спроб")


def parse_project_row(row) -> Project | None:
    is_premium = row.find("div", class_="biggest")
    if is_premium:
        title_tag = is_premium.find("a", class_="visitable")
    else:
        title_tag = row.find("a", class_="biggest")
        
    title = title_tag.text.strip() if title_tag else "Немає назви"
    link = title_tag['href'] if title_tag else "#"
    description_tag = row.find("p")
    description = description_tag.text.strip() if description_tag else "—"
    price_tag = row.find("div", class_="text-green price")
    
    if not price_tag:
        return None  # пропускаємо без ціни
    
    price = int(''.join(re.findall(r'\d+', price_tag.text)))
    tags = [tag.text.strip().lower() for tag in row.find_all("a") if '/projects/skill/' in tag['href']]

    bets_parent = row.find("div", style="line-height: 36px")
    bets_span = bets_parent.find("span", class_="hidden-xs") if bets_parent else None
    if bets_span:
        bets_text = bets_span.text.strip()
        match = re.search(r'(\d+)', bets_text)
        bets = int(match.group(1)) if match else 0
    else:
        bets = 0
    
    return Project(
        title=title,
        link=link,
        description=description,
        price=price,
        tags=tags,
        bets=bets
    )


def is_project_valid(project: Project, user: User) -> bool:
    if user.filter_min_cost is not None and project.price < user.filter_min_cost:
        return False
    if user.filter_max_cost is not None and project.price > user.filter_max_cost:
        return False
    if user.filter_max_bets is not None and project.bets > user.filter_max_bets:
        return False
    if any(word in project.tags for word in user.excluded_tags):
        return False

    return True



async def parse_data(url: str, user: User) -> List[Project]:
    html = get_page(url)
    soup = BeautifulSoup(html, "html.parser")

    rows = soup.find_all("tr", attrs={"data-published": True})
    result = []


    for row in rows:
        project = parse_project_row(row)

        if project is None:
            continue

        if is_project_valid(project, user):
            result.append(project)

    return result
