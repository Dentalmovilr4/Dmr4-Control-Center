import google.generativeai as genai
import os

# Configuramos la IA de Google
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def obtener_analisis_ia(coin_name, change, score):
    try:
        prompt = (
            f"Actúa como un experto en trading de la firma DMR4 AI. "
            f"Analiza esta moneda: {coin_name}, que tuvo un cambio de {change}% "
            f"y un score técnico de {score}/100. "
            f"Escribe un resumen muy breve (2 frases) para Telegram sobre si es "
            f"buen momento para entrar o esperar. Usa un tono profesional y directo."
        )
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # Si falla la IA, devolvemos un mensaje estándar de respaldo
        return "Análisis técnico en proceso. Manténgase alerta a los indicadores."
