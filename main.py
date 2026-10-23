import os
import logging
import secrets
from urllib.parse import quote

from aiohttp import web

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "ferixdiii").strip().lstrip("@")
PAYMENT_PHONE = os.getenv("PAYMENT_PHONE", "+79935801642").strip()
PAYMENT_BANK = os.getenv("PAYMENT_BANK", "Яндекс Банк").strip()
PAYMENT_NAME = os.getenv("PAYMENT_NAME", "Дмитрий").strip()

PRODUCTS = {
    "gemini_pro": {
        "title": "Gemini Pro — 1000 кредитов",
        "price": 599,
        "short": "1 месяц · 1000 кредитов Google Flow · готовый Gmail-аккаунт",
        "description": """Аккаунт Gemini Pro 1000 кредитов (почта | пароль) Gemini Pro - 1 месяц 1000 кредитов

Регион: Республика Корея

Работает из России с любой страной ВПН (Германия, США, Казахстан и т.д).

⚡ 1000 кредитов Google Flow на 1 месяц. Личный готовый аккаунт

🤖 Omni 1.1 + Nano Banana 2

✅ Готовый Gmail-аккаунт

Аккаунт уже настроен - просто входите и создавайте проекты.

⚠️ Важно при входе

Используйте доступ в чистом браузере, где нет других Google-аккаунтов.

Самый простой вариант:
1. Откройте новый профиль браузера или режим инкогнито.
2. Войдите только в выданный Gmail.
3. Пользуйтесь доступом.

❌ Не добавляйте другие Google-аккаунты.
❌ Не переключайтесь между аккаунтами.""",
    },
    "gemini_ultra": {
        "title": "Gemini Ultra — 10 000 кредитов",
        "price": 3800,
        "short": "1 месяц · 10 000 кредитов · личный аккаунт",
        "description": """Gemini Ultra 10 000 кредитов Личный аккаунт Gemini Ultra на месяц

Доступ к генерации видео через официальный сервис Google Flow:
https://flow.google/

✅ Доступна модель Omni
✅ 10 000 кредитов на аккаунте
✅ Аккаунт передаётся полностью в личное пользование
✅ Все данные можно изменить после получения
🔐 Формат выдачи: Gmail | пароль | 2FA
качество 4к""",
    },
    "banana_group": {
        "title": "Gemini Ultra — Nano Banana 2.1 4K",
        "price": 599,
        "short": "Складчина · 30 дней · безлимитная генерация визуала в 4K",
        "description": """🔥 Складчина GEMINI ULTRA БЕЗЛИМИТ BANANA 2.1 В 4K 🔥

Складчина GEMINI ULTRA — БЕЗЛИМИТ NANO BANANA 2.1 В 4K НА МЕСЯЦ
Месяц генерации визуала в 4K всего за 599 ₽

Доступ к Gemini Ultra для маркетологов, SMM-специалистов, дизайнеров, контент-мейкеров и владельцев бизнеса.

♾️ БЕЗЛИМИТНАЯ ГЕНЕРАЦИЯ
Создавай изображения для своих проектов без оплаты за каждую картинку.

💎 РАЗРЕШЕНИЕ 4K
Детализированный визуал для рекламы, социальных сетей, карточек товаров и коммерческих проектов.

⚡ БЫСТРАЯ ГЕНЕРАЦИЯ
Создавай изображения за короткое время, тестируй идеи и выпускай больше контента.

🗂 У КАЖДОГО СВОЙ ПРОЕКТ
Работай со своими референсами и генерациями - участники не мешают друг другу.

Что можно создавать:
📱 SMM — посты, сторис, обложки и контент для соцсетей
🎯 Маркетинг — рекламные креативы и варианты для A/B-тестов
🛍 E-commerce — визуал товаров и каталоги
👗 Бренды — fashion-съёмки и lifestyle-контент
🎬 AI-контент — персонажи, реалистичные сцены и стартовые кадры для видеогенерации

💰 Стоимость складчины — 599 ₽ за 1 месяц доступа.
Для сравнения: в Higgsfield безлимитная генерация в 4K стоит $7 за 1 день, $16 за 3 дня и $32 за 7 дней.

🔥 30 дней · 4K · безлимитная генерация · 599 ₽
Создавай больше визуала, тестируй больше идей и сокращай расходы на производство контента.""",
    },
    "parser_llm": {
        "title": "Парсер + LLM: 100 сценариев применения",
        "price": 2499,
        "short": "100 готовых сценариев · реальные данные из интернета · анализ с помощью ChatGPT, Gemini и других LLM",
        "description": """ПАРСЕР + LLM: 100 СЦЕНАРИЕВ ПРИМЕНЕНИЯ

Практическое руководство о том, как перейти от обычных запросов к LLM к работе с реальными свежими данными из интернета.

Внутри — 100 готовых идей и сценариев для связки «сборщик данных + нейросеть» (ChatGPT, Gemini и другие модели):
• поиск трендов до того, как они станут мейнстримом
• мониторинг цен и новых офферов конкурентов
• поиск потенциальных клиентов
• анализ вопросов аудитории в комментариях Telegram
• анализ товаров, рекламы, контента и AI-сервисов
• изучение аудитории и многое другое

САМОЕ ЦЕННОЕ — ПРИНЦИП

Это не просто список из 100 пунктов, а механика, которую можно адаптировать под свои задачи.

1. Собери свежие факты из интернета: цифры, тексты, цены, отзывы.
2. Передай этот конкретный массив данных нейросети.
3. Получи анализ, скрытые закономерности, фильтрацию и план действий.

Когда поймёшь эту механику, сможешь адаптировать сценарии под свою нишу, бизнес, профессию или конкретную задачу.

Для этого не обязательно иметь армию программистов и штат аналитиков. Руководство помогает понять, что можно реализовать в связке парсер + LLM и как применять реальные данные без сложной разработки.

💰 Стоимость: 2499 ₽.""",
    },
    "omni_creative_v20": {
        "title": "OMNI CREATIVE AGENT v20.0",
        "price": 2999,
        "short": "Конвейер рекламных креативов · Qwen + GPT Image 2 + Omni",
        "description": """КОНВЕЙЕР РЕКЛАМНЫХ КРЕАТИВОВ ОТ FERIXDI 🚀
OMNI CREATIVE AGENT v20.0

Система автоматизирует создание рекламных креативов через Qwen + GPT Image 2 + Omni.

🔥 Разберётся даже новичок.
Загружаешь файл системы в Qwen, отвечаешь всего на 3 вопроса — и получаешь готовый комплект материалов.

📦 ЧТО НА ВЫХОДЕ
• 📸 Фото-эталон персонажа
• 🎬 6 готовых JSON-промптов для Omni
• 🗣 6 блоков живой речи
• 📱 Сценарий минутного вертикального видео с одним и тем же персонажем во всех сценах

Это позволяет быстро тестировать рекламные гипотезы, сохраняя единый стиль персонажа, естественную подачу и качество результата.

Подойдёт для агентств, фрилансеров, маркетологов и владельцев бизнеса.

⏱️ Вместо примерно 4 часов ручной работы — ориентировочно 15–20 минут до готового рекламного креатива.

Один раз забираешь систему и используешь для новых креативов, экономя время на каждом запуске.

📖 Подробная статья о том, как всё работает, опубликована на канале Ferixdi AI.

💰 Стоимость: 2999 ₽.""",
    },
    "remove_ai_label": {
        "title": "Убираем метку AI-контент из видео",
        "price": 999,
        "short": "Промпт для подготовки AI-видео к публикации · протестировано на Omni",
        "description": """УБИРАЕМ МЕТКУ AI-КОНТЕНТ ИЗ ВИДЕО

Instagram и YouTube могут определять AI-контент по метаданным, служебным маркерам и другим техническим признакам файла. Из-за этого на видео может появляться пометка «AI-контент» или «Создано с помощью ИИ».

Такая метка может влиять на восприятие ролика зрителем. При этом YouTube отдельно уточняет, что сама по себе AI-пометка автоматически не снижает охваты.

ЧТО ВХОДИТ

Готовый промпт для GPT, который помогает подготовить видеофайл к публикации: проверить технические данные, переэкспортировать видео и убрать лишние метаданные там, где это возможно.

Важно: очистка метаданных не гарантирует, что Instagram или YouTube не определят AI-происхождение видео. Платформы могут использовать и другие признаки. Не используйте этот процесс для сокрытия информации, которую платформа требует раскрывать, или для обхода обязательной маркировки.

🧪 Протестировано на видео, сгенерированных с помощью Omni.

💰 Стоимость: 999 ₽.""",
    },
    "seedream_prompts": {
        "title": "🔥 Seedream 5 Pro: 100 горячих промптов",
        "price": 999,
        "short": "100 промптов по фото-референсу · инструкция · примеры и настройки",
        "description": """🔥 SEEDREAM 5 PRO: 100 САМЫХ ГОРЯЧИХ ПРОМПТОВ

«Подожди… это действительно создано всего из одной фотографии?»

Загрузите разрешённый фото-референс — и превратите один снимок в целую AI-фотосессию премиального уровня: новые образы, выразительные позы, необычные ракурсы, кинематографичный свет и атмосферные локации с сохранением узнаваемой внешности персонажа.

📦 ВНУТРИ КОЛЛЕКЦИИ
• 100 тщательно отобранных промптов для Seedream 5 Pro
• Генерация по фото-референсу, а не только по текстовому описанию
• Понятная инструкция по запуску и оплате из России
• Настройки для реализма и стабильности внешности
• Примеры готовых результатов
• Регулярные обновления и новые сценарии

🎁 БОНУС
Подробная инструкция по работе в сервисе, созданию изображений и последующему оживлению фото.

💰 СТОИМОСТЬ ГЕНЕРАЦИИ
• Фото — от 3 ₽ за кадр
• Видео по готовому фото — от 12 ₽

Одно фото → один промпт → целая фотосессия.

🔞 ДОСТУП ТОЛЬКО ДЛЯ СОВЕРШЕННОЛЕТНИХ

Используйте собственные фотографии, образы вымышленных совершеннолетних персонажей или материалы, на использование которых получено явное согласие изображённого человека. Соблюдайте права на изображение и частную жизнь, а также правила сервиса и применимое законодательство. Материалы с участием несовершеннолетних запрещены.

💰 Стоимость коллекции: 999 ₽.""",
    },
    "course": {
        "title": "Охваты на AI. Обучение + партнёрки",
        "price": 10000,
        "short": "Практическое обучение с нуля · AI-видео · охваты · монетизация",
        "description": """Охваты на AI. Обучение + партнёрки ОХВАТЫ НА AI

Практическое обучение тому, как с нуля создавать охватные аккаунты на AI-видео, набирать аудиторию и дальше монетизировать полученный трафик.

Войти в обучение можно в любой момент. Работаем по уже собранной и проверенной методике.

ЧТО БУДЕМ ДЕЛАТЬ

Начинаем с абсолютного нуля.

Разбираемся, какие AI-форматы сейчас получают охваты, где брать идеи, как находить быстрорастущие механики, дешево производить ролики, регулярно публиковаться и анализировать результат.

Основной принцип простой:
сгенерировал → опубликовал → получил данные → разобрал → скорректировал → повторил.

Главная цель первого этапа — научиться системно добывать внимание и раскачать собственный аккаунт.

После этого подключаем монетизацию: свои продукты, услуги, проекты и ПАРТНЁРКИ.

ЧТО ВНУТРИ

• закрытый Telegram-чат
• пошаговые инструкции и статьи
• задания и практика
• генеративный AI-контент
• поиск идей и вирусных механик
• разбор алгоритмов и охватов
• взаимный буст
• разбор аккаунтов и роликов участников
• конвертация внимания в трафик
• монетизация и ПАРТНЁРКИ
• новые тесты, инструменты и рабочие кейсы
• мои ответы и помощь по конкретным ситуациям

Материалы структурированы по отдельным рабочим веткам. К ним можно возвращаться в любое время.

КОМУ ПОДОЙДЁТ

Можно приходить вообще без опыта.

Навыки монтажа, режиссуры или программирования не нужны. Показываю, какие инструменты использовать, что именно делать и в какой последовательности.

Но от вас нужны три вещи:
время, желание и регулярность.

Просто читать материалы недостаточно. Здесь результат появляется через постоянную практику.

КАКАЯ МОДЕЛЬ

Мы не учимся просто делать красивые AI-ролики и искать разовые заказы.

Мы строим собственный долгосрочный актив — охватные аккаунты, которые могут регулярно приводить аудиторию и трафик.

Дальше этот трафик можно направлять в:
ПАРТНЁРКИ / свои продукты / услуги / Telegram / бизнес / лидогенерацию.

Все подробности об обучении, программе и условиях участия: https://t.me/ferixdi_ai/1875

Главный навык обучения — не «уметь генерировать видео».
Главный навык — уметь системно получать внимание с помощью AI и понимать, куда его дальше конвертировать.

РЕЗУЛЬТАТЫ

Методика уже проверена на практике: участники, которые начинали с нуля, набирают тысячи и десятки тысяч подписчиков за кратчайший срок, а отдельные ролики регулярно получают большие охваты.

Это не обещание конкретного результата - цифры зависят прежде всего от количества практики, регулярности и выбранных форматов.

В обучение можно войти в любой момент и начать с нуля.""",
    },
}


