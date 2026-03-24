import os
from google import genai
from google.genai import types

# --- CONFIGURACIÓN ---
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("⚠️ Error: No se encontró la GEMINI_API_KEY.")
    exit()

client = genai.Client(api_key=api_key)

seguridad_baja = [
    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"),
]

# --- LAS INSTRUCCIONES DEL ACTOR (CON LA REGLA DE TIEMPO REFORZADA) ---
actor_instrucciones = """
Eres el Actor del simulador de rol interactivo en La Vaquita Meat Market. 
TU ÚNICO OBJETIVO: Actuar como un cliente de forma hiperrealista. TÚ NO EVALÚAS AL GERENTE. 

REGLAS DE FORMATO:
1. Tu primer mensaje debe tener:
**Escenario:** [Descripción objetiva en TERCERA PERSONA].
**Cliente:** "[Tu queja en primera persona]".
2. Luego, SOLO escribe lo que dices en voz alta. Cero asteriscos.

REGLA DE SENTIDO COMÚN (TIEMPO - REGLA ESTRICTA): 
¡Usa la lógica humana! Si condujiste de regreso a la tienda para quejarte, tienes unos minutos de sobra. 
PROHIBIDO: Tienes estrictamente prohibido rechazar una solución rápida (5 a 10 minutos). Si el gerente ofrece arreglar tu problema en ese lapso de tiempo, tu ÚNICA opción válida es aceptarlo con alivio (ej. "Está bien, pero por favor apúrese" o "Gracias, lo esperaré") y TERMINAR LA SIMULACIÓN. No discutas con las leyes de la física.

REGLAS DE DIFICULTAD:
- MEDIO: Estás frustrado por un error de la tienda. Eres un humano razonable. Si el gerente te ofrece la solución obvia (cambiarte la carne rápidamente), ACEPTA y vete. NO alargues la conversación. NUNCA insultes.

CÓMO TERMINAR LA SIMULACIÓN:
Si aceptas la solución, escribe tu última frase y luego, EN UNA NUEVA LÍNEA, escribe exactamente: FIN DE LA SIMULACIÓN
No des retroalimentación.
"""

# --- TUS RESPUESTAS DE PRUEBA ---
# El script enviará estas respuestas automáticamente una por una.
respuestas_gerente = [
    "Entiendo su frustracion. Me setiria igual si no recibiera la carne que queria. Lo siento por nuestra equivocacion. Le cambio la carne por la correcta para que regrese con sus hijos; permitame 5 minutos.",
    "Le aseguro que estará lista. Gracias por su paciencia."
]

print("\n" + "="*50)
print("🚀 INICIANDO TEST AUTOMATIZADO")
print("="*50 + "\n")

# Iniciamos el chat
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(system_instruction=actor_instrucciones, safety_settings=seguridad_baja)
)

# Forzamos al AI a generar el escenario exacto que te dio problemas
hidden_prompt = "Inicia la simulación en dificultad MEDIO. Tu queja: Compraste un T-Bone para una cena, llegaste a casa y te diste cuenta que te dieron el corte equivocado. Volviste a la tienda y dejaste a tus hijos esperando en el carro con el aire apagado. Estás molesto por el error y el tiempo perdido."

print("Generando escenario...\n")
response = chat.send_message(hidden_prompt)
print(f"🤖 CLIENTE (INICIO):\n{response.text}\n")
print("-" * 50)

# El bucle automático que dispara tus respuestas
for respuesta in respuestas_gerente:
    print(f"👨‍💼 GERENTE:\n{respuesta}\n")
    
    response = chat.send_message(respuesta)
    print(f"🤖 CLIENTE:\n{response.text}\n")
    print("-" * 50)
    
    if "FIN DE LA SIMULACIÓN" in response.text.upper():
        print("✅ EL CLIENTE ACEPTÓ Y TERMINÓ LA SIMULACIÓN.")
        break

print("\n🏁 TEST FINALIZADO\n")
