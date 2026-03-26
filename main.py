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
    HEART es un acrónimo (por sus siglas en inglés) que representa un **método paso a paso probado para manejar quejas y situaciones difíciles** con los clientes. No es solo un guion, es una estrategia psicológica.

    ### ¿Para qué se utiliza?
    Se utiliza para **desescalar la tensión** cuando un cliente está enojado, frustrado o exigente. Te da una estructura clara para calmar la situación, encontrar una solución lógica y despedir al cliente de manera profesional, todo sin perder el control de la conversación.

    ### ¿Por qué es tan importante en La Vaquita?
    En un mercado de alto volumen, los problemas van a suceder. Sin un método, es fácil tomar los gritos de manera personal, ponerse a la defensiva, discutir, o peor aún, regalar mercancía o dinero por pánico. El método HEART te protege a ti y a las ganancias de la tienda, dándote las herramientas para mantenerte firme, profesional y en control total.
    """)
    
    st.divider()
    st.write("### Los 5 Pasos de HEART")
    st.write("Abre y estudia detalladamente cada paso. Luego, baja para completar el Tutorial Guiado.")
    
    with st.expander("👂 H - Hear (Escuchar activamente)", expanded=False):
        st.markdown("""
        Cuando un cliente molesto se comunica contigo, su necesidad principal es sentirse escuchado y comprendido. Sin embargo, **existen dos formas de Escuchar, dependiendo de la situación:**
        
        **1. Escucha Silenciosa (Para quejas sobre empleados, filas, o errores menores):** Si el cliente está molesto por una experiencia en la tienda, o porque un empleado supuestamente fue rudo, tu trabajo es **guardar silencio absoluto**. Deja que se desahogue por completo. NUNCA interrumpas para hacer preguntas aquí; el cliente se sentirá interrogado y pensará que defiendes al empleado. Usa solo asentimientos verbales ("ya veo", "entiendo").
        
        **2. Escucha Investigativa (SOLO para problemas graves de transacciones, como comida o reembolsos sin recibo):**
        Si el cliente pide un reembolso pero no tiene su recibo, no puedes solo quedarte callado. Debes hacer **preguntas de investigación neutrales** *antes* de que termine su historia para buscar la transacción en el sistema ("¿Pagó con tarjeta o en efectivo?").
        """)

    with st.expander("🤝 E - Empathize (Empatizar)", expanded=False):
        st.markdown("""
        Una vez que el cliente ha contado su historia (y tú lo has Escuchado), la empatía construye un puente entre escuchar y resolver. Le demuestra al cliente que comprendes sus sentimientos y validas su frustración, incluso si aún no has determinado de quién es la culpa o cómo solucionarlo.
        
        **Las acciones clave para este paso incluyen:**
        * **Reflejar su urgencia:** Ajusta tu tono para demostrar que te tomas el asunto tan en serio como ellos.
        * **Validar sus emociones:** Usa frases naturales que reconozcan sus sentimientos específicos (por ejemplo: frustración, decepción). Habla como un ser humano, no como un robot.
        * **Evitar ponerse a la defensiva:** Mantente alejado de citar políticas de la empresa o poner excusas.
        * <u>**Empatizar no significa estar de acuerdo con ellos.**</u>
        """, unsafe_allow_html=True)

    with st.expander("🙏 A - Apologize (Ofrecer disculpas)", expanded=False):
        st.markdown("""
        Si el problema es un error comprobado de la tienda (ej. comida en mal estado, cobro doble, sistema caído), asume la responsabilidad en nombre de la empresa con una disculpa clara ("Lo siento que le hayamos fallado con este producto").
        
        🚨 **REGLA PARA QUEJAS DE EMPLEADOS (La Disculpa de Experiencia):**
        Si el cliente se queja de un empleado, NUNCA admitas la culpa del empleado frente al cliente ("Siento que ella fuera grosera"). En su lugar, discúlpate por la **experiencia**: *"Lo siento mucho por la mala experiencia y la frustración que esto le causó."*
        
        🚨 **LA TRAMPA DE LA DISCULPA (Errores del Cliente):**
        Si el problema fue causado por el propio cliente (ej. agarró el producto equivocado, tiró un artículo, leyó mal un letrero), **OMITE ESTE PASO. NO TE DISCULPES.** Disculparte por el error del cliente admite responsabilidad de la tienda y te quita autoridad. Decir "Siento la confusión" es una disculpa disfrazada que también admite culpa. 
        
        En su lugar, usa una **"Empatía Neutral para Salvar el Ego"** en el paso anterior. 
        ❌ *Incorrecto (Culpar a la tienda o asumir):* "Nuestros letreros están muy juntos" o "Seguro venía con prisa".
        ✅ *Correcto (Neutral):* "Entiendo perfectamente la confusión, es un error muy común que a todos nos pasa. Solo para aclarar, el precio correcto es..." y pasa directamente a Resolver (R).
        """)

    with st.expander("🛠️ R - Resolve (Resolver y Reubicar)", expanded=False):
        st.markdown("""
        Después de escuchar, empatizar y disculparse, este paso se trata de actuar y ser transparente sobre la solución. 
        
        **🚨 REGLA PARA QUEJAS DE EMPLEADOS:**
        *Aquí* es donde finalmente haces tus preguntas de investigación ("¿Podría decirme exactamente qué le dijo la empleada?"). Luego, promete un proceso justo ("Voy a investigar esto internamente con el equipo"). Nunca prometas castigos frente al cliente.
        
        **Las acciones clave para este paso incluyen:**
        * **Solucionar el problema:** Resuelve el problema de inmediato si puedes.
        * **Ofrecer opciones:** Dale alternativas al cliente siempre que sea posible.
        * **Personalización silenciosa (Lectura del cliente):** Observa el lenguaje corporal del cliente y adapta tu solución a su situación sin señalar su estrés explícitamente.
        """)

    with st.expander("💖 T - Thank (Agradecer)", expanded=False):
        st.markdown("""
        Aunque pueda parecer contradictorio agradecer a alguien que se acaba de quejar, expresar gratitud es una manera poderosa de cerrar la conversación. Deja al cliente con una impresión final positiva y replantea su queja como comentarios valiosos que ayudan a la empresa a mejorar.
        """)

    st.warning("""💰 **REGLA DE RENTABILIDAD SUPREMA Y PROCEDIMIENTOS**

