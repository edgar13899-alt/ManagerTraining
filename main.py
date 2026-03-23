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
    
    with st.expander("👂 H - Hear (Escuchar activamente)", expanded=False):
        st.markdown("""
        Cuando un cliente molesto se comunica contigo, su necesidad principal es sentirse escuchado y comprendido. Este paso se centra en la escucha activa y en permitir que el cliente se desahogue por completo de su frustración antes de que intentes solucionar nada.
        
        **Las acciones clave durante esta etapa incluyen:**
        * **Guardar silencio:** Resiste el impulso de interrumpir, defenderte u ofrecer soluciones de inmediato.
        * **Prestar atención :** Presta atención a los detalles específicos de su problema para no tener que pedirle que lo repita más tarde.
        """)

    with st.expander("🤝 E - Empathize (Empatizar)", expanded=False):
        st.markdown("""
        Una vez que el cliente ha contado su historia (y tú lo has Escuchado), la empatía construye un puente entre escuchar y resolver. Le demuestra al cliente que comprendes sus sentimientos y validas su frustración, incluso si aún no has determinado de quién es la culpa o cómo solucionarlo.
        
        **Las acciones clave para este paso incluyen:**
        * **Reflejar su urgencia:** Ajusta tu tono para demostrar que te tomas el asunto tan en serio como ellos.
        * **Validar sus emociones:** Usa frases que reconozcan sus sentimientos específicos (por ejemplo: frustración, decepción, pánico) en lugar de solo los hechos logísticos del problema.
        * **Evitar ponerse a la defensiva:** Mantente alejado de citar políticas de la empresa o poner excusas, lo cual invalida de inmediato su experiencia. Empatizar no significa estar de acuerdo con ellos.
        """)

    with st.expander("🙏 A - Apologize (Ofrecer disculpas)", expanded=False):
        st.markdown("""
        Ahora que has escuchado (Hear) y validado sus sentimientos (Empathize), es momento de ofrecer una disculpa sincera. Una disculpa genuina asume la responsabilidad del problema y el impacto específico que tuvo en el cliente, sin señalar a otros ni poner excusas.
        
        **Las acciones clave para este paso incluyen:**
        * **Ser específico:** Discúlpate por el problema exacto en lugar de ofrecer un genérico "Lamento las molestias".
        * **Asumir la responsabilidad:** Acepta la responsabilidad en nombre de la empresa. Usar frases como "Lo siento que le hayamos fallado" es mucho más efectivo que culpar a otro departamento o al servicio de entrega.
        * **Evitar las disculpas falsas:** Mantente alejado de frases como "Lo siento que te sientas así" o "Lamento si esto causó un problema". Estas devuelven la culpa a la reacción del cliente y pueden aumentar su frustración.
        """)

    with st.expander("🛠️ R - Resolve (Resolver y Reubicar)", expanded=False):
        st.markdown("""
        Después de escuchar, empatizar y disculparse, el cliente generalmente está listo para saber cómo solucionarás la situación. Este paso se trata de actuar y ser transparente sobre la solución.
        
        **Las acciones clave para este paso incluyen:**
        * **Solucionar el problema:** Resuelve el problema de inmediato si puedes. Si no puedes, explica exactamente qué medidas estás tomando para solucionarlo.
        * **Ofrecer opciones:** Dale alternativas al cliente siempre que sea posible. Esto le devuelve la sensación de control después de una experiencia frustrante.
        * **Ser transparente:** Comunica claramente los plazos y qué pueden esperar a continuación. Evita hacer promesas que no puedas cumplir.
        """)

    with st.expander("💖 T - Thank (Agradecer)", expanded=False):
        st.markdown("""
        Aunque pueda parecer contradictorio agradecer a alguien que se acaba de quejar, expresar gratitud es una manera poderosa de cerrar la conversación. Deja al cliente con una impresión final positiva y replantea su queja como comentarios valiosos que ayudan a la empresa a mejorar.
        
        **Las acciones clave para este paso incluyen:**
        * **Agradecerles por sus comentarios:** Reconoce que se tomaron el tiempo de señalar un error, lo que te da la oportunidad de solucionarlo.
        * **Apreciar su paciencia:** Reconoce el tiempo y el esfuerzo que dedicaron a resolver el problema contigo.
        * **Reafirmar la relación:** Expresa que valoras que sean clientes y que esperas brindarles un mejor servicio la próxima vez.
        """)
        
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
