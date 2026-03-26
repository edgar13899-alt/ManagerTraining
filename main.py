import streamlit as st
from google import genai
from google.genai import types
import os
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Entrenamiento La Vaquita", 
    page_icon="🥩",
    layout="centered"
)

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# --- CONEXIÓN IA Y SEGURIDAD ---
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("¡Falta la clave API! Por favor, configúrala en los Secrets de Streamlit.")
    st.stop()

client = genai.Client(api_key=api_key)

seguridad_baja = [
    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"),
]

# --- BÓVEDA DE ESCENARIOS ---
departamentos = ["la Carnicería", "la Taquería", "la Panadería", "la Paletería", "las Cajas Principales", "el Pasillo de Abarrotes", "el área de Frutas y Verduras"]

# CATEGORÍA 1: Errores de la tienda (HEART COMPLETO)
problemas_comunes = [
    "un cliente que YA PAGÓ y llegó a su casa, pero tuvo que regresar muy molesto porque descubrió que le dieron el producto equivocado o le falta un artículo en sus bolsas", 
    "un error en la cocina que causó que una orden previa para recoger se retrasara 20 minutos más de lo prometido, y el cliente está impaciente", 
    "un cliente que YA PAGÓ y revisando su recibo nota que se le cobró de más por un error en el sistema o un letrero confuso, exigiendo la diferencia", 
    "un cliente frustrado que intenta devolver un producto argumentando que salió de mala calidad o echado a perder, PERO NO TIENE SU RECIBO DE COMPRA",
    "un empleado que supuestamente le dio un mal trato, lo ignoró o le habló con mala actitud al cliente"
]

# CATEGORÍA 2: Casos Especiales (ERRORES DEL CLIENTE - OMITIR LA 'A' Y USAR EMPATÍA NEUTRAL)
errores_cliente = [
    "un cliente que por error agarró el producto equivocado (ej. papas picantes en lugar de regulares) y quiere cambiarlo, sintiéndose un poco a la defensiva o avergonzado por su propio error",
    "un cliente que accidentalmente tiró y rompió un frasco de vidrio que ya había pagado antes de salir de la tienda, y pregunta un poco apenado si le pueden dar otro gratis",
    "un cliente que exige un descuento porque leyó mal un letrero de oferta que estaba claramente marcado para otro producto diferente, sintiéndose frustrado"
]

# CATEGORÍA 3: Casos Extremos
pesadillas_la_vaquita = [
    "un pago que aparece como 'pendiente' en la app del banco del cliente porque la terminal falló, y el cliente se niega rotundamente a volver a pasar la tarjeta por miedo a que se le cobre doble",
    "un cliente que recoge un pastel de cumpleaños personalizado en la panadería y exige un reembolso completo más el pastel gratis porque el nombre está mal escrito, a pesar de que el gerente tiene la hoja de pedido donde el cliente mismo escribió mal el nombre",
    "un cliente furioso que, después de recibir su pedido en el mostrador de la carnicería, hace un escándalo al enterarse de que no hay caja registradora ahí y se niega a hacer una segunda fila en las cajas principales para pagar",
    "un cliente que tiene un carrito lleno con $200 dólares en mandado, pero el sistema de EBT/tarjetas de beneficios del gobierno se cae a nivel nacional. No tiene otra forma de pagar y se niega a dejar el carrito.",
    "un cliente que trae un folleto de ofertas de otro mercado hispano (como La Michoacana) y exige a gritos que le igualen el precio en una venta masiva de fajitas que la tienda físicamente no puede permitirse igualar.",
    "un cliente que le pide al carnicero que le corte de manera especial 15 libras de una carne cara. El carnicero la corta, la empaqueta, y cuando el cliente ve el precio impreso, dice 'siempre no lo quiero' y lo deja ahí, dejando a la tienda con producto mermado que no puede regresar a la vitrina.",
    "una mujer que quiere devolver una sopa de pollo de la taquería argumentando agresivamente que está 'demasiado picante', a pesar de que la receta de la tienda NO lleva absolutamente nada de picante y nadie más se ha quejado de eso jamás.",
    "un cliente se queja furioso de que un empleado fue grosero al pedirle ayuda (lo ignoró, no hizo contacto visual y solo señaló con el dedo). El cliente exige que lo despidan o lo castiguen frente a él, PERO el gerente sabe que el familiar de ese empleado acaba de fallecer, está pasando por un duelo terrible, y solo vino a trabajar porque necesitaba el dinero.",
    "un cliente acusa a una cajera de darle un pésimo servicio y aventarle el recibo, exigiendo hablar con el gerente para que la regañe frente a todos, PERO el gerente sabe que la cajera acaba de ser insultada cruelmente por el cliente anterior y está al borde de las lágrimas tratando de mantener la compostura.",
    "un cliente que llega con $50 dólares en cortes caros de carne, no tiene ningún recibo de compra, y exige agresivamente un reembolso en efectivo, amenazando con hacer un escándalo monumental si el gerente se niega a darle el dinero."
]

