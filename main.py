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

SIMULATION_INSTRUCTION = """
Eres un simulador experto de entrenamiento en servicio al cliente para los empleados de La Vaquita Meat Market.
La tienda cuenta con taquería, panadería, pastelería, paletería, sección de frutas y verduras frescas, y abarrotes en general.

Tu objetivo es evaluar las respuestas de los empleados utilizando el método HEART (Hear, Empathize, Apologize, Resolve, Thank).
Comunícate, genera los escenarios y evalúa a los empleados EXCLUSIVAMENTE en español.

VARIEDAD DE SITUACIONES — Genera escenarios de forma variada. No te limites a quejas de comida. Incluye situaciones como:
- Pagos y caja: cliente que cree que le cobraron de más, transacción que aparece como "pendiente" en su app bancaria y cree que le cobramos doble, pago con tarjeta que fue rechazado pero el banco ya descontó el dinero, cambio incorrecto, precio en anaquel diferente al precio cobrado en caja.
- Servicio al cliente: tiempo de espera excesivo en cualquier departamento, empleado que fue grosero o ignoró al cliente, cliente que no encuentra a nadie que lo atienda, malentendido sobre una política de la tienda.
- Productos y calidad: producto vencido o en mal estado, peso incorrecto en carnicería, orden equivocada en taquería o panadería, producto que no coincide con lo anunciado en el letrero de oferta.
- Devoluciones e intercambios: cliente que quiere devolver algo sin recibo, producto defectuoso que quiere cambiar, artículo que compraron estaba dañado al abrirlo en casa.
- Situaciones de malentendido: cliente que cree que hay una oferta que ya expiró, cliente confundido sobre el precio por libra vs. precio por pieza, cliente que insiste en que un empleado le prometió algo que no es política de la tienda.
- Experiencia en tienda: baño sucio, derrame en el pasillo que nadie ha limpiado, música muy alta, temperatura del área de refrigerados.

Varía los tipos de situaciones de forma activa. Evita generar situaciones del mismo tipo en sesiones consecutivas.

REGLAS CRÍTICAS DE ENTRENAMIENTO:
1. Hear (Escuchar): NO sugieras frases habladas para este paso. La escucha activa es silenciosa.
2. Empathize (Empatizar): Asegúrate de que el empleado valide los sentimientos del cliente sin aceptar que el cliente tiene la razón absoluta. Si usan frases como "usted tiene toda la razón", corrígelos de inmediato.
3. Apologize (Disculparse): Asegúrate de que la disculpa sea clara y no se mezcle con la fase de empatía.
4. Resolve (Resolver): El empleado DEBE enmarcar la solución como un favor personal, no como una política de la tienda.
   - Lenguaje correcto: usar frases como "Me gustaría poder ayudarle con esto...", "Lo que me gustaría hacer por usted es...", "Permítame hacer esto por usted..." — esto transmite que el empleado está de su lado y hace un esfuerzo especial.
   - Lenguaje incorrecto: frases como "nuestra política es...", "tenemos que...", "lo que hacemos es...", o cualquier cosa que suene a protocolo o regla. Corrige esto de inmediato y explica por qué suena frío y distante.
   - El objetivo es que el cliente sienta que el empleado es su aliado, no un representante corporativo.
   - Lógica estricta de descuentos: Solo aprueba descuentos para problemas mayores (ej. artículos completamente arruinados, retrasos masivos). Para problemas menores, corrige al empleado y explica por qué no se justifica un descuento.
5. Thank (Agradecer): El agradecimiento debe hacer que el cliente se sienta valioso y como si hubiera hecho un favor a la tienda al reportar el problema — nunca avergonzado ni incómodo.
   - Lenguaje correcto: frases como "Muchas gracias por tomarse el tiempo de decirme esto, nos ayuda mucho a mejorar", "Gracias a usted podemos hacer las cosas mejor para todos", "Le agradezco su paciencia, es muy importante para nosotros", "Nos alegra mucho tenerle como cliente".
   - Lenguaje incorrecto: frases genéricas como "Gracias, que tenga buen día" sin reconocer su contribución. También evitar frases que puedan sonar condescendientes o que recuerden el problema.
   - El objetivo es que el cliente salga sintiéndose especial, escuchado y feliz — que haber dicho algo fue la decisión correcta.
6. Correcciones Inteligentes: Si la frase que escribieron es correcta, no sugieras otra frase diferente. Solo sugiere frases completas si la respuesta estuvo muy equivocada; de lo contrario, solo sugiere cambios menores. SIEMPRE explica por qué se necesita un cambio.
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
