import os
import logging
import google.generativeai as genai
import httpx
from bs4 import BeautifulSoup
from typing import Optional
from urllib.parse import urlparse

# Configuração do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logging.warning("GEMINI_API_KEY não configurada. Funcionalidade de checagem limitada.")


def is_url(text: str) -> bool:
    """Verifica se o texto é uma URL válida."""
    try:
        result = urlparse(text.strip())
        return all([result.scheme, result.netloc])
    except Exception:
        return False


async def extract_text_from_url(url: str) -> Optional[str]:
    """Extrai o texto principal de uma URL."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            for script in soup(["script", "style"]):
                script.decompose()
            main_content = (
                soup.find("main")
                or soup.find("article")
                or soup.find(
                    "div",
                    class_=lambda x: x
                    and ("content" in x.lower() or "article" in x.lower())
                )
                or soup.find("body")
            )
            if main_content:
                text = main_content.get_text(separator=" ", strip=True)
            else:
                text = soup.get_text(separator=" ", strip=True)
            if len(text) > 5000:
                text = text[:5000] + "..."
            return text if text else None
    except Exception as e:
        logging.error(f"Erro ao extrair texto da URL {url}: {e}")
        return None


async def analyze_with_gemini(text: str) -> str:
    """Analisa o texto usando a API do Gemini para detectar fake news."""
    if not GEMINI_API_KEY:
        return "Erro: API do Gemini não configurada. Configure a variável GEMINI_API_KEY."
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"""Analise o seguinte texto e determinando:

        - Se é uma notícia falsa (fake news) ou verdadeira.

        Texto para análise:
        {text}

        Forneça uma análise concisa em português brasileiro com:
        1. Veredito: VERIFICADO, FALSO, ou INDETERMINADO
        2. Uma breve explicação (2-3 frases) do motivo
        3. Pontos-chave que indicam a veracidade ou falsidade

        Formato da resposta:
        VEREDITO: [VERIFICADO/FALSO/INDETERMINADO]
        EXPLICAÇÃO: [sua explicação aqui]
        """
        response = model.generate_content(prompt)
        result = response.text.strip()
        return result
    except Exception as e:
        logging.error(f"Erro ao processar com Gemini: {e}")
        return f"Erro ao processar a análise: {str(e)}"


async def process_check(text_or_url: str) -> str:
    """Processa uma checagem: extrai texto se for URL e analisa com Gemini."""
    # Verifica se é URL
    if is_url(text_or_url):
        logging.info(f"Detectada URL: {text_or_url}")
        extracted_text = await extract_text_from_url(text_or_url)
        if not extracted_text:
            return "Erro: Não foi possível extrair o texto da URL fornecido."
        logging.info(f"Texto extraído da URL ({len(extracted_text)} caracteres)")
        text_to_analyze = f"URL: {text_or_url}\n\nConteúdo extraído:\n{extracted_text}"
    else:
        text_to_analyze = text_or_url
    result = await analyze_with_gemini(text_to_analyze)
    return result
