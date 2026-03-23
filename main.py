import streamlit as st
from google import genai
from google.genai import types
import os

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

# --- CONEXIÓN IA ---
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("¡Falta la clave API! Por favor, configúrala en los Secrets de Streamlit.")
    st.stop()

client = genai.Client(api_key=api_key)

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
    st.write("En La Vaquita Meat Market, el excelente servicio al cliente es nuestra prioridad. Estudia detalladamente los 5 pasos y luego baja para completar el Tutorial Guiado.")
    
    st.divider()
    
    with st.expander("👂 H - Hear (Escuchar)", expanded=False):
        st.write("**Escucha activamente y en silencio.**")
        st.write("El primer paso es dejar que el cliente se desahogue completamente sin interrumpirlo. Mantén contacto visual, asiente con la cabeza y ten un lenguaje corporal abierto. Muchas veces, un cliente molesto solo necesita sentir que alguien lo está escuchando antes de calmarse. **No ofrezcas soluciones todavía.**")

    with st.expander("🤝 E - Empathize (Empatizar)", expanded=False):
        st.write("**Valida sus sentimientos sin darle la razón absoluta.**")
        st.write("Demuestra que entiendes su frustración poniéndote en sus zapatos, pero no admitas que la tienda hizo algo malo si no tienes todos los hechos.")
        st.write("✅ *Correcto:* 'Entiendo completamente por qué está frustrado con el tiempo de espera en su hora de comida.' (Validas su emoción).")
        st.write("❌ *Incorrecto:* 'Tiene toda la razón, nuestra taquería es muy lenta hoy.' (Culpas a tu propio equipo).")

    with st.expander("🙏 A - Apologize (Disculparse)", expanded=False):
        st.write("**Ofrece una disculpa sincera y asume la responsabilidad.**")
        st.write("Incluso si el error no fue tuyo directamente, tú representas a La Vaquita. No pongas excusas ni le eches la culpa al proveedor, a otro cajero o al sistema.")
        st.write("✅ *Correcto:* 'Le pido una sincera disculpa por este inconveniente. Sé que su tiempo es valioso.'")

    with st.expander("🛠️ R - Resolve (Resolver y Reubicar)", expanded=False):
        st.write("**Soluciona el problema y protege el piso de ventas.**")
        st.write("🚨 **REGLA DE REUBICACIÓN:** Si un cliente está alterado, haciendo un escándalo o deteniendo la fila, tu PRIMERA acción antes de resolver el problema debe ser sugerir moverlo de lugar.")
        st.write("Usa tu buen juicio como gerente para llevar al cliente a otra área más tranquila y adecuada (a un lado del mostrador, una mesa vacía, un pasillo menos concurrido, etc.) para evitar interrumpir a otros clientes.")
        st.write("*Sobre los descuentos:* Un descuento o producto gratis es el último recurso. Intenta resolver el problema con un cambio o corrección primero.")

    with st.expander("💖 T - Thank (Agradecer)", expanded=False):
        st.write("**Agradece al cliente por su paciencia y por informarnos.**")
        st.write("Termina la interacción con una nota positiva. Queremos que el cliente se vaya sintiendo que nos importa su opinión para que regrese.")
        st.write("✅ *Correcto:* 'Le agradezco mucho su paciencia mientras resolvíamos esto, y gracias por informarnos para poder mejorar nuestro servicio.'")
        
    st.error("🛑 **REGLA CERO: ESTABLECER LÍMITES**")
    st.write("El cliente es importante, pero **el respeto hacia ti y tu equipo es innegociable.** Si un cliente usa insultos, lenguaje vulgar o denigra a un empleado, DEBES establecer un límite profesional de inmediato. No toleres el abuso verbal solo por cerrar una venta.")
    st.write("✅ *Correcto:* 'Señor, quiero ayudarle a resolver su problema con su pedido, pero le pido que nos comuniquemos con respeto o no podré seguir asistiéndole.'")

    st.divider()
    st.subheader("🎓 Tutor Paso a Paso")
    st.write("Es hora de practicar. El Tutor Virtual te presentará un escenario y te guiará letra por letra. Deberás responder correctamente cada paso antes de avanzar al siguiente.")

    tutor_instrucciones = """
    Eres el Tutor de Entrenamiento de La Vaquita Meat Market. Tu trabajo es enseñar el método HEART paso a paso.
    
    INSTRUCCIONES DE TUTORÍA:
    1. En tu primer mensaje, presenta un escenario conflictivo (ej. en la carnicería o cajas).
    2. Luego, pregúntale al usuario: "¿Qué harías para el paso H (Hear)?"
    3. Espera su respuesta. Si es correcta (guardar silencio, escuchar activamente), felicítalo y pregúntale por el paso E (Empathize).
    4. Si se equivoca o intenta saltarse pasos (ej. resolver el problema de inmediato), corrígelo amablemente y oblígalo a responder el paso actual correctamente.
    5. Guíalo secuencialmente: H -> E -> A -> R -> T. 
    6. Cuando lleguen a la R (Resolve), asegúrate de que apliquen la Regla de Reubicación. El gerente debe proponer mover al cliente a otra área. Evalúa lógicamente si el lugar que el usuario sugiere es una buena decisión para desescalar la situación sin interrumpir el flujo de la tienda.
    7. Una vez que completen la T (Thank), felicítalos, diles que están listos para el Simulador, y da por terminado el tutorial.
    """

    if "tutor_history" not in st.session_state:
        st.session_state.tutor_history = []

    if len(st.session_state.tutor_history) == 0:
        if st.button("Iniciar Tutorial Guiado"):
            with st.spinner("Preparando tu primera lección..."):
                chat = client.chats.create(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(system_instruction=tutor_instrucciones)
                )
                hidden_prompt = "Hola. Preséntame un escenario en La Vaquita y pídeme que complete el primer paso (H). No me des las respuestas."
                response = chat.send_message(hidden_prompt)
                
            st.session_state.tutor_history.append({"role": "user", "content": hidden_prompt, "hidden": True})
            st.session_state.tutor_history.append({"role": "model", "content": response.text, "hidden": False})
            st.rerun()
    else:
        formatted_tutor_history = []
        for msg in st.session_state.tutor_history:
            if not msg.get("hidden", False):
                formatted_tutor_history.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

        for msg in st.session_state.tutor_history:
            if not msg.get("hidden", False):
                ui_role = "assistant" if msg["role"] == "model" else "user"
                with st.chat_message(ui_role):
                    st.markdown(msg["content"])

        tutor_input = st.chat_input("Escribe tu respuesta para el paso actual...")

        if tutor_input:
            with st.chat_message("user"):
                st.markdown(tutor_input)
            
            st.session_state.tutor_history.append({"role": "user", "content": tutor_input, "hidden": False})

            chat = client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(system_instruction=tutor_instrucciones),
                history=formatted_tutor_history
            )

            with st.chat_message("assistant"):
                with st.spinner("El tutor está revisando tu respuesta..."):
                    response = chat.send_message(tutor_input)
                st.markdown(response.text)
                
            st.session_state.tutor_history.append({"role": "model", "content": response.text, "hidden": False})
        
        st.divider()
        if st.button("Reiniciar Tutorial"):
            st.session_state.tutor_history = []
            st.rerun()

