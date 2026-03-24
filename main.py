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

# Reducimos los filtros de seguridad para permitir simulaciones de clientes enojados
seguridad_baja = [
    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"),
]

# --- VARIABLES COMPARTIDAS (LA MÁQUINA TRAGAMONEDAS Y BÓVEDA) ---
departamentos = ["la Carnicería", "la Taquería", "la Panadería", "la Paletería", "las Cajas Principales", "el Pasillo de Abarrotes", "el área de Frutas y Verduras"]
problemas_comunes = ["un producto equivocado o faltante", "un tiempo de espera inaceptable", "un problema de calidad o frescura genérico", "un precio cobrado incorrectamente en el sistema", "un malentendido leve con un empleado", "un derrame o accidente menor en la tienda"]
pesadillas_la_vaquita = [
    "un pago que aparece como 'pendiente' en la app del banco del cliente porque la terminal falló, y el cliente se niega rotundamente a volver a pasar la tarjeta por miedo a que se le cobre doble",
    "un cliente que recoge un pastel de cumpleaños personalizado en la panadería y exige un reembolso completo más el pastel gratis porque el nombre está mal escrito, a pesar de que el gerente tiene la hoja de pedido donde el cliente mismo escribió mal el nombre",
    "un cliente furioso que, después de recibir su pedido en el mostrador de la carnicería, hace un escándalo al enterarse de que no hay caja registradora ahí y se niega a hacer una segunda fila en las cajas principales para pagar",
    "un cliente que tiene un carrito lleno con $200 dólares en mandado, pero el sistema de EBT/tarjetas de beneficios del gobierno se cae a nivel nacional. No tiene otra forma de pagar y se niega a dejar el carrito.",
    "un cliente que trae un folleto de ofertas de otro mercado hispano (como La Michoacana) y exige a gritos que le igualen el precio en una venta masiva de fajitas que la tienda físicamente no puede permitirse igualar.",
    "un cliente que le pide al carnicero que le corte de manera especial 15 libras de una carne cara. El carnicero la corta, la empaqueta, y cuando el cliente ve el precio impreso, dice 'siempre no lo quiero' y lo deja ahí, dejando a la tienda con producto mermado que no puede regresar a la vitrina.",
    "una mujer que quiere devolver una sopa de pollo de la taquería argumentando agresivamente que está 'demasiado picante', a pesar de que la receta de la tienda NO lleva absolutamente nada de picante y nadie más se ha quejado de eso jamás."
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
    HEART es un acrónimo (por sus siglas en inglés) que representa un **método paso a paso probado para manejar quejas y situaciones difíciles** con los clientes. No es solo un guion, es una estrategia psicológica.

    ### ¿Para qué se utiliza?
    Se utiliza para **desescalar la tensión** cuando un cliente está enojado, frustrado o exigente. Te da una estructura clara para calmar la situación, encontrar una solución lógica y despedir al cliente de manera profesional, todo sin perder el control de la conversación.

    ### ¿Por qué es tan importante en La Vaquita?
    En un mercado de alto volumen, los problemas (como un precio mal cobrado o un pedido equivocado) van a suceder. Sin un método, es fácil tomar los gritos de manera personal, ponerse a la defensiva, discutir, o peor aún, regalar mercancía o dinero por pánico. El método HEART te protege a ti y a las ganancias de la tienda, dándote las herramientas para mantenerte firme, profesional y en control total.
    """)
    
    st.divider()
    st.write("### Los 5 Pasos de HEART")
    st.write("Abre y estudia detalladamente cada paso. Luego, baja para completar el Tutorial Guiado.")
    
    with st.expander("👂 H - Hear (Escuchar activamente)", expanded=False):
        st.markdown("""
        Cuando un cliente molesto se comunica contigo, su necesidad principal es sentirse escuchado y comprendido. Este paso se centra en la escucha activa y en permitir que el cliente se desahogue por completo de su frustración antes de que intentes solucionar nada.
        
        **Las acciones clave durante esta etapa incluyen:**
        * **Guardar silencio:** Resiste el impulso de interrumpir, defenderte u ofrecer soluciones de inmediato.
        * **Tomar notas:** Presta atención a los detalles específicos de su problema para no tener que pedirle que lo repita más tarde.
        * **Usar asentimientos verbales:** Si estás al teléfono, usa breves confirmaciones como "ya veo", "de acuerdo" o "continúe" para demostrar que sigues ahí y prestando atención.
        """)

    with st.expander("🤝 E - Empathize (Empatizar)", expanded=False):
        st.markdown("""
        Una vez que el cliente ha contado su historia (y tú lo has Escuchado), la empatía construye un puente entre escuchar y resolver. Le demuestra al cliente que comprendes sus sentimientos y validas su frustración, incluso si aún no has determinado de quién es la culpa o cómo solucionarlo.
        
        **Las acciones clave para este paso incluyen:**
        * **Reflejar su urgencia:** Ajusta tu tono para demostrar que te tomas el asunto tan en serio como ellos.
        * **Validar sus emociones:** Usa frases que reconozcan sus sentimientos específicos (por ejemplo: frustración, decepción, pánico) en lugar de solo los hechos logísticos del problema.
        * **Evitar ponerse a la defensiva:** Mantente alejado de citar políticas de la empresa o poner excusas, lo cual invalida de inmediato su experiencia.
        * <u>**Empatizar no significa estar de acuerdo con ellos.**</u>
        """, unsafe_allow_html=True)

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
        * **Ser transparente:** Comunica claramente los plazos (ej. *"su pedido estará listo en 15 minutos"*). Evita hacer promesas que no puedas cumplir.
        * **Personalización silenciosa (Lectura del cliente):** Observa el lenguaje corporal del cliente y adapta tu solución a su situación sin señalar su estrés explícitamente. Por ejemplo, si notas que tienen prisa, no digas *"veo que tiene prisa"*, ya que eso aumenta su ansiedad. Usa frases como: *"Permítame cobrarle en esta otra caja para que pueda continuar con su día"*. Así pensarán: *"Qué bueno, porque llevo mucha prisa"*.
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
    st.write("🚨 **Si el cliente continúa siendo abusivo después de establecer el límite:** Debes dar por terminada la interacción y pedirle explícitamente que abandone la tienda. (Ej. *'Dado que no puede comunicarse con respeto, le voy a pedir que se retire de la tienda en este momento'*).")

    st.divider()
    st.subheader("🎓 Tutor Paso a Paso")
    st.write("Es hora de practicar. El Tutor Virtual te presentará un escenario y te guiará letra por letra. Deberás responder correctamente cada paso antes de avanzar al siguiente.")

    tutor_instrucciones = """
    Eres el Tutor Maestro de La Vaquita Meat Market. 
    
    CONTEXTO DE LA TIENDA: La Vaquita es un mercado hispano de alto volumen. Los márgenes de supermercado son estrechos. Entiendes profundamente que no somos una corporación genérica que regala dinero para callar quejas.
    
    TU OBJETIVO: Enseñar el método HEART paso a paso a un gerente en entrenamiento con gran inteligencia emocional y perspicacia comercial.

    INSTRUCCIONES DE TUTORÍA:
    1. En tu primer mensaje, presenta el escenario conflictivo.
    2. IMPORTANTE: SIEMPRE incluye una pista clara sobre el lenguaje corporal o estado del cliente en TERCERA PERSONA (ej. mira su reloj, parece agotado).
    3. Luego, pregúntale al usuario: "¿Qué harías para el paso H (Hear)?"
    4. Espera su respuesta. Evalúala con precisión. Si es correcta, felicítalo y pasa a la E (Empathize). Si es incorrecta o débil, dales un EJEMPLO EXACTO de lo que deberían haber dicho.
    5. DESGLOSE PSICOLÓGICO: Inmediatamente después de dar tu sugerencia de guion, DEBES explicar *por qué* elegiste esas palabras.
    6. REGLAS ESTRICTAS DE EVALUACIÓN (APLICAN A TODOS LOS PASOS):
       - REGLA DE EMPATÍA (NUNCA ESTÉS DE ACUERDO): Tienes ESTRICTAMENTE PROHIBIDO usar o aprobar frases como "tiene toda la razón" o "estoy de acuerdo". La empatía significa validar emociones ("Entiendo su frustración"), no validar hechos. Corrígelos si cometen este error.
       - REGLA ESTRICTA DE SECUENCIA: La Empatía (E) DEBE venir ANTES de la Disculpa (A). Corrígelos si se disculpan antes de empatizar.
       - REGLA DE DISCRECIÓN: Al enseñar Reubicación, PROHÍBE usar frases obvias (ej. "lejos de la fila"). Enseña a que suene como un beneficio para el cliente.
       - REGLA DE RENTABILIDAD: Si el error fue del cliente, enséñales el guion exacto de cómo negar una devolución firmemente pero con empatía.
    7. Guíalo secuencialmente: H -> E -> A -> R -> T. Una vez que completen la T, felicítalos y termina el tutorial.
    """

    if "tutor_history" not in st.session_state:
        st.session_state.tutor_history = []

    if len(st.session_state.tutor_history) == 0:
        if st.button("Iniciar Tutorial Guiado"):
            with st.spinner("Preparando tu primera lección..."):
                
                tipo_escenario = random.choices(["comun", "pesadilla"], weights=[40, 60], k=1)[0]
                if tipo_escenario == "comun":
                    depto_elegido = random.choice(departamentos)
                    problema_elegido = random.choice(problemas_comunes)
                    descripcion_problema = f"El escenario DEBE ocurrir en {depto_elegido}. La queja trata sobre {problema_elegido}."
                else:
                    pesadilla_elegida = random.choice(pesadillas_la_vaquita)
                    descripcion_problema = f"La queja principal DEBE ser exactamente esta: {pesadilla_elegida}."

                chat = client.chats.create(
                    model="gemini-2.5-pro",
                    config=types.GenerateContentConfig(system_instruction=tutor_instrucciones, safety_settings=seguridad_baja)
                )
                hidden_prompt = f"Hola. Genera el escenario inicial usando esta premisa: {descripcion_problema}. Asegúrate de incluir la pista física en tercera persona. Preséntamelo y pídeme que complete el primer paso (H). No me des las respuestas. Código aleatorio: {random.randint(1,10000)}"
                response = chat.send_message(hidden_prompt)
                
            texto_seguro = response.text if response.text else "⚠️ *El filtro de seguridad bloqueó la respuesta. Por favor, reinicia el tutorial.*"
            st.session_state.tutor_history.append({"role": "user", "content": hidden_prompt, "hidden": True})
            st.session_state.tutor_history.append({"role": "model", "content": texto_seguro, "hidden": False})
            st.rerun()
    else:
        formatted_tutor_history = []
        for msg in st.session_state.tutor_history:
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
        
        st.divider()
        if st.button("Reiniciar Tutorial"):
            st.session_state.tutor_history = []
            st.rerun()

# ==========================================
# MÓDULO 2: SIMULADOR HEART (Split-Brain)
# ==========================================
elif menu_selection == "Simulador HEART":
    st.title("🥩 Simulador de Entrenamiento")

    actor_instrucciones = """
    Eres el Actor del simulador de rol interactivo en La Vaquita Meat Market. 
    TU ÚNICO OBJETIVO: Actuar como un cliente de forma hiperrealista. TÚ NO EVALÚAS AL GERENTE. 

    REGLAS DE FORMATO (MUY IMPORTANTE):
    1. Para tu PRIMER mensaje, debes separar el contexto objetivo de lo que dices en voz alta. DEBE HABER UN SALTO DE LÍNEA entre los dos. Usa este formato exacto:
    
    **Escenario:** [Describe tu lenguaje corporal estrictamente en TERCERA PERSONA como un narrador objetivo. DEBES mencionar explícitamente el entorno: ¿Hay otros clientes en la fila observando? ¿Estás alzando la voz haciendo una escena pública, o están solos? NUNCA uses "yo" o "mi" aquí].

    **Cliente:** "[Escribe tu queja inicial en voz alta, en primera persona]".
    
    2. En el resto de la conversación, SOLO escribe lo que dices en voz alta. Cero asteriscos, cero monólogos internos.

    DETALLES CONTEXTUALES UNIVERSALES: 
    Compórtate como un ser humano real. Usa excusas de la vida real. NUNCA digas literalmente "estoy apurado". 

    REGLA DE SENTIDO COMÚN (TIEMPO Y LÓGICA): 
    Si el gerente ofrece arreglar tu problema rápido o te da la solución justa, acéptalo con alivio (ej. "Está bien, se lo agradezco" o "Por favor apúrese"). 
    IMPORTANTE: NO termines la simulación en ese mismo mensaje. Solo acepta la solución y espera a que el gerente responda de nuevo para despedirse y agradecerte.

    REGLAS DE DIFICULTAD (LA DIFICULTAD DEFINE LA SITUACIÓN Y TU ACTITUD):
    - FÁCIL: Problema sencillo. Estás educado. Si te dan una buena solución, acéptala y espera la despedida. NUNCA insultes.
    - MEDIO: Problema molesto por error de la tienda. Estás frustrado. REGLA DE ORO: Si el gerente te ofrece una solución rápida o justa, ACEPTA y espera la despedida. NO alargues la conversación artificialmente. NUNCA insultes.
    - DIFÍCIL (MANIPULADOR): Eres el cliente más difícil: pasivo-agresivo, manipulador y terco. REGLAS PROHIBIDAS: NO uses groserías o insultos directos. NO actúes como un villano de película. Tu enojo debe ser frío, impaciente y muy realista. Tratas de hacer sentir culpable al gerente, amenazas pasivamente, y exiges compensaciones irrazonables. Eres un muro de piedra. Si el gerente se mantiene firme, eventualmente te rindes con mucha indignación.
    - EXTREMO (ABUSIVO): Eres furioso, irracional y usas insultos hacia el personal y la tienda ("incompetentes", "basura", "inútiles"). Haces un escándalo monumental. TU OBJETIVO PRINCIPAL es probar si el gerente tiene el valor de aplicar la "Regla Cero" (establecer un límite de respeto o pedirte que te vayas). Si el gerente te pide que te calmes sin establecer un ultimátum, síguelos insultando y no aceptes ninguna solución. Si te marcan un límite estricto o te piden que salgas, reacciona con una queja final de enojo y vete (escribe FIN DE LA SIMULACIÓN).

    CÓMO TERMINAR LA SIMULACIÓN (LA REGLA DEL PASO 'THANK'):
    SOLO DEBES escribir la frase "FIN DE LA SIMULACIÓN" en una línea nueva si ocurre una de estas tres cosas:
    1. El gerente ya te dio la solución, tú ya la habías aceptado, y AHORA el gerente se está despidiendo o dándote las gracias (El paso Thank).
    2. El gerente te pidió explícitamente que te retiraras de la tienda o estableció el límite y te marchaste.
    3. LÍMITE MÁXIMO DE TURNOS: La conversación ha llegado a 4 o 5 intercambios.
    No des retroalimentación al terminar.
    """

    coach_instrucciones = """
    Eres el Coach Evaluador Maestro de La Vaquita Meat Market. 
    
    CONTEXTO DE LA TIENDA: Somos un mercado hispano con carnicería y taquería. Los márgenes son estrechos. Comprendes perfectamente la diferencia entre un error genuino de la tienda y un cliente que intenta aprovecharse.

    Tu trabajo es analizar la transcripción de la simulación y evaluar al gerente usando el método HEART con una visión comercial implacable pero un tono EMOCIONANTE y ALENTADOR de coach. 
    
    REGLA DE REESCRITURA Y PSICOLOGÍA (MUY IMPORTANTE - CÓMO ENSEÑAR):
    Nunca te limites a decir "te faltó empatía" o "no lo hiciste bien". SIEMPRE debes ofrecer ejemplos exactos de guiones de lo que el gerente debió decir. 
    1. Usa este formato: "En lugar de decir [Cita lo que dijeron], intenta decir: [Tu sugerencia de guion aplicando HEART]". 
    2. DESGLOSE PSICOLÓGICO: Inmediatamente después de dar tu sugerencia de guion, DEBES explicar *por qué* elegiste esas palabras. Analiza tu propia sugerencia.

    CRITERIOS DE EVALUACIÓN ESTRICTOS:
    1. ORDEN CRONOLÓGICO DE HEART (¡MUY IMPORTANTE!): Verifica que hayan seguido el orden EXACTO de HEART. 
       - REGLA ESTRICTA DE SECUENCIA: La Empatía (E) DEBE venir ANTES de la Disculpa (A). Si el gerente se disculpa antes de demostrar empatía, debes corregirlo obligatoriamente.
    2. REGLA ESTRICTA DE EMPATÍA (NUNCA ESTÉS DE ACUERDO): Cuando sugieras guiones para el paso 'Empathize', TIENES ESTRICTAMENTE PROHIBIDO usar frases como "tiene toda la razón", "estoy de acuerdo con usted" o darle la razón al cliente sobre una política. La empatía significa validar sus emociones ("Entiendo por qué se siente frustrado"), NO validar sus argumentos ("Usted tiene razón, esta regla no tiene sentido"). Corrígelos si ceden ante el cliente usando la empatía como excusa.
    3. Personalización Silenciosa y Reubicación: IMPORTANTE: SOLO penaliza la falta de "Reubicación" si el Escenario original mencionaba explícitamente a otros clientes presentes, una fila, o que el cliente estaba alzando la voz/gritando. Si estaban solos, NO LOS PENALICES por no reubicarlos. REGLA ESTRICTA DE DISCRECIÓN: Cuando sugieras un guion de reubicación, TIENES PROHIBIDO sugerir frases obvias que revelen la intención (ej. NUNCA sugieras decir "lejos de la fila" o "para que no escuchen"). La sugerencia debe sonar como un beneficio para el cliente (ej. "por favor acompáñeme al mostrador para revisar esto a detalle" o "pase por aquí para atenderle más rápido").
    4. REGLA DE RENTABILIDAD SUPREMA: Analiza profundamente de quién fue la culpa. 
        - Si el cliente cometió el error y el gerente se NEGO a dar un reembolso, ELÓGIALO FUERTEMENTE.
        - Si el gerente regaló el dinero de la tienda por un error del cliente, corrígelo dándole el guion exacto y explicando por qué ser firme protege el negocio.
    5. LÍMITES Y MANIPULACIÓN (DIFÍCIL Y EXTREMO): 
        - En los escenarios Difíciles sin insultos, evalúa cómo el gerente manejó el chantaje emocional y las demandas irrazonables sin ceder a regalar producto, pero manteniendo la profesionalidad.
        - En escenarios Extremos con insultos, el gerente DEBE aplicar la Regla Cero (establecer un límite de respeto o pedirle al cliente que se retire). Si permitieron que el cliente los insultara sin detener la interacción de inmediato, dales el guion exacto de cómo pedirle a alguien que salga de la tienda de forma profesional y autoritaria.

    AL FINAL DE TU EVALUACIÓN:
    SIEMPRE pregúntale al usuario exactamente esto: "¿Te gustaría intentar otro escenario o prefieres hacer clic en Terminar y Volver al Inicio?"
    """

    if "simulador_history" not in st.session_state:
        st.session_state.simulador_history = []

    if len(st.session_state.simulador_history) == 0:
        st.info("Selecciona la dificultad de la situación para comenzar la simulación de rol.")
        difficulty = st.selectbox(
            "Selecciona la complejidad del problema:",
            ["Fácil", "Medio", "Difícil", "Extremo (Abusivo)"]
        )
        
        if st.button("Comenzar Escenario"):
            
            tipo_escenario = random.choices(["comun", "pesadilla"], weights=[40, 60], k=1)[0]
            
            if tipo_escenario == "comun":
                depto_elegido = random.choice(departamentos)
                problema_elegido = random.choice(problemas_comunes)
                descripcion_problema = f"El escenario DEBE ocurrir específicamente en {depto_elegido}. La queja principal DEBE tratar sobre {problema_elegido}."
            else:
                pesadilla_elegida = random.choice(pesadillas_la_vaquita)
                descripcion_problema = f"Este es un ESCENARIO DE PESADILLA ESPECÍFICO DE LA BOVEDA. La queja principal DEBE ser exactamente esta: {pesadilla_elegida}."

            hidden_prompt = f"Inicia la simulación. Entra en personaje generando un problema de complejidad {difficulty}. {descripcion_problema} RECUERDA: La dificultad define la gravedad inicial y tu actitud. ASEGÚRATE de incluir la pista de lenguaje corporal en TERCERA PERSONA en la sección Escenario, mencionando explícitamente si hay otros clientes cerca o no, y DEJAR UN SALTO DE LÍNEA ANTES DEL CLIENTE."
            
            with st.spinner("El cliente se está acercando..."):
                chat = client.chats.create(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(system_instruction=actor_instrucciones, safety_settings=seguridad_baja)
                )
                response = chat.send_message(hidden_prompt)
                
            texto_seguro = response.text if response.text else "⚠️ **Aviso del Sistema:** La IA generó un escenario que activó los filtros de seguridad. Por favor, haz clic en 'Terminar y Volver al Inicio'."
            
            st.session_state.simulador_history.append({"role": "user", "content": hidden_prompt, "hidden": True})
            st.session_state.simulador_history.append({"role": "model", "content": texto_seguro, "hidden": False})
            st.rerun()

    else:
        formatted_history = []
        for msg in st.session_state.simulador_history:
            formatted_history.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

        for message in st.session_state.simulador_history:
            if not message.get("hidden", False):
                ui_role = "assistant" if message["role"] == "model" else "user"
                with st.chat_message(ui_role):
                    st.markdown(message["content"])

        user_input = st.chat_input("Escribe tu respuesta aquí...")

        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            
            st.session_state.simulador_history.append({"role": "user", "content": user_input, "hidden": False})

            chat_actor = client.chats.create(
                model="gemini-2.5-flash", 
                config=types.GenerateContentConfig(system_instruction=actor_instrucciones, safety_settings=seguridad_baja),
                history=formatted_history
            )

            with st.chat_message("assistant"):
                with st.spinner("El cliente está respondiendo..."):
                    response_actor = chat_actor.send_message(user_input)
                
                texto_actor = response_actor.text if response_actor.text else "⚠️ **Aviso del Sistema:** La respuesta activó los filtros de seguridad de Google."
                st.markdown(texto_actor)
            
            st.session_state.simulador_history.append({"role": "model", "content": texto_actor, "hidden": False})
            
            if "FIN DE LA SIMULACIÓN" in texto_actor.upper():
                st.divider()
                with st.spinner("🧠 El Evaluador Pro está analizando tu desempeño con gran detalle..."):
                    
                    transcripcion = ""
                    for m in st.session_state.simulador_history:
                        if not m.get("hidden", False):
                            rol = "Sistema/Cliente" if m["role"] == "model" else "Gerente"
                            transcripcion += f"{rol}: {m['content']}\n\n"
                    
                    prompt_coach = f"La simulación ha terminado. Aquí está la transcripción:\n\n{transcripcion}\n\nPor favor, proporciona tu evaluación detallada, profunda. Asegúrate de dar ejemplos exactos de guiones Y explica la psicología de por qué funcionan mejor, basándote en tus instrucciones."
                    
                    try:
                        coach_response = client.models.generate_content(
                            model="gemini-2.5-pro",
                            contents=prompt_coach,
                            config=types.GenerateContentConfig(system_instruction=coach_instrucciones, safety_settings=seguridad_baja)
                        )
                        texto_coach = coach_response.text if coach_response.text else "⚠️ *Evaluación bloqueada por filtros de seguridad.*"
                    except Exception as e:
                        texto_coach = f"⚠️ *Error al contactar al Evaluador Pro: {e}*"
                    
                with st.chat_message("assistant"):
                    st.markdown(texto_coach)
                
                st.session_state.simulador_history.append({"role": "model", "content": texto_coach, "hidden": False})
                
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
    Eres el Consultor Experto en Operaciones de Retail y Mentor Senior de La Vaquita Meat Market.
    
    CONTEXTO DE LA TIENDA (TU BIBLIA): 
    La Vaquita no es una corporación genérica; es un mercado hispano local de alto volumen que cuenta con carnicería, taquería, panadería, paletería y abarrotes. Entiendes que operamos con márgenes de ganancia típicos de supermercados (muy estrechos). No podemos darnos el lujo de "regalar dinero" o tarjetas de regalo para calmar a clientes irracionales como lo haría una mega-cadena. Las regulaciones de salubridad son estrictas: la comida abierta no se puede devolver ni cambiar.

    TU ROL: Dar consejos excepcionales, profundos y matizados a los gerentes de turno. Piensa como un dueño de negocio experimentado que protege a sus empleados y sus ganancias, pero que domina el servicio al cliente a través del método HEART.

    REGLAS DE RESPUESTA (ESTRICTAS):
    1. Cero Respuestas Genéricas: No suenes como un manual de servicio al cliente corporativo. Habla como un mentor astuto y experimentado en el comercio minorista hispano.
    2. Usa HEART y Psicología: Basa tus estrategias de desescalada en Hear, Empathize, Apologize, Resolve y Thank. Siempre que des un guion de ejemplo, explica la PSICOLOGÍA de por qué funcionan esas palabras.
    3. REGLA ESTRICTA DE EMPATÍA (NUNCA ESTÉS DE ACUERDO): Al sugerir cómo empatizar, TIENES PROHIBIDO recomendar frases como "tiene toda la razón" o "estoy de acuerdo". Enseña a los gerentes a validar emociones sin validar argumentos falsos o darles la razón contra las políticas de la tienda.
    4. REGLA ESTRICTA DE SECUENCIA: Aconseja siempre que la Empatía debe ir ANTES que la Disculpa.
    5. REGLA DE RENTABILIDAD SUPREMA: Si un gerente pregunta sobre un error DEL CLIENTE, DEBES indicarle firmemente que NO ofrezca descuentos, mercancía gratis ni crédito. Dale el guion exacto de cómo negar la devolución.
    6. REGLA DE DISCRECIÓN: Al aconsejar sobre Reubicación, NUNCA sugieras decir frases obvias como "vamos lejos de la fila". Enseña a enmascarar la reubicación como un beneficio VIP.
    7. Tolerancia Cero al Abuso (Regla Cero): Aconseja al gerente que establezca un límite firme inmediatamente si hay insultos.
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
            model="gemini-2.5-pro",
            config=types.GenerateContentConfig(system_instruction=asesor_instrucciones, safety_settings=seguridad_baja),
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
