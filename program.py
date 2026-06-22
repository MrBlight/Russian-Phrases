import os
import sys
import random
import time
import json

# ==============================================================================
# DATA SECTION: The "Super Detailed Table"
# ==============================================================================

# Cyrillic Alphabet Reference Data
ALPHABET_DATA = [
    {'char': 'А', 'name': 'A', 'sound': 'ah', 'example': 'как (like)'},
    {'char': 'Б', 'name': 'Be', 'sound': 'b', 'example': 'банан (banana)'},
    {'char': 'В', 'name': 'Ve', 'sound': 'v', 'example': 'вода (water)'},
    {'char': 'Г', 'name': 'Ge', 'sound': 'g', 'example': 'город (city)'},
    {'char': 'Д', 'name': 'De', 'sound': 'd', 'example': 'дом (house)'},
    {'char': 'Е', 'name': 'Ye', 'sound': 'ye', 'example': 'есть (to eat/is)'},
    {'char': 'Ё', 'name': 'Yo', 'sound': 'yo', 'example': 'ёж (hedgehog)'},
    {'char': 'Ж', 'name': 'Zhe', 'sound': 'zh (like s in pleasure)', 'example': 'жизнь (life)'},
    {'char': 'З', 'name': 'Ze', 'sound': 'z', 'example': 'зима (winter)'},
    {'char': 'И', 'name': 'I', 'sound': 'ee', 'example': 'интерес (interest)'},
    {'char': 'Й', 'name': 'Short I', 'sound': 'y (like boy)', 'example': 'йогурт (yogurt)'},
    {'char': 'К', 'name': 'Ka', 'sound': 'k', 'example': 'кот (cat)'},
    {'char': 'Л', 'name': 'El', 'sound': 'l', 'example': 'лес (forest)'},
    {'char': 'М', 'name': 'Em', 'sound': 'm', 'example': 'мама (mom)'},
    {'char': 'Н', 'name': 'En', 'sound': 'n', 'example': 'нет (no)'},
    {'char': 'О', 'name': 'O', 'sound': 'o/ah (unstressed)', 'example': 'он (he)'},
    {'char': 'П', 'name': 'Pe', 'sound': 'p', 'example': 'привет (hello)'},
    {'char': 'Р', 'name': 'Er', 'sound': 'r (rolled)', 'example': 'русский (Russian)'},
    {'char': 'С', 'name': 'Es', 'sound': 's', 'example': 'спасибо (thank you)'},
    {'char': 'Т', 'name': 'Te', 'sound': 't', 'example': 'ты (you)'},
    {'char': 'У', 'name': 'U', 'sound': 'oo', 'example': 'утро (morning)'},
    {'char': 'Ф', 'name': 'Ef', 'sound': 'f', 'example': 'фрукт (fruit)'},
    {'char': 'Х', 'name': 'Kha', 'sound': 'kh (loch)', 'example': 'хорошо (good)'},
    {'char': 'Ц', 'name': 'Tse', 'sound': 'ts (cats)', 'example': 'цвет (color)'},
    {'char': 'Ч', 'name': 'Che', 'sound': 'ch', 'example': 'что (what)'},
    {'char': 'Ш', 'name': 'Sha', 'sound': 'sh', 'example': 'шоколад (chocolate)'},
    {'char': 'Щ', 'name': 'Shcha', 'sound': 'shch (fresh cheese)', 'example': 'щенок (puppy)'},
    {'char': 'Ъ', 'name': 'Hard Sign', 'sound': '(silent, hardens)', 'example': 'съесть (to eat up)'},
    {'char': 'Ы', 'name': 'Yery', 'sound': 'i (deep throat)', 'example': 'сыр (cheese)'},
    {'char': 'Ь', 'name': 'Soft Sign', 'sound': '(softens)', 'example': 'мать (mother)'},
    {'char': 'Э', 'name': 'E', 'sound': 'e (met)', 'example': 'это (this)'},
    {'char': 'Ю', 'name': 'Yu', 'sound': 'yu', 'example': 'юла (top toy)'},
    {'char': 'Я', 'name': 'Ya', 'sound': 'ya', 'example': 'я (I)'},
]