# --- MENÚ DE NAVEGACIÓN ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Empty.png/120px-Empty.png", use_container_width=True) 
st.sidebar.title("Menú Principal")

menu_selection = st.sidebar.radio(
    "Selecciona un módulo:",
    ["Inicio", "Aprender HEART", "Simulador HEART", "Preguntas al Asesor"]
)

# ==========================================
# MÓDULO 0: INICIO (Dashboard)
# ==========================================
if menu_selection == "Inicio":
    st.title("🏠 Portal de Gerentes - La Vaquita")
    st.write("Bienvenido al centro de entrenamiento y operaciones de La Vaquita Meat Market.")
    
    st.divider()
    
    st.subheader("Ruta de Entrenamiento:")
    
    st.info("📖 **Paso 1: Aprender HEART**\n\nEstudia la metodología oficial y completa el tutorial paso a paso guiado por nuestro instructor virtual.")
    st.warning("🥩 **Paso 2: Simulador HEART**\n\nPon a prueba tus conocimientos en un escenario fluido y realista con clientes difíciles. ¡El simulador evaluará tus respuestas finales!")
    st.success("🧠 **Apoyo: Preguntas al Asesor**\n\nUsa esta herramienta en cualquier momento para hacerle preguntas al asesor virtual sobre cómo manejar situaciones reales en tu turno.")
        
    st.divider()
    st.caption("👈 Usa el menú lateral de la izquierda para comenzar tu entrenamiento.")

