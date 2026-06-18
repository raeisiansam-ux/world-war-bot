#صالح میرزایی و استاد محمد و داریوش تیم برنامه نویسی وی ای پی

"""
ربات جنگ جهانی - نسخه نهایی کامل
برای پیام‌رسان بله
"""

import requests
import json
import sqlite3
import time
import random
import threading
from datetime import datetime, timedelta


BOT_TOKEN = "1610685733:rWgWdD7Zyka0PdyDvqKtewTuqFRPRxsd7rM"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}/"
PAYMENT_TOKEN = "توکن پرداخت هم بزن اینجا"
PAYMENT_TEST_TOKEN = "WALLET-TEST-1111111111111111"

# آیدی عددی ادمین اصلی (همیشه دسترسی کامل دارد)
MAIN_ADMIN_ID = 223726163

# کانال و گروه اجباری
FORCE_CHANNEL = "@Mr_TOMAS_CHANEL"
FORCE_GROUP = "@Mr_TOMAS_CHANEL"

# لیست کامل ۱۹۵ کشور
COUNTRIES = [
    "ایران", "آمریکا", "آلمان", "انگلیس", "فرانسه", "روسیه", "چین", "ژاپن",
    "کره جنوبی", "ترکیه", "عربستان", "امارات", "قطر", "مصر", "مراکش", "نیجریه",
    "برزیل", "آرژانتین", "مکزیک", "کانادا", "استرالیا", "هند", "پاکستان",
    "افغانستان", "عراق", "سوریه", "لبنان", "اردن", "لیبی", "سودان", "اتیوپی",
    "کنیا", "غنا", "سنگال", "آفریقای جنوبی", "اسپانیا", "ایتالیا", "هلند",
    "بلژیک", "سوئد", "نروژ", "فنلاند", "دانمارک", "لهستان", "اوکراین", "گرجستان",
    "آذربایجان", "ارمنستان", "قزاقستان", "ازبکستان", "ترکمنستان", "قرقیزستان",
    "تاجیکستان", "اندونزی", "مالزی", "تایلند", "ویتنام", "فیلیپین", "بنگلادش",
    "نپال", "سریلانکا", "نیوزیلند", "پرتغال", "یونان", "بلغارستان", "رومانی",
    "مجارستان", "جمهوری چک", "اسلواکی", "اتریش", "سوئیس", "کرواسی", "صربستان",
    "بوسنی", "اسلوونی", "آلبانی", "مقدونیه", "مونته‌نگرو", "کوزوو", "مولداوی",
    "بلاروس", "لیتوانی", "لتونی", "استونی", "ایسلند", "ایرلند", "موناکو",
    "لوکزامبورگ", "مالت", "قبرس", "شیلی", "پرو", "کلمبیا", "ونزوئلا", "اکوادور",
    "بولیوی", "پاراگوئه", "اروگوئه", "کاستاریکا", "گواتمالا", "هندوراس",
    "السالوادور", "نیکاراگوئه", "پاناما", "کوبا", "جامائیکا", "هائیتی",
    "جمهوری دومینیکن", "پورتوریکو", "باهاما", "ترینیداد", "باربادوس", "آنگولا",
    "موزامبیک", "زامبیا", "زیمبابوه", "مالاوی", "تانزانیا", "اوگاندا", "رواندا",
    "بوروندی", "جیبوتی", "اریتره", "سومالی", "کامرون", "گابن", "چاد", "نیجر",
    "مالی", "موریتانی", "الجزایر", "تونس", "بوتان", "مالدیو", "موریس", "سیشل",
    "فیجی", "پاپوآ گینه نو", "کامبوج", "لائوس", "مغولستان", "کره شمالی",
    "اسرائیل", "فلسطین", "یمن", "عمان", "کویت", "بحرین", "سنگاپور", "برونئی"
]


