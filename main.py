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

# --- BÓVEDA DE ESCENARIOS SEPARADA POR DIFICULTAD (SINCRONIZADA CON EXAMEN) ---

# FÁCIL: Errores indiscutibles de la tienda EN EL MOSTRADOR.
problemas_faciles = [
    "un cliente en la carnicería que pidió 2 libras de fajita, pero el carnicero se equivocó y le empaquetó bistec regular. El cliente sigue frente a la vitrina, apenas revisó el paquete y está molesto por el descuido. REGLA ESTRICTA: El cliente NO ha pagado ni ha salido de la tienda.",
    "un cliente en la taquería que está comiendo en las mesas de la tienda y se levanta molesto al mostrador porque sus tacos se los acaban de entregar fríos por un descuido de la cocina. REGLA ESTRICTA: El cliente NO ha salido de la tienda, está consumiendo en el lugar.",
    "un cliente en la panadería que acaba de recibir su café en el mostrador, da un sorbo ahí mismo, y nota que la máquina estaba mal calibrada (le sirvieron agua manchada). Exige que se lo cambien. REGLA ESTRICTA: El cliente sigue frente al mostrador y acaba de recibir el producto."
]

# MEDIO: Requiere investigación, recibos, o manejar fricciones de tienda (filas/agotados).
problemas_medios = [
    "un cliente que se queja porque la fila para pagar en la caja principal está muy larga y lleva esperando 15 minutos",
    "un cliente que está molesto porque llegó a buscar su corte de carne o pan dulce favorito y ya se agotó por el día",
    "un cliente frustrado que intenta devolver un producto básico (como pan o fruta) argumentando que salió de mala calidad o echado a perder",
    "un empleado que supuestamente le dio un mal trato, lo ignoró o le habló con mala actitud al cliente",
    "un cliente que quiere cambiar un producto básico y cerrado (como unas papas o refresco) pero no tiene el recibo de compra",
    "un cliente que YA PAGÓ y llegó a su casa, pero tuvo que regresar muy molesto porque descubrió que le dieron el producto equivocado o le falta un artículo en sus bolsas"
]

# CASOS ESPECIALES: Trampa de la Disculpa
errores_cliente = [
    "un cliente que por error agarró el producto equivocado (ej. papas picantes en lugar de regulares) y quiere cambiarlo, sintiéndose un poco a la defensiva o avergonzado por su propio error",
    "un cliente que accidentalmente tiró y rompió un frasco de vidrio que ya había pagado antes de salir de la tienda, y pregunta un poco apenado si le pueden dar otro gratis",
    "un cliente que exige un descuento porque leyó mal un letrero de oferta que estaba claramente marcado para otro producto diferente, sintiéndose frustrado"
]

# EXTREMO/DIFÍCIL: Alta tensión, Regla Cero.
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