def main_keyboard():
    rows = []
    for key, product in PRODUCTS.items():
        if key in ("parser_llm", "omni_creative_v20", "remove_ai_label"):
            continue
        rows.append([InlineKeyboardButton(
            f"{product['title']} · {product['price']:,} ₽".replace(",", " "),
            callback_data=f"product:{key}",
        )])
    rows.append([InlineKeyboardButton("🎁  АКТУАЛЬНЫЕ ПЛЮШКИ  ·  БОНУСЫ", callback_data="perks")])
    rows.append([InlineKeyboardButton("🛍 Другие товары", callback_data="other_products")])
    rows.append([InlineKeyboardButton("🧩 Актуальное расширение Google Flow", url="https://t.me/+Fxcp24v79SwyMjAy")])
    rows.append([InlineKeyboardButton("🔐 Ferixdi VPN", url="https://t.me/ferixdi_vpn_bot")])
    rows.append([InlineKeyboardButton("👥 Чат AI-креаторов", url="https://t.me/ai_neiro_chat")])
    rows.append([
        InlineKeyboardButton("🎨 Бесплатный AI-генератор", url="https://t.me/free_images_ferixdi_bot"),
    ])
    rows.append([
        InlineKeyboardButton("📢 Канал Ferixdi AI", url="https://t.me/ferixdi_ai"),
        InlineKeyboardButton("🆘 Поддержка", url=f"https://t.me/{ADMIN_USERNAME}"),
    ])
    return InlineKeyboardMarkup(rows)


