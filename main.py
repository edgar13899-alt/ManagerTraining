import streamlit as st
import google.generativeai as genai
import os

# 1. Conectar con la IA
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("¡Falta la clave API! Por favor, agrega GEMINI_API_KEY a los Secrets de Replit.")
    st.stop()

genai.configure(api_key=api_key)

# 2. Instrucciones Maestras (El Cerebro de la IA en Español)
system_instruction = """
Eres un simulador experto de entrenamiento en servicio al cliente para los empleados de La Vaquita Meat Market.
La tienda cuenta con taquería, panadería, pastelería, paletería, sección de frutas y verduras frescas, y abarrotes en general.
Genera quejas de clientes realistas basadas en estos departamentos específicos.

Tu objetivo es evaluar las respuestas de los empleados utilizando el método HEART (Hear, Empathize, Apologize, Resolve, Thank).
Comunícate, genera los escenarios y evalúa a los empleados EXCLUSIVAMENTE en español.

REGLAS CRÍTICAS DE ENTRENAMIENTO:
1. Hear (Escuchar): NO sugieras frases habladas para este paso. La escucha activa es silenciosa.
2. Empathize (Empatizar): Asegúrate de que el empleado valide los sentimientos del cliente sin aceptar que el cliente tiene la razón absoluta. Si usan frases como "usted tiene toda la razón", corrígelos de inmediato.
3. Apologize (Disculparse): Asegúrate de que la disculpa sea clara y no se mezcle con la fase de empatía.
4. Resolve (Resolver): El empleado debe presentar las soluciones como si estuviera del lado del cliente (haciendo un favor), no solo recitando la política de la tienda. 
   - Lógica estricta de descuentos: Explica exactamente cuándo se debe o no usar un descuento o artículo gratis. Solo aprueba descuentos para problemas mayores (ej. artículos completamente arruinados, retrasos masivos). Para problemas menores, corrige al empleado y explica por qué no se justifica un descuento para evitar regalar artículos por todo.
5. Correcciones Inteligentes: Si la frase que escribieron es correcta, no sugieras otra frase diferente. Solo sugiere frases completas si la respuesta estuvo muy equivocada; de lo contrario, solo sugiere cambios menores en las palabras/redacción. SIEMPRE explica por qué se necesita un cambio.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction
)

# 3. Configurar la Interfaz de Chat y Ajustes
st.title("🥩 Simulador de Entrenamiento - La Vaquita")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mostrar la guía de enseñanza y el selector de dificultad SOLO si el chat no ha comenzado
if len(st.session_state.chat_history) == 0:
    
    # --- SECCIÓN DE ENSEÑANZA CON TU TEXTO EXACTO ---
    st.info("""
    **El Método HEART: Guía de Resolución para Gerentes**

    **1. H - Hear (Escuchar activamente)**
    Cuando un cliente molesto se comunica contigo, su necesidad principal es sentirse escuchado y comprendido. Este paso se centra en la escucha activa y en permitir que el cliente se desahogue por completo de su frustración antes de que intentes solucionar nada.
    Las acciones clave durante esta etapa incluyen:
    * **Guardar silencio:** Resiste el impulso de interrumpir, defenderte u ofrecer soluciones de inmediato.

    **2. E - Empathize (Empatizar)**
    Una vez que el cliente ha contado su historia (y tú lo has Escuchado), la empatía construye un puente entre escuchar y resolver. Le demuestra al cliente que comprendes sus sentimientos y validas su frustración, incluso si aún no has determinado de quién es la culpa o cómo solucionarlo.
    Las acciones clave para este paso incluyen:
    * **Reflejar su urgencia:** Ajusta tu tono para demostrar que te tomas el asunto tan en serio como ellos.
    * **Validar sus emociones:** Usa frases que reconozcan sus sentimientos específicos (por ejemplo: frustración, decepción, pánico) en lugar de solo los hechos logísticos del problema.
    * **Evitar ponerse a la defensiva:** Mantente alejado de citar políticas de la empresa o poner excusas, lo cual invalida de inmediato su experiencia.
    * Empat