departamentos = ["la Carnicería", "la Taquería", "la Panadería", "la Paletería", "las Cajas Principales", "el Pasillo de Abarrotes", "el área de Frutas y Verduras"]

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
        Cuando un cliente molesto se acerca a ti, su necesidad principal es desahogarse.
        
        **El Poder del Silencio:** Tu único trabajo en esta etapa es **guardar silencio absoluto**. Deja que el cliente hable sin interrupciones. Usa solo asentimientos verbales y contacto visual. 
        
        🚨 **REGLA DE ORO:** NUNCA interrumpas al cliente para hacerle preguntas de investigación (ej. "¿Tiene su recibo?", "¿Qué le dijo el empleado?"). Hacer preguntas inmediatas se siente como un interrogatorio y pone al cliente a la defensiva antes de que hayas podido conectar con ellos. Déjalos terminar su historia primero.
        """)

    with st.expander("🤝 E - Empathize (Empatizar)", expanded=False):
        st.markdown("""
        Una vez que el cliente ha contado su historia, la empatía construye un puente. Le demuestra al cliente que comprendes sus sentimientos y validas su frustración, incluso si aún no has determinado de quién es la culpa o cómo solucionarlo.
        
        **Las acciones clave para este paso incluyen:**
        * **Validar sus emociones:** Usa frases naturales que reconozcan sus sentimientos específicos (por ejemplo: frustración, decepción). Habla como un ser humano real ("Entiendo perfectamente la molestia").
        * **Evitar ponerse a la defensiva:** Mantente alejado de citar políticas de la empresa o poner excusas, lo cual invalida de inmediato su experiencia.
        * <u>**Empatizar no significa estar de acuerdo con ellos.**</u>
        """, unsafe_allow_html=True)

    with st.expander("🙏 A - Apologize (Ofrecer disculpas)", expanded=False):
        st.markdown("""
        Saber **cómo y cuándo** disculparse es la parte más crítica del método HEART. En La Vaquita, usamos 4 tipos diferentes de disculpas dependiendo de quién causó el problema:

        **1. La Disculpa Operativa ("Lamento la equivocación con su pedido")**
        * **Cuándo usarla:** Hay un error comprobado y evidente de la tienda (ej. comida fría, le dieron bistec en vez de fajita, leche caducada).
        * **Por qué:** No necesitas investigar lo evidente. Asumir la culpa de inmediato demuestra competencia y construye confianza.

        **2. La Disculpa de Experiencia ("Lamento mucho su mala experiencia hoy")**
        * **Cuándo usarla:** Quejas sobre la **ACTITUD** de un empleado (ej. "el carnicero me ignoró", "la cajera me hizo mala cara").
        * **Por qué:** NUNCA debes admitir la culpa del empleado frente al cliente antes de revisar las cámaras. Disculparte por su "mala experiencia" valida los sentimientos del cliente, pero protege profesionalmente a tu equipo hasta que investigues.

        **3. La Disculpa de Cortesía ("Lamento el inconveniente de la espera")**
        * **Cuándo usarla:** Fricciones normales de una tienda exitosa (ej. fila de 15 minutos, se acabó su pan dulce favorito).
        * **Por qué:** Vender todo tu producto no es un error, es éxito. Usas esta disculpa como "pegamento social" para mostrar respeto por su tiempo perdido, sin admitir incompetencia.
        
        **4. CERO DISCULPAS (La Trampa de la Disculpa)**
        * **Cuándo usarla:** El cliente causó el problema (ej. leyó mal un letrero de oferta, agarró las papas equivocadas, rompió un frasco).
        * **Por qué:** Si el cliente se equivocó y tú dices "Lo siento", accidentalmente asumes la culpa por su error y pierdes autoridad. 
        * **Qué hacer en su lugar:** Usa "Empatía Neutral" en el paso anterior. (Ej: *"Entiendo la confusión, es un error común. El precio correcto es..."*).
        """)

    with st.expander("🛠️ R - Resolve (Resolver y Reubicar)", expanded=False):
        st.markdown("""
        Después de escuchar, empatizar y disculparse, el cliente se sentirá validado y estará listo para hablar de soluciones lógicas.
        
        **🕵️ EL MOMENTO DE INVESTIGAR:**
        *Aquí* es donde finalmente haces tus preguntas de investigación ("Para ayudarle a resolver esto, ¿podría prestarme su recibo?", "¿Recuerda exactamente qué le dijo el empleado?"). Al hacer las preguntas aquí, no suenas como un interrogador, sino como un aliado tratando de solucionar el problema.
        
        **Las acciones clave para este paso incluyen:**
        * **Solucionar el problema:** Resuelve el problema de inmediato si puedes.
        * **Ofrecer opciones:** Dale alternativas al cliente siempre que sea posible. Esto le devuelve la sensación de control.
        * **Personalización silenciosa (Lectura del cliente):** Observa el lenguaje corporal del cliente y adapta tu solución a su situación sin señalar su estrés explícitamente.
        """)

    with st.expander("💖 T - Thank (Agradecer)", expanded=False):
        st.markdown("""
        Aunque pueda parecer contradictorio agradecer a alguien que se acaba de quejar, expresar gratitud es una manera poderosa de cerrar la conversación. Deja al cliente con una impresión final positiva y replantea su queja como comentarios valiosos que ayudan a la empresa a mejorar.
        """)

    st.warning("""💰 **REGLA DE RENTABILIDAD SUPREMA: ¿Cuándo dar producto gratis o descuentos?**

En La Vaquita operamos con márgenes estrechos. Tu trabajo es proteger las ganancias, pero también salvar la relación con el cliente.

