import os

import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

generation_config = {
  "temperature": 0,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config
)

reviews = pd.read_csv('reviews-entrega-MercadoAgil-imagens.csv')
for index, review in reviews.iterrows():
  reviewer_id = review['reviewer_id']
  reviewer_email = review['reviewer_email']
  review_image = review['review_image']

  print(f'Processando imagem do review {reviewer_id} de {reviewer_email}...')
  arquivo_imagem = genai.upload_file(path=f'image/{review_image}')
  prompt = 'Transcreva detalhadamente o arquivo de imagem em anexo.'
  response = model.generate_content([prompt, arquivo_imagem])
  with open(f"transcricoes-imagem/{reviewer_id}.txt", "w", encoding="utf-8") as arquivo:
    print(f'Salvando transcrição do imagem do review {reviewer_id} de {reviewer_email}...')
    arquivo.write(response.text)