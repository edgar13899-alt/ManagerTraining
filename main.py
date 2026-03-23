import streamlit as st
from google import genai
from google.genai import types
import os

# 1. Conectar con la IA
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("¡Falta la clave API! Por favor, agrega GEMINI_API_KEY a los Secrets de Replit.")
    st.stop()

client = genai.Client(api_key=api_key)

# ── System instructions ──────────────────────────────────────────────────────

system_instruction = """
    Eres un simulador de rol interactivo para entrenar empleados y gerentes en La Vaquita Meat Market. 
    Departamentos: taquería, panadería, pastelería, paletería, frutas/verduras frescas y abarrotes.

    TU OBJETIVO:
    Actuar como el cliente en una conversación continua de ida y vuelta. NO evalúes de inmediato. Responde a lo que te diga el gerente, reacciona a su tono y pon a prueba sus habilidades antes de aceptar una solución.

    REGLAS DE ACTUACIÓN (Dependiendo de la dificultad elegida):
    - FÁCIL: Eres razonable. Si el gerente es amable, escucha y ofrece una solución justa, acéptala rápidamente y sé agradecido.
    - MEDIO: Estás apurado y frustrado. Pon peros a su primera solución (ej. "Sí, pero ya perdí 20 minutos"). Haz preguntas difíciles. Cede solo si muestran buena empatía y una resolución verdaderamente útil.
    - DIFÍCIL: Estás furioso. Interrumpe al gerente. Haz un escándalo público. 
        * Curva de Reubicación: Si estás gritando y el gerente intenta resolver el problema en medio de la tienda sin pedirte que te muevas a un área más privada (como el mostrador de servicio al cliente o una mesa), haz tu escándalo MÁS FUERTE y quéjate de que todos te están viendo.
        * Límite de Abuso (Trampa): Ocasionalmente, cruza la línea con un insulto o actitud denigrante. Si el gerente solo se disculpa y acepta el abuso verbal, sé más agresivo. El gerente DEBE establecer un límite firme (ej. "Le pido que nos comuniquemos con respeto"). Si establecen el límite, cálmate un poco o retírate de la tienda.

    CÓMO TERMINAR LA SIMULACIÓN Y EVALUAR:
    Mantente en tu personaje durante varios intercambios (3 a 6 mensajes), o hasta que el gerente resuelva el problema satisfactoriamente, o hasta que el gerente establezca un límite firme ante un insulto. 
    CUANDO LA INTERACCIÓN LLEGUE A SU FIN NATURAL, escribe en negritas "### [FIN DE LA SIMULACIÓN]" y sal de tu personaje. 
    Inmediatamente después, proporciona una evaluación completa del desempeño del gerente utilizando el método HEART:
    - H (Hear): ¿Guardaron silencio y no te interrumpieron inicialmente?
    - E (Empathize): ¿Validaron tu frustración sin darte la razón absoluta?
    - A (Apologize): ¿Fue genuina su disculpa?
    - R (Resolve): ¿Te reubicaron correctamente según el departamento? ¿La solución fue buena sin regalar demasiado?
    - T (Thank): ¿Agradecieron tu paciencia?
    """
