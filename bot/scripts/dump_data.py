import asyncio

from sqlalchemy.sql import select

from bot.db.models import Category, CategoryItem, Base
from bot.db.session import async_session, engine, create_db




async def create_categories():
    async with async_session() as session:
        session.add(Category(name="Програмування"))
        session.add(Category(name="Дизайн та арт"))
        session.add(Category(name="Фото, аудіо та відео"))
        session.add(Category(name="Переклади"))
        session.add(Category(name="Робота з текстами"))
        await session.commit()
        print("Categories created successfully")

async def create_category_items():
    async with async_session() as session:
        programming_id = await session.scalar(select(Category.id).where(Category.name == "Програмування"))
        design_id = await session.scalar(select(Category.id).where(Category.name == "Дизайн та арт"))
        photo_id = await session.scalar(select(Category.id).where(Category.name == "Фото, аудіо та відео"))
        translation_id = await session.scalar(select(Category.id).where(Category.name == "Переклади"))
        text_id = await session.scalar(select(Category.id).where(Category.name == "Робота з текстами"))

        

        programming_items = [
            ["AI та машинне навчання", "https://freelancehunt.com/ua/projects/skill/mashinne-navchannya/175.html"],
            ["AR та VR розробка","https://freelancehunt.com/ua/projects/skill/ar-ta-vr-rozrobka/185.html"],
            ["C та C++","https://freelancehunt.com/ua/projects/skill/ta-cplusplus/2.html"],
            ["C#","https://freelancehunt.com/ua/projects/skill/c/24.html"],
            ["CMS","https://freelancehunt.com/ua/projects/skill/cms/78.html"],
            ["HTML та CSS верстання","https://freelancehunt.com/ua/projects/skill/html-ta-css-verstannya/124.html"],
            ["Java","https://freelancehunt.com/ua/projects/skill/java/13.html"],
            ["Javascript та Typescript","https://freelancehunt.com/ua/projects/skill/javascript/28.html"],
            ["PHP","https://freelancehunt.com/ua/projects/skill/php/1.html"],
            ["Python","https://freelancehunt.com/ua/projects/skill/python/22.html"],
            ["Бази даних та SQL","https://freelancehunt.com/ua/projects/skill/bazi-danih/86.html"],
            ["Вбудовані системи та мікроконтролери","https://freelancehunt.com/ua/projects/skill/vbudovani-sistemi-ta-mikrokontroleri/176.html"],
            ["Веб-програмування","https://freelancehunt.com/ua/projects/skill/veb-programuvannya/99.html"],
            ["Десктопні додатки","https://freelancehunt.com/ua/projects/skill/prikladne-programuvannya/103.html"],
            ["Криптовалюта та blockchain","https://freelancehunt.com/ua/projects/skill/blockchain/182.html"],
            ["Парсинг даних","https://freelancehunt.com/ua/projects/skill/parsing-danih/169.html"],
            ["Розробка ігор","https://freelancehunt.com/ua/projects/skill/igrovi-programi/88.html"],
            ["Розробка ботів","https://freelancehunt.com/ua/projects/skill/rozrobka-botiv/180.html"],
            ["Тестування та QA","https://freelancehunt.com/ua/projects/skill/testuvannya-ta/57.html"]
        ]
        design_items = [
            ["3D моделювання та візуалізація", "https://freelancehunt.com/ua/projects/skill/stvorennya-3d-modeley/59.html"],
            ["AI у дизайні", "https://freelancehunt.com/ua/projects/skill/ai-u-dizayni/186.html"],
            ["VR та AR дизайн", "https://freelancehunt.com/ua/projects/skill/vr-ta-ar-dizayn/187.html"],
            ["Іконки та піксельна графіка", "https://freelancehunt.com/ua/projects/skill/ikonki-ta-pikselna-grafika/93.html"],
            ["Ілюстрації та малюнки", "https://freelancehunt.com/ua/projects/skill/ilyustratsiyi-ta-malyunki/90.html"],
            ["Інфографіка", "https://freelancehunt.com/ua/projects/skill/infografika/172.html"],
            ["Банери", "https://freelancehunt.com/ua/projects/skill/baneri/41.html"],
            ["Векторна графіка", "https://freelancehunt.com/ua/projects/skill/vektorna-grafika/58.html"],
            ["Дизайн інтерфейсів (UI/UX)", "https://freelancehunt.com/ua/projects/skill/dizayn-interfeysiv/42.html"],
            ["Дизайн інтер’єрів", "https://freelancehunt.com/ua/projects/skill/dizayn-inter-eriv/106.html"],
            ["Дизайн візиток", "https://freelancehunt.com/ua/projects/skill/dizayn-vizitok/156.html"],
            ["Дизайн виставкових стендів", "https://freelancehunt.com/ua/projects/skill/dizayn-vistavkovih-stendiv/132.html"],
            ["Дизайн мобільних додатків", "https://freelancehunt.com/ua/projects/skill/dizayn-mobilnih-dodatkiv/179.html"],
            ["Дизайн одягу", "https://freelancehunt.com/ua/projects/skill/dizayn-odyagu/198.html"],
            ["Дизайн пакування та етикетки", "https://freelancehunt.com/ua/projects/skill/dizayn-pakuvannya-ta-etiketki/117.html"],
            ["Дизайн сайтів", "https://freelancehunt.com/ua/projects/skill/dizayn-saytiv/43.html"],
            ["Живопис і графіка", "https://freelancehunt.com/ua/projects/skill/zhivopis-grafika/141.html"],
            ["Зовнішня реклама", "https://freelancehunt.com/ua/projects/skill/zovnishnya-reklama/109.html"],
            ["Логотипи", "https://freelancehunt.com/ua/projects/skill/logotipi/17.html"],
            ["Оформлення сторінок у соціальних мережах", "https://freelancehunt.com/ua/projects/skill/oformlennya-storinok-sotsialnih-merezhah/151.html"],
            ["Поліграфічний дизайн", "https://freelancehunt.com/ua/projects/skill/poligrafichniy-dizayn/75.html"],
            ["Предметний дизайн", "https://freelancehunt.com/ua/projects/skill/predmetniy-dizayn/164.html"],
            ["Розробка презентацій", "https://freelancehunt.com/ua/projects/skill/rozrobka-prezentatsiy/114.html"],
            ["Розробка шрифтів", "https://freelancehunt.com/ua/projects/skill/rozrobka-shriftiv/152.html"],
            ["Фірмовий стиль", "https://freelancehunt.com/ua/projects/skill/firmoviy-stil/77.html"]
        ]
        photo_items = [
            ["AI cинтез голосу", "https://freelancehunt.com/ua/projects/skill/ai-cintez-golosu/191.html"],
            ["AI cтворення відео", "https://freelancehunt.com/ua/projects/skill/ai-ctvorennya-video/192.html"],
            ["Анімація", "https://freelancehunt.com/ua/projects/skill/animatsiya/91.html"],
            ["Аудіо та відео монтаж", "https://freelancehunt.com/ua/projects/skill/audio-ta-video-montazh/113.html"],
            ["Відеореклама", "https://freelancehunt.com/ua/projects/skill/videoreklama/144.html"],
            ["Музика", "https://freelancehunt.com/ua/projects/skill/muzika/100.html"],
            ["Обробка аудіо", "https://freelancehunt.com/ua/projects/skill/obrobka-audio/102.html"],
            ["Обробка відео", "https://freelancehunt.com/ua/projects/skill/obrobka-video/101.html"],
            ["Обробка фото", "https://freelancehunt.com/ua/projects/skill/obrobka-foto/18.html"],
            ["Послуги диктора", "https://freelancehunt.com/ua/projects/skill/poslugi-diktora/143.html"],
            ["Транскрибування", "https://freelancehunt.com/ua/projects/skill/transkribuvannya/122.html"],
            ["Фільмування", "https://freelancehunt.com/ua/projects/skill/filmuvannya/161.html"],
            ["Фотографування", "https://freelancehunt.com/ua/projects/skill/fotografuvannya/139.html"]
        ]
        translation_items = [
            ["Іспанська мова", "https://freelancehunt.com/ua/projects/skill/ispanska-mova/84.html"],
            ["Англійська мова", "https://freelancehunt.com/ua/projects/skill/angliyska-mova/79.html"],
            ["Локалізація ПЗ, сайтів та ігор", "https://freelancehunt.com/ua/projects/skill/lokalizatsiya-pz-saytiv-ta-igor/157.html"],
            ["Німецька мова", "https://freelancehunt.com/ua/projects/skill/nimetska-mova/80.html"],
            ["Переклад текстів", "https://freelancehunt.com/ua/projects/skill/pereklad-tekstiv/37.html"],
            ["Польська мова", "https://freelancehunt.com/ua/projects/skill/polska-mova/195.html"],
            ["Українська мова", "https://freelancehunt.com/ua/projects/skill/ukrayinska-mova/196.html"],
            ["Французька мова", "https://freelancehunt.com/ua/projects/skill/frantsuzka-mova/158.html"]
        ]
        text_items = [
            ["AI обробка текстів", "https://freelancehunt.com/ua/projects/skill/ai-obrobka-tekstiv/197.html"],
            ["Вірші, пісні, проза", "https://freelancehunt.com/ua/projects/skill/virshi-pisni-proza/140.html"],
            ["Копірайтинг", "https://freelancehunt.com/ua/projects/skill/kopirayting/76.html"],
            ["Написання статей", "https://freelancehunt.com/ua/projects/skill/napisannya-statey/38.html"],
            ["Написання сценаріїв", "https://freelancehunt.com/ua/projects/skill/napisannya-stsenariyiv/163.html"],
            ["Неймінг і слогани", "https://freelancehunt.com/ua/projects/skill/neyming-slogani/123.html"],
            ["Публікація оголошень", "https://freelancehunt.com/ua/projects/skill/publikatsiya-ogoloshen/138.html"],
            ["Редагування та коректура текстів", "https://freelancehunt.com/ua/projects/skill/redaguvannya-ta-korektura-tekstiv/168.html"],
            ["Рерайтинг", "https://freelancehunt.com/ua/projects/skill/rerayting/125.html"],
            ["Технічна документація", "https://freelancehunt.com/ua/projects/skill/tehnichna-dokumentatsiya/97.html"]
        ]

        for item in programming_items:
            session.add(CategoryItem(name=item[0], category_id=programming_id, link=item[1]))
        for item in design_items:
            session.add(CategoryItem(name=item[0], category_id=design_id, link=item[1]))
        for item in photo_items:
            session.add(CategoryItem(name=item[0], category_id=photo_id, link=item[1]))
        for item in translation_items:
            session.add(CategoryItem(name=item[0], category_id=translation_id, link=item[1]))
        for item in text_items:
            session.add(CategoryItem(name=item[0], category_id=text_id, link=item[1]))

        await session.commit()
        print("Category items created successfully")


async def dump_data():
    await create_db(drop=True)
    
    await create_categories()
    await create_category_items()

if __name__ == "__main__":
    asyncio.run(dump_data())