# ==========================================
# MÓDULO 1: APRENDER HEART (Tutorial Guiado)
# ==========================================
elif menu_selection == "Aprender HEART":
    st.title("📖 El Método HEART")
    
    st.markdown("""
    ### ¿Qué es el método HEART?
    HEART es un acrónimo que representa un **método paso a paso probado para manejar quejas y situaciones difíciles**. No es solo un guion, es una estrategia psicológica. Te da una estructura clara para calmar la situación, encontrar una solución lógica y despedir al cliente de manera profesional.
    """)
    
    st.divider()
    st.write("### Los 5 Pasos de HEART")
    st.write("Abre y estudia detalladamente cada paso. Luego, baja para completar el Tutorial Guiado.")
    
    with st.expander("👂 H - Hear (Escuchar activamente)", expanded=False):
        st.markdown("""
        Cuando un cliente molesto se comunica contigo, su necesidad principal es sentirse escuchado y comprendido. Sin embargo, **existen dos formas de Escuchar, dependiendo de la situación:**
        
        **1. Escucha Silenciosa (Para el 90% de las quejas comunes):** Si el cliente está molesto por una larga fila o error menor, guarda silencio absoluto. Deja que se desahogue. Interrumpir para hacer preguntas aquí solo los hará enojar más. Usa solo asentimientos verbales ("ya veo", "entiendo").
        
        **2. Escucha Investigativa (Para problemas graves o reembolsos sin recibo):**
        Si el cliente hace una acusación grave o pide un reembolso sin recibo, debes hacer **preguntas de investigación neutrales** *antes* de que termine su historia. 
        *Ejemplo Sin Recibo:* "¿Pagó con tarjeta o en efectivo?". El objetivo es buscar la transacción en el sistema.
        """)

    with st.expander("🤝 E - Empathize (Empatizar)", expanded=False):
        st.markdown("""
        Una vez que el cliente ha contado su historia, la empatía construye un puente. Le demuestra al cliente que comprendes sus sentimientos y validas su frustración.
        
        * **Validar sus emociones:** Usa frases que reconozcan sus sentimientos específicos (frustración, decepción).
        * **Evitar ponerse a la defensiva:** Mantente alejado de citar políticas de la empresa o poner excusas.
        * <u>**Empatizar no significa estar de acuerdo con ellos.**</u>
        """, unsafe_allow_html=True)

    with st.expander("🙏 A - Apologize (Ofrecer disculpas) *¡CUIDADO!*", expanded=False):
        st.markdown("""
        Si el problema es culpa de la tienda, asume la responsabilidad en nombre de la empresa. Usar frases como "Lo siento que le hayamos fallado" es mucho más efectivo que culpar a otro departamento.
        
        🚨 **LA TRAMPA DE LA DISCULPA (Errores del Cliente):**
        Si el problema fue causado por el propio cliente (ej. agarró el producto equivocado, tiró sus propios huevos, leyó mal un letrero), **OMITE ESTE PASO. NO TE DISCULPES.** Disculparte por el error del cliente admite responsabilidad de la tienda y te quita autoridad. Decir "Siento la confusión" es una disculpa disfrazada que también admite culpa. 
        
        En su lugar, usa una **"Empatía Neutral para Salvar el Ego"** en el paso anterior. 
        ❌ *Incorrecto (Culpar a la tienda o asumir):* "Nuestros letreros están muy juntos" o "Seguro venía con prisa".
        ✅ *Correcto (Neutral):* "Entiendo perfectamente la confusión, es un error muy común que a todos nos pasa. Solo para aclarar, el precio correcto es..." y pasa directamente a Resolver (R).
        """)

    with st.expander("🛠️ R - Resolve (Resolver y Reubicar)", expanded=False):
        st.markdown("""
        Después de escuchar y empatizar, este paso se trata de actuar y ser transparente sobre la solución. Resuelve el problema de inmediato si puedes, u ofrece opciones para devolverle al cliente la sensación de control.
        """)

    with st.expander("💖 T - Thank (Agradecer)", expanded=False):
        st.markdown("""
        Agradecer es una manera poderosa de cerrar la conversación. Agradece su paciencia y reafirma la relación expresando que valoras que sean clientes.
        """)

    st.warning("""💰 **REGLA DE RENTABILIDAD SUPREMA Y PROCEDIMIENTOS**

* **Devoluciones Sin Recibo:** ¡No digas 'no' inmediatamente! Pregunta cómo pagaron. Si fue con Tarjeta, pídeles revisar su app. Si fue en Efectivo, haz preguntas para acotar la búsqueda. **SI LA BÚSQUEDA FALLA:** Usa el sistema como escudo. Di: *'Revisé minuciosamente y al no aparecer la transacción, no me es posible autorizar un reembolso.'* * **Error del Cliente:** NUNCA regales dinero, ofrezcas descuentos ni reembolsos monetarios si el cliente causó el problema.
* **Cortesía de Bajo Costo (Agua Fresca / Pan Dulce):** SÍ dar cortesía cuando la cocina comete un error o hay falla del sistema. NO dar cortesía cuando es una fila regular larga en un día ocupado. Regalar producto por el éxito de la tienda destruye las ganancias.
""")
        
    st.error("🛑 **REGLA CERO: ESTABLECER LÍMITES**\nEl respeto hacia ti y tu equipo es innegociable. Si un cliente usa insultos, establece un límite profesional de inmediato. Si continúa, pídele explícitamente que abandone la tienda.")

    st.divider()
    st.subheader("🎓 Tutor Paso a Paso")
    st.write("El Tutor Virtual te presentará un escenario y te guiará letra por letra.")

    tutor_instrucciones = """
    Eres el Tutor Maestro de La Vaquita Meat Market. 
    
    INSTRUCCIONES DE TUTORÍA:
    1. Presenta el escenario conflictivo con una pista en TERCERA PERSONA.
    2. Pregunta: "¿Qué harías para el paso H (Hear)?" y guía secuencialmente (H -> E -> A -> R -> T).
    3. REGLAS ESTRICTAS DE EVALUACIÓN:
       - PROTOCOLO SIN RECIBO: Si el cliente no tiene recibo, DEBEN preguntar cómo pagaron en (H).
       - REGLA DEL GAME MASTER: Si el gerente revisará el sistema, asume el rol del sistema e infórmale el resultado ANTES de pedirle que siga con (R).
       - LA TRAMPA DE LA DISCULPA (Error del cliente): Si el cliente causó el problema (ej. leyó mal un letrero, tiró algo), el gerente DEBE SALTARSE la disculpa (A). Su trabajo en Empatía (E) es usar una "Empatía Neutral para salvar el ego" ("Entiendo la confusión, a todos nos pasa"). ESTÁ PROHIBIDO usar disculpas suaves ("siento la confusión"), culpar a la tienda ("los letreros están juntos") o asumir ("venía con prisa"). Penalízalo si lo hace.
       - SEPARACIÓN DE ETAPAS: Empatía va SOLO en la etapa (E).
       - EMPATÍA VS. ACUERDO: Prohibido aprobar "tiene toda la razón".
       - REGLA DE CORTESÍAS: Cortesías solo para errores de tienda, nunca para filas normales.
    """

    if "tutor_history" not in st.session_state:
        st.session_state.tutor_history = []

    if len(st.session_state.tutor_history) == 0:
        if st.button("Iniciar Tutorial Guiado"):
            with st.spinner("Preparando tu primera lección..."):
                tipo_escenario = random.choices(["comun", "pesadilla", "especial"], weights=[50, 30, 20], k=1)[0]
                if tipo_escenario == "comun":
                    depto_elegido = random.choice(departamentos)
                    problema_elegido = random.choice(problemas_comunes)
                    descripcion_problema = f"La queja trata sobre {problema_elegido}. FÍSICAMENTE: El cliente se acerca a ti (el gerente) en las Cajas Principales."
                elif tipo_escenario == "especial":
                    problema_elegido = random.choice(errores_cliente)
                    descripcion_problema = f"ESTE ES UN CASO ESPECIAL DE ERROR DEL CLIENTE. {problema_elegido}. El cliente se acerca a Cajas."
                else:
                    pesadilla_elegida = random.choice(pesadillas_la_vaquita)
                    descripcion_problema = f"La queja principal DEBE ser exactamente esta: {pesadilla_elegida}."

                hidden_prompt = f"Hola. Genera el escenario inicial usando esta premisa: {descripcion_problema}. Preséntamelo y pídeme que complete el primer paso (H). No me des las respuestas. Código aleatorio: {random.randint(1,10000)}"
                
                try:
                    chat = client.chats.create(
                        model="gemini-2.5-pro",
                        config=types.GenerateContentConfig(system_instruction=tutor_instrucciones, safety_settings=seguridad_baja)
                    )
                    response = chat.send_message(hidden_prompt)
                    texto_seguro = response.text if response.text else "⚠️ *El filtro de seguridad bloqueó la respuesta.*"
                    st.session_state.tutor_history.append({"role": "user", "content": hidden_prompt, "hidden": True})
                    st.session_state.tutor_history.append({"role": "model", "content": texto_seguro, "hidden": False})
                    st.rerun()
                except Exception as e:
                    st.error("⚠️ Servidores ocupados (Error 503). Por favor, intenta de nuevo.")
    else:
        chat_container = st.container()
        
        with chat_container:
            for msg in st.session_state.tutor_history:
                if not msg.get("hidden", False):
                    ui_role = "assistant" if msg["role"] == "model" else "user"
                    with st.chat_message(ui_role):
                        st.markdown(msg["content"])

        tutor_input = st.chat_input("Escribe tu respuesta para el paso actual...")

        if tutor_input:
            st.session_state.tutor_history.append({"role": "user", "content": tutor_input, "hidden": False})

            with chat_container:
                with st.chat_message("user"):
                    st.markdown(tutor_input)

                formatted_tutor_history = []
                for msg in st.session_state.tutor_history[:-1]:
                    formatted_tutor_history.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

                try:
                    chat = client.chats.create(
                        model="gemini-2.5-pro",
                        config=types.GenerateContentConfig(system_instruction=tutor_instrucciones, safety_settings=seguridad_baja),
                        history=formatted_tutor_history
                    )

                    with st.chat_message("assistant"):
                        with st.spinner("El tutor está revisando tu respuesta..."):
                            response = chat.send_message(tutor_input)
                        texto_seguro = response.text if response.text else "⚠️ *El filtro de seguridad bloqueó la respuesta.*"
                        st.markdown(texto_seguro)
                        
                    st.session_state.tutor_history.append({"role": "model", "content": texto_seguro, "hidden": False})
                except Exception as e:
                    st.session_state.tutor_history.pop()
                    st.error("⚠️ Error 503: Servidor ocupado. Vuelve a enviar tu respuesta.")
        
        st.divider()
        if st.button("Reiniciar Tutorial"):
            st.session_state.tutor_history = []
            st.rerun()