STRESS_GUIDE_TEXT = """
================================================================================
HOW TO READ STRESS MARKS IN RUSSIAN
================================================================================

In Russian, word stress is CRITICAL. Unlike English, stress in Russian is 
unpredictable and can change the meaning or pronunciation of vowels completely.

1. THE MARK: 
   We use an ACUTE ACCENT ( ´ ) over a vowel to indicate stress.
   Example: мОлодец (well done) vs молокО (milk).

2. VOWEL REDUCTION (The "Ah" Sound):
   - The letter 'O' is pronounced like 'AH' when NOT stressed.
     Example: мОлоко (milk-o) -> Pronounced: mu-la-KO.
   - The letter 'A' is also reduced to a schwa sound ('uh') when unstressed.

3. WHY IT MATTERS:
   If you ignore stress, Russians might not understand you.
   - зАмок = castle
   - замОк = lock

4. HOW TO USE THIS PROGRAM:
   - Look at the bold/accented vowel in the "Stressed" column.
   - Say that syllable LOUDER and LONGER.
   - Reduce the other 'O's and 'A's to 'uh' sounds.

================================================================================
"""

# Vocabulary and Phrases organized by Level
# Structure: { "cyrillic": "...", "stressed": "...", "phonetic": "...", "latinized": "...", "translation": "..." }

