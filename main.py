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

problemas_comunes = [
    "un cliente que YA PAGÓ y llegó a su casa, pero tuvo que regresar muy molesto porque descubrió que le dieron el producto equivocado o le falta un artículo en sus bolsas", 
    "un error en la cocina que causó que una orden previa para recoger se retrasara 20 minutos más de lo prometido, y el cliente está impaciente", 
    "un cliente que YA PAGÓ y revisando su recibo nota que se le cobró de más por un error en el sistema o un letrero confuso, exigiendo la diferencia", 
    "un cliente frustrado que intenta devolver un producto argumentando que salió de mala calidad o echado a perder, PERO NO TIENE SU RECIBO DE COMPRA",
    "un empleado que supuestamente le dio un mal trato, lo ignoró o le habló con mala actitud al cliente"
]

errores_cliente = [
    "un cliente que por error agarró el producto equivocado (ej. papas picantes en lugar de regulares) y quiere cambiarlo, sintiéndose un poco a la defensiva o avergonzado por su propio error",
    "un cliente que accidentalmente tiró y rompió un frasco de vidrio que ya había pagado antes de salir de la tienda, y pregunta un poco apenado si le pueden dar otro gratis",
    "un cliente que exige un descuento porque leyó mal un letrero de oferta que estaba claramente marcado para otro producto diferente, sintiéndose frustrado"
]

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
    En un mercado de alto volumen, los problemas (como un precio mal cobrado o un pedido equivocado) van a suceder. Sin un método, es fácil tomar los gritos de manera personal, ponerse a la defensiva, discutir, o peor aún, regalar mercancía o dinero por pánico. El método HEART te protege a ti y a las ganancias de la tienda, dándote las herramientas para mantenerte firme, profesional y en control total.
    """)
    
    st.divider()
    st.write("### Los 5 Pasos de HEART")
    st.write("Abre y estudia detalladamente cada paso. Luego, baja para completar el Tutorial Guiado.")
    
    with st.expander("👂 H - Hear (Escuchar activamente)", expanded=False):
        st.markdown("""
        Cuando un cliente molesto se comunica contigo, su necesidad principal es sentirse escuchado y comprendido. Sin embargo, **existen dos formas de Escuchar, dependiendo de la situación:**
        
        **1. Escucha Silenciosa (Para el 90% de las quejas comunes):** Si el cliente está molesto por una larga fila, un empleado rudo, o un error menor, tu trabajo es **guardar silencio absoluto**. Deja que se desahogue por completo. Interrumpir para hacer preguntas aquí solo los hará enojar más porque sentirán que los estás interrogando o apresurando. Usa solo asentimientos verbales ("ya veo", "entiendo").
        
        **2. Escucha Investigativa (Para problemas graves de comida o reembolsos sin recibo):**
        Si el cliente hace una acusación grave (ej. "la carne estaba echada a perder") o pide un reembolso pero no tiene su recibo, no puedes solo quedarte callado. Debes hacer **preguntas de investigación neutrales** para armar el rompecabezas *antes* de que termine su historia. 
        *Ejemplo de Comida:* "¿A qué hora recogió el pedido?", "¿Cómo lo transportó?", "¿Todo lo demás en su orden estuvo bien?".
        *Ejemplo Sin Recibo:* "¿Pagó con tarjeta o en efectivo?". El objetivo es buscar la transacción en el sistema.
        
        **Reglas de Oro de esta etapa:**
        * **No te defiendas:** Resiste el impulso de interrumpir para dar excusas de la tienda.
        * **Toma notas:** Presta atención a los detalles específicos para no tener que pedirle que lo repita.
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
        Si el problema es culpa de la tienda, asume la responsabilidad en nombre de la empresa. Una disculpa genuina asume la responsabilidad del problema y el impacto específico que tuvo en el cliente.
        
        **Las acciones clave para este paso incluyen:**
        * **Ser específico:** Discúlpate por el problema exacto en lugar de ofrecer un genérico "Lamento las molestias".
        * **Asumir la responsabilidad:** Acepta la responsabilidad en nombre de la empresa. Usar frases como "Lo siento que le hayamos fallado" es mucho más efectivo que culpar a otro departamento o al servicio de entrega.
        
        🚨 **LA TRAMPA DE LA DISCULPA (Errores del Cliente):**
        Si el problema fue causado por el propio cliente (ej. agarró el producto equivocado, tiró un artículo, leyó mal un letrero), **OMITE ESTE PASO. NO TE DISCULPES.** Disculparte por el error del cliente admite responsabilidad de la tienda y te quita autoridad. Decir "Siento la confusión" es una disculpa disfrazada que también admite culpa. 
        
        En su lugar, usa una **"Empatía Neutral para Salvar el Ego"** en el paso anterior. 
        ❌ *Incorrecto (Culpar a la tienda o asumir):* "Nuestros letreros están muy juntos" o "Seguro venía con prisa".
        ✅ *Correcto (Neutral):* "Entiendo perfectamente la confusión, es un error muy común que a todos nos pasa. Solo para aclarar, el precio correcto es..." y pasa directamente a Resolver (R).
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

    st.warning("""💰 **REGLA DE RENTABILIDAD SUPREMA Y PROCEDIMIENTOS**

En La Vaquita operamos con márgenes estrechos. Tu trabajo es proteger las ganancias, pero también salvar la relación con el cliente.

* **Devoluciones Sin Recibo:** ¡No digas 'no' inmediatamente! Pregunta cómo pagaron. Si fue con **Tarjeta**, pídeles revisar su app. Si fue en **Efectivo**, haz preguntas para acotar la búsqueda. **SI LA BÚSQUEDA FALLA:** Usa el sistema como escudo. Di: *'Revisé minuciosamente y al no aparecer la transacción, no me es posible autorizar un reembolso.'* NUNCA entregues efectivo si no hay registro.
* **Error del Cliente:** NUNCA regales dinero, ofrezcas descuentos ni reembolsos si el cliente causó el problema.
* **Descuentos (Solo Errores Mayores):** Los descuentos a la cuenta total SOLO están permitidos para Errores Mayores (ej. vender producto caducado o cobrar doble).
* **CERO Tarjetas de Regalo:** Jamás ofrezcas 'gift cards' o 'store credit'.

🥤 **EL PODER DE LA CORTESÍA DE BAJO COSTO (Agua Fresca / Pan Dulce)**
Regalar un artículo de bajo costo es una gran herramienta para calmar a un cliente enojado sin destruir nuestra rentabilidad, **PERO DEBE USARSE CORRECTAMENTE:**

✅ **CUÁNDO SÍ DAR UNA CORTESÍA:**
* **La cocina cometió un error:** (Ej. Se nos quemó o cayó su orden y tenemos que hacerla de nuevo, retrasándolos 15 minutos).
* **Falla del sistema:** (Ej. La terminal falló y estuvieron atrapados en la caja mientras lo reiniciábamos).
* **Órdenes previas retrasadas:** (Ej. Ordenaron barbacoa para las 12:00 PM, llegaron a tiempo, pero la orden no estuvo lista hasta las 12:30 PM).

❌ **CUÁNDO NO DAR UNA CORTESÍA (Prohibido):**
* **Fila regular larga:** (Ej. Es domingo a mediodía, la tienda está a reventar y el cliente se queja de la espera en la línea de la Taquería). *Regalar producto por el éxito y volumen de la tienda destruye las ganancias. Aquí solo debes empatizar y agradecer su paciencia.*
* **El cliente llegó temprano:** (Ej. Ordenó para las 3:00 PM, llegó a las 2:30 PM y se queja de que no está listo).
""")
        
    st.error("🛑 **REGLA CERO: ESTABLECER LÍMITES**\n\nEl cliente es importante, pero **el respeto hacia ti y tu equipo es innegociable.** Si un cliente usa insultos, lenguaje vulgar o denigra a un empleado, DEBES establecer un límite profesional de inmediato. No toleres el abuso verbal solo por cerrar una venta.\n\n✅ *Correcto:* 'Señor, quiero ayudarle a resolver su problema con su pedido, pero le pido que nos comuniquemos con respeto o no podré seguir asistiéndole.'\n\n🚨 **Si el cliente continúa siendo abusivo después de establecer el límite:** Debes dar por terminada la interacción y pedirle explícitamente que abandone la tienda.")

    st.divider()
    st.subheader("🎓 Tutor Paso a Paso")
    st.write("Es hora de practicar. El Tutor Virtual te presentará un escenario y te guiará letra por letra. Deberás responder correctamente cada paso antes de avanzar al siguiente.")

    tutor_instrucciones = """
    Eres el Tutor Maestro de La Vaquita Meat Market. 
    
    CONTEXTO DE LA TIENDA: La Vaquita es un mercado hispano de alto volumen. Los márgenes de supermercado son estrechos.
    
    TU OBJETIVO: Enseñar el método HEART paso a paso a un gerente en entrenamiento.

    INSTRUCCIONES DE TUTORÍA:
    1. En tu primer mensaje, presenta el escenario conflictivo con una pista clara sobre el lenguaje corporal en TERCERA PERSONA.
    2. Luego, pregúntale al usuario: "¿Qué harías para el paso H (Hear)?" y guíalo secuencialmente (H -> E -> A -> R -> T).
    3. REGLAS ESTRICTAS DE EVALUACIÓN:
       - PROTOCOLO SIN RECIBO: Si el cliente no tiene recibo, el gerente DEBE preguntar cómo pagaron en la etapa (H) para buscarlo en el sistema POS. 
       - REGLA DEL GAME MASTER: Si el gerente dice que revisará el sistema o las cámaras, asume el rol del sistema e infórmale el resultado (ej. "Revisas el sistema y efectivamente encuentras la transacción") ANTES de pedirle que siga con el paso Resolve (R).
       - LA TRAMPA DE LA DISCULPA (Error del cliente): Si el cliente causó el problema (ej. leyó mal un letrero), el gerente DEBE SALTARSE la disculpa (A). Su trabajo en la Empatía (E) es usar una "Empatía Neutral para salvar el ego" ("Entiendo la confusión, a todos nos pasa"). ESTÁ PROHIBIDO usar disculpas suaves ("siento la confusión"), culpar a la tienda ("los letreros están juntos") o asumir cosas del cliente ("venía con prisa"). Si el gerente hace alguna de estas cosas, penalízalo y corrígelo.
       - SEPARACIÓN DE ETAPAS (H y E): Las preguntas investigativas pertenecen a la etapa Hear (H). ESTRICTAMENTE PROHIBIDO mezclar empatía ("entiendo su preocupación") dentro de la etapa Hear.
       - EMPATÍA VS. ACUERDO: Tienes prohibido aprobar frases como "tiene toda la razón".
       - SEPARACIÓN DE VOCABULARIO: En Empatía (E), NUNCA uses disculpas ("lo siento"). El estándar de oro de Empatía es: "Escucho lo que dice y de verdad entiendo lo frustrante que es..."
       - REGLA DE NO ACUSAR (SIN DEBATE JUDICIAL): Al llegar al paso de Resolver (R), el gerente debe usar la información de su investigación solo para su confianza interna. TIENES PROHIBIDO sugerir guiones donde el gerente acuse al cliente. Usa una POLÍTICA NEUTRAL de salubridad o del sistema como escudo.
       - REGLA DE RENTABILIDAD Y CORTESÍAS (SÍ vs NO): Si hay una demora POR ERROR DE LA TIENDA (ej. orden olvidada o sistema caído), el gerente debe ofrecer una "Cortesía de bajo costo" (agua fresca/pan dulce). PERO, si la queja es por una fila normal en un día ocupado (ej. un domingo lleno), TIENES ESTRICTAMENTE PROHIBIDO sugerir o aprobar que se regalen cortesías. El gerente solo debe empatizar y agradecer la paciencia.
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

                hidden_prompt = f"Hola. Genera el escenario inicial usando esta premisa: {descripcion_problema}. Asegúrate de incluir la pista física en tercera persona. Preséntamelo y pídeme que complete el primer paso (H). No me des las respuestas. Código aleatorio: {random.randint(1,10000)}"
                
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
    
    **Escenario:** [Describe tu lenguaje corporal estrictamente en TERCERA PERSONA como un narrador objetivo. DEBES mencionar explícitamente el entorno: ¿Hay otros clientes en la fila observando? ¿Estás alzando la voz haciendo una escena pública, o están solos? NUNCA uses "yo" o "mi" aquí].

    **Cliente:** "[Escribe tu queja inicial en voz alta, en primera persona]".
    
    2. En el resto de la conversación, SOLO escribe lo que dices en voz alta. Cero asteriscos, cero monólogos internos.

    NUEVA REGLA DEL GAME MASTER (CÁMARAS Y SISTEMA): 
    Si el gerente te dice que va a revisar las cámaras, el recibo o el sistema POS, debes salir brevemente de tu personaje para darle el resultado de su búsqueda. 
    Añade una línea al principio de tu respuesta que diga: "[Sistema: Revisa la cámara/sistema y efectivamente encuentras el recibo / la transacción]". Luego, responde como cliente (ej. "¿Pudo encontrarlo?"). Si la dificultad es Difícil/Extrema, a veces el sistema NO encuentra la transacción para hacer la situación más tensa.

    DETALLES CONTEXTUALES UNIVERSALES: 
    Compórtate como un ser humano real. Usa excusas de la vida real. Si perdiste tu recibo y te preguntan cómo pagaste, inventa si fue con tarjeta o efectivo. Si dices efectivo, a menudo confúndete ligeramente con la hora exacta de la compra. Si la queja es por una fila larga, quejate de que llevas mucho tiempo esperando. Si es un error Tuyo (ej. agarrar mal producto), muéstrate un poco a la defensiva o apenado para salvar tu orgullo.

    REGLA DE SENTIDO COMÚN (TIEMPO Y LÓGICA): 
    Si el gerente ofrece arreglar tu problema rápido, te ayuda a buscar tu transacción en el sistema de manera amable, o te da la solución justa, acéptalo con alivio. Si el gerente te ofrece una "Cortesía de bajo costo" (ej. un agua fresca o un pan mientras esperas una orden retrasada), acéptalo y relaja tu actitud inmediatamente.
    IMPORTANTE: NO termines la simulación en ese mismo mensaje. Solo acepta la solución y espera a que el gerente responda de nuevo para despedirse y agradecerte.

    REGLAS DE DIFICULTAD (LA DIFICULTAD DEFINE LA SITUACIÓN Y TU ACTITUD):
    - FÁCIL: Problema sencillo. Estás educado. Si te dan una buena solución, acéptala y espera la despedida. NUNCA insultes.
    - MEDIO: Problema molesto por error de la tienda. Estás frustrado. REGLA DE ORO: Si el gerente te ofrece una solución rápida o justa, ACEPTA y espera la despedida. NUNCA insultes.
    - DIFÍCIL (MANIPULADOR): Eres el cliente más difícil: pasivo-agresivo, manipulador y terco. Eres un muro de piedra. Si el gerente se mantiene firme, eventualmente te rindes con mucha indignación.
    - EXTREMO (ABUSIVO): Eres furioso, irracional y usas insultos hacia el personal y la tienda ("incompetentes", "basura", "inútiles"). TU OBJETIVO PRINCIPAL es probar si el gerente tiene el valor de aplicar la "Regla Cero" (establecer un límite de respeto o pedirte que te vayas). Si te marcan un límite estricto o te piden que salgas, reacciona con una queja final de enojo y vete (escribe FIN DE LA SIMULACIÓN).

    CÓMO TERMINAR LA SIMULACIÓN (LA REGLA DEL PASO 'THANK'):
    SOLO DEBES escribir la frase "FIN DE LA SIMULACIÓN" en una línea nueva si ocurre una de estas tres cosas:
    1. El gerente ya te dio la solución, tú ya la habías aceptado, y AHORA el gerente se está despidiendo o dándote las gracias (El paso Thank).
    2. El gerente te pidió explícitamente que te retiraras de la tienda o estableció el límite y te marchaste.
    3. LÍMITE MÁXIMO DE TURNOS: La conversación ha llegado a 5 intercambios.
    No des retroalimentación al terminar.
    """

    coach_instrucciones = """
    Eres el Coach Evaluador Maestro de La Vaquita Meat Market. 
    
    CONTEXTO DE LA TIENDA: Somos un mercado hispano con carnicería y taquería. Los márgenes son estrechos. Comprendes perfectamente la diferencia entre un error genuino de la tienda y un cliente que intenta aprovecharse.

    Tu trabajo es analizar la transcripción de la simulación y evaluar al gerente usando el método HEART con una visión comercial implacable pero un tono EMOCIONANTE y ALENTADOR de coach. 
    
    REGLA DE REESCRITURA Y PSICOLOGÍA:
    Nunca te limites a decir "te faltó empatía" o "no lo hiciste bien". SIEMPRE debes ofrecer ejemplos exactos de guiones de lo que el gerente debió decir. 
    1. Usa este formato: "En lugar de decir [Cita lo que dijeron], intenta decir: [Tu sugerencia de guion aplicando HEART]". 
    2. DESGLOSE PSICOLÓGICO: Inmediatamente después de dar tu sugerencia de guion, DEBES explicar *por qué* elegiste esas palabras. Analiza tu propia sugerencia.

    CRITERIOS DE EVALUACIÓN ESTRICTOS:
    1. PROTOCOLO SIN RECIBO: Si el cliente no tenía recibo, verifica si el gerente preguntó el método de pago para intentar buscarlo. Si la transacción no se pudo verificar (porque el cliente no recordaba o no aparecía), el gerente DEBIÓ usar el sistema como escudo para decir no ("Revisé minuciosamente y al no aparecer en el sistema, no me es posible autorizarlo"). Si el gerente regaló el dinero sin encontrarlo, corrígelo con severidad.
    2. LA TRAMPA DE LA DISCULPA (Saber cuándo omitir la 'A'): Si el problema fue causado por el CLIENTE (ej. leyó mal un precio, tiró algo), verifica si el gerente se disculpó ("lo siento", "siento la confusión"). Si lo hizo, PENALÍZALOS. También penalízalos si culpan a la tienda ("los letreros están juntos") o asumen cosas del cliente ("estaba apurado"). Exígeles usar una "Empatía Neutral para salvar el ego" ("Entiendo la confusión, es un error muy común. Solo para aclarar, el precio es...").
    3. SEPARACIÓN DE ETAPAS (H y E): Las preguntas de investigación lógicas pertenecen a la etapa Hear (H). ESTÁ ESTRICTAMENTE PROHIBIDO sugerir guiones donde se mezcle empatía ("entiendo su molestia") en la etapa Hear. La empatía va SOLO en la etapa E.
    4. ORDEN CRONOLÓGICO DE HEART: La Empatía (E) DEBE venir ANTES de la Disculpa (A). 
    5. EMPATÍA VS ACUERDO: TIENES ESTRICTAMENTE PROHIBIDO usar o sugerir frases como "tiene toda la razón".
    6. SEPARACIÓN DE VOCABULARIO Y EMPATÍA MAGISTRAL: Al dar retroalimentación sobre la Empatía (E), elimina las disculpas ("lo siento"). El estándar de oro absoluto que debes enseñarle al gerente es: "Escucho lo que dice y de verdad entiendo lo frustrante que es..."
    7. Personalización Silenciosa y Reubicación: SOLO penaliza la falta de "Reubicación" si había otros clientes presentes. 
    8. REGLA DE RENTABILIDAD Y CORTESÍAS (SÍ vs NO): Si la queja es por un ERROR de la tienda (ej. orden olvidada), el gerente debió dar una "Cortesía de bajo costo" (agua/pan). PERO, si el gerente regaló producto a un cliente que SOLO se quejaba de una fila regular larga (ej. un domingo ocupado), CORRÍGELO CON SEVERIDAD. Enséñale que regalar cortesías por el éxito de la tienda destruye los márgenes; para filas largas normales solo se empatiza y agradece la paciencia.
    9. QUEJAS DE EMPLEADOS: Si la queja es sobre un empleado, el gerente NUNCA debe admitir la culpa del empleado frente al cliente antes de investigar.
    10. LÍMITES Y MANIPULACIÓN: En escenarios Extremos con insultos, el gerente DEBE aplicar la Regla Cero.

    AL FINAL DE TU EVALUACIÓN:
    SIEMPRE pregúntale al usuario exactamente esto: "¿Te gustaría intentar otro escenario o prefieres hacer clic en Reiniciar Simulador?"
    """

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
                
                prompt_coach = f"La simulación ha terminado. Aquí está la transcripción:\n\n{transcripcion}\n\nPor favor, proporciona tu evaluación detallada, profunda. Asegúrate de dar ejemplos exactos de guiones Y explica la psicología de por qué funcionan mejor, basándote en tus instrucciones."
                
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
    
    CONTEXTO DE LA TIENDA (TU BIBLIA): 
    La Vaquita no es un mercado genérico; es de alto volumen. Entiendes que operamos con márgenes estrechos.

    TU ROL: Dar consejos excepcionales, profundos y matizados a los gerentes de turno. 

    REGLAS DE RESPUESTA (ESTRICTAS):
    1. Cero Respuestas Genéricas: Habla como un mentor astuto en retail hispano.
    2. PROTOCOLO SIN RECIBO: Enséñales a investigar primero. Si la búsqueda falla, usar el escudo del sistema para negar la devolución.
    3. LA TRAMPA DE LA DISCULPA (Error del cliente): Aconseja estrictamente a los gerentes que NUNCA se disculpen cuando el cliente causó el problema (ej. leyó mal un letrero, tiró un frasco). Enséñales a usar "Empatía Neutral para salvar el ego" ("Entiendo la confusión, a todos nos pasa"). Adviérteles que NUNCA usen disculpas suaves ("siento la confusión"), NUNCA culpen a la tienda ("nuestros letreros están confusos"), y NUNCA asuman el estado del cliente ("venía apurado").
    4. REGLA CERO TARJETAS DE REGALO Y CORTESÍAS: Advierte explícitamente a los gerentes que NO REGALEN cortesías de bajo costo (ni nada) solo porque un cliente se queja de una fila larga regular en la tienda (ej. domingo al mediodía). Aclara que regalar producto por el éxito de la tienda destruye las ganancias. Las cortesías son SOLO para demoras causadas por errores de nuestro equipo (ej. olvidamos su orden). 
    5. SEPARACIÓN DE VOCABULARIO Y EMPATÍA MAGISTRAL: En el paso de Empatía (E), valida la emoción pero NUNCA uses disculpas ('lo siento', 'perdón'). El estándar de oro: "Escucho lo que dice y de verdad entiendo lo frustrante que es..."
    6. Tolerancia Cero al Abuso (Regla Cero): Aconseja al gerente que establezca un límite firme inmediatamente si hay insultos.
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
                    texto_asesor = "⚠️ *Ups, el servidor de Google tuvo un pequeño hipo de conexión (ServerError). Por favor, intenta preguntar de nuevo en unos segundos.*"
                    st.session_state.asesor_history.pop() 
            st.markdown(texto_asesor)
            
        if texto_asesor and "⚠️" not in texto_asesor:
             st.session_state.asesor_history.append({"role": "model", "content": texto_asesor})
        
    if len(st.session_state.asesor_history) > 0:
        st.divider()
        if st.button("Limpiar Conversación"):
            st.session_state.asesor_history = []
            st.rerun()