# ==========================================
# MÓDULO 2: SIMULADOR HEART (Split-Brain)
# ==========================================
elif menu_selection == "Simulador HEART":
    st.title("🥩 Simulador de Entrenamiento")
    st.write("Practica tus habilidades. Cuando termines, presiona 'Terminar y Evaluar' para recibir feedback del Coach.")

    if "simulador_history" not in st.session_state:
        st.session_state.simulador_history = []
    if "simulador_concluido" not in st.session_state:
        st.session_state.simulador_concluido = False
    if "coach_feedback" not in st.session_state:
        st.session_state.coach_feedback = ""
    if "api_error" not in st.session_state:
        st.session_state.api_error = False

    actor_instrucciones = """
    Eres el Actor del simulador de rol interactivo en La Vaquita Meat Market. 
    TU ÚNICO OBJETIVO: Actuar como un cliente de forma hiperrealista. TÚ NO EVALÚAS AL GERENTE. 

    REGLAS DE FORMATO:
    1. Para tu PRIMER mensaje:
    **Escenario:** [Describe tu lenguaje corporal estrictamente en TERCERA PERSONA].
    **Cliente:** "[Escribe tu queja inicial en voz alta]".
    2. Cero asteriscos después del primer mensaje.

    NUEVA REGLA DEL GAME MASTER (CÁMARAS Y SISTEMA): 
    Si el gerente te dice que va a revisar las cámaras, recibo o sistema POS, sal brevemente de personaje. Añade una línea al principio: "[Sistema: Revisa la cámara/sistema y efectivamente encuentras el recibo / la transacción]". Luego, responde como cliente.

    DETALLES CONTEXTUALES UNIVERSALES: 
    Usa excusas de la vida real. Si es un error Tuyo (ej. agarrar mal producto, romper algo), muéstrate un poco a la defensiva o apenado para salvar tu orgullo.

    REGLA DE SENTIDO COMÚN: 
    Si el gerente te ayuda o te da una solución justa, acéptalo con alivio. NO termines la simulación en ese mismo mensaje. Solo acepta y espera a que el gerente se despida.

    REGLAS DE DIFICULTAD:
    - FÁCIL: Educado.
    - MEDIO: Frustrado. Si dan solución justa, ACEPTA. NUNCA insultes.
    - DIFÍCIL: Pasivo-agresivo y terco. Eres un muro de piedra. 
    - EXTREMO (ABUSIVO): Furioso e insultos. TU OBJETIVO PRINCIPAL es probar si aplican la "Regla Cero". Si te marcan límite estricto, reacciona y vete (escribe FIN DE LA SIMULACIÓN).

    CÓMO TERMINAR LA SIMULACIÓN:
    SOLO DEBES escribir la frase "FIN DE LA SIMULACIÓN" en una línea nueva si el gerente completó la interacción y se despidió (El paso Thank), o si te pidió que te retiraras.
    """

    coach_instrucciones = """
    Eres el Coach Evaluador Maestro de La Vaquita Meat Market. 
    Tu trabajo es analizar la transcripción de la simulación y evaluar al gerente usando el método HEART con una visión comercial implacable.
    
    REGLA DE REESCRITURA Y PSICOLOGÍA:
    Ofrece ejemplos exactos de guiones. "En lugar de decir [Cita], intenta decir: [Tu sugerencia]". Explica la psicología de por qué elegiste esas palabras.

    CRITERIOS DE EVALUACIÓN ESTRICTOS:
    1. PROTOCOLO SIN RECIBO: Si la búsqueda falló, el gerente DEBIÓ usar el sistema como escudo para decir no.
    2. LA TRAMPA DE LA DISCULPA (Saber cuándo omitir la 'A'): Si el problema fue causado por el CLIENTE (ej. leyó mal un precio, tiró algo), verifica si el gerente se disculpó ("lo siento", "siento la confusión"). Si lo hizo, PENALÍZALOS. También penalízalos si culpan a la tienda ("los letreros están juntos") o asumen cosas del cliente ("estaba apurado"). Exígeles usar una "Empatía Neutral para salvar el ego" ("Entiendo la confusión, es un error muy común. Solo para aclarar, el precio es...").
    3. SEPARACIÓN DE ETAPAS (H y E): La empatía va SOLO en la etapa E.
    4. REGLA DE RENTABILIDAD Y CORTESÍAS: Cortesías solo para errores de la tienda.
    5. LÍMITES: En escenarios Extremos con insultos, el gerente DEBE aplicar la Regla Cero.

    AL FINAL DE TU EVALUACIÓN:
    SIEMPRE pregunta: "¿Te gustaría intentar otro escenario o prefieres hacer clic en Reiniciar Simulador?"
    """

    if len(st.session_state.simulador_history) == 0 and not st.session_state.simulador_concluido:
        st.info("Selecciona la dificultad de la situación para comenzar la simulación.")
        difficulty = st.selectbox(
            "Selecciona la complejidad del problema:",
            ["Fácil", "Medio", "Difícil", "Extremo (Abusivo)", "Casos Especiales (Errores del Cliente)"]
        )
        
        if st.button("Comenzar Escenario"):
            if difficulty in ["Fácil", "Medio"]:
                depto_elegido = random.choice(departamentos)
                problema_elegido = random.choice(problemas_comunes)
                descripcion_problema = f"La queja trata sobre {problema_elegido}. FÍSICAMENTE: El cliente se acerca directamente a ti en las Cajas Principales."
            elif difficulty == "Casos Especiales (Errores del Cliente)":
                problema_elegido = random.choice(errores_cliente)
                descripcion_problema = f"ESTE ES UN CASO ESPECIAL DE ERROR DEL CLIENTE. La situación es: {problema_elegido}. FÍSICAMENTE: El cliente se acerca a ti en Cajas Principales."
            else:
                pesadilla_elegida = random.choice(pesadillas_la_vaquita)
                descripcion_problema = f"La queja principal DEBE ser exactamente esta: {pesadilla_elegida}."

            hidden_prompt = f"Inicia la simulación. Entra en personaje generando un problema de complejidad '{difficulty}'. {descripcion_problema}. ASEGÚRATE de incluir la pista de lenguaje corporal."
            
            with st.spinner("El cliente se está acercando..."):
                try:
                    chat = client.chats.create(
                        model="gemini-2.5-flash",
                        config=types.GenerateContentConfig(system_instruction=actor_instrucciones, safety_settings=seguridad_baja)
                    )
                    response = chat.send_message(hidden_prompt)
                    texto_seguro = response.text if response.text else "⚠️ **Aviso del Sistema:** Filtro activado."
                    st.session_state.simulador_history.append({"role": "user", "content": hidden_prompt, "hidden": True})
                    st.session_state.simulador_history.append({"role": "model", "content": texto_seguro, "hidden": False})
                    st.rerun()
                except Exception as e:
                    st.error("⚠️ Error 503. Por favor, intenta de nuevo en unos segundos.")

    elif not st.session_state.simulador_concluido:
        chat_container = st.container()

        with chat_container:
            for message in st.session_state.simulador_history:
                if not message.get("hidden", False):
                    ui_role = "assistant" if message["role"] == "model" else "user"
                    with st.chat_message(ui_role):
                        st.markdown(message["content"])

        user_input = st.chat_input("Escribe tu respuesta aquí...")

        if user_input:
            st.session_state.simulador_history.append({"role": "user", "content": user_input, "hidden": False})

            with chat_container:
                with st.chat_message("user"):
                    st.markdown(user_input)

                formatted_history = []
                for msg in st.session_state.simulador_history[:-1]:
                    formatted_history.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

                try:
                    chat_actor = client.chats.create(
                        model="gemini-2.5-flash", 
                        config=types.GenerateContentConfig(system_instruction=actor_instrucciones, safety_settings=seguridad_baja),
                        history=formatted_history
                    )

                    with st.chat_message("assistant"):
                        with st.spinner("El cliente está respondiendo..."):
                            response_actor = chat_actor.send_message(user_input)
                        texto_actor = response_actor.text if response_actor.text else "⚠️ **Aviso del Sistema:** Filtro activado."
                        st.markdown(texto_actor)
                    
                    st.session_state.simulador_history.append({"role": "model", "content": texto_actor, "hidden": False})
                    
                    if "FIN DE LA SIMULACIÓN" in texto_actor.upper():
                        st.session_state.simulador_concluido = True
                        st.rerun()
                except Exception as e:
                    st.session_state.simulador_history.pop()
                    st.error("⚠️ Error 503. Por favor, vuelve a enviar tu mensaje.")

        st.divider()
        st.caption("¿Resolviste el problema? Haz clic abajo para ser evaluado por el Coach.")
        if st.button("Terminar y Evaluar"):
            st.session_state.simulador_concluido = True
            st.rerun()

    if st.session_state.simulador_concluido:
        for message in st.session_state.simulador_history:
            if not message.get("hidden", False):
                ui_role = "assistant" if message["role"] == "model" else "user"
                with st.chat_message(ui_role):
                    st.markdown(message["content"])
                    
        st.divider()
        st.subheader("🛑 SIMULACIÓN TERMINADA.")
        
        if not st.session_state.coach_feedback:
            with st.spinner("🧠 El Evaluador Pro está analizando tu desempeño con gran detalle..."):
                transcripcion = ""
                for m in st.session_state.simulador_history:
                    if not m.get("hidden", False):
                        rol = "Sistema/Cliente" if m["role"] == "model" else "Gerente"
                        transcripcion += f"{rol}: {m['content']}\n\n"
                
                prompt_coach = f"La simulación ha terminado. Transcripción:\n\n{transcripcion}\n\nProporciona tu evaluación detallada."
                
                try:
                    coach_response = client.models.generate_content(
                        model="gemini-2.5-pro",
                        contents=prompt_coach,
                        config=types.GenerateContentConfig(system_instruction=coach_instrucciones, safety_settings=seguridad_baja)
                    )
                    st.session_state.coach_feedback = coach_response.text if coach_response.text else "⚠️ *Filtro de seguridad.*"
                    st.session_state.api_error = False
                except Exception as e:
                    st.session_state.api_error = True

        if st.session_state.api_error:
            st.error("⚠️ Error 503. No hemos podido generar tu evaluación.")
            if st.button("🔄 Reintentar Evaluación"):
                st.session_state.coach_feedback = ""
                st.session_state.api_error = False
                st.rerun()
        else:
            with st.chat_message("assistant", avatar="🧠"):
                st.markdown(st.session_state.coach_feedback)
                
            st.divider()
            if st.button("Reiniciar Simulador"):
                st.session_state.simulador_history = []
                st.session_state.simulador_concluido = False
                st.session_state.coach_feedback = ""
                st.session_state.api_error = False
                st.rerun()

