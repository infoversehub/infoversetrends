"""
InfoVerse Hub V2
Prompt Builder
"""


def build_prompt(topic):
    """
    Build ChatGPT prompt.
    """

    title = topic.get("title", "")
    summary = topic.get("summary", "")
    source = topic.get("link", "")
    category = topic.get("category", "")

    prompt = f"""
# Topic

Title:
{title}

Category:
{category}

Summary:
{summary}

Source:
{source}

--------------------------------------------

Write a comprehensive SEO article in HTML.

Requirements:

- Write only the article.
- Do NOT generate html/head/body.
- Do NOT generate CSS.
- Do NOT generate JavaScript.
- Use only:

<h2>
<h3>
<p>
<ul>
<li>
<table>

Generate:

- SEO Title
- Meta Description
- Article
- FAQ
- Tables when needed
- Lists when needed

The article should be well-structured, original, easy to read, and approximately 1200-1800 words.

Return HTML only.
"""

    return prompt