LEARN_INSTRUCTION = """
Eres un instructor experto del método HEART para empleados de La Vaquita Meat Market.
Tu misión es enseñar cada paso del método HEART de forma interactiva, uno por uno, en este orden: H → E → A → R → T.
Comunícate EXCLUSIVAMENTE en español.

VARIEDAD DE SITUACIONES — Las situaciones de práctica no deben limitarse a quejas de comida. Varía activamente entre:
- Pagos y caja: cobro de más, transacción "pendiente" en app bancaria que el cliente cree que es doble cobro, tarjeta rechazada pero el banco ya descontó, cambio incorrecto, precio en anaquel diferente al cobrado.
- Servicio al cliente: tiempo de espera excesivo, empleado que fue grosero, nadie disponible para atender, malentendido sobre política de la tienda.
- Productos y calidad: producto vencido, peso incorrecto en carnicería, orden equivocada, producto que no coincide con el anuncio de oferta.
- Devoluciones: quiere devolver sin recibo, producto defectuoso, artículo dañado al abrirlo en casa.
- Malentendidos: oferta que ya expiró, confusión precio por libra vs. precio por pieza, cliente insiste en que un empleado le prometió algo.
- Experiencia en tienda: baño sucio, derrame sin limpiar, temperatura de refrigeradores.

ESTRUCTURA DE CADA LECCIÓN:
1. Explica el paso actual de forma clara y concisa (qué es, por qué importa, qué errores evitar).
2. Presenta una situación corta y realista de cliente de La Vaquita — escoge de la variedad de situaciones de arriba, no solo quejas de comida.
3. Pide al empleado que escriba SOLO la respuesta correspondiente a ese paso.
4. Evalúa su respuesta:
   - Si está bien: felicítalo brevemente y avanza al siguiente paso.
   - Si tiene errores: explica exactamente qué estuvo mal y por qué, muestra cómo mejorarla, y pídele que lo intente de nuevo. No avances hasta que lo haga bien.
5. Cuando el empleado domine un paso, anuncia claramente que pasas al siguiente (ej. "¡Excelente! Pasamos ahora al paso E - Empathize.").
6. Al terminar los 5 pasos, felicita al empleado y resume brevemente sus fortalezas y áreas de mejora.
7. Después del resumen, pregúntale al empleado si quiere seguir practicando con una nueva situación o si prefiere ir al Simulador completo. Si dice que sí quiere seguir practicando, crea una nueva situación diferente de cliente de La Vaquita y vuelve a empezar desde el paso H con el mismo nivel de exigencia. Puedes repetir este ciclo tantas veces como el empleado lo desee, siempre con situaciones distintas y departamentos variados.

REGLAS IMPORTANTES:
- Evalúa SOLO el paso que se está practicando en ese momento. No pidas que el empleado haga todos los pasos a la vez.
- Para el paso H (Hear): recuerda que escuchar es silencioso. El empleado debe describir qué haría (ej. "Dejaría que el cliente hable sin interrumpirlo"), NO escribir una frase que diría en voz alta.
- Para el paso E (Empathize): rechaza frases como "usted tiene toda la razón" porque implican que el cliente tiene razón objetivamente.
- Para el paso A (Apologize): asegúrate de que la disculpa sea específica y no se mezcle con la empatía.
- Para el paso R (Resolve): el empleado DEBE sonar como si estuviera haciendo un favor personal, no siguiendo una política. Enseña y exige frases como "Me gustaría poder ayudarle con esto...", "Lo que me gustaría hacer por usted es...", "Permítame hacer esto por usted...". Corrige de inmediato si usan lenguaje de política como "nuestra política es...", "tenemos que..." o "lo que hacemos es...". Explica por qué ese lenguaje suena frío. Solo aprueba descuentos para problemas graves; corrige si los ofrecen por problemas menores.
- Para el paso T (Thank): el agradecimiento debe hacer que el cliente sienta que hizo un favor a la tienda al reportar el problema — que fue la decisión correcta hablar. Exige frases específicas que reconozcan su contribución como "Gracias por tomarse el tiempo de decirme esto, nos ayuda a mejorar" o "Gracias a usted podemos hacer las cosas mejor para todos nuestros clientes". Rechaza agradecimientos genéricos como "Gracias, buen día" sin explicación ni reconocimiento. El objetivo es que el cliente salga sintiéndose especial, valioso y feliz.
- Usa el mismo escenario de cliente durante toda la lección para que haya continuidad.

Comienza presentándote, explicando brevemente cómo funciona esta lección, y empezando inmediatamente con el paso H.
"""

# ── Helpers ──────────────────────────────────────────────────────────────────

def build_chat(instruction, history):
    formatted = [
        types.Content(role=m["role"], parts=[types.Part(text=m["content"])])
        for m in history
    ]
    return client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=instruction),
        history=formatted
    )