# ==========================================
# MÓDULO 2: SIMULADOR HEART (Method Actor)
# ==========================================
elif menu_selection == "Simulador HEART":
    st.title("🥩 Simulador de Entrenamiento")

    simulador_instrucciones = """
    Eres un simulador de rol interactivo para entrenar empleados y gerentes en La Vaquita Meat Market. 
    Departamentos: taquería, panadería, pastelería, paletería, frutas/verduras frescas y abarrotes.

    TU OBJETIVO:
    Actuar como el cliente en una conversación continua de ida y vuelta. NO evalúes de inmediato. Responde a lo que te diga el gerente, reacciona a su tono y pon a prueba sus habilidades antes de aceptar una solución.

    REGLAS DE ACTUACIÓN (Dependiendo de la dificultad elegida):
    - FÁCIL: Eres razonable. Si el gerente es amable, escucha y ofrece una solución justa, acéptala rápidamente y sé agradecido.
    - MEDIO: Estás apurado y frustrado. Pon peros a su primera solución (ej. "Sí, pero ya perdí 20 minutos"). Haz preguntas difíciles. Cede solo si muestran buena empatía y una resolución verdaderamente útil.
    - DIFÍCIL: Estás furioso. Interrumpe al gerente. Haz un escándalo público. 
        * Curva de Reubicación: Si estás gritando y el gerente intenta resolver el problema en medio de la tienda sin sugerir que se muevan a otra área más adecuada, haz tu escándalo MÁS FUERTE y quéjate de que todos te están viendo.
        * Límite de Abuso (Trampa): Ocasionalmente, cruza la línea con un insulto o actitud denigrante. Si el gerente solo se disculpa y acepta el abuso verbal, sé más agresivo. El gerente DEBE establecer un límite firme (ej. "Le pido que nos comuniquemos con respeto"). Si establecen el límite, cálmate un poco o retírate de la tienda.

    CÓMO TERMINAR LA SIMULACIÓN Y EVALUAR:
    Mantente en tu personaje durante varios intercambios (3 a 6 mensajes), o hasta que el gerente resuelva el problema satisfactoriamente, o hasta que el gerente establezca un límite firme ante un insulto. 
    CUANDO LA INTERACCIÓN LLEGUE A SU FIN NATURAL, escribe en negritas "### [FIN DE LA SIMULACIÓN]" y sal de tu personaje. 
    Inmediatamente después, proporciona una evaluación completa del desempeño del gerente utilizando el método HEART:
    - H (Hear): ¿Guardaron silencio y no te interrumpieron inicialmente?
    - E (Empathize): ¿Validaron tu frustración sin darte la razón absoluta?
    - A (Apologize): ¿Fue genuina su disculpa?
    - R (Resolve): ¿Te invitaron a moverte a una zona lógica y menos disruptiva para hablar y resolver el problema? ¿La solución fue buena sin regalar demasiado?
    - T (Thank): ¿Agradecieron tu paciencia?
    """

    if "simulador_history" not in st.session_state:
        st.session_state.simulador_history = []

    if len(st.session_state.simulador_history) == 0:
        st.info("Selecciona la actitud del cliente para comenzar la simulación de rol.")
        difficulty = st.selectbox(
            "Selecciona el tipo de cliente:",
            ["Fácil", "Medio", "Difícil"]
        )
        
        if st.button("Comenzar Escenario"):
            hidden_prompt = f"Inicia la simulación. Entra en personaje como un cliente con dificultad {difficulty}. Presenta tu queja inicial en un solo párrafo. Recuerda: eres el cliente, NO el evaluador todavía."
            
            with st.spinner("El cliente se está acercando..."):
                chat = client.chats.create(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(system_instruction=simulador_instrucciones)
                )
                response = chat.send_message(hidden_prompt)
                
            st.session_state.simulador_history.append({"role": "user", "content": hidden_prompt, "hidden": True})
            st.session_state.simulador_history.append({"role": "model", "content": response.text, "hidden": False})
            st.rerun()

    else:
        formatted_history = []
        for msg in st.session_state.simulador_history:
            if not msg.get("hidden", False):
                formatted_history.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

        for message in st.session_state.simulador_history:
            if not message.get("hidden", False):
                ui_role = "assistant" if message["role"] == "model" else "user"
                with st.chat_message(ui_role):
                    st.markdown(message["content"])

        user_input = st.chat_input("Escribe tu respuesta al cliente aquí...")

        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            
            st.session_state.simulador_history.append({"role": "user", "content": user_input, "hidden": False})

            chat = client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(system_instruction=simulador_instrucciones),
                history=formatted_history
            )

            with st.chat_message("assistant"):
                with st.spinner("El cliente está respondiendo..."):
                    response = chat.send_message(user_input)
                st.markdown(response.text)
                
            st.session_state.simulador_history.append({"role": "model", "content": response.text, "hidden": False})
        
        st.divider()
        if st.button("Terminar y Volver al Inicio"):
            st.session_state.simulador_history = []
            st.rerun()