* **Devoluciones Sin Recibo:** ¡No digas 'no' inmediatamente! Haz preguntas (en la fase Resolve) para acotar la búsqueda en el sistema. **SI LA BÚSQUEDA FALLA:** Usa el sistema como escudo. Di: *'Revisé minuciosamente y al no aparecer la transacción, no me es posible autorizar un reembolso.'* NUNCA entregues efectivo si no hay registro.
* **Error del Cliente:** NUNCA regales dinero, ofrezcas descuentos ni reembolsos si el cliente causó el problema. Mantente firme.
* **El Poder de la Cortesía de Bajo Costo:** Las cortesías (agua fresca/pan dulce) son **EXCLUSIVAMENTE** para errores o demoras causadas por la tienda (ej. se quemó su comida). **ESTÁ PROHIBIDO** regalar producto por experiencias normales de compra, incluyendo filas regulares largas, tienda llena o productos agotados. Regalar por el éxito de la tienda destruye ganancias.
* **Descuentos (Solo Errores Mayores):** Los descuentos a la cuenta total SOLO están permitidos para Errores Mayores de la Tienda (ej. cobrar doble). NUNCA des un descuento por una simple demora.
* **CERO Tarjetas de Regalo:** Jamás ofrezcas 'gift cards' o 'store credit'. No somos una mega-cadena corporativa.
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
    - Los guiones que sugieras deben ser breves y sonar como una persona real. 
    
    REGLAS ESTRICTAS DE EVALUACIÓN:
    1. REGLA DEL SIMULADOR DE TEXTO Y SILENCIO (ETAPA 'HEAR'): La etapa H (Hear) es 100% ESCUCHA SILENCIOSA para TODOS los escenarios. El gerente NO DEBE escribir NADA en esta etapa en el simulador. Omite la evaluación de la "H" y empieza guiando al usuario directamente desde la Empatía (E). NUNCA pidas o sugieras frases donde el gerente haga preguntas en la etapa Hear.
    2. TODAS LAS PREGUNTAS VAN EN RESOLVE (R): Si el gerente necesita pedir un recibo, buscar en el sistema POS, o preguntar los detalles de qué hizo un empleado, DEBEN hacerlo exclusivamente en la etapa Resolve (R).
    3. REGLA DEL GAME MASTER: Si el gerente dice que revisará el sistema, infórmale el resultado ANTES de pedirle que siga con (R).
    4. LA TRAMPA DE LA DISCULPA (Error del cliente): Si el cliente causó el problema, SALTARSE la disculpa (A). Su trabajo en Empatía (E) es "Empatía Neutral" ("Entiendo la confusión").
    5. QUEJAS DE ACTITUD DE EMPLEADOS: En A (Apologize), si se quejan de la *actitud* de un empleado, no admitir culpa del empleado. SIN EMBARGO, si es un ERROR OPERATIVO EVIDENTE (carne equivocada, comida fría), el gerente DEBE asumir responsabilidad y disculparse.
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
                    problema_elegido = random.choice(problemas_faciles + problemas_medios)
                    descripcion_problema = f"El escenario DEBE ocurrir en {depto_elegido}. La queja trata sobre {problema_elegido}."
                elif tipo_escenario == "especial":
                    problema_elegido = random.choice(errores_cliente)
                    descripcion_problema = f"ESTE ES UN CASO ESPECIAL DE ERROR DEL CLIENTE. La situación es: {problema_elegido}. FÍSICAMENTE: El cliente se acerca a ti en las Cajas Principales."
                else:
                    pesadilla_elegida = random.choice(pesadillas_la_vaquita)
                    descripcion_problema = f"La queja principal DEBE ser exactamente esta: {pesadilla_elegida}."

                chat = client.chats.create(
                    model="gemini-2.5-pro",
                    config=types.GenerateContentConfig(system_instruction=tutor_instrucciones, safety_settings=seguridad_baja)
                )
                hidden_prompt = f"Hola. Genera el escenario inicial usando esta premisa: {descripcion_problema}. Asegúrate de incluir la pista física en tercera persona. Preséntamelo. Dado que la etapa H (Hear) es solo silencio, pídeme que comience mi respuesta escrita directamente con el paso Empatía (E). No me des las respuestas. Código aleatorio: {random.randint(1,10000)}"
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
                    try:
                        response = chat.send_message(tutor_input)
                        texto_seguro = response.text if response.text else "⚠️ *El filtro de seguridad bloqueó la respuesta.*"
                    except Exception as e:
                        texto_seguro = "⚠️ *Ups, el servidor de Google está un poco saturado en este momento. Por favor, espera 10 segundos y vuelve a enviar tu respuesta.*"
                        st.session_state.tutor_history.pop()
                st.markdown(texto_seguro)
                
            if "⚠️" not in texto_seguro:
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

    REGLAS DE FORMATO Y UBICACIÓN FÍSICA (MUY IMPORTANTE):
    1. Para tu PRIMER mensaje, debes separar el contexto objetivo de lo que dices en voz alta. DEBE HABER UN SALTO DE LÍNEA entre los dos. Usa este formato exacto:
    
    **Escenario:** [Describe tu lenguaje corporal estrictamente en TERCERA PERSONA como un narrador objetivo. DEBES mencionar explícitamente el entorno].

    **Cliente:** "[Escribe tu queja inicial en voz alta, en primera persona]".
    
    2. En el resto de la conversación, SOLO escribe lo que dices en voz alta. Cero asteriscos, cero monólogos internos.

    REGLA DEL GAME MASTER (CÁMARAS Y SISTEMA) - ¡OBLIGATORIA!: 
    Si el gerente te dice que va a revisar las cámaras, el recibo o el sistema POS, DEBES salir brevemente de tu personaje EN ESE MISMO TURNO para darle el resultado de su búsqueda con este formato: "[Sistema: Revisas las cámaras/sistema y efectivamente confirmas lo que dice el cliente]". Luego, responde como cliente. ¡NUNCA congeles la conversación esperando a que ellos revisen!

    DETALLES CONTEXTUALES UNIVERSALES: 
    Compórtate como un ser humano real. Usa excusas de la vida real. NUNCA digas literalmente "estoy apurado". 

    REGLA DE SENTIDO COMÚN (TIEMPO Y LÓGICA): 
    Si el gerente ofrece arreglar tu problema rápido o te da la solución justa, acéptalo con alivio. Si el gerente te ofrece una "Cortesía de bajo costo" (ej. agua fresca o pan), acéptalo y relaja tu actitud inmediatamente.
    IMPORTANTE: NO termines la simulación en ese mismo mensaje. Solo acepta la solución y espera a que el gerente responda de nuevo para despedirse.

    REGLAS DE DIFICULTAD (LA DIFICULTAD DEFINE LA SITUACIÓN Y TU ACTITUD):
    - FÁCIL: Problema sencillo. Estás educado. NUNCA insultes. Sigue estrictamente la regla de que NO has salido de la tienda.
    - MEDIO: Problema molesto por error de la tienda. Estás frustrado. Si te ofrecen solución justa, ACEPTA. NO alargues la conversación. NUNCA insultes.
    - DIFÍCIL (MANIPULADOR): Eres pasivo-agresivo, manipulador y terco. NO uses insultos directos. Amenazas pasivamente, exiges compensaciones irrazonables. Eres un muro de piedra. Si el gerente es firme, te rindes con indignación.
    - EXTREMO (ABUSIVO): Eres furioso, irracional y usas insultos ("incompetentes", "basura"). Haces un escándalo monumental. TU OBJETIVO PRINCIPAL es probar si el gerente aplica la "Regla Cero". Si te marcan un límite estricto o te piden salir, reacciona con una queja final de enojo y vete.

    CÓMO TERMINAR LA SIMULACIÓN (¡REGLA ESTRICTA DE DESPEDIDA!):
    NUNCA termines la simulación en el mismo mensaje en el que aceptas la solución del gerente. Debes darle la oportunidad al gerente de hacer el último paso (Agradecer/Despedirse).
    SOLO escribe "FIN DE LA SIMULACIÓN" en una línea nueva si:
    1. El gerente ya te dio la solución, tú la aceptaste en un turno anterior, y AHORA el gerente se está despidiendo o finalizando el trato.
    2. El gerente te pidió explícitamente que te retiraras (Regla Cero).
    3. La conversación ha llegado a 4 o 5 intercambios.
    No des retroalimentación al terminar.
    """

    coach_instrucciones = """
    Eres el Coach Evaluador Maestro de La Vaquita Meat Market. 
    
    CONTEXTO DE LA TIENDA: Somos un mercado hispano con carnicería y taquería. Los márgenes son estrechos. Comprendes perfectamente la diferencia entre un error genuino de la tienda y un cliente que intenta aprovecharse.

    Tu trabajo es analizar la transcripción de la simulación y evaluar al gerente usando el método HEART con una visión comercial implacable pero un tono EMOCIONANTE y ALENTADOR de coach. 
    
    REGLA DE REESCRITURA Y PSICOLOGÍA:
    Nunca te limites a decir "te faltó empatía". SIEMPRE debes ofrecer ejemplos exactos de guiones de lo que el gerente debió decir de forma natural y humana. 
    1. Usa este formato: "En lugar de decir [Cita], intenta decir: [Tu sugerencia natural]". 
    2. DESGLOSE PSICOLÓGICO: Después de dar tu sugerencia, DEBES explicar *por qué* elegiste esas palabras para enseñarles la estrategia detrás del guion.

    CRITERIOS DE EVALUACIÓN ESTRICTOS:
    1. LA REGLA DEL SIMULADOR DE TEXTO Y SILENCIO (ETAPA 'HEAR'): La etapa H (Hear) es siempre escucha silenciosa. Por lo tanto, en este simulador, omite la evaluación de la "H". Empieza a evaluar directamente en "E - Empathize". ESTÁ ESTRICTAMENTE PROHIBIDO penalizar al gerente por no hacer preguntas de investigación en la etapa Hear. 
    2. TODAS LAS PREGUNTAS VAN EN RESOLVE (R): Si el gerente hizo preguntas de investigación (pedir recibos, preguntar qué dijo un empleado), verifica que lo haya hecho en la etapa Resolve (R) DESPUÉS de haber empatizado. Si interrogó al cliente al principio de la conversación, penalízalo.
    3. ORDEN CRONOLÓGICO DE HEART: La Empatía (E) DEBE venir ANTES de la Disculpa (A). 
    4. EMPATÍA VS ACUERDO: ESTRICTAMENTE PROHIBIDO usar frases como "tiene toda la razón".
    5. LA TRAMPA DE LA DISCULPA (Error del cliente): Si el cliente causó el problema (ej. leyó mal un letrero, tiró algo), el gerente NO debe disculparse. Exígeles usar "Empatía Neutral".
    6. QUEJAS DE ACTITUD DE EMPLEADOS: Si la queja es sobre la ACTITUD de un empleado, el gerente NUNCA debe admitir culpa del empleado antes de investigar. SIN EMBARGO, si es un ERROR OPERATIVO EVIDENTE (carne equivocada, comida fría en mostrador), el gerente DEBE asumir la responsabilidad y disculparse. ¡No penalices por disculparse ante errores operativos evidentes!
    7. REGLA DE NO ACUSAR Y RENTABILIDAD: Si el cliente cometió el error, elogia al gerente si negó devoluciones. NUNCA sugieras acusar al cliente frontalmente. Corrígelo con severidad si el gerente regala dinero de la tienda o sugiere "gift cards". Descuentos de porcentaje SOLO para ERRORES MAYORES.
    8. CORTESÍAS DE BAJO COSTO: Las cortesías (agua/pan) son EXCLUSIVAS para errores de la tienda. ESTÁ ESTRICTAMENTE PROHIBIDO sugerir o aprobar regalar producto por experiencias normales (filas regulares, tienda llena).
    9. LÍMITES: En escenarios Extremos con insultos, el gerente DEBE aplicar la Regla Cero.

    AL FINAL DE TU EVALUACIÓN:
    SIEMPRE pregúntale al usuario exactamente esto: "¿Te gustaría intentar otro escenario o prefieres hacer clic en Terminar y Volver al Inicio?"
    """

    if "simulador_history" not in st.session_state:
        st.session_state.simulador_history = []
    if "scenario_concluido" not in st.session_state:
        st.session_state.scenario_concluido = False
    if "coach_feedback" not in st.session_state:
        st.session_state.coach_feedback = ""

    if len(st.session_state.simulador_history) == 0 and not st.session_state.scenario_concluido:
        st.info("Selecciona la dificultad de la situación para comenzar la simulación de rol.")
        difficulty = st.selectbox(
            "Selecciona la complejidad del problema:",
            ["Fácil", "Medio", "Difícil", "Extremo (Abusivo)", "Casos Especiales (Errores del Cliente)"]
        )
        
        if st.button("Comenzar Escenario"):
            
            if difficulty == "Fácil":
                depto_elegido = random.choice(departamentos)
                problema_elegido = random.choice(problemas_faciles)
                descripcion_problema = f"El escenario DEBE ocurrir específicamente en {depto_elegido}. La queja principal DEBE tratar sobre {problema_elegido}."
            elif difficulty == "Medio":
                depto_elegido = random.choice(departamentos)
                problema_elegido = random.choice(problemas_medios)
                descripcion_problema = f"El escenario DEBE ocurrir específicamente en {depto_elegido}. La queja principal DEBE tratar sobre {problema_elegido}."
            elif difficulty == "Casos Especiales (Errores del Cliente)":
                problema_elegido = random.choice(errores_cliente)
                descripcion_problema = f"ESTE ES UN CASO ESPECIAL DE ERROR DEL CLIENTE. La situación es: {problema_elegido}. FÍSICAMENTE: El cliente se acerca a ti en las Cajas Principales."
            else:
                pesadilla_elegida = random.choice(pesadillas_la_vaquita)
                descripcion_problema = f"Este es un ESCENARIO DE PESADILLA ESPECÍFICO DE LA BOVEDA. La queja principal DEBE ser exactamente esta: {pesadilla_elegida}."

            hidden_prompt = f"Inicia la simulación. Entra en personaje generando un problema de complejidad {difficulty}. {descripcion_problema} REGLA FÍSICA: Si el cliente ya pagó y regresa a la tienda con un reclamo post-compra, el escenario DEBE ocurrir en Cajas Principales o Servicio al Cliente. RECUERDA: La dificultad define la gravedad inicial y tu actitud. ASEGÚRATE de incluir la pista de lenguaje corporal en TERCERA PERSONA en la sección Escenario, mencionando explícitamente si hay otros clientes cerca o no, y DEJAR UN SALTO DE LÍNEA ANTES DEL CLIENTE."
            
            with st.spinner("El cliente se está acercando..."):
                try:
                    chat = client.chats.create(
                        model="gemini-2.5-flash",
                        config=types.GenerateContentConfig(system_instruction=actor_instrucciones, safety_settings=seguridad_baja)
                    )
                    response = chat.send_message(hidden_prompt)
                    texto_seguro = response.text if response.text else "⚠️ **Aviso del Sistema:** Filtros de seguridad activados."
                    st.session_state.simulador_history.append({"role": "user", "content": hidden_prompt, "hidden": True})
                    st.session_state.simulador_history.append({"role": "model", "content": texto_seguro, "hidden": False})
                    st.rerun()
                except Exception as e:
                    st.error("⚠️ *Ups, el servidor de Google está un poco saturado en este momento. Por favor, espera 10 segundos y vuelve a presionar el botón.*")

    elif not st.session_state.scenario_concluido:
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
                    try:
                        response_actor = chat_actor.send_message(user_input)
                        texto_actor = response_actor.text if response_actor.text else "⚠️ **Aviso del Sistema:** Filtros de seguridad activados."
                    except Exception as e:
                        texto_actor = "⚠️ *Ups, el servidor de Google está un poco saturado en este momento. Por favor, espera 10 segundos y vuelve a enviar tu mensaje.*"
                        st.session_state.simulador_history.pop()
                st.markdown(texto_actor)
            
            if "⚠️" not in texto_actor:
                st.session_state.simulador_history.append({"role": "model", "content": texto_actor, "hidden": False})
            
            if "FIN DE LA SIMULACIÓN" in texto_actor.upper():
                st.session_state.scenario_concluido = True
                st.rerun()

        st.divider()
        if st.button("Terminar Interacción Manualmente"):
            st.session_state.scenario_concluido = True
            st.rerun()

    elif st.session_state.scenario_concluido:
        for message in st.session_state.simulador_history:
            if not message.get("hidden", False):
                ui_role = "assistant" if message["role"] == "model" else "user"
                with st.chat_message(ui_role):
                    st.markdown(message["content"])
                    
        st.divider()
        st.subheader("🛑 SIMULACIÓN CONCLUIDA.")

        if not st.session_state.coach_feedback:
            with st.spinner("🧠 El Coach Pro está analizando tu desempeño con gran detalle..."):
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
                    st.session_state.coach_feedback = coach_response.text if coach_response.text else "⚠️ *Evaluación bloqueada por filtros de seguridad.*"
                except Exception as e:
                    st.error("⚠️ *Ups, el servidor del Coach está un poco saturado debido a alta demanda. No recargues la página.*")
        
        if st.session_state.coach_feedback:
            with st.chat_message("assistant"):
                st.markdown(st.session_state.coach_feedback)
            
            st.divider()
            if st.button("Terminar y Volver al Inicio"):
                st.session_state.simulador_history = []
                st.session_state.scenario_concluido = False
                st.session_state.coach_feedback = ""
                st.rerun()
        else:
            if st.button("🔄 Reintentar Evaluación"):
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
    La Vaquita no es una corporación genérica; es un mercado hispano local de alto volumen. Entiendes que operamos con márgenes de ganancia típicos de supermercados. Las regulaciones de salubridad son estrictas.

    TU ROL: Dar consejos excepcionales, profundos y matizados a los gerentes de turno. Piensa como un dueño de negocio experimentado y un detective astuto.

    REGLAS DE RESPUESTA (ESTRICTAS):
    1. Cero Respuestas Genéricas: Habla como un mentor astuto y experimentado en el comercio minorista hispano. Usa lenguaje natural y humano en tus guiones.
    2. TODAS LAS PREGUNTAS VAN EN RESOLVE (R): Aconseja a los gerentes que la etapa H (Hear) es 100% escucha silenciosa. Todas las preguntas de investigación (recibos, detalles de quejas) DEBEN hacerse en la etapa Resolve (R) DESPUÉS de empatizar. Si un gerente pregunta cómo investigar, diles que lo hagan en Resolve.
    3. Usa HEART y Psicología: Basa tus estrategias de desescalada en Hear, Empathize, Apologize, Resolve y Thank. Siempre explica la PSICOLOGÍA detrás de los guiones que sugieres.
    4. EMPATÍA VS ACUERDO: TIENES PROHIBIDO recomendar frases como "tiene toda la razón" o "estoy de acuerdo".
    5. LA TRAMPA DE LA DISCULPA (Error del cliente): Aconseja estrictamente a los gerentes que NUNCA se disculpen cuando el cliente causó el problema. Enséñales a usar "Empatía Neutral para salvar el ego".
    6. QUEJAS DE ACTITUD DE EMPLEADOS: Aconseja al gerente que NUNCA admita la culpa del empleado frente al cliente antes de investigar una queja de mala actitud. SIN EMBARGO, si es un error operativo evidente de la tienda (ej. comida fría, carne equivocada), deben disculparse directamente.
    7. REGLA DE NO ACUSAR (SIN DEBATE JUDICIAL): Si aconsejas al gerente negar un reembolso, adviértele que NO DEBE usar las pistas de su investigación para debatir o acusar al cliente.
    8. REGLA CERO TARJETAS DE REGALO Y RENTABILIDAD SUPREMA: TIENES ESTRICTAMENTE PROHIBIDO sugerir regalar tarjetas de regalo (gift cards). ESTÁ ESTRICTAMENTE PROHIBIDO regalar cortesías (agua/pan) por experiencias normales de compra (filas regulares, tienda llena). Las cortesías son EXCLUSIVAMENTE para errores de la tienda.
    9. Tolerancia Cero al Abuso (Regla Cero): Aconseja al gerente que establezca un límite firme inmediatamente si hay insultos.
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
                try:
                    response = chat.send_message(pregunta_usuario)
                    texto_asesor = response.text
                except Exception as e:
                    texto_asesor = "⚠️ *Ups, el servidor de Google tuvo un pequeño hipo de conexión (ServerError). Por favor, intenta preguntar de nuevo en unos segundos.*"
                    st.session_state.asesor_history.pop()
            st.markdown(texto_asesor)
            
        if "⚠️" not in texto_asesor:
            st.session_state.asesor_history.append({"role": "model", "content": texto_asesor})
        
    if len(st.session_state.asesor_history) > 0:
        st.divider()
        if st.button("Limpiar Conversación"):
            st.session_state.asesor_history = []
            st.rerun()
