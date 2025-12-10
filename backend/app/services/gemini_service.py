import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import logging
import re
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup

load_dotenv()

# Configurar a API do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def extract_text_from_url(url: str) -> str:
    try:
        # Validar formato básico de URL
        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL deve começar com http:// ou https://")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Verificar se o conteúdo é HTML
        content_type = response.headers.get('content-type', '').lower()
        if 'html' not in content_type:
            raise ValueError("A URL não retorna conteúdo HTML")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove scripts e styles
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Tenta encontrar o conteúdo principal usando várias estratégias
        article = (soup.find('article') or 
                  soup.find('main') or 
                  soup.find('div', class_=lambda x: x and ('content' in x.lower() or 'article' in x.lower() or 'post' in x.lower())) or
                  soup.find('div', id=lambda x: x and ('content' in x.lower() or 'article' in x.lower() or 'post' in x.lower())))
        
        if article:
            text = article.get_text(separator=' ', strip=True)
        else:
            body = soup.find('body')
            if body:
                text = body.get_text(separator=' ', strip=True)
            else:
                text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text).strip()
        
        if not text or len(text) < 50:
            raise ValueError("Não foi possível extrair conteúdo suficiente da URL")
        
        # Limita o tamanho do texto
        return text[:5000] if len(text) > 5000 else text
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de requisição ao acessar URL {url}: {e}")
        raise ValueError(f"Erro ao acessar a URL: {str(e)}")
    except Exception as e:
        logging.error(f"Erro ao extrair texto da URL {url}: {e}")
        raise ValueError(f"Não foi possível extrair o conteúdo da URL: {str(e)}")


def analyze_news_with_gemini(text: str) -> Dict[str, Any]:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY não configurada no .env")
    
    response_text = ""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        prompt = f"""Você é um verificador de fatos especializado. Analise a seguinte notícia e retorne APENAS um JSON válido com a seguinte estrutura:

        {{
            "score": <número de 0 a 100, onde 0 = falsa e 100 = verídica>,
            "veredito": "<VERDADEIRA ou FALSA ou INCERTA>",
            "explicacao": "<explicação detalhada em português sobre por que essa pontuação foi atribuída>",
            "fontes": [
                "<URL de fonte confiável 1>",
                "<URL de fonte confiável 2>",
                "<URL de fonte confiável 3>"
            ]
        }}

        Notícia para análise:
        {text}

        IMPORTANTE: Retorne APENAS o JSON, sem markdown, sem código, sem explicações adicionais."""

        response = model.generate_content(prompt)
        
        response_text = response.text.strip()
        
        # Remover markdown code blocks
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1]) if len(lines) > 2 else response_text
        
        result = json.loads(response_text)
        
        # Validar e garantir que os campos estão presentes
        if "score" not in result:
            raise ValueError("Resposta do Gemini não contém 'score'")
        if "veredito" not in result:
            raise ValueError("Resposta do Gemini não contém 'veredito'")
        if "explicacao" not in result:
            raise ValueError("Resposta do Gemini não contém 'explicacao'")
        if "fontes" not in result:
            result["fontes"] = []
        
        # Validar que o score está no range correto
        score = int(result["score"])
        if score < 0:
            score = 0
        elif score > 100:
            score = 100
        result["score"] = score
        
        # Validar que fontes é uma lista
        if not isinstance(result["fontes"], list):
            result["fontes"] = []
        
        return result
        
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao fazer parse do JSON da resposta do Gemini: {e}")
        if response_text:
            logging.error(f"Resposta recebida: {response_text}")
        raise ValueError(f"Resposta inválida do Gemini: {str(e)}")
    except Exception as e:
        logging.error(f"Erro ao chamar API do Gemini: {e}")
        raise ValueError(f"Erro ao processar com Gemini: {str(e)}")