En La Vaquita operamos con márgenes estrechos. Tu trabajo es proteger las ganancias, pero también salvar la relación con el cliente.

* **Devoluciones Sin Recibo:** ¡No digas 'no' inmediatamente! Pregunta cómo pagaron. Si fue con **Tarjeta**, pídeles revisar su app. Si fue en **Efectivo**, haz preguntas para acotar la búsqueda. **SI LA BÚSQUEDA FALLA:** Usa el sistema como escudo. Di: *'Revisé minuciosamente y al no aparecer la transacción, no me es posible autorizar un reembolso.'* NUNCA entregues efectivo si no hay registro.
* **Error del Cliente:** NUNCA regales dinero, ofrezcas descuentos ni reembolsos si el cliente causó el problema.
* **Descuentos (Solo Errores Mayores):** Los descuentos a la cuenta total SOLO están permitidos para Errores Mayores de la tienda (ej. vender producto caducado o cobrar doble).
* **CERO Tarjetas de Regalo:** Jamás ofrezcas 'gift cards' o 'store credit'.

🥤 **EL PODER DE LA CORTESÍA DE BAJO COSTO (Agua Fresca / Pan Dulce)**
Regalar un artículo de bajo costo es una gran herramienta para calmar a un cliente enojado sin destruir nuestra rentabilidad, **PERO DEBE USARSE CORRECTAMENTE Y EXCLUSIVAMENTE PARA ERRORES DE LA TIENDA:**