DATA_LEVELS = {
    1: {
        "phrases": [
            {"cyrillic": "Привет", "stressed": "ПривЕт", "phonetic": "pree-VYET", "latinized": "Privet", "translation": "Hello / Hi"},
            {"cyrillic": "Спасибо", "stressed": "СпасИбо", "phonetic": "spa-SEE-ba", "latinized": "Spasibo", "translation": "Thank you"},
            {"cyrillic": "Да", "stressed": "Да", "phonetic": "da", "latinized": "Da", "translation": "Yes"},
            {"cyrillic": "Нет", "stressed": "Нет", "phonetic": "nyet", "latinized": "Nyet", "translation": "No"},
            {"cyrillic": "Как дела?", "stressed": "Как делА?", "phonetic": "kak dee-LA?", "latinized": "Kak dela?", "translation": "How are things?"},
            {"cyrillic": "Хорошо", "stressed": "ХорошО", "phonetic": "kha-ra-SHO", "latinized": "Khorosho", "translation": "Good / Okay"},
            {"cyrillic": "Пока", "stressed": "ПокА", "phonetic": "pa-KA", "latinized": "Poka", "translation": "Bye (informal)"},
            {"cyrillic": "Извините", "stressed": "ИзвинИте", "phonetic": "iz-vi-NEE-tye", "latinized": "Izvinite", "translation": "Excuse me / Sorry"},
            {"cyrillic": "Я не понимаю", "stressed": "Я не понимАю", "phonetic": "ya ne pa-ni-MA-yu", "latinized": "Ya ne ponimayu", "translation": "I don't understand"},
            {"cyrillic": "Где ...?", "stressed": "Где ...?", "phonetic": "gdye ...?", "latinized": "Gde ...?", "translation": "Where is ...?"},
            {"cyrillic": "Что это?", "stressed": "Что Это?", "phonetic": "shto E-ta?", "latinized": "Chto eto?", "translation": "What is this?"},
            {"cyrillic": "Меня зовут...", "stressed": "МенЯ зовУт...", "phonetic": "mi-NYA za-VOOT...", "latinized": "Menya zovut...", "translation": "My name is..."},
        ],
        "words": [
            {"cyrillic": "Я", "stressed": "Я", "phonetic": "ya", "latinized": "Ya", "translation": "I"},
            {"cyrillic": "Ты", "stressed": "Ты", "phonetic": "ty", "latinized": "Ty", "translation": "You (informal)"},
            {"cyrillic": "Он", "stressed": "Он", "phonetic": "on", "latinized": "On", "translation": "He"},
            {"cyrillic": "Она", "stressed": "ОнА", "phonetic": "a-NA", "latinized": "Ona", "translation": "She"},
            {"cyrillic": "Мы", "stressed": "Мы", "phonetic": "my", "latinized": "My", "translation": "We"},
            {"cyrillic": "Туалет", "stressed": "ТуалЕт", "phonetic": "too-a-LYET", "latinized": "Tualet", "translation": "Toilet"},
            {"cyrillic": "Вода", "stressed": "ВодА", "phonetic": "va-DA", "latinized": "Voda", "translation": "Water"},
            {"cyrillic": "Еда", "stressed": "ЕдА", "phonetic": "yi-DA", "latinized": "Yeda", "translation": "Food"},
            {"cyrillic": "Дом", "stressed": "Дом", "phonetic": "dom", "latinized": "Dom", "translation": "House/Home"},
            {"cyrillic": "Мама", "stressed": "мАма", "phonetic": "MA-ma", "latinized": "Mama", "translation": "Mom"},
        ]
    },
    2: {
        "phrases": [
            {"cyrillic": "Я хочу...", "stressed": "Я хочУ...", "phonetic": "ya kha-CHU...", "latinized": "Ya khochu...", "translation": "I want..."},
            {"cyrillic": "Я люблю...", "stressed": "Я люблЮ...", "phonetic": "ya lyub-LYU...", "latinized": "Ya lyublyu...", "translation": "I love..."},
            {"cyrillic": "Я знаю", "stressed": "Я знАю", "phonetic": "ya ZNA-yu", "latinized": "Ya znayu", "translation": "I know"},
            {"cyrillic": "Я не знаю", "stressed": "Я не знАю", "phonetic": "ya ne ZNA-yu", "latinized": "Ya ne znayu", "translation": "I don't know"},
            {"cyrillic": "Я вижу...", "stressed": "Я вИжу...", "phonetic": "ya VEE-zhu...", "latinized": "Ya vizhu...", "translation": "I see..."},
            {"cyrillic": "Я думаю...", "stressed": "Я дУмаю...", "phonetic": "ya DU-ma-yu...", "latinized": "Ya dumayu...", "translation": "I think..."},
            {"cyrillic": "Я иду...", "stressed": "Я идУ...", "phonetic": "ya ee-DU...", "latinized": "Ya idu...", "translation": "I am going..."},
            {"cyrillic": "Это есть...", "stressed": "Это есть...", "phonetic": "E-ta yest...", "latinized": "Eto yest...", "translation": "This is..."},
            {"cyrillic": "У меня есть...", "stressed": "У менЯ есть...", "phonetic": "u mi-NYA yest...", "latinized": "U menya yest...", "translation": "I have..."},
            {"cyrillic": "Сколько стоит?", "stressed": "скОлько стОит?", "phonetic": "SKOL-ka STO-it?", "latinized": "Skolko stoit?", "translation": "How much does it cost?"},
        ],
        "words": [
            {"cyrillic": "Любить", "stressed": "ЛюбИть", "phonetic": "lyu-BIT'", "latinized": "Lyubit'", "translation": "To love"},
            {"cyrillic": "Хотеть", "stressed": "ХотЕть", "phonetic": "kha-TET'", "latinized": "Khotet'", "translation": "To want"},
            {"cyrillic": "Знать", "stressed": "ЗнАть", "phonetic": "ZNAT'", "latinized": "Znat'", "translation": "To know"},
            {"cyrillic": "Видеть", "stressed": "вИдеть", "phonetic": "VEE-det'", "latinized": "Videt'", "translation": "To see"},
            {"cyrillic": "Думать", "stressed": "дУмать", "phonetic": "DU-mat'", "latinized": "Dumat'", "translation": "To think"},
            {"cyrillic": "Делать", "stressed": "дЕлать", "phonetic": "DYE-lat'", "latinized": "Delat'", "translation": "To do/make"},
            {"cyrillic": "Говорить", "stressed": "ГоворИть", "phonetic": "ga-va-RIT'", "latinized": "Govorit'", "translation": "To speak"},
            {"cyrillic": "Понимать", "stressed": "ПонимАть", "phonetic": "pa-ni-MAT'", "latinized": "Ponimat'", "translation": "To understand"},
            {"cyrillic": "Работать", "stressed": "РабОтать", "phonetic": "ra-BO-tat'", "latinized": "Rabotat'", "translation": "To work"},
            {"cyrillic": "Жить", "stressed": "Жить", "phonetic": "zhit'", "latinized": "Zhit'", "translation": "To live"},
        ]
    },
    3: {
        "phrases": [
            {"cyrillic": "Я буду...", "stressed": "Я бУду...", "phonetic": "ya BU-du...", "latinized": "Ya budu...", "translation": "I will be..."},
            {"cyrillic": "Я сделаю...", "stressed": "Я сдЕлаю...", "phonetic": "ya SDYE-la-yu...", "latinized": "Ya sdelayu...", "translation": "I will do..."},
            {"cyrillic": "Мне нравится...", "stressed": "Мне нрАвится...", "phonetic": "mne NRA-vit-sya...", "latinized": "Mne nravitsya...", "translation": "I like... (lit: It pleases me)"},
            {"cyrillic": "Мне не нравится", "stressed": "Мне не нрАвится", "phonetic": "mne ne NRA-vit-sya", "latinized": "Mne ne nravitsya", "translation": "I don't like it"},
            {"cyrillic": "Я ненавижу...", "stressed": "Я ненавИжу...", "phonetic": "ya ni-na-VI-zhu...", "latinized": "Ya nenavizhu...", "translation": "I hate..."},
            {"cyrillic": "Почему это...?", "stressed": "ПочемУ Это...?", "phonetic": "pa-chi-MU E-ta...?", "latinized": "Pochemu eto...?", "translation": "Why is it...?"},
            {"cyrillic": "Потому что...", "stressed": "ПотомУ что...", "phonetic": "pa-ta-MU chta...", "latinized": "Potomu chto...", "translation": "Because..."},
            {"cyrillic": "Я могу...", "stressed": "Я могУ...", "phonetic": "ya ma-GU...", "latinized": "Ya mogu...", "translation": "I can..."},
            {"cyrillic": "Я должен...", "stressed": "Я дОлжен...", "phonetic": "ya DOL-zhen...", "latinized": "Ya dolzhen...", "translation": "I must / I should..."},
            {"cyrillic": "Давай пойдем...", "stressed": "давАй пойдЕм...", "phonetic": "da-VAI pay-DYOM...", "latinized": "Davay poydem...", "translation": "Let's go..."},
        ],
        "words": [
            {"cyrillic": "Буду", "stressed": "бУду", "phonetic": "BU-du", "latinized": "Budu", "translation": "I will be"},
            {"cyrillic": "Мочь", "stressed": "Мочь", "phonetic": "moch'", "latinized": "Moch'", "translation": "To be able to"},
            {"cyrillic": "Нравиться", "stressed": "нрАвиться", "phonetic": "NRA-vit-sya", "latinized": "Nravitsya", "translation": "To be pleasing"},
            {"cyrillic": "Ненавидеть", "stressed": "НенавИдеть", "phonetic": "ni-na-VE-det'", "latinized": "Nenavidet'", "translation": "To hate"},
            {"cyrillic": "Почему", "stressed": "ПочемУ", "phonetic": "pa-chi-MU", "latinized": "Pochemu", "translation": "Why"},
            {"cyrillic": "Потому что", "stressed": "ПотомУ что", "phonetic": "pa-ta-MU chta", "latinized": "Potomu chto", "translation": "Because"},
            {"cyrillic": "Когда", "stressed": "КогдА", "phonetic": "kag-DA", "latinized": "Kogda", "translation": "When"},
            {"cyrillic": "Где", "stressed": "Где", "phonetic": "gdye", "latinized": "Gde", "translation": "Where"},
            {"cyrillic": "Куда", "stressed": "КудА", "phonetic": "ku-DA", "latinized": "Kuda", "translation": "Where to"},
            {"cyrillic": "Откуда", "stressed": "ОткУда", "phonetic": "at-KU-da", "latinized": "Otkuda", "translation": "Where from"},
        ]
    },
    4: {
        "phrases": [
            {"cyrillic": "Если бы я знал...", "stressed": "ЕслИ бы я знАл...", "phonetic": "yes-LI by ya ZNAL...", "latinized": "Yesli by ya znal...", "translation": "If I knew..."},
            {"cyrillic": "Я бы хотел...", "stressed": "Я бы хотЕл...", "phonetic": "ya by kha-TYEL...", "latinized": "Ya by khotel...", "translation": "I would like..."},
            {"cyrillic": "Надо было...", "stressed": "нАдо бЫло...", "phonetic": "NA-da BY-lo...", "latinized": "Nado bylo...", "translation": "It was necessary to..."},
            {"cyrillic": "Всё равно", "stressed": "Всё равнО", "phonetic": "vsyo rav-NO", "latinized": "Vsyo ravno", "translation": "Doesn't matter / Anyway"},
            {"cyrillic": "Конечно", "stressed": "КонЕчно", "phonetic": "ka-NYECH-na", "latinized": "Konechno", "translation": "Of course"},
            {"cyrillic": "На самом деле", "stressed": "На самОм дЕле", "phonetic": "na sa-MOM DYE-lie", "latinized": "Na samom dele", "translation": "Actually / In fact"},
            {"cyrillic": "Кстати", "stressed": "СтАти", "phonetic": "STA-ti", "latinized": "Stati", "translation": "By the way"},
            {"cyrillic": "Я согласен", "stressed": "Я соглАсен", "phonetic": "ya sag-LA-sin", "latinized": "Ya soglasen", "translation": "I agree (male)"},
            {"cyrillic": "Я не согласен", "stressed": "Я не соглАсен", "phonetic": "ya ne sag-LA-sin", "latinized": "Ya ne soglasen", "translation": "I disagree (male)"},
            {"cyrillic": "Что случилось?", "stressed": "Что случИлось?", "phonetic": "shto slu-CHEE-los?", "latinized": "Chto sluchilos?", "translation": "What happened?"},
        ],
        "words": [
            {"cyrillic": "Если", "stressed": "ЕслИ", "phonetic": "yes-LI", "latinized": "Yesli", "translation": "If"},
            {"cyrillic": "Бы", "stressed": "бы", "phonetic": "by", "latinized": "By", "translation": "Would (particle)"},
            {"cyrillic": "Хотя", "stressed": "Хотя", "phonetic": "kha-TYA", "latinized": "Khotya", "translation": "Although"},
            {"cyrillic": "Поэтому", "stressed": "ПоэтОму", "phonetic": "pa-E-to-mu", "latinized": "Poetomu", "translation": "Therefore"},
            {"cyrillic": "Вдруг", "stressed": "Вдруг", "phonetic": "vdroog", "latinized": "Vdrug", "translation": "Suddenly"},
            {"cyrillic": "Наверное", "stressed": "навЕрное", "phonetic": "na-VYER-na-ye", "latinized": "Navernoe", "translation": "Probably"},
            {"cyrillic": "Точно", "stressed": "тОчно", "phonetic": "TOCH-na", "latinized": "Tochno", "translation": "Exactly"},
            {"cyrillic": "Правда", "stressed": "прАвда", "phonetic": "PRAV-da", "latinized": "Pravda", "translation": "Truth / Really?"},
            {"cyrillic": "Всегда", "stressed": "ВсегдА", "phonetic": "fsig-DA", "latinized": "Vsegda", "translation": "Always"},
            {"cyrillic": "Никогда", "stressed": "НикогдА", "phonetic": "ni-kag-DA", "latinized": "Nikogda", "translation": "Never"},
        ]
    },
    5: {
        "phrases": [
            {"cyrillic": "Как насчет того, чтобы...?", "stressed": "Как насчЕт тогО, чтОбы...?", "phonetic": "kak nas-CHYET ta-VO, CHTO-by...?", "latinized": "Kak naschet togo, chtoby...?", "translation": "How about...?"},
            {"cyrillic": "Мне кажется, что...", "stressed": "Мне кАжется, что...", "phonetic": "mne KAZH-et-sya, chto...", "latinized": "Mne kazhetsya, chto...", "translation": "It seems to me that..."},
            {"cyrillic": "Я имею в виду...", "stressed": "Я имЕю в видУ...", "phonetic": "ya i-MYEU v vi-DU...", "latinized": "Ya imeyu v vidu...", "translation": "I mean..."},
            {"cyrillic": "Не могли бы вы...?", "stressed": "Не моглИ бы вы...?", "phonetic": "ne mag-LI by vy...?", "latinized": "Ne mogli by vy...?", "translation": "Could you...? (polite)"},
            {"cyrillic": "Лучше поздно, чем никогда", "stressed": "лУчше пОздно, чЕм никогдА", "phonetic": "LUCH-shye POZD-na, CHEM ni-kag-DA", "latinized": "Luchshe pozdno, chem nikogda", "translation": "Better late than never"},
            {"cyrillic": "Руки не доходят", "stressed": "рУки не дохОдят", "phonetic": "RU-ki ne da-KHO-dyat", "latinized": "Ruki ne dokhodyat", "translation": "I haven't got round to it (lit: hands don't reach)"},
            {"cyrillic": "Дело в том, что...", "stressed": "дЕло в том, что...", "phonetic": "DYE-la v tom, chto...", "latinized": "Delo v tom, chto...", "translation": "The thing is that..."},
            {"cyrillic": "В конце концов", "stressed": "В концЕ концОв", "phonetic": "v kan-TSYE kan-TSOF", "latinized": "V kontse kontsov", "translation": "In the end / Finally"},
            {"cyrillic": "Честно говоря", "stressed": "чЕстно говорЯ", "phonetic": "CHYES-na ga-va-RYA", "latinized": "Chestno govorya", "translation": "Honestly speaking"},
            {"cyrillic": "Само собой разумеется", "stressed": "самО собОй разумЕется", "phonetic": "sa-MO sa-BOY ra-zu-MYE-et-sya", "latinized": "Samo soboy razumeyetsya", "translation": "Needless to say / Of course"},
        ],
        "words": [
            {"cyrillic": "Кажется", "stressed": "кАжется", "phonetic": "KAZH-et-sya", "latinized": "Kazhetsya", "translation": "It seems"},
            {"cyrillic": "Видимо", "stressed": "вИдимо", "phonetic": "VEE-di-ma", "latinized": "Vidimo", "translation": "Apparently"},
            {"cyrillic": "Надеюсь", "stressed": "надЕюсь", "phonetic": "na-DYU-yus'", "latinized": "Nadeyus'", "translation": "I hope"},
            {"cyrillic": "Боюсь", "stressed": "боЮсь", "phonetic": "ba-YUS'", "latinized": "Boyus'", "translation": "I'm afraid"},
            {"cyrillic": "Удивительно", "stressed": "удивИтельно", "phonetic": "u-di-VI-tel-na", "latinized": "Udivitelno", "translation": "Surprisingly"},
            {"cyrillic": "К сожалению", "stressed": "К сожалЕнию", "phonetic": "k sa-zha-LE-niyu", "latinized": "K sozhaleniyu", "translation": "Unfortunately"},
            {"cyrillic": "Наоборот", "stressed": "НаоборОт", "phonetic": "na-o-bo-ROT", "latinized": "Naoborot", "translation": "On the contrary"},
            {"cyrillic": "Вряд ли", "stressed": "Вряд ли", "phonetic": "vryad li", "latinized": "Vryad li", "translation": "Hardly / Unlikely"},
            {"cyrillic": "Едва ли", "stressed": "Едва ли", "phonetic": "yed-va li", "latinized": "Yedva li", "translation": "Scarcely"},
            {"cyrillic": "Безусловно", "stressed": "БезуслОвно", "phonetic": "bi-zus-LOV-na", "latinized": "Bezuslovno", "translation": "Unconditionally"},
        ]
    }
}

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title="RUSSIAN MASTER"):
    clear_screen()
    print("=" * 60)
    print(f"{title:^60}")
    print("=" * 60)
    print()