def product_keyboard(key):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Подробнее о товаре", callback_data=f"details:{key}")],
        [InlineKeyboardButton(f"🛒 Купить · {PRODUCTS[key]['price']:,} ₽".replace(",", " "), callback_data=f"buy:{key}")],
        [InlineKeyboardButton("⬅️ В каталог", callback_data="catalog")],
    ])


def detail_keyboard(key):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🛒 Купить · {PRODUCTS[key]['price']:,} ₽".replace(",", " "), callback_data=f"buy:{key}")],
        [InlineKeyboardButton("⬅️ Назад к товару", callback_data=f"product:{key}")],
        [InlineKeyboardButton("🏪 В каталог", callback_data="catalog")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "✦ FERIXDI AI SHOP ✦\n"
        "AI-инструменты • доступы • полезные возможности\n\n"
        "Добро пожаловать! Здесь собраны инструменты для создания AI-контента и практические материалы.\n\n"
        "👇 Выберите интересующий раздел или товар\n"
        "📦 Нажмите на товар — увидите цену и краткое описание\n"
        "📖 Внутри товара есть полные условия\n"
        "🛒 Для оформления нажмите «Купить»\n\n"
        "🎁 Загляните в «Актуальные плюшки» — там бонусы и предложения сервисов"
    )
    await update.effective_message.reply_text(text, reply_markup=main_keyboard())