✅ **CUÁNDO SÍ DAR UNA CORTESÍA:**
* **La cocina cometió un error:** (Ej. Se nos quemó o cayó su orden y tenemos que hacerla de nuevo, retrasándolos 15 minutos).
* **Falla del sistema:** (Ej. La terminal falló y estuvieron atrapados en la caja mientras lo reiniciábamos).
* **Órdenes previas retrasadas por culpa de la tienda:** (Ej. Ordenaron barbacoa para las 12:00 PM, llegaron a tiempo, pero no estuvo lista hasta las 12:30 PM).

❌ **CUÁNDO NO DAR UNA CORTESÍA (Totalmente Prohibido):**
* **Para CUALQUIER experiencia normal de compra:** Esto incluye filas largas regulares (incluso si la tienda está muy llena), un producto que se agotó normalmente, el estacionamiento lleno, ruido en la tienda, o si el cliente llegó antes de la hora de su pedido. *Regalar producto por las fricciones normales del éxito y volumen de la tienda destruye las ganancias y acostumbra mal al cliente. Aquí solo debes empatizar y agradecer su paciencia.*
""")
        
    st.error("🛑 **REGLA CERO: ESTABLECER LÍMITES**\n\nEl cliente es importante, pero **el respeto hacia ti y tu equipo es innegociable.** Si un cliente usa insultos, lenguaje vulgar o denigra a un empleado, DEBES establecer un límite profesional de inmediato. No toleres el abuso verbal solo por cerrar una venta.\n\n✅ *Correcto:* 'Señor, quiero ayudarle a resolver su problema con su pedido, pero le pido que nos comuniquemos con respeto o no podré seguir asistiéndole.'\n\n🚨 **Si el cliente continúa siendo abusivo después de establecer el límite:** Debes dar por terminada la interacción y pedirle explícitamente que abandone la tienda.")

    st.divider()
    st.subheader("🎓 Tutor Paso a Paso")
    st.write("Es hora de practicar. El Tutor Virtual te presentará un escenario y te guiará letra por letra. Deberás responder correctamente cada paso antes de avanzar al siguiente.")

    tutor_instrucciones = """
    Eres el Tutor Maestro de La Vaquita Meat Market. 
    
    CONTEXTO DE LA TIENDA: La Vaquita es un mercado hispano de alto volumen. Los márgenes de supermercado son estrechos.
    
    TU OBJETIVO: Enseñar el método HEART paso a paso a un gerente en entrenamiento.

    INSTRUCCIONES DE TUTORÍA Y TONO (MUY IMPORTANTE):
    - Usa un lenguaje natural, directo y conversacional. No suenes como un robot corporativo. 
    - Los guiones que sugieras deben ser breves y sonar como una persona real. Evita frases artificiales como "Escucho todo lo que me dice". Usa cosas más naturales como "Entiendo lo frustrante que es esto".
    
    REGLAS ESTRICTAS DE EVALUACIÓN:
    1. REGLA DEL SIMULADOR DE TEXTO (ETAPA 'HEAR'): Si la queja requiere "Escucha Silenciosa", el gerente NO DEBE escribir NADA. Omite la evaluación de la "H" y empieza guiando desde la Empatía (E). NUNCA sugieras frases donde el gerente pida al cliente que repita lo que ya dijo en el texto.
    2. PROTOCOLO SIN RECIBO: Si el cliente no tiene recibo, el gerente DEBE preguntar cómo pagaron en (H) o (R) para buscarlo en el POS. 
    3. REGLA DEL GAME MASTER: Si el gerente dice que revisará el sistema, infórmale el resultado ANTES de pedirle que siga con (R).
    4. LA TRAMPA DE LA DISCULPA (Error del cliente): Si el cliente causó el problema, SALTARSE la disculpa (A). Su trabajo en Empatía (E) es "Empatía Neutral" ("Entiendo la confusión").
    5. QUEJAS SOBRE EMPLEADOS: En A (Apologize), DEBE disculparse por la mala *experiencia*, pero NO admitir culpa del empleado. En R (Resolve), DEBE hacer preguntas para investigar y prometer revisión interna.
    6. REGLA DE RENTABILIDAD Y CORTESÍAS: Cortesías SOLO para errores comprobados de la tienda. NUNCA por experiencias normales de compra (filas, etc).
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
                    descripcion_problema = f"La queja trata sobre {problema_elegido}. FÍSICAMENTE: El cliente se acerca directamente a ti (el gerente) en las Cajas Principales / Servicio al Cliente (o en el mostrador de {depto_elegido} si es una orden activa). NUNCA pongas al cliente deambulando por los pasillos si ya pagó o viene a hacer un reclamo post-compra."
                elif tipo_escenario == "especial":
                    problema_elegido = random.choice(errores_cliente)
                    descripcion_problema = f"ESTE ES UN CASO ESPECIAL DE ERROR DEL CLIENTE. La situación es: {problema_elegido}. FÍSICAMENTE: El cliente se acerca a ti en las Cajas Principales."
                else:
                    pesadilla_elegida = random.choice(pesadillas_la_vaquita)
                    descripcion_problema = f"La queja principal DEBE ser exactamente esta: {pesadilla_elegida}."

                hidden_prompt = f"Hola. Genera el escenario inicial usando esta premisa: {descripcion_problema}. Asegúrate de incluir la pista física en tercera persona. Preséntamelo. Si es un escenario de escucha silenciosa, pídeme que comience directamente con el paso Empatía (E). Si es de investigar recibos, pídeme el paso (H). Código: {random.randint(1,10000)}"
                
                try:
                    chat = client.chats.create(
                        model="gemini-2.5-pro",
                        config=types.GenerateContentConfig(system_instruction=tutor_instrucciones, safety_settings=seguridad_baja)
                    )
                    response = chat.send_message(hidden_prompt)
                    texto_seguro = response.text if response.text else "⚠️ *El filtro de seguridad bloqueó la respuesta. Por favor, reinicia el tutorial.*"
                    st.session_state.tutor_history.append({"role": "user", "content": hidden_prompt, "hidden": True})
                    st.session_state.tutor_history.append({"role": "model", "content": texto_seguro, "hidden": False})
                    st.rerun()
                except Exception as e:
                    st.error("⚠️ Servidores ocupados (Error 503). Por favor, intenta de nuevo en unos segundos.")
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

    REGLAS DE FORMATO (MUY IMPORTANTE):
    1. Para tu PRIMER mensaje, debes separar el contexto objetivo de lo que dices en voz alta. DEBE HABER UN SALTO DE LÍNEA entre los dos. Usa este formato exacto:
    
    **Escenario:** [Describe tu lenguaje corporal estrictamente en TERCERA PERSONA como un narrador objetivo].

    **Cliente:** "[Escribe tu queja inicial en voz alta, en primera persona]".
    
    2. En el resto de la conversación, SOLO escribe lo que dices en voz alta. Cero asteriscos, cero monólogos internos.

    NUEVA REGLA DEL GAME MASTER (CÁMARAS Y SISTEMA): 
    Si el gerente te dice que va a revisar las cámaras, el recibo o el sistema POS, debes salir brevemente de tu personaje para darle el resultado de su búsqueda con este formato: "[Sistema: Revisa la cámara/sistema y efectivamente encuentras el recibo]". Luego, responde como cliente.

    DETALLES CONTEXTUALES UNIVERSALES: 
    Compórtate como un ser humano real. Usa excusas de la vida real. Si la queja es por una fila larga, quejate de que llevas mucho tiempo esperando. Si es un error Tuyo, muéstrate un poco a la defensiva o apenado.

    REGLAS DE DIFICULTAD (LA DIFICULTAD DEFINE LA SITUACIÓN Y TU ACTITUD):
    - FÁCIL: Problema sencillo. Estás educado. 
    - MEDIO: Estás frustrado. Si el gerente te ofrece una solución rápida o justa, ACEPTA y espera la despedida. NUNCA insultes.
    - DIFÍCIL (MANIPULADOR): Eres pasivo-agresivo y terco. Si el gerente se mantiene firme, te rindes con indignación.
    - EXTREMO (ABUSIVO): Eres furioso y usas insultos. TU OBJETIVO es probar si el gerente aplica la "Regla Cero". Si te marcan límite, vete (escribe FIN DE LA SIMULACIÓN).

    CÓMO TERMINAR LA SIMULACIÓN:
    SOLO DEBES escribir la frase "FIN DE LA SIMULACIÓN" en una línea nueva si el gerente completó la interacción, si te pidió que te retiraras, o si llegaron a 5 intercambios.
    """

    coach_instrucciones = """
    Eres el Coach Evaluador Maestro de La Vaquita Meat Market. 
    
    CONTEXTO Y TONO (MUY IMPORTANTE): 
    Evalúa al gerente de forma directa y concisa. NO escribas párrafos gigantes de filosofía. Ve directo al grano.
    Cuando sugieras un guion para el gerente, DEBE sonar como un ser humano real. ESTÁ ESTRICTAMENTE PROHIBIDO sugerir frases robóticas o poco naturales como "Escucho todo lo que me dice" o "Comprendo plenamente su perspectiva". Usa un lenguaje natural, conversacional y directo (ej. "Entiendo perfectamente la frustración", "Lamento la mala experiencia").

    CRITERIOS DE EVALUACIÓN ESTRICTOS:
    1. REGLA DEL SIMULADOR DE TEXTO (OMITIR 'HEAR'): Dado que este es un simulador de texto, la etapa de "Escucha Silenciosa" ocurre cuando el gerente lee el mensaje. OMITE LA SECCIÓN "H - Hear" EN TU EVALUACIÓN por completo. Empieza a evaluar directamente en "E - Empathize". ESTÁ ESTRICTAMENTE PROHIBIDO penalizar al gerente por no escribir "lo escucho" o pedirles que repitan la historia.
    2. PROTOCOLO SIN RECIBO: Si el cliente no tenía recibo, ¿preguntó el método de pago? Si no apareció, ¿usó el sistema como escudo?
    3. QUEJAS SOBRE EMPLEADOS (LA DISCULPA DE EXPERIENCIA): En A (Apologize), el gerente DEBE disculparse SOLO por la mala *experiencia*, y NO admitir culpa del empleado. En R (Resolve), DEBE hacer preguntas de investigación y prometer revisión interna.
    4. LA TRAMPA DE LA DISCULPA (Error del cliente): Si el cliente causó el problema, el gerente NO debe disculparse. Exígeles usar "Empatía Neutral".
    5. REGLA DE RENTABILIDAD Y CORTESÍAS: Cortesías SOLO para errores comprobados de la tienda. ESTÁ PROHIBIDO regalar producto por experiencias normales (filas, etc).
    6. LÍMITES: En escenarios Extremos con insultos, el gerente DEBE aplicar la Regla Cero.

    AL FINAL DE TU EVALUACIÓN:
    SIEMPRE pregúntale al usuario exactamente esto: "¿Te gustaría intentar otro escenario o prefieres hacer clic en Reiniciar Simulador?"
    """

    # --- INICIO DEL SIMULADOR ---
    if len(st.session_state.simulador_history) == 0 and not st.session_state.simulador_concluido:
        st.info("Selecciona la dificultad de la situación para comenzar la simulación de rol.")
        difficulty = st.selectbox(
            "Selecciona la complejidad del problema:",
            ["Fácil", "Medio", "Difícil", "Extremo (Abusivo)", "Casos Especiales (Errores del Cliente)"]
        )
        
        if st.button("Comenzar Escenario"):
            
            if difficulty in ["Fácil", "Medio"]:
                depto_elegido = random.choice(departamentos)
                problema_elegido = random.choice(problemas_comunes)
                descripcion_problema = f"La queja trata sobre {problema_elegido}. FÍSICAMENTE: El cliente se acerca directamente a ti (el gerente) en las Cajas Principales / Servicio al Cliente (o en el mostrador de {depto_elegido} si es una orden activa). NUNCA pongas al cliente deambulando por los pasillos si ya pagó o viene a hacer un reclamo post-compra."
            elif difficulty == "Casos Especiales (Errores del Cliente)":
                problema_elegido = random.choice(errores_cliente)
                descripcion_problema = f"ESTE ES UN CASO ESPECIAL DE ERROR DEL CLIENTE. La situación es: {problema_elegido}. FÍSICAMENTE: El cliente se acerca a ti en las Cajas Principales."
            else:
                pesadilla_elegida = random.choice(pesadillas_la_vaquita)
                descripcion_problema = f"Este es un ESCENARIO DE PESADILLA ESPECÍFICO DE LA BOVEDA. La queja principal DEBE ser exactamente esta: {pesadilla_elegida}."

            hidden_prompt = f"Inicia la simulación. Entra en personaje generando un problema de complejidad {difficulty}. {descripcion_problema} RECUERDA: La dificultad define la gravedad inicial y tu actitud. ASEGÚRATE de incluir la pista de lenguaje corporal en TERCERA PERSONA en la sección Escenario, mencionando explícitamente si hay otros clientes cerca o no, y DEJAR UN SALTO DE LÍNEA ANTES DEL CLIENTE."
            
            with st.spinner("El cliente se está acercando..."):
                try:
                    chat = client.chats.create(
                        model="gemini-2.5-flash",
                        config=types.GenerateContentConfig(system_instruction=actor_instrucciones, safety_settings=seguridad_baja)
                    )
                    response = chat.send_message(hidden_prompt)
                    texto_seguro = response.text if response.text else "⚠️ **Aviso del Sistema:** La IA generó un escenario que activó los filtros de seguridad. Por favor, haz clic en 'Reiniciar Simulador'."
                    st.session_state.simulador_history.append({"role": "user", "content": hidden_prompt, "hidden": True})
                    st.session_state.simulador_history.append({"role": "model", "content": texto_seguro, "hidden": False})
                    st.rerun()
                except Exception as e:
                    st.error("⚠️ Los servidores de Google están experimentando alta demanda (Error 503). Por favor, intenta de nuevo en unos segundos.")

    # --- DESARROLLO DEL SIMULADOR ---
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
                        
                        texto_actor = response_actor.text if response_actor.text else "⚠️ **Aviso del Sistema:** La respuesta activó los filtros de seguridad de Google."
                        st.markdown(texto_actor)
                    
                    st.session_state.simulador_history.append({"role": "model", "content": texto_actor, "hidden": False})
                    
                    if "FIN DE LA SIMULACIÓN" in texto_actor.upper():
                        st.session_state.simulador_concluido = True
                        st.rerun()
                except Exception as e:
                    st.session_state.simulador_history.pop()
                    st.error("⚠️ El servidor de Google tuvo un problema de conexión (Error 503). Por favor, vuelve a enviar tu mensaje.")

        st.divider()
        st.caption("¿Resolviste el problema? Haz clic abajo para ser evaluado por el Coach.")
        if st.button("Terminar y Evaluar"):
            st.session_state.simulador_concluido = True
            st.rerun()

    # --- RESULTADOS DEL SIMULADOR ---
    if st.session_state.simulador_concluido:
        for message in st.session_state.simulador_history:
            if not message.get("hidden", False):
                ui_role = "assistant" if message["role"] == "model" else "user"
                with st.chat_message(ui_role):
                    st.markdown(message["content"])
                    
        st.divider()
        st.subheader("🛑 SIMULACIÓN TERMINADA.")
        
        if not st.session_state.coach_feedback:
            with st.spinner("🧠 El Evaluador Pro está analizando tu desempeño..."):
                transcripcion = ""
                for m in st.session_state.simulador_history:
                    if not m.get("hidden", False):
                        rol = "Sistema/Cliente" if m["role"] == "model" else "Gerente"
                        transcripcion += f"{rol}: {m['content']}\n\n"
                
                prompt_coach = f"La simulación ha terminado. Aquí está la transcripción:\n\n{transcripcion}\n\nPor favor, proporciona tu evaluación detallada, profunda y CONCISA. Asegúrate de dar ejemplos exactos de guiones Y explica la psicología de por qué funcionan mejor, basándote en tus instrucciones."
                
                try:
                    coach_response = client.models.generate_content(
                        model="gemini-2.5-pro",
                        contents=prompt_coach,
                        config=types.GenerateContentConfig(system_instruction=coach_instrucciones, safety_settings=seguridad_baja)
                    )
                    st.session_state.coach_feedback = coach_response.text if coach_response.text else "⚠️ *Evaluación bloqueada por filtros de seguridad.*"
                    st.session_state.api_error = False
                except Exception as e:
                    st.session_state.api_error = True

        if st.session_state.api_error:
            st.error("⚠️ Los servidores de Google están experimentando alta demanda (Error 503). No hemos podido generar tu evaluación.")
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
    
    CONTEXTO Y TONO: 
    Habla como un mentor astuto y directo. NUNCA uses frases robóticas o excesivamente formales ("Escucho todo lo que me dice"). Usa un lenguaje natural y humano.

    REGLAS DE RESPUESTA (ESTRICTAS):
    1. QUEJAS SOBRE EMPLEADOS: Aconseja estrictamente que NUNCA interrumpan al cliente en la fase (H) Hear para investigar. Deben dejarlo desahogarse. En la fase (A) Apologize, deben disculparse por la mala *experiencia*, pero NO admitir culpa del empleado. Las preguntas de investigación se hacen hasta la fase (R) Resolve.
    2. LA TRAMPA DE LA DISCULPA (Error del cliente): Aconseja estrictamente a los gerentes que NUNCA se disculpen cuando el cliente causó el problema. Enséñales a usar "Empatía Neutral".
    3. PROTOCOLO SIN RECIBO: Enséñales a investigar primero. Si la búsqueda falla, usar el escudo del sistema para negar la devolución.
    4. REGLA CERO TARJETAS DE REGALO Y CORTESÍAS: Advierte explícitamente a los gerentes que NO REGALEN cortesías de bajo costo por NINGUNA experiencia normal de compra. Las cortesías son EXCLUSIVAMENTE para demoras causadas por errores comprobados de la tienda.
    5. Tolerancia Cero al Abuso (Regla Cero): Aconseja al gerente que establezca un límite firme inmediatamente si hay insultos.
    """

    if "asesor_history" not in st.session_state:
        st.session_state.asesor_history = []

    for msg in st.session_state.asesor_history:
        ui_role = "assistant" if msg["role"] == "model" else "user"
        with st.chat_message(ui_role):
            st.markdown(msg["content"])

    pregunta_usuario = st.chat_input("Ej: ¿Qué hago si un cliente no está de acuerdo con la política de devoluciones?")

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
                    texto_asesor = "⚠️ *Ups, el servidor de Google tuvo un pequeño hipo de conexión. Por favor, intenta preguntar de nuevo en unos segundos.*"
                    st.session_state.asesor_history.pop() 
            st.markdown(texto_asesor)
            
        if texto_asesor and "⚠️" not in texto_asesor:
             st.session_state.asesor_history.append({"role": "model", "content": texto_asesor})
        
    if len(st.session_state.asesor_history) > 0:
        st.divider()
        if st.button("Limpiar Conversación"):
            st.session_state.asesor_history = []
            st.rerun()