# ==========================================
# MÓDULO 3: PREGUNTAS AL ASESOR
# ==========================================
elif menu_selection == "Preguntas al Asesor":
    st.title("🧠 Asesoría para Gerentes")
    st.write("¿Tienes dudas sobre cómo manejar una situación específica en la tienda? Pregúntale al asesor experto de La Vaquita.")
    
    asesor_instrucciones = """
    Eres un asesor experto en operaciones de retail y servicio al cliente, contratado exclusivamente para ser el mentor de los gerentes de La Vaquita Meat Market.
    Conoces a fondo la tienda (taquería, panadería, pastelería, paletería, frutas/verduras y abarrotes).
    
    Tus reglas:
    1. Da respuestas directas, prácticas y profesionales. No uses respuestas genéricas; adáptalas al entorno de un mercado hispano concurrido.
    2. Usa el método HEART como base para tus recomendaciones cuando aplique.
    3. Ten en cuenta las reglas estrictas de la tienda: NUNCA tolerar el abuso a los empleados (los gerentes deben establecer límites profesionales) y SIEMPRE pedirles a los clientes ruidosos o conflictivos que se muevan a otra área para no afectar las ventas.
    4. Responde en español, con un tono alentador pero firme.
    """

    if "asesor_history" not in st.session_state:
        st.session_state.asesor_history = []

    for msg in st.session_state.asesor_history:
        ui_role = "assistant" if msg["role"] == "model" else "user"
        with st.chat_message(ui_role):
            st.markdown(msg["content"])

    pregunta_usuario = st.chat_input("Ej: ¿Qué hago si un cliente no está de acuerdo con la política de devoluciones?")

    if pregunta_usuario:
        with st.chat_message("user"):
            st.markdown(pregunta_usuario)
        
        st.session_state.asesor_history.append({"role": "user", "content": pregunta_usuario})

        formatted_asesor_history = [{"role": m["role"], "parts": [{"text": m["content"]}]} for m in st.session_state.asesor_history[:-1]]

        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(system_instruction=asesor_instrucciones),
            history=formatted_asesor_history
        )

        with st.chat_message("assistant"):
            with st.spinner("Buscando la mejor solución..."):
                response = chat.send_message(pregunta_usuario)
            st.markdown(response.text)
            
        st.session_state.asesor_history.append({"role": "model", "content": response.text})
        
    if len(st.session_state.asesor_history) > 0:
        st.divider()
        if st.button("Limpiar Conversación"):
            st.session_state.asesor_history = []
            st.rerun()