def init_db():
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS players
                 (user_id INTEGER PRIMARY KEY,
                  country TEXT UNIQUE,
                  phone TEXT,
                  money REAL,
                  coin REAL,
                  diamond REAL,
                  tech_level INTEGER,
                  popularity REAL,
                  last_active TIMESTAMP,
                  is_banned INTEGER DEFAULT 0,
                  total_games INTEGER DEFAULT 0,
                  wins INTEGER DEFAULT 0,
                  join_date TIMESTAMP)''')
    

    c.execute('''CREATE TABLE IF NOT EXISTS buildings
                 (user_id INTEGER,
                  type TEXT,
                  level INTEGER,
                  PRIMARY KEY(user_id, type))''')
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS military
                 (user_id INTEGER,
                  equip_type TEXT,
                  count INTEGER,
                  PRIMARY KEY(user_id, equip_type))''')
    

    c.execute('''CREATE TABLE IF NOT EXISTS alliances
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  from_user INTEGER,
                  to_user INTEGER,
                  status TEXT,
                  message TEXT,
                  timestamp TIMESTAMP)''')
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS ally_messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  from_user INTEGER,
                  to_user INTEGER,
                  message TEXT,
                  timestamp TIMESTAMP,
                  is_read INTEGER DEFAULT 0)''')
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS trades
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  from_user INTEGER,
                  to_user INTEGER,
                  commodity TEXT,
                  amount REAL,
                  price REAL,
                  status TEXT,
                  timestamp TIMESTAMP)''')
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS stock_assets
                 (user_id INTEGER,
                  asset_type TEXT,
                  amount REAL,
                  PRIMARY KEY(user_id, asset_type))''')
    

    c.execute('''CREATE TABLE IF NOT EXISTS bonds
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  bond_type TEXT,
                  amount REAL,
                  start_date TIMESTAMP,
                  end_date TIMESTAMP,
                  interest REAL,
                  status TEXT)''')
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS purchases
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  amount_toman REAL,
                  currency_type TEXT,
                  currency_amount REAL,
                  timestamp TIMESTAMP)''')
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS war_scenarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  from_user INTEGER,
                  from_country TEXT,
                  to_user INTEGER,
                  to_country TEXT,
                  scenario TEXT,
                  status TEXT,
                  result TEXT,
                  timestamp TIMESTAMP)''')
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS support_tickets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  user_country TEXT,
                  subject TEXT,
                  message TEXT,
                  status TEXT,
                  admin_response TEXT,
                  timestamp TIMESTAMP)''')

    c.execute('''CREATE TABLE IF NOT EXISTS admins
                 (user_id INTEGER PRIMARY KEY,
                  name TEXT,
                  permissions TEXT,
                  added_by INTEGER,
                  timestamp TIMESTAMP)''')
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS daily_events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  event_type TEXT,
                  description TEXT,
                  effect TEXT,
                  date DATE)''')
    
    conn.commit()
    conn.close()


def send_message(chat_id, text, keyboard=None):
    """ارسال پیام"""
    url = BASE_URL + "sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        print(f"خطا: {e}")
        return None

def edit_message(chat_id, message_id, text, keyboard=None):
    """ویرایش پیام"""
    url = BASE_URL + "editMessageText"
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    
    try:
        return requests.post(url, json=data, timeout=10).json()
    except:
        return None

def answer_callback(callback_id):
    """پاسخ به callback query"""
    url = BASE_URL + "answerCallbackQuery"
    try:
        requests.post(url, json={"callback_query_id": callback_id}, timeout=5)
    except:
        pass

def request_contact(chat_id):
    """درخواست شماره تماس"""
    keyboard = {
        "keyboard": [
            [{"text": "📱 ارسال شماره تماس", "request_contact": True}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    send_message(chat_id, "📱 **لطفاً شماره تماس خود را ارسال کنید**\n\n"
                         "برای ادامه بازی، نیاز به تأیید شماره تماس داریم.", keyboard)

def check_force_join(chat_id, user_id):
    """بررسی عضویت در کانال"""
    # با توجه به محدودیت‌های API بله، این بخش ساده شده
    return True


def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "🏛️ قلمروی من", "callback_data": "my_realm"}],
            [{"text": "🤝 اتحاد", "callback_data": "alliance"}],
            [{"text": "⚔️ جنگ", "callback_data": "war"}],
            [{"text": "🏬 فروشگاه", "callback_data": "shop"}],
            [{"text": "📈 بازار بورس", "callback_data": "stock"}],
            [{"text": "ℹ️ درباره ما", "callback_data": "about"}],
            [{"text": "🗨️ پشتیبانی", "callback_data": "support"}]
        ]
    }

def realm_menu():
    return {
        "inline_keyboard": [
            [{"text": "💰 خزانه داری", "callback_data": "treasury"}],
            [{"text": "🪖 دارایی نظامی", "callback_data": "military_assets"}],
            [{"text": "💡 دانش و فناوری", "callback_data": "tech"}],
            [{"text": "🙂 رضایت مردمی", "callback_data": "popularity"}],
            [{"text": "🏗️ ساختمان‌ها", "callback_data": "buildings"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_main"}]
        ]
    }

def alliance_menu():
    return {
        "inline_keyboard": [
            [{"text": "🤝 اعلام اتحاد", "callback_data": "declare_alliance"}],
            [{"text": "✉️ مکالمه با متحد", "callback_data": "ally_chat"}],
            [{"text": "💰 ارسال پول", "callback_data": "send_money"}],
            [{"text": "🏭 آغاز تجارت", "callback_data": "start_trade"}],
            [{"text": "📋 لیست متحدان", "callback_data": "allies_list"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_main"}]
        ]
    }

def war_menu():
    return {
        "inline_keyboard": [
            [{"text": "⚔️ اعلام جنگ", "callback_data": "declare_war"}],
            [{"text": "📜 ارسال سناریو", "callback_data": "send_scenario"}],
            [{"text": "👩🏼‍💻 حمله سایبری", "callback_data": "cyber_attack"}],
            [{"text": "📜 تاریخچه جنگ", "callback_data": "war_history"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_main"}]
        ]
    }

def shop_menu():
    return {
        "inline_keyboard": [
            [{"text": "💵 خرید دلار", "callback_data": "buy_dollar"}],
            [{"text": "🪙 خرید سکه", "callback_data": "buy_coin"}],
            [{"text": "💎 خرید الماس", "callback_data": "buy_diamond"}],
            [{"text": "⚔️ خرید تجهیزات", "callback_data": "buy_equipment"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_main"}]
        ]
    }

def equipment_menu():
    return {
        "inline_keyboard": [
            [{"text": "🇺🇸 جنگنده آمریکایی", "callback_data": "fighter_us"}],
            [{"text": "🇷🇺 جنگنده روسی", "callback_data": "fighter_ru"}],
            [{"text": "🇨🇳 جنگنده چینی", "callback_data": "fighter_cn"}],
            [{"text": "🇪🇺 جنگنده اروپایی", "callback_data": "fighter_eu"}],
            [{"text": "🇹🇷 جنگنده ترکیه‌ای", "callback_data": "fighter_tr"}],
            [{"text": "🇯🇵 جنگنده ژاپنی", "callback_data": "fighter_jp"}],
            [{"text": "🇮🇷 جنگنده ایرانی", "callback_data": "fighter_ir"}],
            [{"text": "🇮🇱 جنگنده اسرائیلی", "callback_data": "fighter_il"}],
            [{"text": "🇮🇳 جنگنده هندی", "callback_data": "fighter_in"}],
            [{"text": "🚜 تانک", "callback_data": "tank"}],
            [{"text": "🚀 موشک", "callback_data": "missile"}],
            [{"text": "🚁 بالگرد", "callback_data": "helicopter"}],
            [{"text": "🛸 پهپاد", "callback_data": "drone"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_shop"}]
        ]
    }

def buildings_menu():
    return {
        "inline_keyboard": [
            [{"text": "🏥 بیمارستان", "callback_data": "building_hospital"}],
            [{"text": "🏦 بانک", "callback_data": "building_bank"}],
            [{"text": "🏨 هتل", "callback_data": "building_hotel"}],
            [{"text": "🏫 مدرسه", "callback_data": "building_school"}],
            [{"text": "🎓 دانشگاه", "callback_data": "building_university"}],
            [{"text": "🛢️ پالایشگاه نفت", "callback_data": "building_oil"}],
            [{"text": "🏭 کارخانه تسلیحات", "callback_data": "building_factory"}],
            [{"text": "🏭 کارخانه فولاد", "callback_data": "building_steel"}],
            [{"text": "🏭 کارخانه هواپیما", "callback_data": "building_aircraft"}],
            [{"text": "🛡️ پدافند هوایی", "callback_data": "building_air_defense"}],
            [{"text": "🧱 سنگر", "callback_data": "building_bunker"}],
            [{"text": "📡 رادار", "callback_data": "building_radar"}],
            [{"text": "🌾 مزرعه", "callback_data": "building_farm"}],
            [{"text": "📦 بندر تجاری", "callback_data": "building_port"}],
            [{"text": "🏭 منطقه آزاد", "callback_data": "building_freezone"}],
            [{"text": "☢️ مرکز هسته‌ای", "callback_data": "building_nuclear"}],
            [{"text": "🛰️ پایگاه فضایی", "callback_data": "building_space"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_realm"}]
        ]
    }

def tech_submenu():
    return {
        "inline_keyboard": [
            [{"text": "💡 تحقیق در فناوری", "callback_data": "research_tech"}],
            [{"text": "🛰️ فناوری ماهواره‌ای", "callback_data": "tech_satellite"}],
            [{"text": "🪖 فناوری نظامی", "callback_data": "tech_military"}],
            [{"text": "⛰️ زیست و فناوری", "callback_data": "tech_environment"}],
            [{"text": "🌾 فناوری کشاورزی", "callback_data": "tech_agriculture"}],
            [{"text": "📚 علم و فناوری", "callback_data": "tech_science"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_realm"}]
        ]
    }

def stock_menu():
    return {
        "inline_keyboard": [
            [{"text": "🌍 شاخص‌های جهانی", "callback_data": "stock_indices"}],
            [{"text": "🛢️ کالاهای قابل معامله", "callback_data": "stock_commodities"}],
            [{"text": "🏢 سهام تسلیحاتی", "callback_data": "stock_stocks"}],
            [{"text": "💱 نرخ ارز", "callback_data": "stock_currency"}],
            [{"text": "📜 اوراق قرضه", "callback_data": "stock_bonds"}],
            [{"text": "📊 دارایی من", "callback_data": "stock_assets"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_main"}]
        ]
    }

def support_menu():
    return {
        "inline_keyboard": [
            [{"text": "🪄 ارسال ایده", "callback_data": "send_idea"}],
            [{"text": "🐛 گزارش باگ", "callback_data": "report_bug"}],
            [{"text": "💵 مشکل خرید", "callback_data": "payment_issue"}],
            [{"text": "🤝 اعلام همکاری", "callback_data": "cooperation"}],
            [{"text": "📖 دفترچه راهنما", "callback_data": "guide"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_main"}]
        ]
    }

# ==================== اطلاعات تجهیزات ====================
FIGHTERS = {
    "us": [
        {"name": "F-15 Eagle", "price": 100_000_000, "attack": 85, "defense": 80},
        {"name": "F-14 Tomcat", "price": 38_000_000, "attack": 75, "defense": 70},
        {"name": "F-22 Raptor", "price": 150_000_000, "attack": 98, "defense": 95},
        {"name": "F-18 Super Hornet", "price": 70_000_000, "attack": 82, "defense": 78}
    ],
    "ru": [
        {"name": "Su-57", "price": 55_000_000, "attack": 90, "defense": 85},
        {"name": "Su-35", "price": 60_000_000, "attack": 85, "defense": 82},
        {"name": "MiG-29", "price": 30_000_000, "attack": 70, "defense": 65},
        {"name": "MiG-31", "price": 15_000_000, "attack": 65, "defense": 60}
    ],
    "cn": [
        {"name": "J-10", "price": 40_000_000, "attack": 72, "defense": 68},
        {"name": "J-16", "price": 50_000_000, "attack": 78, "defense": 74},
        {"name": "J-20", "price": 110_000_000, "attack": 88, "defense": 85}
    ],
    "eu": [
        {"name": "Eurofighter Typhoon", "price": 90_000_000, "attack": 86, "defense": 84},
        {"name": "Rafale", "price": 120_000_000, "attack": 89, "defense": 87},
        {"name": "Gripen", "price": 60_000_000, "attack": 80, "defense": 78}
    ],
    "tr": [
        {"name": "KAAN", "price": 100_000_000, "attack": 82, "defense": 80}
    ],
    "jp": [
        {"name": "F-2", "price": 120_000_000, "attack": 84, "defense": 82}
    ],
    "ir": [
        {"name": "صاعقه", "price": 8_000_000, "attack": 50, "defense": 45},
        {"name": "کوثر", "price": 10_000_000, "attack": 55, "defense": 50},
        {"name": "آذرخش", "price": 9_000_000, "attack": 52, "defense": 48}
    ],
    "il": [
        {"name": "کفیر", "price": 5_000_000, "attack": 48, "defense": 45}
    ],
    "in": [
        {"name": "Tejas MK1A", "price": 35_000_000, "attack": 68, "defense": 65},
        {"name": "Tejas MK2", "price": 50_000_000, "attack": 75, "defense": 72}
    ]
}

TANKS = [
    {"name": "M1 Abrams", "price": 8_000_000, "attack": 85, "defense": 90},
    {"name": "T-90", "price": 4_500_000, "attack": 80, "defense": 85},
    {"name": "Leopard 2", "price": 7_000_000, "attack": 88, "defense": 88},
    {"name": "Challenger 2", "price": 8_500_000, "attack": 82, "defense": 92},
    {"name": "Type 99", "price": 3_500_000, "attack": 78, "defense": 82}
]

MISSILES = [
    {"name": "موشک بالستیک", "price": 2_000_000, "attack": 95, "range": 3000},
    {"name": "موشک کروز", "price": 1_500_000, "attack": 90, "range": 2500},
    {"name": "موشک ضد هوایی", "price": 500_000, "attack": 85, "range": 200}
]

HELICOPTERS = [
    {"name": "AH-64 Apache", "price": 20_000_000, "attack": 88, "defense": 75},
    {"name": "Mi-28 Havoc", "price": 15_000_000, "attack": 85, "defense": 72},
    {"name": "Ka-52 Alligator", "price": 16_000_000, "attack": 86, "defense": 73}
]

DRONES = [
    {"name": "MQ-9 Reaper", "price": 30_000_000, "attack": 82, "defense": 60},
    {"name": "Bayraktar TB2", "price": 5_000_000, "attack": 70, "defense": 55},
    {"name": "Shahed 136", "price": 20_000, "attack": 60, "defense": 40}
]

# ==================== اطلاعات ساختمان‌ها ====================
BUILDINGS_DATA = {
    "hospital": {"name": "🏥 بیمارستان", "cost": [5_000_000, 20_000_000, 100_000_000], 
                 "effect": ["ظرفیت ۵۰۰ نفر", "ظرفیت ۵۰۰۰ نفر", "ظرفیت ۲۰۰۰۰ نفر + کاهش ۵۰% مرگ"], "tech_req": [1, 2, 3]},
    "bank": {"name": "🏦 بانک", "cost": [10_000_000, 50_000_000, 200_000_000],
             "effect": ["سود ۰.۲% روزانه", "سود ۰.۵% + وام ۵۰۰M", "سود ۱% + ضرب سکه"], "tech_req": [1, 2, 3]},
    "hotel": {"name": "🏨 هتل", "cost": [3_000_000, 15_000_000, 75_000_000],
              "effect": ["۵۰k دلار/روز", "۲۵۰k دلار/روز", "۱M دلار/روز + سرمایه‌گذار"], "tech_req": [1, 1, 2]},
    "school": {"name": "🏫 مدرسه", "cost": [2_000_000, 10_000_000, 50_000_000],
               "effect": ["پوشش ۳۰% کودکان", "پوشش ۶۰% کودکان", "پوشش ۹۵% کودکان"], "tech_req": [1, 1, 2]},
    "university": {"name": "🎓 دانشگاه", "cost": [15_000_000, 60_000_000, 250_000_000],
                   "effect": ["۱ نقطه تحقیق/روز", "۳ نقطه تحقیق + آزمایشگاه", "۸ نقطه تحقیق + پروژه فضایی"], "tech_req": [2, 3, 4]},
    "oil_refinery": {"name": "🛢️ پالایشگاه نفت", "cost": [30_000_000, 100_000_000, 500_000_000],
                     "effect": ["۵M دلار/روز", "۲۰M دلار/روز", "۸۰M دلار/روز"], "tech_req": [2, 2, 3]},
    "factory": {"name": "🏭 کارخانه تسلیحات", "cost": [20_000_000, 80_000_000, 300_000_000],
                "effect": ["۱۰ تانک/روز", "۵۰ تانک/روز", "۲۰۰ تانک/روز"], "tech_req": [2, 3, 4]},
    "steel_factory": {"name": "🏭 کارخانه فولاد", "cost": [15_000_000, 60_000_000, 250_000_000],
                      "effect": ["کاهش ۱۰% هزینه ساخت", "کاهش ۲۰% هزینه ساخت", "کاهش ۳۰% هزینه ساخت"], "tech_req": [2, 3, 4]},
    "aircraft_factory": {"name": "🏭 کارخانه هواپیما", "cost": [50_000_000, 200_000_000, 800_000_000],
                         "effect": ["تولید جنگنده با ۲۰% تخفیف", "تولید با ۳۰% تخفیف", "تولید با ۴۰% تخفیف"], "tech_req": [3, 4, 5]},
    "air_defense": {"name": "🛡️ پدافند هوایی", "cost": [25_000_000, 100_000_000, 400_000_000],
                    "effect": ["۲۰% شانس ساقط کردن", "۴۰% شانس", "۶۰% شانس"], "tech_req": [2, 3, 4]},
    "bunker": {"name": "🧱 سنگر", "cost": [10_000_000, 40_000_000, 150_000_000],
               "effect": ["ذخیره ۵۰ سرباز", "ذخیره ۲۰۰ سرباز", "ذخیره ۵۰۰ سرباز"], "tech_req": [1, 2, 3]},
    "radar": {"name": "📡 رادار", "cost": [15_000_000, 60_000_000, 250_000_000],
              "effect": ["هشدار ۱۰ دقیقه قبل", "هشدار ۲۰ دقیقه قبل", "هشدار ۳۰ دقیقه قبل"], "tech_req": [2, 3, 4]},
    "farm": {"name": "🌾 مزرعه", "cost": [1_000_000, 5_000_000, 20_000_000],
             "effect": ["تغذیه ۱۰% مردم", "تغذیه ۳۰% مردم", "تغذیه ۷۰% + صادرات"], "tech_req": [1, 1, 2]},
    "port": {"name": "📦 بندر تجاری", "cost": [25_000_000, 100_000_000, 400_000_000],
             "effect": ["+۲۰% درآمد تجارت", "+۳۵% درآمد تجارت", "+۵۰% درآمد تجارت"], "tech_req": [2, 3, 4]},
    "freezone": {"name": "🏭 منطقه آزاد", "cost": [50_000_000, 200_000_000, 800_000_000],
                 "effect": ["-۱۰% قیمت فروشگاه", "-۱۵% قیمت", "-۲۰% قیمت + سرمایه‌گذار"], "tech_req": [3, 4, 5]},
    "nuclear": {"name": "☢️ مرکز هسته‌ای", "cost": [500_000_000, 2_000_000_000, 10_000_000_000],
                "effect": ["قابلیت ساخت بمب اتم", "موشک هسته‌ای", "پیشرفته"], "tech_req": [5, 6, 7]},
    "space": {"name": "🛰️ پایگاه فضایی", "cost": [300_000_000, 1_000_000_000, 5_000_000_000],
              "effect": ["ماهواره ساده", "ماهواره جاسوسی", "ماهواره پیشرفته"], "tech_req": [4, 5, 6]}
}

# ==================== بسته‌های خرید ====================
DOLLAR_PACKS = [
    {"amount": 1_000_000_000, "price": 30_000},
    {"amount": 3_000_000_000, "price": 60_000},
    {"amount": 5_000_000_000, "price": 90_000},
    {"amount": 8_000_000_000, "price": 270_000},
    {"amount": 10_000_000_000, "price": 810_000},
    {"amount": 20_000_000_000, "price": 2_000_000},
    {"amount": 30_000_000_000, "price": 3_000_000}
]

COIN_PACKS = [
    {"amount": 100_000_000, "price": 53_000},
    {"amount": 300_000_000, "price": 76_000},
    {"amount": 500_000_000, "price": 136_000},
    {"amount": 800_000_000, "price": 167_000},
    {"amount": 1_000_000_000, "price": 173_000},
    {"amount": 2_000_000_000, "price": 430_000}
]

DIAMOND_PACKS = [
    {"amount": 1000, "price": 37_000},
    {"amount": 3000, "price": 53_000},
    {"amount": 4000, "price": 123_000},
    {"amount": 5000, "price": 148_000},
    {"amount": 8000, "price": 169_000},
    {"amount": 10_000, "price": 254_000},
    {"amount": 15_000, "price": 270_000},
    {"amount": 20_000, "price": 312_000}
]

# ==================== بازار بورس ====================
COMMODITIES = {
    "oil": {"name": "🛢️ نفت", "price": 80.0, "change": 3, "trend": "up", "max": 20000},
    "gold": {"name": "🪙 طلا", "price": 1900.0, "change": -1, "trend": "down", "max": 5000},
    "wheat": {"name": "🌾 گندم", "price": 350.0, "change": 2, "trend": "up", "max": 50000},
    "copper": {"name": "⛏️ مس", "price": 4.20, "change": -0.5, "trend": "down", "max": 100000},
    "uranium": {"name": "🚀 اورانیوم", "price": 120.0, "change": 8, "trend": "up", "max": 5000}
}

STOCKS = {
    "lockheed": {"name": "لاکهید مارتین 🇺🇸", "price": 450.0, "change": 10, "dividend": 0.05},
    "boeing": {"name": "بوئینگ 🇺🇸", "price": 280.0, "change": -3, "dividend": 0.03},
    "roe": {"name": "روسوبورون اکسپورت 🇷🇺", "price": 120.0, "change": 20, "dividend": 0.02},
    "northrop": {"name": "نورتروپ گرومن 🇺🇸", "price": 520.0, "change": 12, "dividend": 0.04},
    "dassault": {"name": "Dassault 🇪🇺", "price": 320.0, "change": -1, "dividend": 0.045}
}

BONDS = [
    {"name": "اسناد خزانه", "days": 30, "interest": 8, "min": 10_000_000},
    {"name": "اوراق قرضه جنگی", "days": 15, "interest": 15, "min": 50_000_000},
    {"name": "اوراق توسعه ملی", "days": 60, "interest": 12, "min": 20_000_000}
]

# متغیرهای موقت
temp_data = {}
temp_purchase = {}
country_page = 0

# ==================== دستورات اصلی ====================
def start_command(chat_id, user_id):
    if not check_force_join(chat_id, user_id):
        return
    
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM players WHERE user_id=?", (user_id,))
    player = c.fetchone()
    
    if player:
        if player[9] == 1:  # is_banned
            send_message(chat_id, "🚫 شما از بازی مسدود شده‌اید!")
        else:
            c.execute("UPDATE players SET last_active=? WHERE user_id=?", (datetime.now(), user_id))
            conn.commit()
            send_message(chat_id, f"✨ **خوش برگشتی {player[1]}!**\n\n💰 موجودی: {player[3]:,.0f} دلار\n🙂 رضایت: {player[7]}%\n💡 تکنولوژی: سطح {player[6]}", main_menu())
    else:
        # درخواست شماره تماس
        request_contact(chat_id)
        temp_data[user_id] = {"waiting": "phone"}
    
    conn.close()

def save_phone_and_select_country(chat_id, user_id, phone):
    """ذخیره شماره و نمایش کشورها"""
    temp_data[user_id] = {"phone": phone, "waiting": "country"}
    show_countries_list(chat_id, user_id, 0)

def show_countries_list(chat_id, user_id, page):
    """نمایش کشورها با صفحه‌بندی"""
    items_per_page = 10
    total_pages = (len(COUNTRIES) + items_per_page - 1) // items_per_page
    start = page * items_per_page
    end = min(start + items_per_page, len(COUNTRIES))
    
    countries_page = COUNTRIES[start:end]
    
    keyboard = {"inline_keyboard": []}
    
    for country in countries_page:
        keyboard["inline_keyboard"].append([{"text": country, "callback_data": f"select_{country}"}])
    
    # دکمه‌های صفحه‌بندی
    nav_buttons = []
    if page > 0:
        nav_buttons.append({"text": "⬅️ قبلی", "callback_data": f"country_page_{page-1}"})
    if page < total_pages - 1:
        nav_buttons.append({"text": "بعدی ➡️", "callback_data": f"country_page_{page+1}"})
    
    if nav_buttons:
        keyboard["inline_keyboard"].append(nav_buttons)
    
    keyboard["inline_keyboard"].append([{"text": "📋 مشاهده همه (۱۹۵ کشور)", "callback_data": "show_all_countries"}])
    
    send_message(chat_id, 
                 f"🌍 **مرحله ۲: انتخاب کشور**\n\n"
                 f"📞 شماره شما ثبت شد.\n\n"
                 f"⚠️ **توجه مهم:** پس از انتخاب کشور، دیگر نمی‌توانید آن را تغییر دهید!\n\n"
                 f"📋 صفحه {page+1} از {total_pages} - {len(COUNTRIES)} کشور:\n"
                 f"کشور خود را انتخاب کنید:", keyboard)

def select_country(chat_id, user_id, country):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    # بررسی تکراری نبودن کشور
    c.execute("SELECT * FROM players WHERE country=?", (country,))
    existing = c.fetchone()
    
    if existing:
        send_message(chat_id, f"⚠️ کشور **{country}** قبلاً توسط بازیکن دیگری انتخاب شده است!\nلطفاً کشور دیگری انتخاب کنید.")
    else:
        phone = temp_data.get(user_id, {}).get("phone", "")
        # ایجاد بازیکن جدید
        c.execute("INSERT INTO players (user_id, country, phone, money, coin, diamond, tech_level, popularity, last_active, join_date) VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (user_id, country, phone, 10_000_000, 0, 0, 1, 70.0, datetime.now(), datetime.now()))
        
        # ساختمان‌های اولیه
        for building in ["hospital", "school", "bank", "farm", "oil_refinery"]:
            c.execute("INSERT INTO buildings (user_id, type, level) VALUES (?,?,1)", (user_id, building))
        
        # سهام اولیه تصادفی
        stock_keys = list(STOCKS.keys())
        random_stock = random.choice(stock_keys)
        c.execute("INSERT INTO stock_assets (user_id, asset_type, amount) VALUES (?,?,?)",
                  (user_id, f"stock_{random_stock}", 100))
        
        conn.commit()
        
        if user_id in temp_data:
            del temp_data[user_id]
        
        send_message(chat_id, 
                     f"🎉 **تبریک!** شما کشور **{country}** را انتخاب کردید!\n\n"
                     f"💰 **دارایی اولیه:**\n"
                     f"• {10_000_000:,} دلار بازی\n"
                     f"🙂 **رضایت مردمی:** ۷۰%\n"
                     f"💡 **سطح تکنولوژی:** ۱\n"
                     f"📈 **سهام اولیه:** ۱۰۰ سهم از {STOCKS[random_stock]['name']}\n\n"
                     f"🏛️ **ساختمان‌های اولیه:**\n"
                     f"• بیمارستان سطح ۱\n• مدرسه سطح ۱\n• بانک سطح ۱\n• مزرعه سطح ۱\n• پالایشگاه نفت سطح ۱\n\n"
                     f"⚡️ از منوی اصلی بازی را شروع کنید!", main_menu())
    
    conn.close()

# ==================== قلمروی من ====================
def treasury(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT money, coin, diamond FROM players WHERE user_id=?", (user_id,))
    money, coin, diamond = c.fetchone()
    
    # محاسبه سود روزانه از بانک
    c.execute("SELECT level FROM buildings WHERE user_id=? AND type='bank'", (user_id,))
    bank = c.fetchone()
    bank_interest = 0
    if bank:
        rates = {1: 0.002, 2: 0.005, 3: 0.01}
        bank_interest = money * rates.get(bank[0], 0)
    
    # محاسبه درآمد از ساختمان‌ها
    daily_income = 0
    c.execute("SELECT type, level FROM buildings WHERE user_id=?", (user_id,))
    buildings = c.fetchall()
    for b_type, level in buildings:
        if b_type == "hotel":
            incomes = {1: 50_000, 2: 250_000, 3: 1_000_000}
            daily_income += incomes.get(level, 0)
        elif b_type == "oil_refinery":
            incomes = {1: 5_000_000, 2: 20_000_000, 3: 80_000_000}
            daily_income += incomes.get(level, 0)
    
    text = f"💰 **خزانه داری**\n\n"
    text += f"💵 **دلار بازی:** {money:,.0f}\n"
    text += f"🪙 **سکه:** {coin:,.0f} (حداکثر ۴ میلیارد)\n"
    text += f"💎 **الماس:** {diamond:,.0f} (حداکثر ۲۵,۰۰۰)\n\n"
    
    if bank_interest > 0:
        text += f"🏦 **سود روزانه بانک:** +{bank_interest:,.0f} دلار\n"
    if daily_income > 0:
        text += f"🏨 **درآمد روزانه:** +{daily_income:,.0f} دلار\n"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "🏦 دریافت سود بانکی", "callback_data": "collect_interest"}],
            [{"text": "🏦 دریافت وام", "callback_data": "get_loan"}],
            [{"text": "💰 تبدیل ارز", "callback_data": "convert_currency"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_realm"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)
    conn.close()

def collect_interest(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT money FROM players WHERE user_id=?", (user_id,))
    money = c.fetchone()[0]
    
    c.execute("SELECT level FROM buildings WHERE user_id=? AND type='bank'", (user_id,))
    bank = c.fetchone()
    
    if bank:
        rates = {1: 0.002, 2: 0.005, 3: 0.01}
        interest = money * rates.get(bank[0], 0)
        
        if interest > 0:
            c.execute("UPDATE players SET money = money + ? WHERE user_id=?", (interest, user_id))
            conn.commit()
            send_message(chat_id, f"✅ **{interest:,.0f} دلار** سود بانکی به حساب شما اضافه شد!")
        else:
            send_message(chat_id, "❌ سودی برای دریافت وجود ندارد.")
    else:
        send_message(chat_id, "❌ شما بانک ندارید! ابتدا بانک بسازید.")
    
    conn.close()
    treasury(chat_id, user_id)

def get_loan(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT level FROM buildings WHERE user_id=? AND type='bank'", (user_id,))
    bank = c.fetchone()
    
    if bank and bank[0] >= 2:
        loan_amounts = {2: 500_000_000, 3: 2_000_000_000}
        max_loan = loan_amounts.get(bank[0], 500_000_000)
        
        keyboard = {
            "inline_keyboard": [
                [{"text": f"💰 دریافت وام {max_loan:,.0f} دلار", "callback_data": f"take_loan_{max_loan}"}],
                [{"text": "🔙 بازگشت", "callback_data": "treasury"}]
            ]
        }
        send_message(chat_id, f"🏦 **وام بانکی**\n\n"
                             f"حداکثر وام: **{max_loan:,.0f} دلار**\n"
                             f"نرخ بازپرداخت: ۲۰٪ سود\n"
                             f"مدت بازپرداخت: ۳۰ روز", keyboard)
    else:
        send_message(chat_id, "❌ برای دریافت وام به بانک سطح ۲ یا بالاتر نیاز دارید!")
    
    conn.close()

def take_loan(chat_id, user_id, amount):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("UPDATE players SET money = money + ? WHERE user_id=?", (amount, user_id))
    conn.commit()
    conn.close()
    
    send_message(chat_id, f"✅ **وام {amount:,.0f} دلار** به حساب شما اضافه شد!")
    treasury(chat_id, user_id)

def convert_currency(chat_id, user_id):
    keyboard = {
        "inline_keyboard": [
            [{"text": "💵 دلار → 🪙 سکه", "callback_data": "convert_dollar_coin"}],
            [{"text": "💵 دلار → 💎 الماس", "callback_data": "convert_dollar_diamond"}],
            [{"text": "🪙 سکه → 💎 الماس", "callback_data": "convert_coin_diamond"}],
            [{"text": "🔙 بازگشت", "callback_data": "treasury"}]
        ]
    }
    send_message(chat_id, "💱 **تبدیل ارز**\n\nلطفاً نوع تبدیل را انتخاب کنید:", keyboard)

def military_assets(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT equip_type, count FROM military WHERE user_id=?", (user_id,))
    items = c.fetchall()
    
    total_power = 0
    if items:
        text = "🪖 **دارایی نظامی**\n\n"
        for item in items:
            text += f"• **{item[0]}:** {item[1]:,} دستگاه\n"
            if any(x in item[0] for x in ["F-", "Su-", "J-", "MiG"]):
                total_power += item[1] * 85
            elif "تانک" in item[0]:
                total_power += item[1] * 70
            elif "موشک" in item[0]:
                total_power += item[1] * 95
        text += f"\n📊 **قدرت نظامی:** {total_power:,.0f}"
    else:
        text = "🪖 **دارایی نظامی**\n\nشما هیچ تجهیزاتی ندارید!"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "⚔️ خرید تجهیزات", "callback_data": "buy_equipment"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_realm"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)
    conn.close()

def show_popularity(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT popularity FROM players WHERE user_id=?", (user_id,))
    popularity = c.fetchone()[0]
    
    # عوامل مؤثر
    factors = []
    new_popularity = popularity
    
    c.execute("SELECT level FROM buildings WHERE user_id=? AND type='hospital'", (user_id,))
    hospital = c.fetchone()
    if hospital:
        new_popularity += hospital[0] * 2
        factors.append(f"🏥 بیمارستان سطح {hospital[0]}: +{hospital[0]*2}%")
    else:
        new_popularity -= 10
        factors.append("⚠️ بدون بیمارستان: -10%")
    
    c.execute("SELECT level FROM buildings WHERE user_id=? AND type='school'", (user_id,))
    school = c.fetchone()
    if school:
        new_popularity += school[0] * 1.5
        factors.append(f"🏫 مدرسه سطح {school[0]}: +{school[0]*1.5}%")
    
    c.execute("SELECT level FROM buildings WHERE user_id=? AND type='farm'", (user_id,))
    farm = c.fetchone()
    if farm:
        new_popularity += farm[0] * 2
        factors.append(f"🌾 مزرعه سطح {farm[0]}: +{farm[0]*2}%")
    else:
        new_popularity -= 15
        factors.append("⚠️ بدون مزرعه: -15%")
    
    new_popularity = max(0, min(100, new_popularity))
    c.execute("UPDATE players SET popularity = ? WHERE user_id=?", (new_popularity, user_id))
    conn.commit()
    
    text = f"🙂 **رضایت مردمی**\n\n"
    text += f"📊 **وضعیت فعلی:** {new_popularity:.1f}%\n\n"
    
    if new_popularity >= 80:
        text += "🌟 **عالی!** مردم از شما حمایت می‌کنند.\n"
    elif new_popularity >= 60:
        text += "👍 **خوب.** مردم نسبتاً راضی هستند.\n"
    elif new_popularity >= 40:
        text += "😐 **متوسط.** باید بهبود ببخشید.\n"
    else:
        text += "⚠️ **بحرانی!** احتمال کودتا!\n"
    
    text += f"\n**عوامل مؤثر:**\n"
    for factor in factors:
        text += f"• {factor}\n"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "🏗️ ساخت/ارتقای ساختمان", "callback_data": "buildings"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_realm"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)
    conn.close()

def tech_menu_func(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT tech_level FROM players WHERE user_id=?", (user_id,))
    tech_level = c.fetchone()[0]
    
    c.execute("SELECT level FROM buildings WHERE user_id=? AND type='university'", (user_id,))
    university = c.fetchone()
    uni_level = university[0] if university else 0
    
    research_points = [0, 1, 3, 8][uni_level] if uni_level <= 3 else 0
    
    text = f"💡 **دانش و فناوری**\n\n"
    text += f"📊 **سطح تکنولوژی:** {tech_level}\n"
    text += f"🎓 **دانشگاه سطح:** {uni_level}\n"
    text += f"🔬 **نقاط تحقیق روزانه:** {research_points}\n\n"
    
    text += f"**🔓 فناوری‌ها:**\n"
    techs = [
        {"name": "🛰️ ماهواره‌ای", "level": 3, "desc": "پرتاب ماهواره جاسوسی"},
        {"name": "💻 سایبری", "level": 4, "desc": "حمله سایبری"},
        {"name": "🪖 نظامی نسل ۵", "level": 5, "desc": "جنگنده پیشرفته"},
        {"name": "🌾 کشاورزی", "level": 2, "desc": "+۵۰% تولید غذا"},
        {"name": "🏥 پزشکی", "level": 3, "desc": "کاهش مرگ در جنگ"},
        {"name": "☢️ هسته‌ای", "level": 8, "desc": "ساخت بمب اتم"}
    ]
    
    for tech in techs:
        if tech_level >= tech["level"]:
            status = "✅"
        else:
            status = f"🔒 نیاز به سطح {tech['level']}"
        text += f"{status} **{tech['name']}**\n   {tech['desc']}\n"
    
    send_message(chat_id, text, tech_submenu())
    conn.close()

# ==================== ساختمان‌ها ====================
def buildings_menu_func(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    text = "🏗️ **ساختمان‌های کشور**\n\n"
    
    for key, building in list(BUILDINGS_DATA.items())[:10]:
        c.execute("SELECT level FROM buildings WHERE user_id=? AND type=?", (user_id, key))
        current = c.fetchone()
        level = current[0] if current else 0
        
        if level == 0:
            status = "❌ ساخته نشده"
        elif level < 3:
            status = f"سطح {level}"
        else:
            status = f"سطح {level} (حداکثر)"
        
        text += f"{building['name']}: {status}\n"
        text += f"   ✨ {building['effect'][min(level, 2)]}\n"
    
    send_message(chat_id, text, buildings_menu())
    conn.close()

def show_building(chat_id, user_id, building_type):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT level FROM buildings WHERE user_id=? AND type=?", (user_id, building_type))
    current = c.fetchone()
    current_level = current[0] if current else 0
    
    c.execute("SELECT money, tech_level FROM players WHERE user_id=?", (user_id,))
    money, tech_level = c.fetchone()
    
    building = BUILDINGS_DATA[building_type]
    
    text = f"**{building['name']}**\n\n"
    text += f"📊 **سطح فعلی:** {current_level}\n\n"
    
    upgrade_buttons = []
    
    for i, (cost, effect, tech_req) in enumerate(zip(building["cost"], building["effect"], building["tech_req"]), 1):
        if current_level >= i:
            text += f"✅ **سطح {i}:** {effect}\n"
        elif tech_level >= tech_req:
            text += f"📈 **سطح {i}:** {effect}\n"
            text += f"   💰 هزینه: {cost:,} دلار\n"
            if current_level == i - 1:
                upgrade_buttons.append({
                    "text": f"⬆️ ارتقا به سطح {i} ({cost:,} دلار)",
                    "callback_data": f"upgrade_{building_type}_{i}_{cost}"
                })
        else:
            text += f"🔒 **سطح {i}:** نیاز به تکنولوژی سطح {tech_req}\n"
    
    keyboard = {"inline_keyboard": []}
    for btn in upgrade_buttons:
        keyboard["inline_keyboard"].append([btn])
    keyboard["inline_keyboard"].append([{"text": "🔙 بازگشت", "callback_data": "buildings"}])
    
    send_message(chat_id, text, keyboard)
    conn.close()

def upgrade_building(chat_id, user_id, building_type, new_level, cost):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT money FROM players WHERE user_id=?", (user_id,))
    money = c.fetchone()[0]
    
    if money >= cost:
        c.execute("UPDATE players SET money = money - ? WHERE user_id=?", (cost, user_id))
        c.execute("INSERT OR REPLACE INTO buildings (user_id, type, level) VALUES (?,?,?)",
                  (user_id, building_type, new_level))
        conn.commit()
        send_message(chat_id, f"✅ **{BUILDINGS_DATA[building_type]['name']}** به سطح {new_level} ارتقا یافت!")
    else:
        send_message(chat_id, f"❌ پول کافی ندارید!\n💰 هزینه: {cost:,} دلار\n💵 موجودی: {money:,} دلار")
    
    conn.close()
    show_building(chat_id, user_id, building_type)

# ==================== فروشگاه و خرید ====================
def buy_equipment_menu_func(chat_id):
    send_message(chat_id, "⚔️ **خرید تجهیزات نظامی**\n\nلطفاً دسته تجهیزات را انتخاب کنید:", equipment_menu())

def show_fighters(chat_id, country_code, title):
    fighters = FIGHTERS.get(country_code, [])
    if not fighters:
        send_message(chat_id, "❌ جنگنده‌ای یافت نشد.")
        return
    
    text = f"🛫 **{title}**\n\n"
    buttons = []
    
    for fighter in fighters:
        text += f"• **{fighter['name']}**\n"
        text += f"   💰 قیمت: {fighter['price']:,} دلار\n"
        text += f"   ⚔️ حمله: {fighter['attack']} | 🛡️ دفاع: {fighter['defense']}\n\n"
        buttons.append({
            "text": f"خرید {fighter['name']} - {fighter['price']:,} دلار",
            "callback_data": f"buy_fighter_{fighter['name'].replace(' ', '_')}_{fighter['price']}"
        })
    
    buttons.append({"text": "🔙 بازگشت", "callback_data": "buy_equipment"})
    keyboard = {"inline_keyboard": [[b] for b in buttons]}
    send_message(chat_id, text, keyboard)

def show_tanks(chat_id):
    text = "🚜 **تانک‌ها**\n\n"
    buttons = []
    for tank in TANKS:
        text += f"• **{tank['name']}**\n"
        text += f"   💰 قیمت: {tank['price']:,} دلار\n"
        text += f"   ⚔️ حمله: {tank['attack']} | 🛡️ دفاع: {tank['defense']}\n\n"
        buttons.append({
            "text": f"خرید {tank['name']} - {tank['price']:,} دلار",
            "callback_data": f"buy_tank_{tank['name'].replace(' ', '_')}_{tank['price']}"
        })
    buttons.append({"text": "🔙 بازگشت", "callback_data": "buy_equipment"})
    keyboard = {"inline_keyboard": [[b] for b in buttons]}
    send_message(chat_id, text, keyboard)

def show_missiles(chat_id):
    text = "🚀 **موشک‌ها**\n\n"
    buttons = []
    for missile in MISSILES:
        text += f"• **{missile['name']}**\n"
        text += f"   💰 قیمت: {missile['price']:,} دلار\n"
        text += f"   ⚔️ حمله: {missile['attack']} | 📡 برد: {missile['range']}km\n\n"
        buttons.append({
            "text": f"خرید {missile['name']} - {missile['price']:,} دلار",
            "callback_data": f"buy_missile_{missile['name'].replace(' ', '_')}_{missile['price']}"
        })
    buttons.append({"text": "🔙 بازگشت", "callback_data": "buy_equipment"})
    keyboard = {"inline_keyboard": [[b] for b in buttons]}
    send_message(chat_id, text, keyboard)

def buy_item(chat_id, user_id, item_name, price):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT money FROM players WHERE user_id=?", (user_id,))
    money = c.fetchone()[0]
    
    if money >= price:
        c.execute("UPDATE players SET money = money - ? WHERE user_id=?", (price, user_id))
        c.execute("INSERT INTO military (user_id, equip_type, count) VALUES (?,?,1) "
                  "ON CONFLICT(user_id, equip_type) DO UPDATE SET count = count + 1",
                  (user_id, item_name))
        conn.commit()
        send_message(chat_id, f"✅ **{item_name}** خریداری شد!\n💰 هزینه: {price:,} دلار")
    else:
        send_message(chat_id, f"❌ پول کافی ندارید!\n💰 قیمت: {price:,} دلار\n💵 موجودی: {money:,} دلار")
    
    conn.close()

# ==================== پرداخت ====================
def buy_dollar_menu(chat_id):
    buttons = []
    for pack in DOLLAR_PACKS:
        buttons.append([{
            "text": f"💲{pack['amount']:,} دلار ⬅️ {pack['price']:,} تومان",
            "callback_data": f"pay_dollar_{pack['amount']}_{pack['price']}"
        }])
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "back_shop"}])
    
    keyboard = {"inline_keyboard": buttons}
    send_message(chat_id, "💰 **خرید دلار بازی**\n\nلطفاً بسته را انتخاب کنید:", keyboard)

def buy_coin_menu(chat_id):
    buttons = []
    for pack in COIN_PACKS:
        buttons.append([{
            "text": f"🪙{pack['amount']:,} سکه ⬅️ {pack['price']:,} تومان",
            "callback_data": f"pay_coin_{pack['amount']}_{pack['price']}"
        }])
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "back_shop"}])
    
    keyboard = {"inline_keyboard": buttons}
    send_message(chat_id, "🪙 **خرید سکه بازی** (حداکثر ۴ میلیارد)\n\nلطفاً بسته را انتخاب کنید:", keyboard)

def buy_diamond_menu(chat_id):
    buttons = []
    for pack in DIAMOND_PACKS:
        buttons.append([{
            "text": f"💎{pack['amount']:,} الماس ⬅️ {pack['price']:,} تومان",
            "callback_data": f"pay_diamond_{pack['amount']}_{pack['price']}"
        }])
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "back_shop"}])
    
    keyboard = {"inline_keyboard": buttons}
    send_message(chat_id, "💎 **خرید الماس بازی** (حداکثر ۲۵,۰۰۰)\n\nلطفاً بسته را انتخاب کنید:", keyboard)

def create_payment(chat_id, user_id, amount_toman, currency_type, currency_amount):
    """ایجاد درخواست پرداخت با روش صحیح"""
    url = BASE_URL + "sendInvoice"
    
    # ساختار صحیح برای sendInvoice در پیام‌رسان بله
    data = {
        "chat_id": chat_id,
        "title": f"خرید {currency_type} بازی",
        "description": f"مقدار: {currency_amount:,} {currency_type}",
        "payload": f"payment_{user_id}_{currency_type}_{currency_amount}",
        "provider_token": PAYMENT_TOKEN,
        "currency": "IRT",
        "prices": [
            {
                "label": f"{currency_amount:,} {currency_type}",
                "amount": amount_toman * 10  # تبدیل به دینار (تومان * 10)
            }
        ],
        "start_parameter": "world_war_bot_payment"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        
        if result.get("ok"):
            send_message(chat_id, f"💰 **درخواست پرداخت ارسال شد!**\n\n"
                                 f"💵 مبلغ: {amount_toman:,} تومان\n"
                                 f"🎁 دریافت: {currency_amount:,} {currency_type}\n\n"
                                 f"✅ لطفاً پرداخت را در پنجره باز شده تکمیل کنید.")
        else:
            error_msg = result.get('description', 'خطای نامشخص')
            send_message(chat_id, f"❌ خطا در ایجاد پرداخت: {error_msg}\n\n"
                                 f"لطفاً بعداً تلاش کنید یا با پشتیبانی تماس بگیرید.")
    except Exception as e:
        send_message(chat_id, f"❌ خطا: {str(e)}\n\nلطفاً بعداً تلاش کنید.")

def pre_checkout_query(query):
    """پاسخ به pre_checkout_query"""
    url = BASE_URL + "answerPreCheckoutQuery"
    data = {
        "pre_checkout_query_id": query["id"],
        "ok": True
    }
    try:
        requests.post(url, json=data, timeout=10)
    except:
        pass

def successful_payment(chat_id, user_id, payload, total_amount, currency):
    """پرداخت موفق - اضافه کردن موجودی"""
    try:
        parts = payload.split("_")
        if len(parts) >= 4:
            currency_type = parts[2]
            currency_amount = int(parts[3])
            
            conn = sqlite3.connect('world_war.db')
            c = conn.cursor()
            
            if currency_type == "dollar":
                c.execute("UPDATE players SET money = money + ? WHERE user_id=?", (currency_amount, user_id))
            elif currency_type == "coin":
                c.execute("UPDATE players SET coin = coin + ? WHERE user_id=?", (currency_amount, user_id))
            else:
                c.execute("UPDATE players SET diamond = diamond + ? WHERE user_id=?", (currency_amount, user_id))
            
            conn.commit()
            conn.close()
            
            send_message(chat_id, f"✅ **پرداخت موفق!**\n\n"
                                 f"🎁 {currency_amount:,} {currency_type} به حساب شما اضافه شد.\n"
                                 f"🙏 از حمایت شما سپاسگزاریم!")
    except Exception as e:
        print(f"خطا در successful_payment: {e}")

# ==================== اتحاد ====================
def declare_alliance(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT user_id, country FROM players WHERE user_id!=? AND is_banned=0", (user_id,))
    players = c.fetchall()
    
    if not players:
        send_message(chat_id, "❌ هیچ بازیکن دیگری وجود ندارد.")
        conn.close()
        return
    
    buttons = []
    for pid, country in players[:20]:
        # بررسی اتحاد موجود
        c.execute("SELECT * FROM alliances WHERE ((from_user=? AND to_user=?) OR (from_user=? AND to_user=?)) AND status='accepted'",
                  (user_id, pid, pid, user_id))
        if not c.fetchone():
            buttons.append([{"text": f"🤝 {country}", "callback_data": f"alliance_{pid}_{country}"}])
    
    if not buttons:
        send_message(chat_id, "❌ هیچ کشور قابل اتحادی یافت نشد.")
    else:
        buttons.append([{"text": "🔙 بازگشت", "callback_data": "back_main"}])
        keyboard = {"inline_keyboard": buttons}
        send_message(chat_id, "🤝 **اعلام اتحاد**\n\nکشور مورد نظر را انتخاب کنید:", keyboard)
    
    conn.close()

def send_alliance_request(chat_id, user_id, target_id, target_country):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT country FROM players WHERE user_id=?", (user_id,))
    my_country = c.fetchone()[0]
    
    c.execute("INSERT INTO alliances (from_user, to_user, status, message, timestamp) VALUES (?,?,?,?,?)",
              (user_id, target_id, "pending", f"درخواست اتحاد از {my_country}", datetime.now()))
    conn.commit()
    conn.close()
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ پذیرش", "callback_data": f"accept_{user_id}"}],
            [{"text": "❌ رد", "callback_data": f"reject_{user_id}"}]
        ]
    }
    
    send_message(target_id, f"🤝 **درخواست اتحاد**\n\nکشور **{my_country}** درخواست اتحاد با شما دارد.", keyboard)
    send_message(chat_id, f"✅ درخواست اتحاد به **{target_country}** ارسال شد.")

def accept_alliance(chat_id, user_id, requester_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("UPDATE alliances SET status='accepted' WHERE from_user=? AND to_user=? AND status='pending'",
              (requester_id, user_id))
    conn.commit()
    
    c.execute("SELECT country FROM players WHERE user_id=?", (requester_id,))
    requester_country = c.fetchone()[0]
    conn.close()
    
    send_message(chat_id, f"✅ شما با **{requester_country}** متحد شدید!")
    send_message(requester_id, f"✅ **{requester_country}** درخواست اتحاد شما را پذیرفت!")

def allies_list(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT from_user, to_user FROM alliances WHERE (from_user=? OR to_user=?) AND status='accepted'",
              (user_id, user_id))
    alliances = c.fetchall()
    
    if not alliances:
        send_message(chat_id, "📋 **لیست متحدان**\n\nشما هیچ متحدی ندارید.")
        conn.close()
        return
    
    allied_ids = set()
    for a in alliances:
        if a[0] == user_id:
            allied_ids.add(a[1])
        else:
            allied_ids.add(a[0])
    
    text = "🤝 **لیست متحدان شما**\n\n"
    for aid in allied_ids:
        c.execute("SELECT country FROM players WHERE user_id=?", (aid,))
        country = c.fetchone()
        if country:
            text += f"• **{country[0]}**\n"
    
    conn.close()
    send_message(chat_id, text)

def ally_chat(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT from_user, to_user FROM alliances WHERE (from_user=? OR to_user=?) AND status='accepted'",
              (user_id, user_id))
    alliances = c.fetchall()
    
    allied_ids = set()
    for a in alliances:
        if a[0] == user_id:
            allied_ids.add(a[1])
        else:
            allied_ids.add(a[0])
    
    if not allied_ids:
        send_message(chat_id, "❌ شما متحدی ندارید.")
        conn.close()
        return
    
    buttons = []
    for aid in allied_ids:
        c.execute("SELECT country FROM players WHERE user_id=?", (aid,))
        country = c.fetchone()
        if country:
            buttons.append([{"text": f"✉️ {country[0]}", "callback_data": f"chat_ally_{aid}"}])
    
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "back_main"}])
    keyboard = {"inline_keyboard": buttons}
    send_message(chat_id, "✉️ **مکالمه با متحد**\n\nانتخاب کنید:", keyboard)
    conn.close()

def start_chat_with_ally(chat_id, user_id, target_id):
    temp_data[user_id] = {"action": "ally_chat", "target": target_id}
    send_message(chat_id, "✉️ **ارسال پیام به متحد**\n\nپیام خود را بنویسید:")

def send_money_to_ally(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT from_user, to_user FROM alliances WHERE (from_user=? OR to_user=?) AND status='accepted'",
              (user_id, user_id))
    alliances = c.fetchall()
    
    allied_ids = set()
    for a in alliances:
        if a[0] == user_id:
            allied_ids.add(a[1])
        else:
            allied_ids.add(a[0])
    
    if not allied_ids:
        send_message(chat_id, "❌ شما متحدی ندارید.")
        conn.close()
        return
    
    buttons = []
    for aid in allied_ids:
        c.execute("SELECT country FROM players WHERE user_id=?", (aid,))
        country = c.fetchone()
        if country:
            buttons.append([{"text": f"💰 {country[0]}", "callback_data": f"send_money_{aid}"}])
    
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "back_main"}])
    keyboard = {"inline_keyboard": buttons}
    send_message(chat_id, "💰 **ارسال پول به متحد**\n\nانتخاب کنید:", keyboard)
    conn.close()

def process_send_money(chat_id, user_id, target_id):
    temp_data[user_id] = {"action": "send_money", "target": target_id}
    send_message(chat_id, "💰 **ارسال پول**\n\nمبلغ (به دلار) را وارد کنید:")

def transfer_money(chat_id, user_id, target_id, amount):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT money FROM players WHERE user_id=?", (user_id,))
    sender_money = c.fetchone()[0]
    
    if sender_money >= amount:
        c.execute("UPDATE players SET money = money - ? WHERE user_id=?", (amount, user_id))
        c.execute("UPDATE players SET money = money + ? WHERE user_id=?", (amount, target_id))
        conn.commit()
        
        c.execute("SELECT country FROM players WHERE user_id=?", (user_id,))
        sender_country = c.fetchone()[0]
        
        send_message(chat_id, f"✅ مبلغ {amount:,} دلار با موفقیت ارسال شد!")
        send_message(target_id, f"💰 شما مبلغ {amount:,} دلار از {sender_country} دریافت کردید!")
    else:
        send_message(chat_id, f"❌ پول کافی ندارید!\nموجودی: {sender_money:,} دلار")
    
    conn.close()

# ==================== جنگ ====================
def declare_war_menu(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT country FROM players WHERE user_id=?", (user_id,))
    my_country = c.fetchone()[0]
    
    # دریافت کشورهای دیگر (به جز متحدان)
    c.execute("""SELECT DISTINCT p.user_id, p.country FROM players p 
                 WHERE p.user_id!=? AND p.is_banned=0
                 AND NOT EXISTS (SELECT 1 FROM alliances a 
                                WHERE ((a.from_user=p.user_id AND a.to_user=?) 
                                OR (a.from_user=? AND a.to_user=p.user_id)) 
                                AND a.status='accepted')""",
              (user_id, user_id, user_id))
    players = c.fetchall()
    
    if not players:
        send_message(chat_id, "❌ هیچ کشور قابل حمله‌ای وجود ندارد.")
        conn.close()
        return
    
    buttons = []
    for pid, country in players[:20]:
        buttons.append([{"text": f"⚔️ {country}", "callback_data": f"war_declare_{pid}_{country}"}])
    
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "back_main"}])
    keyboard = {"inline_keyboard": buttons}
    send_message(chat_id, f"⚔️ **اعلام جنگ**\n\nکشور شما: **{my_country}**\nلطفاً کشور هدف را انتخاب کنید:", keyboard)
    conn.close()

def declare_war_target(chat_id, user_id, target_id, target_country):
    temp_data[user_id] = {"action": "declare_war", "target": target_id, "target_country": target_country}
    send_message(chat_id, f"⚔️ **اعلام جنگ به {target_country}**\n\n"
                         f"لطفاً سناریوی حمله خود را بنویسید:\n\n"
                         f"مثال:\n"
                         f"«با ۲۰ فروند F-22 و ۵۰ تانک به پایگاه هوایی دشمن حمله می‌کنم...»")

def save_war_scenario(chat_id, user_id, target_id, target_country, scenario):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT country FROM players WHERE user_id=?", (user_id,))
    my_country = c.fetchone()[0]
    
    c.execute("INSERT INTO war_scenarios (from_user, from_country, to_user, to_country, scenario, status, timestamp) VALUES (?,?,?,?,?,?,?)",
              (user_id, my_country, target_id, target_country, scenario, "pending", datetime.now()))
    conn.commit()
    conn.close()
    
    send_message(chat_id, f"✅ **سناریوی جنگ ثبت شد!**\n\n"
                         f"🎯 هدف: {target_country}\n\n"
                         f"📜 سناریو:\n{scenario[:300]}\n\n"
                         f"مدیران ربات سناریو را بررسی کرده و نتیجه را اعلام می‌کنند.")

def cyber_attack_check(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT tech_level FROM players WHERE user_id=?", (user_id,))
    tech_level = c.fetchone()[0]
    conn.close()
    
    if tech_level >= 4:
        send_message(chat_id, "👩🏼‍💻 **حمله سایبری**\n\n"
                             "برای انجام حمله سایبری، کشور هدف را وارد کنید:")
        temp_data[user_id] = {"action": "cyber_attack"}
    else:
        send_message(chat_id, f"❌ **حمله سایبری قفل است!**\n\n"
                             f"نیاز به تکنولوژی سطح ۴ دارید.\n"
                             f"سطح فعلی: {tech_level}")

def war_history(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT from_country, to_country, scenario, status, timestamp FROM war_scenarios WHERE from_user=? OR to_user=? ORDER BY timestamp DESC LIMIT 10",
              (user_id, user_id))
    wars = c.fetchall()
    conn.close()
    
    if not wars:
        send_message(chat_id, "📜 **تاریخچه جنگ‌ها**\n\nشما هنوز در هیچ جنگی شرکت نکرده‌اید.")
        return
    
    text = "📜 **تاریخچه جنگ‌ها**\n\n"
    for war in wars:
        from_c, to_c, scenario, status, time = war
        status_emoji = "✅" if status == "accepted" else "⏳" if status == "pending" else "❌"
        text += f"{status_emoji} {from_c} → {to_c}\n"
        text += f"   📅 {time[:16]}\n"
        text += f"   📝 {scenario[:50]}...\n\n"
    
    send_message(chat_id, text)

# ==================== بورس ====================
def stock_menu_func(chat_id):
    send_message(chat_id, "📈 **بازار جهانی بورس**\n\n"
                         "خرید و فروش کالاها و سهام:", stock_menu())

def stock_indices(chat_id):
    text = "🌍 **شاخص‌های جهانی**\n\n"
    text += "🇺🇸 داو جونز: ۴۲,۵۰۰ 🔻 -۲%\n"
    text += "🇨🇳 شانگهای: ۳,۲۰۰ 🔺 +۱.۵%\n"
    text += "🇪🇺 یورو استاکس: ۴,۸۰۰ 🔻 -۰.۸%\n"
    text += "🛢️ شاخص انرژی: ۳,۱۰۰ 🔺 +۵%\n\n"
    text += "💡 تحلیل: افزایش شاخص انرژی نشانه تنش در خاورمیانه است."
    
    keyboard = {"inline_keyboard": [[{"text": "🔄 به‌روزرسانی", "callback_data": "stock_indices"}]]}
    send_message(chat_id, text, keyboard)

def stock_commodities(chat_id):
    text = "🛢️ **کالاهای قابل معامله**\n\n"
    for key, commodity in COMMODITIES.items():
        arrow = "🔺" if commodity["trend"] == "up" else "🔻"
        text += f"{commodity['name']}: {commodity['price']} دلار {arrow} {abs(commodity['change'])}%\n"
        text += f"   حداکثر: {commodity['max']:,} واحد\n\n"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "📊 خرید کالا", "callback_data": "buy_commodity"}],
            [{"text": "💰 فروش کالا", "callback_data": "sell_commodity"}],
            [{"text": "🔙 بازگشت", "callback_data": "stock"}]
        ]
    }
    send_message(chat_id, text, keyboard)

def stock_stocks(chat_id):
    text = "🏢 **سهام شرکت‌های تسلیحاتی**\n\n"
    for key, stock in STOCKS.items():
        arrow = "🔺" if stock["change"] > 0 else "🔻"
        text += f"{stock['name']}: {stock['price']} دلار {arrow} {abs(stock['change'])}%\n"
        text += f"   سود تقسیمی: {stock['dividend']*100}%\n\n"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "📊 خرید سهام", "callback_data": "buy_stock"}],
            [{"text": "💰 فروش سهام", "callback_data": "sell_stock"}],
            [{"text": "🔙 بازگشت", "callback_data": "stock"}]
        ]
    }
    send_message(chat_id, text, keyboard)

def stock_currency(chat_id):
    text = "💱 **نرخ ارز**\n\n"
    text += "💲 دلار → 🪙 سکه: ۱ دلار = ۰.۰۰۰۱ سکه\n"
    text += "💲 دلار → 💎 الماس: ۱۰,۰۰۰ دلار = ۱ الماس\n"
    text += "🪙 سکه → 💎 الماس: ۱۰۰ سکه = ۱ الماس\n\n"
    text += "💡 نرخ تبدیل سکه به الماس ممکن است تغییر کند."
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "🔄 تبدیل دلار به سکه", "callback_data": "convert_dollar_coin"}],
            [{"text": "🔄 تبدیل سکه به الماس", "callback_data": "convert_coin_diamond"}],
            [{"text": "🔙 بازگشت", "callback_data": "stock"}]
        ]
    }
    send_message(chat_id, text, keyboard)

def stock_bonds(chat_id):
    text = "📜 **اوراق قرضه و سرمایه‌گذاری**\n\n"
    for bond in BONDS:
        text += f"**{bond['name']}**\n"
        text += f"   📅 مدت: {bond['days']} روز\n"
        text += f"   💰 سود: {bond['interest']}%\n"
        text += f"   💵 حداقل سرمایه: {bond['min']:,} دلار\n\n"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "📈 خرید اوراق", "callback_data": "buy_bond"}],
            [{"text": "🔙 بازگشت", "callback_data": "stock"}]
        ]
    }
    send_message(chat_id, text, keyboard)

def stock_assets(chat_id, user_id):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT money, coin, diamond FROM players WHERE user_id=?", (user_id,))
    money, coin, diamond = c.fetchone()
    
    c.execute("SELECT asset_type, amount FROM stock_assets WHERE user_id=?", (user_id,))
    assets = c.fetchall()
    conn.close()
    
    text = "📊 **دارایی شما در بورس**\n\n"
    text += f"💰 نقدینگی: {money:,.0f} دلار\n"
    text += f"🪙 سکه: {coin:,.0f}\n"
    text += f"💎 الماس: {diamond:,.0f}\n\n"
    
    if assets:
        text += "**سرمایه‌گذاری‌ها:**\n"
        for asset_type, amount in assets:
            if asset_type.startswith("stock_"):
                stock_key = asset_type.replace("stock_", "")
                if stock_key in STOCKS:
                    value = amount * STOCKS[stock_key]["price"]
                    text += f"• {STOCKS[stock_key]['name']}: {amount:,.0f} سهم (ارزش: {value:,.0f} دلار)\n"
    
    send_message(chat_id, text)

def buy_commodity(chat_id):
    buttons = []
    for key, commodity in COMMODITIES.items():
        buttons.append([{"text": f"{commodity['name']} - {commodity['price']} دلار", 
                         "callback_data": f"buy_comm_{key}"}])
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "stock_commodities"}])
    keyboard = {"inline_keyboard": buttons}
    send_message(chat_id, "📊 **خرید کالا**\n\nانتخاب کنید:", keyboard)

def buy_stock(chat_id):
    buttons = []
    for key, stock in STOCKS.items():
        buttons.append([{"text": f"{stock['name']} - {stock['price']} دلار", 
                         "callback_data": f"buy_stock_{key}"}])
    buttons.append([{"text": "🔙 بازگشت", "callback_data": "stock_stocks"}])
    keyboard = {"inline_keyboard": buttons}
    send_message(chat_id, "📊 **خرید سهام**\n\nانتخاب کنید:", keyboard)

# ==================== پشتیبانی ====================
def support_menu_func(chat_id):
    send_message(chat_id, "📞 **پشتیبانی و ارتباط با ما**\n\nلطفاً موضوع را انتخاب کنید:", support_menu())

def send_idea(chat_id):
    temp_data[chat_id] = {"waiting": "idea"}
    send_message(chat_id, "💡 **ارسال ایده**\n\nایده خود را بنویسید:\n\n🎁 پاداش: ۱۰۰ الماس")

def report_bug(chat_id):
    temp_data[chat_id] = {"waiting": "bug"}
    send_message(chat_id, "🐛 **گزارش باگ**\n\nمشکل را توضیح دهید:\n\n🎁 پاداش: ۲۰۰ سکه")

def payment_issue(chat_id):
    temp_data[chat_id] = {"waiting": "payment_issue"}
    send_message(chat_id, "💵 **مشکل در خرید**\n\nاطلاعات را بنویسید:\n\n• مبلغ\n• زمان\n• نوع ارز")

def cooperation(chat_id):
    temp_data[chat_id] = {"waiting": "cooperation"}
    send_message(chat_id, "🤝 **اعلام همکاری**\n\nنمونه کار و توضیحات:")

def guide(chat_id):
    text = "📖 **دفترچه راهنما**\n\n"
    text += "🌟 شروع: /start\n"
    text += "💰 ارزها: دلار، سکه (۴ میلیارد حد), الماس (۲۵,۰۰۰ حد)\n"
    text += "⚔️ جنگ: اعلام جنگ + سناریو\n"
    text += "🤝 اتحاد: تجارت و همکاری\n"
    text += "🏭 ساختمان: ۱۷ نوع با ۳ سطح\n"
    text += "📈 بورس: کالا، سهام، اوراق\n\n"
    text += "🔗 کانال: @lantern_war_game"
    send_message(chat_id, text)

def about_us(chat_id):
    text = "🌍 **ربات جنگ جهانی**\n\n"
    text += "بازی استراتژیک مدیریت کشور\n\n"
    text += "👥 تیم Lantern Games\n"
    text += "📅 ۲۰۲۵\n\n"
    text += "امکانات:\n"
    text += "• ۱۹۵ کشور\n"
    text += "• ۱۷ ساختمان\n"
    text += "• بورس و تجارت\n"
    text += "• سیستم اتحاد و جنگ\n\n"
    text += "هدف: ابرقدرت جهانی!"
    send_message(chat_id, text, main_menu())

def save_ticket(user_id, subject, message):
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    
    c.execute("SELECT country FROM players WHERE user_id=?", (user_id,))
    country = c.fetchone()
    country_name = country[0] if country else "ناشناس"
    
    c.execute("INSERT INTO support_tickets (user_id, user_country, subject, message, status, timestamp) VALUES (?,?,?,?,?,?)",
              (user_id, country_name, subject, message, "pending", datetime.now()))
    conn.commit()
    conn.close()
    
    send_message(user_id, f"✅ پیام شما ثبت شد.\nتیم پشتیبانی ۲۴ ساعت آینده پاسخ می‌دهد.")

# ==================== پنل ادمین ====================
def is_admin(user_id):
    if user_id == MAIN_ADMIN_ID:
        return True
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    c.execute("SELECT 1 FROM admins WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def admin_menu():
    return {
        "inline_keyboard": [
            [{"text": "📊 آمار بازی", "callback_data": "admin_stats"}],
            [{"text": "🎫 تیکت‌های پشتیبانی", "callback_data": "admin_tickets"}],
            [{"text": "🚫 مسدود کردن کاربر", "callback_data": "admin_ban"}],
            [{"text": "✅ رفع مسدودیت", "callback_data": "admin_unban"}],
            [{"text": "📢 پیام همگانی", "callback_data": "admin_broadcast"}],
            [{"text": "👤 افزودن ادمین", "callback_data": "admin_addadmin"}],
            [{"text": "🔙 بازگشت", "callback_data": "back_main"}]
        ]
    }

def admin_panel(chat_id, user_id):
    if not is_admin(user_id):
        send_message(chat_id, "⛔ شما دسترسی ادمین ندارید.")
        return
    send_message(chat_id, "🛠️ **پنل مدیریت**\n\nیک گزینه را انتخاب کنید:", admin_menu())

def admin_stats(chat_id, user_id):
    if not is_admin(user_id):
        return
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM players")
    total_players = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM players WHERE is_banned=1")
    banned = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM support_tickets WHERE status='pending'")
    pending_tickets = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM war_scenarios")
    total_wars = c.fetchone()[0]
    conn.close()

    text = "📊 **آمار بازی**\n\n"
    text += f"👥 کل بازیکنان: {total_players}\n"
    text += f"🚫 مسدود شده: {banned}\n"
    text += f"🎫 تیکت‌های در انتظار: {pending_tickets}\n"
    text += f"⚔️ کل سناریوهای جنگی: {total_wars}\n"
    send_message(chat_id, text, admin_menu())

def admin_tickets(chat_id, user_id):
    if not is_admin(user_id):
        return
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    c.execute("SELECT id, user_id, user_country, subject, message FROM support_tickets WHERE status='pending' ORDER BY id DESC LIMIT 10")
    tickets = c.fetchall()
    conn.close()

    if not tickets:
        send_message(chat_id, "✅ تیکت در انتظاری وجود ندارد.", admin_menu())
        return

    keyboard = {"inline_keyboard": []}
    text = "🎫 **تیکت‌های در انتظار:**\n\n"
    for tid, uid, country, subject, message in tickets:
        text += f"**#{tid}** | {country} | {subject}\n{message[:100]}\n\n"
        keyboard["inline_keyboard"].append([{"text": f"✍️ پاسخ به #{tid}", "callback_data": f"admin_reply_{tid}"}])
    keyboard["inline_keyboard"].append([{"text": "🔙 بازگشت", "callback_data": "admin_panel"}])
    send_message(chat_id, text, keyboard)

def admin_reply_request(chat_id, user_id, ticket_id):
    if not is_admin(user_id):
        return
    temp_data[user_id] = {"action": f"admin_reply_{ticket_id}"}
    send_message(chat_id, f"✍️ پاسخ خود برای تیکت #{ticket_id} را بنویسید:")

def admin_ban_request(chat_id, user_id):
    if not is_admin(user_id):
        return
    temp_data[user_id] = {"action": "admin_ban"}
    send_message(chat_id, "🚫 آیدی عددی کاربری که می‌خواهید مسدود کنید را وارد کنید:")

def admin_unban_request(chat_id, user_id):
    if not is_admin(user_id):
        return
    temp_data[user_id] = {"action": "admin_unban"}
    send_message(chat_id, "✅ آیدی عددی کاربری که می‌خواهید رفع مسدودیت کنید را وارد کنید:")

def admin_broadcast_request(chat_id, user_id):
    if not is_admin(user_id):
        return
    temp_data[user_id] = {"action": "admin_broadcast"}
    send_message(chat_id, "📢 متن پیام همگانی را بنویسید (برای همه بازیکنان غیرمسدود ارسال می‌شود):")

def admin_addadmin_request(chat_id, user_id):
    if not is_admin(user_id):
        return
    temp_data[user_id] = {"action": "admin_addadmin"}
    send_message(chat_id, "👤 آیدی عددی کاربری که می‌خواهید ادمین شود را وارد کنید:")

# ==================== پردازش اصلی ====================
def handle_callback(chat_id, user_id, callback_data):
    # منوهای اصلی
    if callback_data == "back_main":
        send_message(chat_id, "🏠 منوی اصلی", main_menu())
    elif callback_data == "back_realm":
        send_message(chat_id, "🏛️ قلمروی من", realm_menu())
    elif callback_data == "back_shop":
        send_message(chat_id, "🏬 فروشگاه", shop_menu())
    
    # قلمروی من
    elif callback_data == "my_realm":
        send_message(chat_id, "🏛️ قلمروی من", realm_menu())
    elif callback_data == "treasury":
        treasury(chat_id, user_id)
    elif callback_data == "collect_interest":
        collect_interest(chat_id, user_id)
    elif callback_data == "get_loan":
        get_loan(chat_id, user_id)
    elif callback_data.startswith("take_loan_"):
        amount = int(callback_data.replace("take_loan_", ""))
        take_loan(chat_id, user_id, amount)
    elif callback_data == "convert_currency":
        convert_currency(chat_id, user_id)
    elif callback_data == "military_assets":
        military_assets(chat_id, user_id)
    elif callback_data == "popularity":
        show_popularity(chat_id, user_id)
    elif callback_data == "tech":
        tech_menu_func(chat_id, user_id)
    
    # ساختمان‌ها
    elif callback_data == "buildings":
        buildings_menu_func(chat_id, user_id)
    elif callback_data.startswith("building_"):
        building_type = callback_data.replace("building_", "")
        if building_type in BUILDINGS_DATA:
            show_building(chat_id, user_id, building_type)
    elif callback_data.startswith("upgrade_"):
        parts = callback_data.split("_")
        building_type = parts[1]
        new_level = int(parts[2])
        cost = int(parts[3])
        upgrade_building(chat_id, user_id, building_type, new_level, cost)
    
    # فروشگاه
    elif callback_data == "shop":
        send_message(chat_id, "🏬 فروشگاه", shop_menu())
    elif callback_data == "buy_dollar":
        buy_dollar_menu(chat_id)
    elif callback_data == "buy_coin":
        buy_coin_menu(chat_id)
    elif callback_data == "buy_diamond":
        buy_diamond_menu(chat_id)
    elif callback_data == "buy_equipment":
        buy_equipment_menu_func(chat_id)
    elif callback_data.startswith("fighter_"):
        country_map = {"us": "🇺🇸 آمریکایی", "ru": "🇷🇺 روسی", "cn": "🇨🇳 چینی", 
                       "eu": "🇪🇺 اروپایی", "tr": "🇹🇷 ترکیه‌ای", "jp": "🇯🇵 ژاپنی",
                       "ir": "🇮🇷 ایرانی", "il": "🇮🇱 اسرائیلی", "in": "🇮🇳 هندی"}
        code = callback_data.replace("fighter_", "")
        show_fighters(chat_id, code, country_map.get(code, "جنگنده"))
    elif callback_data == "tank":
        show_tanks(chat_id)
    elif callback_data == "missile":
        show_missiles(chat_id)
    elif callback_data.startswith("buy_fighter_") or callback_data.startswith("buy_tank_") or callback_data.startswith("buy_missile_"):
        parts = callback_data.split("_")
        name = "_".join(parts[2:-1])
        price = int(parts[-1])
        buy_item(chat_id, user_id, name.replace("_", " "), price)
    
    # پرداخت
    elif callback_data.startswith("pay_dollar_"):
        parts = callback_data.split("_")
        amount = int(parts[2])
        price = int(parts[3])
        create_payment(chat_id, user_id, price, "دلار", amount)
    elif callback_data.startswith("pay_coin_"):
        parts = callback_data.split("_")
        amount = int(parts[2])
        price = int(parts[3])
        create_payment(chat_id, user_id, price, "سکه", amount)
    elif callback_data.startswith("pay_diamond_"):
        parts = callback_data.split("_")
        amount = int(parts[2])
        price = int(parts[3])
        create_payment(chat_id, user_id, price, "الماس", amount)
    
    # اتحاد
    elif callback_data == "alliance":
        send_message(chat_id, "🤝 اتحاد", alliance_menu())
    elif callback_data == "declare_alliance":
        declare_alliance(chat_id, user_id)
    elif callback_data.startswith("alliance_"):
        parts = callback_data.split("_")
        target_id = int(parts[1])
        target_country = "_".join(parts[2:])
        send_alliance_request(chat_id, user_id, target_id, target_country)
    elif callback_data.startswith("accept_"):
        requester_id = int(callback_data.replace("accept_", ""))
        accept_alliance(chat_id, user_id, requester_id)
    elif callback_data == "allies_list":
        allies_list(chat_id, user_id)
    elif callback_data == "ally_chat":
        ally_chat(chat_id, user_id)
    elif callback_data.startswith("chat_ally_"):
        target_id = int(callback_data.replace("chat_ally_", ""))
        start_chat_with_ally(chat_id, user_id, target_id)
    elif callback_data == "send_money":
        send_money_to_ally(chat_id, user_id)
    elif callback_data.startswith("send_money_"):
        target_id = int(callback_data.replace("send_money_", ""))
        process_send_money(chat_id, user_id, target_id)
    
    # جنگ
    elif callback_data == "war":
        send_message(chat_id, "⚔️ جنگ", war_menu())
    elif callback_data == "declare_war":
        declare_war_menu(chat_id, user_id)
    elif callback_data.startswith("war_declare_"):
        parts = callback_data.split("_")
        target_id = int(parts[2])
        target_country = "_".join(parts[3:])
        declare_war_target(chat_id, user_id, target_id, target_country)
    elif callback_data == "send_scenario":
        temp_data[user_id] = {"action": "send_scenario"}
        send_message(chat_id, "📜 **سناریوی حمله**\n\nسناریوی خود را بنویسید:")
    elif callback_data == "cyber_attack":
        cyber_attack_check(chat_id, user_id)
    elif callback_data == "war_history":
        war_history(chat_id, user_id)
    
    # بورس
    elif callback_data == "stock":
        stock_menu_func(chat_id)
    elif callback_data == "stock_indices":
        stock_indices(chat_id)
    elif callback_data == "stock_commodities":
        stock_commodities(chat_id)
    elif callback_data == "stock_stocks":
        stock_stocks(chat_id)
    elif callback_data == "stock_currency":
        stock_currency(chat_id)
    elif callback_data == "stock_bonds":
        stock_bonds(chat_id)
    elif callback_data == "stock_assets":
        stock_assets(chat_id, user_id)
    elif callback_data == "buy_commodity":
        buy_commodity(chat_id)
    elif callback_data == "buy_stock":
        buy_stock(chat_id)
    
    # پشتیبانی
    elif callback_data == "support":
        support_menu_func(chat_id)
    elif callback_data == "send_idea":
        send_idea(chat_id)
    elif callback_data == "report_bug":
        report_bug(chat_id)
    elif callback_data == "payment_issue":
        payment_issue(chat_id)
    elif callback_data == "cooperation":
        cooperation(chat_id)
    elif callback_data == "guide":
        guide(chat_id)
    
    # درباره ما
    elif callback_data == "about":
        about_us(chat_id)
    
    # انتخاب کشور
    elif callback_data.startswith("country_page_"):
        page = int(callback_data.replace("country_page_", ""))
        show_countries_list(chat_id, user_id, page)
    elif callback_data == "show_all_countries":
        text = "🌍 **لیست کامل کشورها (۱۹۵ کشور):**\n\n"
        for i, country in enumerate(COUNTRIES, 1):
            text += f"{i}. {country}\n"
            if i % 30 == 0:
                text += "\n"
        send_message(chat_id, text)
    elif callback_data.startswith("select_"):
        country = callback_data.replace("select_", "")
        select_country(chat_id, user_id, country)

    # پنل ادمین
    elif callback_data == "admin_panel":
        admin_panel(chat_id, user_id)
    elif callback_data == "admin_stats":
        admin_stats(chat_id, user_id)
    elif callback_data == "admin_tickets":
        admin_tickets(chat_id, user_id)
    elif callback_data == "admin_ban":
        admin_ban_request(chat_id, user_id)
    elif callback_data == "admin_unban":
        admin_unban_request(chat_id, user_id)
    elif callback_data == "admin_broadcast":
        admin_broadcast_request(chat_id, user_id)
    elif callback_data == "admin_addadmin":
        admin_addadmin_request(chat_id, user_id)
    elif callback_data.startswith("admin_reply_"):
        ticket_id = callback_data.replace("admin_reply_", "")
        admin_reply_request(chat_id, user_id, ticket_id)

def handle_text_message(chat_id, user_id, text):
    # بررسی وضعیت انتظار
    if user_id in temp_data:
        action = temp_data[user_id].get("action") or temp_data[user_id].get("waiting")
        
        if action == "phone":
            if text.startswith("09") and len(text) == 11:
                temp_data[user_id] = {"phone": text}
                show_countries_list(chat_id, user_id, 0)
                return True
            else:
                send_message(chat_id, "❌ شماره نامعتبر. لطفاً شماره ۱۱ رقمی خود را وارد کنید.")
                return True
        
        elif action == "declare_war":
            target_id = temp_data[user_id].get("target")
            target_country = temp_data[user_id].get("target_country")
            if target_id:
                save_war_scenario(chat_id, user_id, target_id, target_country, text)
                del temp_data[user_id]
            return True
        
        elif action == "send_scenario":
            save_ticket(user_id, "سناریوی جنگی", text)
            send_message(chat_id, "✅ سناریوی شما ثبت شد. مدیران بررسی می‌کنند.")
            del temp_data[user_id]
            return True
        
        elif action == "cyber_attack":
            send_message(chat_id, f"👩🏼‍💻 **حمله سایبری به {text}**\n\nسناریوی حمله سایبری خود را بنویسید:")
            temp_data[user_id] = {"action": "cyber_scenario", "target": text}
            return True
        
        elif action == "cyber_scenario":
            save_ticket(user_id, f"حمله سایبری به {temp_data[user_id]['target']}", text)
            send_message(chat_id, "✅ سناریوی حمله سایبری ثبت شد.")
            del temp_data[user_id]
            return True
        
        elif action == "ally_chat":
            target_id = temp_data[user_id].get("target")
            if target_id:
                send_message(target_id, f"✉️ **پیام از متحد:**\n\n{text}")
                send_message(chat_id, "✅ پیام ارسال شد.")
                del temp_data[user_id]
            return True
        
        elif action == "send_money":
            try:
                amount = int(text)
                target_id = temp_data[user_id].get("target")
                if target_id:
                    transfer_money(chat_id, user_id, target_id, amount)
                    del temp_data[user_id]
            except:
                send_message(chat_id, "❌ لطفاً عدد وارد کنید.")
            return True
        
        elif action == "idea":
            save_ticket(user_id, "ایده", text)
            send_message(chat_id, "✅ ایده شما ثبت شد. در صورت پیاده‌سازی، جایزه می‌گیرید.")
            del temp_data[user_id]
            return True
        
        elif action == "bug":
            save_ticket(user_id, "گزارش باگ", text)
            send_message(chat_id, "✅ باگ شما ثبت شد. بررسی می‌شود.")
            del temp_data[user_id]
            return True
        
        elif action == "payment_issue":
            save_ticket(user_id, "مشکل در خرید", text)
            send_message(chat_id, "✅ مشکل خرید ثبت شد. پشتیبانی تماس می‌گیرد.")
            del temp_data[user_id]
            return True
        
        elif action == "cooperation":
            save_ticket(user_id, "درخواست همکاری", text)
            send_message(chat_id, "✅ درخواست همکاری ثبت شد.")
            del temp_data[user_id]
            return True

        # ===== اکشن‌های پنل ادمین =====
        elif action == "admin_ban":
            if not is_admin(user_id):
                del temp_data[user_id]
                return True
            try:
                target = int(text)
                conn = sqlite3.connect('world_war.db')
                c = conn.cursor()
                c.execute("UPDATE players SET is_banned=1 WHERE user_id=?", (target,))
                conn.commit()
                conn.close()
                send_message(chat_id, f"🚫 کاربر `{target}` مسدود شد.", admin_menu())
                send_message(target, "🚫 شما از بازی مسدود شدید.")
            except:
                send_message(chat_id, "❌ آیدی نامعتبر است.")
            del temp_data[user_id]
            return True

        elif action == "admin_unban":
            if not is_admin(user_id):
                del temp_data[user_id]
                return True
            try:
                target = int(text)
                conn = sqlite3.connect('world_war.db')
                c = conn.cursor()
                c.execute("UPDATE players SET is_banned=0 WHERE user_id=?", (target,))
                conn.commit()
                conn.close()
                send_message(chat_id, f"✅ کاربر `{target}` رفع مسدودیت شد.", admin_menu())
                send_message(target, "✅ مسدودیت شما رفع شد. می‌توانید دوباره بازی کنید.")
            except:
                send_message(chat_id, "❌ آیدی نامعتبر است.")
            del temp_data[user_id]
            return True

        elif action == "admin_broadcast":
            if not is_admin(user_id):
                del temp_data[user_id]
                return True
            conn = sqlite3.connect('world_war.db')
            c = conn.cursor()
            c.execute("SELECT user_id FROM players WHERE is_banned=0")
            all_users = c.fetchall()
            conn.close()
            sent = 0
            for (uid,) in all_users:
                send_message(uid, f"📢 **پیام مدیریت:**\n\n{text}")
                sent += 1
                time.sleep(0.05)
            send_message(chat_id, f"✅ پیام به {sent} بازیکن ارسال شد.", admin_menu())
            del temp_data[user_id]
            return True

        elif action == "admin_addadmin":
            if not is_admin(user_id):
                del temp_data[user_id]
                return True
            try:
                target = int(text)
                conn = sqlite3.connect('world_war.db')
                c = conn.cursor()
                c.execute("INSERT OR IGNORE INTO admins (user_id, name, permissions, added_by, timestamp) VALUES (?,?,?,?,?)",
                          (target, "ادمین", "full", user_id, datetime.now()))
                conn.commit()
                conn.close()
                send_message(chat_id, f"✅ کاربر `{target}` به عنوان ادمین اضافه شد.", admin_menu())
            except:
                send_message(chat_id, "❌ آیدی نامعتبر است.")
            del temp_data[user_id]
            return True

        elif action and action.startswith("admin_reply_"):
            if not is_admin(user_id):
                del temp_data[user_id]
                return True
            ticket_id = action.replace("admin_reply_", "")
            conn = sqlite3.connect('world_war.db')
            c = conn.cursor()
            c.execute("SELECT user_id FROM support_tickets WHERE id=?", (ticket_id,))
            row = c.fetchone()
            if row:
                target_user = row[0]
                c.execute("UPDATE support_tickets SET status='answered', admin_response=? WHERE id=?", (text, ticket_id))
                conn.commit()
                send_message(target_user, f"📩 **پاسخ پشتیبانی:**\n\n{text}")
                send_message(chat_id, "✅ پاسخ ارسال شد.", admin_menu())
            conn.close()
            del temp_data[user_id]
            return True
    
    return False

# ==================== تابع اصلی ====================
def get_updates(offset=0):
    url = BASE_URL + "getUpdates"
    try:
        response = requests.get(url, params={"offset": offset, "timeout": 30}, timeout=35)
        if response.status_code == 200:
            return response.json()
        else:
            return {"ok": False}
    except Exception as e:
        return {"ok": False}

def ensure_main_admin():
    """ثبت خودکار ادمین اصلی در دیتابیس"""
    conn = sqlite3.connect('world_war.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO admins (user_id, name, permissions, added_by, timestamp) VALUES (?,?,?,?,?)",
              (MAIN_ADMIN_ID, "ادمین اصلی", "full", MAIN_ADMIN_ID, datetime.now()))
    conn.commit()
    conn.close()

def main():
    print("=" * 50)
    print("🌍 ربات جنگ جهانی - نسخه کامل")
    print("=" * 50)
    
    # تست اتصال
    print("🔄 تست اتصال...")
    try:
        test = requests.get(BASE_URL + "getMe", timeout=10)
        if test.status_code == 200:
            data = test.json()
            print(f"✅ اتصال برقرار! @{data['result']['username']}")
        else:
            print(f"❌ خطا: {test.status_code}")
            return
    except Exception as e:
        print(f"❌ خطا: {e}")
        return
    
    init_db()
    ensure_main_admin()
    print("✅ دیتابیس آماده است")
    print("📡 در حال دریافت پیام‌ها...")
    print("=" * 50)
    
    offset = 0
    
    while True:
        try:
            updates = get_updates(offset)
            
            if updates.get("ok") and "result" in updates:
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    
                    # پیام متنی
                    if "message" in update:
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        user_id = msg["from"]["id"]
                        
                        # شماره تماس
                        if "contact" in msg:
                            phone = msg["contact"]["phone_number"]
                            if user_id in temp_data and temp_data[user_id].get("waiting") == "phone":
                                temp_data[user_id] = {"phone": phone}
                                show_countries_list(chat_id, user_id, 0)
                            continue
                        
                        if "text" in msg:
                            text = msg["text"].strip()
                            
                            if text == "/start":
                                start_command(chat_id, user_id)
                            elif text == "/help":
                                guide(chat_id)
                            elif text == "/about":
                                about_us(chat_id)
                            elif text == "/id":
                                send_message(chat_id, f"🆔 آیدی: `{user_id}`")
                            elif text == "/admin":
                                admin_panel(chat_id, user_id)
                            else:
                                if not handle_text_message(chat_id, user_id, text):
                                    send_message(chat_id, "❌ دستور نامعتبر. /help")
                    
                    # دکمه‌ها
                    elif "callback_query" in update:
                        callback = update["callback_query"]
                        chat_id = callback["message"]["chat"]["id"]
                        user_id = callback["from"]["id"]
                        data = callback["data"]
                        
                        handle_callback(chat_id, user_id, data)
                        answer_callback(callback["id"])
                    
                    # پرداخت
                    elif "pre_checkout_query" in update:
                        pre_checkout_query(update["pre_checkout_query"])
                    
                    elif "successful_payment" in update:
                        payment = update["successful_payment"]
                        successful_payment(chat_id, user_id, payment["invoice_payload"], 
                                         payment["total_amount"], payment["currency"])
            
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print("\n🛑 ربات متوقف شد.")
            break
        except Exception as e:
            print(f"❌ خطا: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()