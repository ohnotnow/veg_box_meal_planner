# Veg-Box Meal Planner

The Veg-Box Meal Planner is a Python script designed to help you make the most out of your weekly vegetable box. It automatically fetches the latest vegetable box contents from your supplier, generates creative recipe ideas, and even suggests a weekly meal plan based on the ingredients in your box.

## Features

- Fetches the latest PDF containing the contents of your vegetable box.
- Extracts ingredients from the PDF.
- Uses an AI model (groq/mixtral by default) to suggest recipe ideas and a meal plan tailored to the your palette.
- Outputs the recipes and meal plan in Markdown format.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or later.
- Libraries: `requests`, `io`, `re`, `argparse`, `asyncio`, `PyPDF2`, `BeautifulSoup`.
- An API Key for an AI model (eg, OpenAI, Groq, etc - groq is the default https://groq.com/ .  Eg `export GROQ_API_KEY=12345`)

You can install the required libraries using pip:

```bash
pip install -r requirements.txt
```

## Usage

To use the Veg-Box Meal Planner, run the script with the following command:

```bash
python main.py --organic [VEG_BOX_TYPE]
```

Replace `[VEG_BOX_TYPE]` with the type of your veg box, e.g., `MEDITERRANEAN` or `ROOTS NO FRUITS`.

```bash
python main.py --organic 'roots no fruits'
```

The script will print the results to the terminal, and also save them to a markdown file called 'recipe_ideas.md'.

## Customising
There are three prompts that are given to the AI model near the top of the script.  Change those to suit your needs, any special
dietary requirements, etc.

## License

Distributed under the MIT License. See `LICENSE` for more information.
