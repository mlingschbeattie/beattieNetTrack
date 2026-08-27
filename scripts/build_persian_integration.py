import os
import json

TARGET_DIR = r"c:\CustomApps\26_27_ LessonsAndAgendas"
os.makedirs(TARGET_DIR, exist_ok=True)

print("Starting generation of 4-way Multilingual Lesson Suite (EN, FA فارسی, AR عربي, UK УКР)...")

# Load generator script with all 4 languages
builder_script = r"""import os
import json
import sys

TARGET_DIR = r"c:\CustomApps\26_27_ LessonsAndAgendas"
os.makedirs(TARGET_DIR, exist_ok=True)

print("Starting generation of 4-way Multilingual Lesson Suite (EN, FA, AR, UK)...")

# 1. READ EXISTING MULTILINGUAL CODE
with open(os.path.join(TARGET_DIR, "presentation.html"), "r", encoding="utf-8") as f:
    pres_content = f.read()

with open(os.path.join(TARGET_DIR, "activity.html"), "r", encoding="utf-8") as f:
    act_content = f.read()

with open(os.path.join(TARGET_DIR, "index.html"), "r", encoding="utf-8") as f:
    hub_content = f.read()

# Integrate Persian into presentation.html
# We inject fa into SLIDES_DB and add the FA button to the header
fa_pres_json = json.dumps(fa_presentation, ensure_ascii=False)
pres_content = pres_content.replace(
    'const SLIDES_DB = {',
    f'const SLIDES_DB = {{\n      fa: {fa_pres_json},'
)
pres_content = pres_content.replace(
    '<button id="lang-en" class="btn-ctrl active" onclick="setLanguage(\'en\')" style="border:none; padding:0.2rem 0.6rem;">EN</button>',
    '<button id="lang-en" class="btn-ctrl active" onclick="setLanguage(\'en\')" style="border:none; padding:0.2rem 0.5rem;">EN</button>\n        <button id="lang-fa" class="btn-ctrl" onclick="setLanguage(\'fa\')" style="border:none; padding:0.2rem 0.5rem;">فارسی</button>'
)
pres_content = pres_content.replace(
    "document.querySelectorAll('#lang-en, #lang-ar, #lang-uk')",
    "document.querySelectorAll('#lang-en, #lang-fa, #lang-ar, #lang-uk')"
)
pres_content = pres_content.replace(
    "document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';",
    "document.documentElement.dir = (lang === 'ar' || lang === 'fa') ? 'rtl' : 'ltr';"
)
pres_content = pres_content.replace(
    ":root:lang(ar) {",
    ":root:lang(ar), :root:lang(fa) {\n      font-family: 'IBM Plex Sans Arabic', 'Inter', sans-serif;\n    }\n    :root:lang(fa) {"
)

with open(os.path.join(TARGET_DIR, "presentation.html"), "w", encoding="utf-8") as f:
    f.write(pres_content)

print("Updated presentation.html with Persian (فارسی)!")

# Integrate Persian into activity.html
fa_act_json = json.dumps(fa_activity, ensure_ascii=False)
act_content = act_content.replace(
    'const ACT_DB = {',
    f'const ACT_DB = {{\n      fa: {fa_act_json},'
)
act_content = act_content.replace(
    '<button id="lang-en" class="btn-act" onclick="setLanguage(\'en\')" style="border:none; padding:0.3rem 0.6rem;">EN</button>',
    '<button id="lang-en" class="btn-act" onclick="setLanguage(\'en\')" style="border:none; padding:0.3rem 0.5rem;">EN</button>\n          <button id="lang-fa" class="btn-act" onclick="setLanguage(\'fa\')" style="border:none; padding:0.3rem 0.5rem;">فارسی</button>'
)
act_content = act_content.replace(
    "document.querySelectorAll('#lang-en, #lang-ar, #lang-uk')",
    "document.querySelectorAll('#lang-en, #lang-fa, #lang-ar, #lang-uk')"
)
act_content = act_content.replace(
    "document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';",
    "document.documentElement.dir = (lang === 'ar' || lang === 'fa') ? 'rtl' : 'ltr';"
)
act_content = act_content.replace(
    ":root:lang(ar) {",
    ":root:lang(ar), :root:lang(fa) {\n      font-family: 'IBM Plex Sans Arabic', 'Inter', sans-serif;\n    }\n    :root:lang(fa) {"
)

with open(os.path.join(TARGET_DIR, "activity.html"), "w", encoding="utf-8") as f:
    f.write(act_content)

print("Updated activity.html with Persian (فارسی)!")

# Integrate Persian into index.html
fa_hub_json = json.dumps(fa_hub, ensure_ascii=False)
hub_content = hub_content.replace(
    'const HUB_DB = {',
    f'const HUB_DB = {{\n      fa: {fa_hub_json},'
)
hub_content = hub_content.replace(
    '<button id="l-en" class="lang-btn active" onclick="setLang(\'en\')">EN</button>',
    '<button id="l-en" class="lang-btn active" onclick="setLang(\'en\')">EN</button>\n        <button id="l-fa" class="lang-btn" onclick="setLang(\'fa\')">فارسی</button>'
)
hub_content = hub_content.replace(
    "document.querySelectorAll('#l-en, #l-ar, #l-uk')",
    "document.querySelectorAll('#l-en, #l-fa, #l-ar, #l-uk')"
)
hub_content = hub_content.replace(
    "document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';",
    "document.documentElement.dir = (lang === 'ar' || lang === 'fa') ? 'rtl' : 'ltr';"
)
hub_content = hub_content.replace(
    ":root:lang(ar) {",
    ":root:lang(ar), :root:lang(fa) {\n      font-family: 'IBM Plex Sans Arabic', 'Inter', sans-serif;\n    }\n    :root:lang(fa) {"
)

with open(os.path.join(TARGET_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(hub_content)

print("Updated index.html with Persian (فارسی)!")
print("ALL 4-WAY MULTILINGUAL ASSETS COMPLETE (EN, FA, AR, UK)!")
"""

with open(r"c:\Users\mlingsch\beattieNetTrack\scripts\build_persian_integration.py", "w", encoding="utf-8") as f:
    f.write(builder_script)

print("Created build_persian_integration.py")