# ==========================================
# MÓDULO 3: PREGUNTAS AL ASESOR
# ==========================================
elif menu_selection == "Preguntas al Asesor":
    st.title("🧠 Asesoría para Gerentes")
    st.write("¿Tienes dudas sobre cómo manejar una situación específica en la tienda? Pregúntale al asesor experto de La Vaquita.")
    
    asesor_instrucciones = """
    Eres el Consultor Experto en Operaciones de Retail y Mentor Senior de La Vaquita Meat Market.
    
    CONTEXTO DE LA TIENDA (TU BIBLIA): 
    La Vaquita es de alto volumen. Operamos con márgenes estrechos.

    REGLAS DE RESPUESTA (ESTRICTAS):
    1. Cero Respuestas Genéricas: Habla como un mentor astuto en retail hispano.
    2. PROTOCOLO SIN RECIBO: Investigar primero, usar escudo del sistema después si la búsqueda falla.
    3. LA TRAMPA DE LA DISCULPA (Error del cliente): Aconseja estrictamente a los gerentes que NUNCA se disculpen cuando el cliente causó el problema (ej. leyó mal un letrero, tiró un frasco). Enséñales a usar "Empatía Neutral para salvar el ego" ("Entiendo la confusión, a todos nos pasa"). Adviérteles que NUNCA usen disculpas suaves ("siento la confusión"), NUNCA culpen a la tienda ("nuestros letreros están confusos"), y NUNCA asuman el estado del cliente ("venía apurado").
    4. REGLA CERO TARJETAS DE REGALO Y CORTESÍAS: Advierte explícitamente a los gerentes que NO REGALEN cortesías de bajo costo solo por filas regulares en la tienda.
    5. Tolerancia Cero al Abuso: Aconseja al gerente que establezca límites firmes inmediatamente si hay insultos.
    """

    if "asesor_history" not in st.session_state:
        st.session_state.asesor_history = []

    for msg in st.session_state.asesor_history:
        ui_role = "assistant" if msg["role"] == "model" else "user"
        with st.chat_message(ui_role):
            st.markdown(msg["content"])

    pregunta_usuario = st.chat_input("Ej: ¿Qué hago si un cliente lee mal un letrero?")

    if pregunta_usuario:
        st.session_state.asesor_history.append({"role": "user", "content": pregunta_usuario})
        
        with st.chat_message("user"):
            st.markdown(pregunta_usuario)

        formatted_asesor_history = [{"role": m["role"], "parts": [{"text": m["content"]}]} for m in st.session_state.asesor_history[:-1]]

        with st.chat_message("assistant"):
            with st.spinner("Buscando la mejor solución..."):
                try:
                    chat = client.chats.create(
                        model="gemini-2.5-pro",
                        config=types.GenerateContentConfig(system_instruction=asesor_instrucciones, safety_settings=seguridad_baja),
                        history=formatted_asesor_history
                    )
                    response = chat.send_message(pregunta_usuario)
                    texto_asesor = response.text
                except Exception as e:
                    texto_asesor = "⚠️ *Error 503. Intenta preguntar de nuevo.*"
                    st.session_state.asesor_history.pop() 
            st.markdown(texto_asesor)
            
        if texto_asesor and "⚠️" not in texto_asesor:
             st.session_state.asesor_history.append({"role": "model", "content": texto_asesor})
        
    if len(st.session_state.asesor_history) > 0:
        st.divider()
        if st.button("Limpiar Conversación"):
            st.session_state.asesor_history = []
            st.rerun()