def wait_for_enter():
    input("\nPress Enter to continue...")

# ==============================================================================
# FEATURE: ALPHABET TABLE
# ==============================================================================

def show_alphabet_table():
    print_header("THE CYRILLIC ALPHABET")
    print(f"{'Char':<6} | {'Name':<12} | {'Sound':<25} | {'Example'}")
    print("-" * 60)
    for item in ALPHABET_DATA:
        print(f"{item['char']:<6} | {item['name']:<12} | {item['sound']:<25} | {item['example']}")
    print("-" * 60)
    wait_for_enter()

# ==============================================================================
# FEATURE: STRESS GUIDE
# ==============================================================================

def show_stress_guide():
    print_header("UNDERSTANDING STRESS MARKS")
    print(STRESS_GUIDE_TEXT)
    wait_for_enter()

# ==============================================================================
# FEATURE: BROWSE LEVELS (SPREADSHEET VIEW)
# ==============================================================================

def browse_levels():
    while True:
        print_header("BROWSE ALL DATA (SPREADSHEET VIEW)")
        print("Select a level to view (1-5), or '0' to go back:")
        for i in range(1, 6):
            count_p = len(DATA_LEVELS[i]["phrases"])
            count_w = len(DATA_LEVELS[i]["words"])
            print(f"  {i}. Level {i} ({count_p} phrases, {count_w} words)")
        
        choice = input("\nChoice: ").strip()
        if choice == '0':
            break
        elif choice.isdigit() and 1 <= int(choice) <= 5:
            level = int(choice)
            view_level_data(level)
        else:
            print("Invalid choice.")
            time.sleep(1)