def render_history(history):
    for msg in history:
        if not msg.get("hidden", False):
            role = "assistant" if msg["role"] == "model" else "user"
            with st.chat_message(role):
                st.markdown(msg["content"])

def reset():
    for key in ["app_mode", "chat_history", "learn_history"]:
        st.session_state.pop(key, None)
    st.rerun()

# ── Session state defaults ────────────────────────────────────────────────────

if "app_mode" not in st.session_state:
    st.session_state.app_mode = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "learn_history" not in st.session_state:
    st.session_state.learn_history = []

# ── UI ────────────────────────────────────────────────────────────────────────

st.title("🥩 Simulador de Entrenamiento - La Vaquita")

# ── HOME SCREEN ───────────────────────────────────────────────────────────────
if st.session_state.app_mode is None:

    st.info("""
    **El Método HEART: Guía de Resolución para Gerentes**

    **1. H - Hear (Escuchar activamente)**

    Cuando un cliente molesto se comunica contigo, su necesidad principal es sentirse escuchado y comprendido. Este paso se centra en la escucha activa y en permitir que el cliente se desahogue por completo de su frustración antes de que intentes solucionar nada.

    Las acciones clave durante esta etapa incluyen:
    * **Guardar silencio:** Resiste el impulso de interrumpir, defenderte u ofrecer soluciones de inmediato.

    **2. E - Empathize (Empatizar)**

    Una vez que el cliente ha contado su historia, la empatía construye un puente entre escuchar y resolver. Le demuestra al cliente que comprendes sus sentimientos y validas su frustración, incluso si aún no has determinado de quién es la culpa o cómo solucionarlo.

    Las acciones clave para este paso incluyen:
    * **Reflejar su urgencia:** Ajusta tu tono para demostrar que te tomas el asunto tan en serio como ellos.
    * **Validar sus emociones:** Usa frases que reconozcan sus sentimientos específicos (frustración, decepción, pánico) en lugar de solo los hechos logísticos del problema.
    * **Evitar ponerse a la defensiva:** Mantente alejado de citar políticas de la empresa o poner excusas, lo cual invalida de inmediato su experiencia.
    * **Recordar:** Empatizar no significa estar de acuerdo con ellos ni aceptar que tienen la razón absoluta.

    **3. A - Apologize (Ofrecer disculpas)**

    Una disculpa clara y sincera es diferente a la empatía. Este paso consiste en asumir la responsabilidad en nombre de la empresa por la situación que ocurrió.

    Las acciones clave para este paso incluyen:
    * **Ser específico:** Discúlpate por el problema concreto (ej. "Lamento mucho el tiempo de espera en la taquería").
    * **Asumir responsabilidad:** Habla en nombre de la empresa, no solo de ti mismo.
    * **Evitar disculpas falsas:** Frases como "Lamento si esto le causó algún problema" devuelven la culpa al cliente. Sé directo y genuino.

    **4. R - Resolve (Resolver)**

    Este es el momento de solucionar el problema. El cliente debe sentir que estás de su lado y que estás haciendo un esfuerzo especial por él, no simplemente siguiendo un protocolo.

    Las acciones clave para este paso incluyen:
    * **Actuar de inmediato:** Ofrece una solución concreta o explica exactamente qué pasos estás tomando.
    * **Dar opciones:** Siempre que sea posible, ofrece alternativas para que el cliente sienta que tiene el control.
    * **Aplicar descuentos con criterio:** Solo ofrece descuentos o artículos gratis para problemas mayores (artículos arruinados, esperas excesivas). Para problemas menores, una disculpa y solución rápida son suficientes.

    **5. T - Thank (Agradecer)**

    El último paso transforma una experiencia negativa en una positiva y refuerza la lealtad del cliente.

    Las acciones clave para este paso incluyen:
    * **Agradecer sus comentarios:** "Gracias por hacernos saber lo que pasó" muestra que valoras su opinión.
    * **Apreciar su paciencia:** Reconoce el esfuerzo que hicieron al comunicar el problema.
    * **Reafirmar su valor:** Hazles saber que son importantes para la tienda y que esperas verlos pronto.
    """)

    st.divider()
    st.subheader("¿Qué quieres hacer hoy?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📖 Modo Aprendizaje")
        st.write("El instructor te enseña cada paso del método HEART uno por uno. Te corrige en tiempo real y no avanza hasta que domines cada paso.")
        if st.button("Comenzar Lección", use_container_width=True):
            st.session_state.app_mode = "learn"
            st.rerun()

    with col2:
        st.markdown("### 🎭 Modo Simulación")
        st.write("Practica con un cliente real de La Vaquita. El simulador evalúa toda tu respuesta usando el método HEART completo.")
        if st.button("Ir al Simulador", use_container_width=True):
            st.session_state.app_mode = "practice"
            st.rerun()

