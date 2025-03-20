import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
from pathlib import Path

current_file_path = Path(__file__).resolve().parent
df = pd.read_csv(current_file_path / 'reviews.csv')
df.head()

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Make our prompt here
prompt = f"""
Este é um conjunto de reviews recebidos por uma empresa de e-commerce. A empresa quer saber o que os clientes estão achando dos produtos e serviços.
Encontre qual é o elemento mais comuns que os clientes estão elogiando e qual é os elementos mais comuns que os clientes estão reclamando.
{df['review_comment_message'].sample(100).values}
"""

generation_config = genai.GenerationConfig(
    max_output_tokens=1000,
    temperature=0.0,
)

# Use our prompt
model = genai.GenerativeModel(model_name="gemini-2.0-flash")
response = model.generate_content(prompt, generation_config=generation_config)

print(response.text)
