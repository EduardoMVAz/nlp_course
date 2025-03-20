import os
from dotenv import load_dotenv
import pandas as pd
import google.generativeai as genai
from pathlib import Path
import json

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Get the path for this file
current_file_path = Path(__file__).resolve().parent

# Load the notebook
notebook_path = current_file_path / 'test01-machine_learning.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Get the code cells
code_cells = [
    cell for cell in notebook['cells'] if cell['cell_type'] == 'code'
    and ''.join(cell['source']).startswith('#exercicio')
]

source1 = ''.join(code_cells[0]['source'])
source2 = ''.join(code_cells[1]['source'])

prompt1 = f"""
Você está recebendo a solução de um aluno em relação a uma questão de machine learning. Trata-se de uma questão de classificação de texto. O aluno utilizou um modelo de classificação de texto para classificar reviews de produtos em positivos e negativos. O código do aluno está abaixo. Analise o código e responda as perguntas abaixo.

Código: {source1}

Para cada uma dssas perguntas, utilize apenas as informações presentes no código do aluno. Se o código estiver vazio, responda apenas: "Código vazio".
Se a resposta para alguma das perguntas não estiver o texto, responda: "Informação não encontrada". Caso esteja, inclua um trecho da resposta do aluno que justifique a sua avaliação.

0. O sistema usa, de fato, um modelo bag-of-words para classificação?
1. Qual é o modelo de vetorização de texto usado?
2. Qual é a justificativa apresentada pelo aluno para a escolha do modelo de vetorização de texto?
3. Qual é o modelo de classificação utilizado?
4. Qual é a justificativa apresentada pelo aluno para a escolha do modelo de classificação?
5. Qual é (são) a(s) métrica(s) de avaliação utilizadas pelo aluno?
6. Qual é a justificativa do aluno para cada uma das métricas?
7. Como o aluno lida com o desbalanço na base de dados?
"""

generation_config = genai.GenerationConfig(
    max_output_tokens=1000,
    temperature=0.0,
)

# Use our prompt
model = genai.GenerativeModel(model_name="gemini-2.0-flash")
response = model.generate_content(prompt1, generation_config=generation_config)

print("AVALIAÇÃO DA QUESTÃO 1")
print(response.text)

prompt2 = f"""
Você está recebendo a solução de um aluno em relação a uma questão de machine learning. Trata-se de uma questão de interpretação de um modelo. O código do aluno está abaixo. Analise o código e responda as perguntas abaixo.

Código: {source2}

Para cada uma dssas perguntas, utilize apenas as informações presentes no código do aluno. Se o código estiver vazio, responda apenas: "Código vazio".
Se a resposta para alguma das perguntas não estiver o texto, responda: "Informação não encontrada". Caso esteja, inclua um trecho da resposta do aluno que justifique a sua avaliação.

0. O aluno avalia a importância das features para classificações positivas e negativas? Se sim, como?
1. O uso de cada elemento do sklearn está justificado? Há elementos usados sem justificativa?
2. O aluno usa comentários no código para explicar como suas descobertas corroboram, contradizem, ou relativizam o que foi proposto pelo LLM?
3. O aluno apresenta números que justifiquem suas conclusões quanto a concordar ou não com o LLM? 
"""

generation_config = genai.GenerationConfig(
    max_output_tokens=1000,
    temperature=0.0,
)

# Use our prompt
model = genai.GenerativeModel(model_name="gemini-2.0-flash")
response = model.generate_content(prompt2, generation_config=generation_config)

print("AVALIAÇÃO DA QUESTÃO 2")
print(response.text)