# ── LEARN MODE ────────────────────────────────────────────────────────────────
elif st.session_state.app_mode == "learn":

    st.markdown("### 📖 Modo Aprendizaje — Método HEART")

    if len(st.session_state.learn_history) == 0:
        with st.spinner("Iniciando tu lección..."):
            chat = build_chat(LEARN_INSTRUCTION, [])
            response = chat.send_message("Comienza la lección.")
        st.session_state.learn_history.append({"role": "user", "content": "Comienza la lección.", "hidden": True})
        st.session_state.learn_history.append({"role": "model", "content": response.text, "hidden": False})
        st.rerun()

    render_history(st.session_state.learn_history)

    user_input = st.chat_input("Escribe tu respuesta aquí...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.learn_history.append({"role": "user", "content": user_input, "hidden": False})

        chat = build_chat(LEARN_INSTRUCTION, st.session_state.learn_history[:-1])
        with st.chat_message("assistant"):
            response = chat.send_message(user_input)
            st.markdown(response.text)
        st.session_state.learn_history.append({"role": "model", "content": response.text, "hidden": False})

    st.divider()
    if st.button("⬅ Volver al Inicio"):
        reset()

# ── PRACTICE / SIMULATION MODE ────────────────────────────────────────────────
elif st.session_state.app_mode == "practice":

    st.markdown("### 🎭 Modo Simulación")

    if len(st.session_state.chat_history) == 0:
        st.write("¿Listo? ¡Elige la dificultad para comenzar!")

        difficulty = st.selectbox(
            "Selecciona el tipo de cliente:",
            [
                "Fácil (Ligeramente decepcionado pero tranquilo)",
                "Medio (Frustrado, firme y buscando una solución rápida)",
                "Difícil (Furioso, exigente, hace un escándalo público y amenaza con quejarse)"
            ]
        )

        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("Comenzar Escenario de Entrenamiento", use_container_width=True):
                hidden_prompt = f"Preséntate brevemente con el empleado en español, explica que hoy practicaremos el método HEART y luego presenta inmediatamente el primer escenario del cliente. El nivel de dificultad debe ser: {difficulty}. Espera la respuesta del empleado antes de evaluar."
                chat = build_chat(SIMULATION_INSTRUCTION, [])
                with st.spinner("Generando tu escenario..."):
                    response = chat.send_message(hidden_prompt)
                st.session_state.chat_history.append({"role": "user", "content": hidden_prompt, "hidden": True})
                st.session_state.chat_history.append({"role": "model", "content": response.text, "hidden": False})
                st.rerun()
        with col2:
            if st.button("⬅ Volver", use_container_width=True):
                reset()

    else:
        render_history(st.session_state.chat_history)

        user_input = st.chat_input("Escribe tu respuesta al cliente aquí...")

        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input, "hidden": False})

            chat = build_chat(SIMULATION_INSTRUCTION, st.session_state.chat_history[:-1])
            with st.chat_message("assistant"):
                response = chat.send_message(user_input)
                st.markdown(response.text)
            st.session_state.chat_history.append({"role": "model", "content": response.text, "hidden": False})

        st.divider()
        if st.button("Reiniciar Simulador / Elegir Nueva Dificultad"):
            st.session_state.chat_history = []
            st.rerun()

        if st.button("⬅ Volver al Inicio"):
            reset()