async def show_catalog(query):
    await query.edit_message_text(
        "✦ FERIXDI AI SHOP ✦\n\n"
        "📦 КАТАЛОГ\n"
        "Выберите товар, чтобы посмотреть описание, цену и условия.\n\n"
        "🎁 Не пропустите бонусы в разделе «Актуальные плюшки».",
        reply_markup=main_keyboard(),
    )


async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data or ""

    if data == "catalog":
        await show_catalog(query)
        return

    if data == "other_products":
        other_text = (
            "🛍 ДРУГИЕ ТОВАРЫ\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Дополнительные материалы и инструменты Ferixdi AI\n\n"
            "📘 Парсер + LLM: 100 сценариев применения\n"
            "100 идей для работы с реальными данными из интернета: тренды, конкуренты, клиенты, цены, контент и анализ аудитории.\n\n"
            "Выберите товар, чтобы посмотреть полное описание и условия покупки."
        )
        other_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("📘 Парсер + LLM · 2 499 ₽", callback_data="product:parser_llm")],
            [InlineKeyboardButton("🚀 OMNI CREATIVE AGENT v20.0 · 2 999 ₽", callback_data="product:omni_creative_v20")],
            [InlineKeyboardButton("🎬 Убираем метку AI-контент · 999 ₽", callback_data="product:remove_ai_label")],
            [InlineKeyboardButton("⬅️ В каталог", callback_data="catalog")],
        ])
        await query.edit_message_text(other_text, reply_markup=other_markup)
        return

    if data == "perks":
        perks_text = (
            "🎁 АКТУАЛЬНЫЕ ПЛЮШКИ · БОНУСЫ\n"
            "Бонусы и предложения для AI-контента\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "① MIORA DESIGN\n"
            "💎 1000 кредитов\n"
            "Для нового аккаунта при первой авторизации.\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "② HAILUO AI\n"
            "💎 3000 кредитов\n"
            "Бонус за скачивание приложения на ПК. Начисление проверьте после установки и входа в аккаунт.\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "③ PICSART PRO\n"
            "♾️ Безлимит WAN до конца месяца\n"
            "Для тарифа Pro, если предложение доступно в вашем аккаунте.\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "💡 Условия и доступность бонусов могут меняться — проверьте их на сайте сервиса перед активацией."
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 MIORA DESIGN", url="https://miora.design/")],
            [InlineKeyboardButton("🌐 HAILUO AI", url="https://hailuoai.video/")],
            [InlineKeyboardButton("🌐 PICSART PRO", url="https://picsart.com/")],
            [InlineKeyboardButton("⬅️ В каталог", callback_data="catalog")],
        ])
        await query.edit_message_text(perks_text, reply_markup=markup, disable_web_page_preview=True)
        return

    action, _, key = data.partition(":")
    product = PRODUCTS.get(key)
    if not product:
        await query.edit_message_text(
            "Похоже, этот раздел уже недоступен.\n\nОткройте каталог и выберите товар ещё раз 👇",
            reply_markup=main_keyboard(),
        )
        return

    if action == "product":
        text = (
            f"✦ {product['title']}\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"💳 Стоимость: {product['price']:,} ₽\n\n"
            f"✨ {product['short']}\n\n"
            "📖 Нажмите «Подробнее о товаре», чтобы открыть полное описание.\n"
            "🛒 Нажмите кнопку покупки — покажем сумму и порядок оплаты."
        ).replace(",", " ")
        await query.edit_message_text(text, reply_markup=product_keyboard(key))
        return

    if action == "details":
        # Split long descriptions to stay safely within Telegram's message limit.
        description = product["description"]
        chunks = [description[i:i + 3800] for i in range(0, len(description), 3800)]
        first = f"📖 {product['title']}\n💰 Цена: {product['price']:,} ₽\n\n".replace(",", " ") + chunks[0]
        await query.edit_message_text(first, reply_markup=detail_keyboard(key) if len(chunks) == 1 else None)
        for i, chunk in enumerate(chunks[1:], start=1):
            markup = detail_keyboard(key) if i == len(chunks) - 1 else None
            await context.bot.send_message(chat_id=query.message.chat_id, text=chunk, reply_markup=markup)
        return

    if action == "buy":
        payment_text = (
            "🛒 ОФОРМЛЕНИЕ ЗАКАЗА\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"📦 {product['title']}\n"
            f"💳 К оплате: {product['price']:,} ₽\n\n"
            "🏦 ОПЛАТА ПО СБП\n"
            f"Банк: {PAYMENT_BANK}\n"
            f"Получатель: {PAYMENT_NAME}\n"
            f"Телефон: {PAYMENT_PHONE}\n\n"
            "📌 КАК ЗАВЕРШИТЬ ПОКУПКУ\n"
            "1. Переведите точную сумму через приложение своего банка.\n"
            "2. Нажмите кнопку ниже и откройте чат с продавцом.\n"
            "3. Отправьте чек или скриншот и дождитесь подтверждения.\n\n"
            "🔐 Доступ или товар выдаётся вручную после проверки оплаты. Нажатие кнопки не подтверждает поступление денег."
        ).replace(",", " ")
        encoded = quote(
            f"Здравствуйте! Я оплатил(а) заказ: {product['title']} — {product['price']} ₽. Сейчас отправлю чек.",
            safe="",
        )
        contact_url = f"https://t.me/{ADMIN_USERNAME}?text={encoded}"
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ ОПЛАТИЛ(А) — ОТПРАВИТЬ ЧЕК", url=contact_url)],
            [InlineKeyboardButton("↩️ Вернуться к товару", callback_data=f"product:{key}")],
            [InlineKeyboardButton("⌂ В каталог", callback_data="catalog")],
        ])
        await query.edit_message_text(payment_text, reply_markup=markup)