def view_level_data(level):
    while True:
        print_header(f"LEVEL {level} DATA")
        print("1. View Phrases")
        print("2. View Words")
        print("0. Back to Levels")
        
        sub_choice = input("\nChoice: ").strip()
        if sub_choice == '0':
            break
        elif sub_choice == '1':
            display_table(DATA_LEVELS[level]["phrases"], "Phrases")
        elif sub_choice == '2':
            display_table(DATA_LEVELS[level]["words"], "Words")

def display_table(data_list, title):
    print_header(f"{title} - Level Data")
    # Header
    print(f"{'Cyrillic':<15} | {'Stressed':<15} | {'Phonetic':<15} | {'Latinized':<15} | {'Translation'}")
    print("-" * 85)
    for item in data_list:
        print(f"{item['cyrillic']:<15} | {item['stressed']:<15} | {item['phonetic']:<15} | {item['latinized']:<15} | {item['translation']}")
    print("-" * 85)
    wait_for_enter()

# ==============================================================================
# FEATURE: FLASHCARD LEARNING MODE
# ==============================================================================

def flashcard_mode():
    # Settings
    show_latinized = True
    
    while True:
        print_header("FLASHCARD LEARNING MODE")
        print("Select difficulty level:")
        for i in range(1, 6):
            print(f"  {i}. Level {i}")
        print("  A. All Levels Mixed")
        print("  S. Settings (Toggle Latinized View)")
        print("  0. Back to Main Menu")
        
        choice = input("\nChoice: ").strip().lower()
        
        if choice == '0':
            break
        elif choice == 's':
            show_latinized = not show_latinized
            status = "ON" if show_latinized else "OFF"
            print(f"\nLatinized View turned {status}.")
            time.sleep(1)
            continue
        elif choice == 'a':
            # Combine all data
            all_phrases = []
            all_words = []
            for lvl in DATA_LEVELS.values():
                all_phrases.extend(lvl["phrases"])
                all_words.extend(lvl["words"])
            run_flashcards(all_phrases, "Mixed Phrases", show_latinized)
            run_flashcards(all_words, "Mixed Words", show_latinized)
        elif choice.isdigit() and 1 <= int(choice) <= 5:
            level = int(choice)
            run_flashcards(DATA_LEVELS[level]["phrases"], f"Level {level} Phrases", show_latinized)
            run_flashcards(DATA_LEVELS[level]["words"], f"Level {level} Words", show_latinized)
        else:
            print("Invalid choice.")
            time.sleep(1)

