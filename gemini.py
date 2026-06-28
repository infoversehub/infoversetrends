import time
import json
import google.generativeai as genai

from config import GEMINI_API_KEY

# ==========================================
# CONFIGURE GEMINI
# ==========================================

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)
# ==========================================
# BUILD PROMPT
# ==========================================

def build_prompt(topic):

    language = topic.get("language", "ar")

    if language == "ar":

        return f"""
أنت كاتب محتوى SEO عالمي وخبير في كتابة المقالات المتوافقة مع Google.

اعتمد على المعلومات التالية فقط لفهم الموضوع، ولا تنسخها حرفياً.

العنوان:
{topic["title"]}

الملخص:
{topic["summary"]}

المصدر:
{topic["source"]}

الرابط:
{topic["link"]}

========================

اكتب مقالاً عربياً احترافياً وفريداً 100%.

الشروط:

- لا تذكر أنك ذكاء اصطناعي.
- لا تذكر أنك اعتمدت على مصدر.
- لا تنسخ أي فقرة.
- اكتب بأسلوب بشري.
- اجعل المقال مناسباً لمحركات البحث.
- اكتب مقالاً لا يقل عن 400 كلمة ولا يزيد عن 1000 كلمة.
- اكتب مقالاً كاملاً ومترابطاً دون اختصار مخل.
- إذا لم تستطع إكمال المقال في رد واحد فلا تختصر المحتوى.
- لا تكتب ملخصاً.
- اكتب المقال كاملاً بجميع الأقسام المطلوبة.

أرجع النتيجة بصيغة JSON فقط.

ويجب أن يحتوي JSON على:

title
seo_title
slug
meta_description
category
tags
keywords
article

داخل article:

إذا كان الموضوع عن جهاز أو هاتف أو سيارة أو منتج تقني فيجب أن يتضمن:

- المواصفات الكاملة.
- المميزات.
- العيوب.
- مقارنة مع الإصدار السابق.
- مقارنة مع أبرز المنافسين.
- السعر.
- تاريخ الإطلاق.
- هل يستحق الشراء؟
- أسئلة شائعة FAQ.
- مقدمة
- H2
- H3
- جدول إذا احتاج
- FAQ
- خاتمة
- لا تستخدم Markdown.
- استخدم HTML فقط مثل:
<h2>
<h3>
<p>
<ul>
<li>

لا تضف أي كلام خارج JSON.
"""

    return f"""
You are a professional SEO writer.

Write a unique human-quality article.

Topic:

Title:
{topic["title"]}

Summary:
{topic["summary"]}

Source:
{topic["source"]}

Requirements:

- 1800-2500 words.
- Human writing.
- No plagiarism.
- SEO optimized.
- Return JSON only.

JSON must contain:

title
seo_title
slug
meta_description
category
tags
keywords
article

The article must include:

- Introduction
- H2
- H3
- FAQ
- Conclusion

Use HTML tags only.

Return JSON only.
"""
# ==========================================
# GENERATE ARTICLE
# ==========================================

def generate_article(topic):

    prompt = build_prompt(topic)

    try:

        response = model.generate_content(
    prompt,
    generation_config={
        "temperature": 0.7,
        "max_output_tokens": 8192,
    }
)

        text = response.text.strip()

        print("=" * 50)
print(text)
print("=" * 50)
        # إزالة Markdown إذا أضافه Gemini

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        text = text.strip()

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:

            raise Exception(
                "JSON not found."
            )

        json_text = text[start:end + 1]

        article = json.loads(
            json_text
        )

        return article

    except Exception as e:

        print("=" * 50)
        print("Gemini Error")
        print(e)
        print("=" * 50)

        return None
# ==========================================
# PUBLIC FUNCTION
# ==========================================

def create_article(topic):

    for attempt in range(3):

        article = generate_article(topic)

        if article is not None:

            return {
                "success": True,
                "data": article
            }

        print(
            f"Retry {attempt + 1}/3..."
        )

        time.sleep(2)

    return {
        "success": False,
        "error": "Failed to generate article."
    }
