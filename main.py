import requests
import io
import re
import argparse
import asyncio
from gepetto import ollama, groq
import PyPDF2
from bs4 import BeautifulSoup

ua_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}
recipe_idea_prompt = """
I am a UK-based cook and have the following ingredients. Could you give me some recipe ideas for using them?
"""
meal_plan_prompt = """
I am a UK-based cook and have the following ingredients. Could you give me a week meal-plan which uses them?
"""
weights = """
Please use UK weights and measures and respond in markdown format!
"""

def find_pdf_links(url):
    # use BeautifulSoup to extract all the links from the contents of the url that link to pdfs

    response = requests.get(url, headers=ua_headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = []
    links = soup.find_all('a')
    pdf_links = [link.get('href') for link in links if link.get('href') and link.get('href').endswith('.pdf')]
    return pdf_links

def extract_text_from_pdf(pdf_url):
    # download the pdf
    response = requests.get(pdf_url, headers=ua_headers)
    # use PyPDF2 to extract the text from the pdf
    pdf = PyPDF2.PdfReader(io.BytesIO(response.content))

    text = ''
    for page in pdf.pages:
        text += page.extract_text()
    return text


def get_ingredients(extracted_pdf_text, organic=True, box_type="ROOTS NO FRUITS"):
    # Define the pattern for box sections
    section_pattern = r"ORGANIC BOXES" if organic else r"NON-ORGANIC BOXES"
    box_pattern = box_type.upper() + r":\s*([^\n]+)"

    # Find the relevant section for organic or non-organic
    section_match = re.search(section_pattern + r"(.*?)ORGANIC BOXES" if not organic else r"(.*?)$", extracted_pdf_text, re.DOTALL)
    if section_match:
        section_text = section_match.group(1)

        # Find the box type within the section
        box_match = re.search(box_pattern, section_text)
        if box_match:
            ingredients = box_match.group(1).split()
            ingredients = [re.sub(r'syboes,', 'spring onions,', ingredient, flags=re.IGNORECASE) for ingredient in ingredients]
            return " ".join(ingredients)
        else:
            return "Box type not found."
    else:
        return "Section not found."

async def chat_with_bot(ingredients):
    # bot = ollama.OllamaModel()
    bot = groq.GroqModel()
    response = await bot.chat([{"role": "user", "content": f"{recipe_idea_prompt} {weights} <ingredients>{ingredients}</ingredients>"}])
    recipe_ideas = response.message
    response = await bot.chat([{"role": "user", "content": f"{meal_plan_prompt} {weights} <ingredients>{ingredients}</ingredients>"}])
    meal_plan = response.message
    return recipe_ideas, meal_plan


def main(url, veg_box_type):
    # allow passing two parameters - an organic boolean and a veg box type string - using argparse
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--organic', action='store_true', help='Is the box organic?')

    arg_parser.add_argument('veg_box_type', type=str, help='The type of veg box, eg "MEDITERRANEAN" or "ROOTS NO FRUITS"')
    args = arg_parser.parse_args()
    organic = args.organic
    veg_box_type = args.veg_box_type
    pdf_links = find_pdf_links(url)
    text = ''
    for pdf_link in pdf_links:
        text += extract_text_from_pdf(pdf_link)
    ingredients = get_ingredients(text, organic, veg_box_type)
    if ingredients:
        print(f"Ingredients: {ingredients}")
        print(f"Chatting with bot to get recipe ideas...")
        recipe_ideas, meal_plan = asyncio.run(chat_with_bot(ingredients))
        print(f"Recipe ideas: {recipe_ideas}")
        print(f"Meal plan: {meal_plan}")
        with open('recipe_ideas.md', 'w') as f:
            f.write(f"# Ingredients\n\n {ingredients}\n\n")
            f.write(f"# Recipe Ideas\n\n {recipe_ideas}\n\n")
            f.write(f"# Meal Plan\n\n {meal_plan}\n\n")

if __name__ == '__main__':
    main('https://vegbox.rootsfruitsandflowers.com/what-is-in-my-veg-box/', 'MEDITERRANEAN')