async def health(request: web.Request):
    return web.json_response({"ok": True, "service": "ferixdi-ai-shop"})


async def telegram_webhook(request: web.Request):
    expected_secret = request.app["webhook_secret"]
    received_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if not secrets.compare_digest(received_secret, expected_secret):
        raise web.HTTPForbidden(text="Invalid webhook secret")

    try:
        payload = await request.json()
        update = Update.de_json(payload, request.app["telegram_app"].bot)
        await request.app["telegram_app"].process_update(update)
    except Exception:
        log.exception("Failed to process Telegram webhook update")
        raise web.HTTPBadRequest(text="Invalid update")
    return web.Response(text="OK")


async def on_startup(server: web.Application):
    if not BOT_TOKEN:
        raise RuntimeError("Set BOT_TOKEN in Render environment variables.")

    telegram_app = Application.builder().token(BOT_TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("shop", start))
    telegram_app.add_handler(CallbackQueryHandler(callbacks))

    await telegram_app.initialize()
    await telegram_app.start()

    external_url = os.getenv("RENDER_EXTERNAL_URL", "").strip().rstrip("/")
    if not external_url:
        raise RuntimeError(
            "RENDER_EXTERNAL_URL is missing. Deploy this app as a Render Web Service."
        )

    webhook_secret = os.getenv("WEBHOOK_SECRET", "").strip() or secrets.token_urlsafe(32)
    webhook_url = f"{external_url}/telegram"
    await telegram_app.bot.set_webhook(
        url=webhook_url,
        secret_token=webhook_secret,
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=False,
    )

    server["telegram_app"] = telegram_app
    server["webhook_secret"] = webhook_secret
    log.info("Ferixdi AI Shop webhook configured at %s", webhook_url)


async def on_cleanup(server: web.Application):
    telegram_app = server.get("telegram_app")
    if telegram_app:
        await telegram_app.stop()
        await telegram_app.shutdown()


def create_web_app():
    server = web.Application(client_max_size=1024 * 1024)
    server.router.add_get("/", health)
    server.router.add_get("/health", health)
    server.router.add_post("/telegram", telegram_webhook)
    server.on_startup.append(on_startup)
    server.on_cleanup.append(on_cleanup)
    return server


def main():
    log.info("Starting Ferixdi AI Shop as a webhook web service")
    port = int(os.getenv("PORT", "10000"))
    web.run_app(create_web_app(), host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