def run_flashcards(items, title, show_latinized):
    if not items:
        print("No items found.")
        wait_for_enter()
        return

    random.shuffle(items)
    total = len(items)
    
    print_header(f"STARTING: {title}")
    print(f"Total cards: {total}")
    print("Controls: [Enter] Flip/Next, 'q' Quit, 't' Toggle Latinized")
    wait_for_enter()
    
    current_idx = 0
    
    while current_idx < total:
        item = items[current_idx]
        clear_screen()
        print(f"--- Card {current_idx + 1} of {total} ---")
        print(f"\nTRANSLATION: {item['translation']}\n")
        print("Press Enter to reveal Russian...")
        
        inp = input()
        if inp.lower() == 'q':
            break
        if inp.lower() == 't':
            show_latinized = not show_latinized
            # Re-loop to show same card with new setting
            continue
            
        # Show Card Front
        print(f"\nCYRILLIC:      {item['cyrillic']}")
        print(f"WITH STRESS:   {item['stressed']}")
        print(f"PHONETIC:      {item['phonetic']}")
        if show_latinized:
            print(f"LATINIZED:     {item['latinized']}")
        print("-" * 30)
        print("Press Enter for next card (or 'q' to quit)...")
        
        inp2 = input()
        if inp2.lower() == 'q':
            break
        if inp2.lower() == 't':
            show_latinized = not show_latinized
            continue
            
        current_idx += 1
        
    print(f"\nSession Complete! You reviewed {current_idx} cards.")
    wait_for_enter()

# ==============================================================================
# MAIN MENU
# ==============================================================================

def main_menu():
    while True:
        print_header("RUSSIAN LANGUAGE MASTER")
        print("Learn Russian efficiently with progressive levels.")
        print("-" * 40)
        print("1. Start Flashcard Learning")
        print("2. Browse Spreadsheet Data (By Level)")
        print("3. View Cyrillic Alphabet Table")
        print("4. Guide: Reading Stress Marks")
        print("5. Exit")
        print("-" * 40)
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            flashcard_mode()
        elif choice == '2':
            browse_levels()
        elif choice == '3':
            show_alphabet_table()
        elif choice == '4':
            show_stress_guide()
        elif choice == '5':
            print("Spasibo! Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting gracefully...")
        sys.exit(0)
