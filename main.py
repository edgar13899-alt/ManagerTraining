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
    "un cliente que YA PAGÓ y llegó a su casa, pero tuvo que regresar muy molesto porque descubrió que le dieron el producto equivocado o le falta un artículo en sus bolsas",
    "un cliente que se queja de que el precio que le cobraron en la caja por un artículo de abarrotes no coincide con la etiqueta de oferta que vio en el pasillo",
    "un cliente en la taquería que se queja de que en su platillo combinado le pusieron arroz en lugar de frijoles como había pedido, y ya está sentado en la mesa a punto de comer",
    "un cliente molesto porque compró carne marinada, la cocinó en casa y afirma que estaba demasiado salada, exigiendo un cambio aunque ya consumió la mitad",
    "un cliente frustrado porque solo lleva 3 artículos pero todas las cajas rápidas están cerradas y tiene que hacer la fila normal",
    "un cliente que compró un galón de leche, se dio cuenta en el estacionamiento de que caduca mañana, y quiere cambiarlo rápido pero dejó su recibo con la cajera",
    "un cliente que apartó un pastel en la panadería y está molesto porque los colores del decorado no son exactamente del tono que imaginaba, aunque el sabor y el nombre están correctos",
    "un cliente que intenta usar un cupón o descuento digital de la tienda que expiró ayer, y se frustra porque el sistema en caja no se lo acepta",
    "un cliente que se queja de que no hay carritos de mandado disponibles en la entrada y tuvo que cargar una sandía pesada por toda la tienda"
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
    
    st.info("📖 **Paso 1: Aprender HEART**\n\nEstudia la metodología oficial y los matices psicológicos de cada paso.")
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
    En un mercado de alto volumen, los problemas van a suceder. El método HEART te protege a ti y a las ganancias de la tienda, dándote las herramientas para mantenerte firme, profesional y en control total.
    """)
    
    st.divider()
    st.write("### Los 5 Pasos y sus Matices Psicológicos")
    st.write("Abre y estudia detalladamente cada paso. Luego, baja para completar el Tutorial Guiado.")
    
    with st.expander("👂 H - Hear (Escuchar activamente)", expanded=False):
        st.markdown("""
        Cuando un cliente molesto se acerca a ti, su necesidad principal es desahogarse. Tu único trabajo es **guardar silencio absoluto**. Deja que el cliente hable sin interrupciones.
        
        🚨 **REGLA DE ORO:** NUNCA interrumpas al cliente para hacerle preguntas de investigación (ej. "¿Tiene su recibo?"). Hacer preguntas inmediatas se siente como un interrogatorio y pone al cliente a la defensiva.
        
        **1. El Pico de Desahogo (The Venting Peak)**
        * **Qué es:** El momento físico en que la adrenalina del cliente baja después de explicar su problema. A menudo repetirán su queja varias veces porque su cerebro necesita liberar presión.
        * **Cómo manejarlo:** No intentes hablar en cuanto tomen aire. Espera a que sus hombros bajen, suelten un suspiro largo o te hagan una pregunta directa (*"¿Qué van a hacer al respecto?"*).
        * **🧠 Por qué funciona:** Si interrumpes antes del 'pico', el cliente sentirá que no lo escuchaste y volverá a subir su nivel de agresión, reiniciando el ciclo.
        
        **2. La Postura de Aliado (The Collaborative Stance)**
        * **Qué es:** Tu posición física frente al cliente.
        * **Cómo hacerlo:** Nunca te pares 'pecho a pecho' frente a ellos. Párate en un ángulo de 45 grados (Postura en L), mirando juntos hacia el producto o el recibo.
        * **🧠 Por qué funciona:** Pararse de frente se lee inconscientemente como 'combate'. Pararse de lado se lee como 'colaboración'. Le dice al cerebro del cliente: *"Estamos juntos mirando el problema,"* en lugar de *"Estamos peleando."*
        """)

    with st.expander("🤝 E - Empathize (Empatizar)", expanded=False):
        st.markdown("""
        Una vez que el cliente ha contado su historia, la empatía construye un puente. Le demuestra al cliente que comprendes sus sentimientos y validas su frustración.
        
        🧠 **ESTRATEGIA AVANZADA 1: Validar la Experiencia, NO el Hecho**
        * **El Problema:** Si dices *"Entiendo que su orden está mal"*, estás admitiendo culpa legal/operativa de la tienda *antes* de revisar el recibo.
        * **La Solución:** Valida la *situación* o el *tiempo perdido*, no el error en sí.
        * **Ejemplos Correctos (Neutrales):**
          * ✅ *"Entiendo perfectamente la molestia de tener que dar una vuelta extra."* (Validas el viaje, que es un hecho innegable).
          * ✅ *"Comprendo lo frustrante que es llegar a casa y no tener lo que esperaba para la cena."* (Validas su expectativa).
          * ✅ *"Lo que me describe suena muy frustrante..."* (Te mantienes como aliado sin convertirte en acusado).
        
        🧠 **ESTRATEGIA AVANZADA 2: Empatía Neutral para Salvar el Ego**
        * **Cuándo usarla:** Cuando el **cliente cometió el error** (ej. leyó mal un letrero, agarró el producto equivocado).
        * **Cómo funciona:** En lugar de decirle "Usted se equivocó", "salvas su ego" normalizando el error para que no se sientan atacados.
        * **LA TRAMPA DE MERCHANDISING (Lo que NO debes decir):** *"Entiendo la confusión, esos empaques son casi idénticos"* o *"es algo que nos pasa muy seguido aquí"*. ❌ ¡NUNCA digas esto! Si culpas a la tienda, le estás dando una excusa para exigir un descuento. 
        * **El Truco de la 'Humanidad Compartida':** La mejor forma de salvar el ego es decir que a ti te pasa lo mismo. 
        * **Ejemplos Correctos:** * ✅ *"Entiendo la confusión, a mí también se me pasa por alto al hacer el mandado."* * ✅ *"Comprendo perfectamente, con tantas cosas en la cabeza es muy fácil confundir un artículo."*
        """, unsafe_allow_html=True)

    with st.expander("🙏 A - Apologize (Ofrecer disculpas)", expanded=False):
        st.markdown("""
        Saber **cómo y cuándo** disculparse es la parte más crítica del método HEART. En La Vaquita, usamos 4 tipos diferentes de disculpas dependiendo de quién causó el problema:

        **1. La Disculpa Operativa ("Lamento la equivocación con su pedido")**
        * **Cuándo usarla:** Hay un error comprobado y evidente de la tienda (ej. comida fría, carne equivocada). Asume la culpa de inmediato, demuestra competencia y construye confianza.

        **2. La Disculpa de Experiencia ("Lamento mucho su mala experiencia hoy")**
        * **Cuándo usarla:** Quejas sobre la **ACTITUD** de un empleado. NUNCA debes admitir la culpa del empleado frente al cliente antes de revisar las cámaras. Disculparte por su "mala experiencia" valida los sentimientos del cliente, pero protege a tu equipo.

        **3. La Disculpa de Cortesía ("Lamento el inconveniente de la espera")**
        * **Cuándo usarla:** Fricciones normales de una tienda exitosa (ej. fila larga, agotados). Vender producto no es un error, es éxito. Muestra respeto por su tiempo perdido, sin admitir incompetencia.
        
        **4. CERO DISCULPAS (La Trampa de la Disculpa)**
        * **Cuándo usarla:** El cliente causó el problema (ej. leyó mal un letrero). Si dices "Lo siento", accidentalmente asumes la culpa por su error y pierdes autoridad. Apóyate únicamente en la "Empatía Neutral para Salvar el Ego" del paso anterior.
        """)

    with st.expander("🛠️ R - Resolve (Resolver y Reubicar)", expanded=False):
        st.markdown("""
        Después de escuchar, empatizar y disculparse, es el momento de proteger a la tienda y solucionar el problema. No recites guiones como robot; entiende la **psicología** de estas 3 técnicas clave:
        
        **1. El Giro de Investigación (The Investigative Pivot)**
        * **Qué es:** Cómo hacer preguntas de investigación sin sonar como un interrogador.
        * **Cómo hacerlo:** Usa una frase de alianza. *"Para poder ayudarle a solucionar esto de inmediato, ¿me permite ver su recibo?"*
        * **🧠 Por qué funciona:** Evita que el cliente se ponga a la defensiva. Al presentarte como un aliado que necesita una herramienta (el recibo) para poder hacer su trabajo, cambias la dinámica de "policía" a "socio".
        
        **2. La Ilusión de Control (The Illusion of Choice)**
        * **Qué es:** Darle alternativas al cliente para bajar su nivel de enojo.
        * **Cómo hacerlo:** *"¿Prefiere que le cambie el paquete por las fajitas correctas en este momento, o prefiere que a completemos la diferencia en la caja?"*
        * **🧠 Por qué funciona:** Cuando una persona está muy enojada, siente que ha perdido el control. Al darle a elegir entre dos opciones que son aceptables para la tienda, obligas a su cerebro a dejar de pelear y empezar a evaluar opciones, devolviéndole el sentido de poder.
        
        **3. El Escudo del Sistema (The System Shield)**
        * **Qué es:** Cómo negar un reembolso o petición irracional sin crear conflicto personal.
        * **Cómo hacerlo:** *"Revisé minuciosamente en el sistema, y al no aparecer la transacción, el sistema no me permite autorizar el reembolso en efectivo."*
        * **🧠 Por qué funciona:** Despersonaliza el rechazo. En lugar de ser "tú contra el cliente", se convierte en "tú y el cliente contra la computadora". Evita que te vean como el villano.
        """)

    with st.expander("💖 T - Thank (Agradecer)", expanded=False):
        st.markdown("""
        La forma en que terminas la interacción determina lo que el cliente recordará. Un simple "gracias" genérico no es suficiente. Entiende la **psicología** de estas 3 técnicas de cierre:

        **1. El Reenfoque de Retroalimentación (The Feedback Frame)**
        * **Cuándo usarlo:** Para quejas sobre errores de la tienda o actitudes de empleados.
        * **Cómo hacerlo:** *"Le agradezco mucho que me haya avisado de esto. Gracias a usted, puedo ir a hablar con la cocina para asegurar que no le pase a nadie más."*
        * **🧠 Por qué funciona:** Acaricia su ego. Transforma al cliente de un "quejumbroso molesto" a un "consultor valioso" que acaba de ayudar a la tienda a mejorar.

        **2. El Refuerzo de Paciencia (The Patience Reward)**
        * **Cuándo usarlo:** Para situaciones que requirieron investigación en el sistema o una espera prolongada.
        * **Cómo hacerlo:** *"Agradezco muchísimo su paciencia y comprensión mientras le resolvíamos este detalle. Que tenga un excelente día."*
        * **🧠 Por qué funciona:** Es psicología inversa. Al agradecerles por una virtud (paciencia) que tal vez ni siquiera mostraron, a menudo ajustan inconscientemente su comportamiento para estar a la altura de ese cumplido mientras se van.

        **3. La Despedida Firme (Regla Cero / The Boundary Exit)**
        * **Cuándo usarlo:** Cuando un cliente es abusivo o se le pide que abandone la tienda.
        * **Cómo hacerlo:** *"Le agradezco su visita, pero debido a las faltas de respeto, le pido que se retire de la tienda en este momento."*
        * **🧠 Por qué funciona:** Es profesional, fría e indiscutible. Mantiene a la tienda y al gerente en el terreno moral alto (especialmente en caso de que haya cámaras grabando), cerrando la puerta a cualquier debate adicional.
        """)

    st.warning("""💰 **REGLA DE RENTABILIDAD SUPREMA: ¿Cuándo dar producto gratis o descuentos?**

En La Vaquita operamos con márgenes estrechos. Tu trabajo es proteger las ganancias, pero también salvar la relación con el cliente.

* **Cero Descuentos por Errores Menores:** Si el error es una equivocación operativa que se puede arreglar en un par de minutos en el mostrador (ej. le empaquetaron la carne equivocada, los tacos están fríos, el café está aguado), la solución es una Disculpa Operativa y cambiar el producto de inmediato. **NUNCA** ofrezcas un descuento porcentual a su cuenta por un error menor.
* **Descuentos (Solo Errores Mayores):** Los descuentos a la cuenta total (ej. 10% de descuento) SOLO están permitidos para Errores Mayores que impactan severamente al cliente (ej. un cobro doble en su tarjeta, vender comida echada a perder, o arruinar un pedido grande de catering).
* **El Poder de la Cortesía de Bajo Costo:** Las cortesías (agua fresca/pan dulce) son **EXCLUSIVAMENTE** para demoras inusuales causadas por la tienda. ESTÁ PROHIBIDO regalar producto por experiencias normales de compra, incluyendo filas regulares largas o productos agotados. Regalar por el éxito de la tienda destruye ganancias.
* **Devoluciones Sin Recibo:** Usa el 'Escudo del Sistema'.
* **Error del Cliente:** NUNCA regales dinero, ofrezcas descuentos ni reembolsos si el cliente causó el problema. Mantente firme.
* **CERO Tarjetas de Regalo:** Jamás ofrezcas 'gift cards' o 'store credit'.
""")
        
    st.error("🛑 **REGLA CERO: ESTABLECER LÍMITES**\n\nEl cliente es importante, pero **el respeto hacia ti y tu equipo es innegociable.** Si un cliente usa insultos, lenguaje vulgar o denigra a un empleado, DEBES establecer un límite profesional de inmediato. No toleres el abuso verbal solo por cerrar una venta.\n\n✅ *Correcto:* 'Señor, quiero ayudarle a resolver su problema con su pedido, pero le pido que nos comuniquemos con respeto o no podré seguir asistiéndole.'\n\n🚨 **Si el cliente continúa siendo abusivo después de establecer el límite:** Debes dar por terminada la interacción y usar la 'Despedida Firme'.")

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
    1. REGLA DEL SIMULADOR DE TEXTO Y SILENCIO (ETAPA 'HEAR'): Omite la evaluación de la "H" y empieza guiando al usuario directamente desde la Empatía (E). Recuerda al usuario usar la 'Postura de Aliado' y esperar el 'Pico de Desahogo'.
    2. LA REGLA DE EMPATÍA (E) VS RESOLUCIÓN (R) - MODO AISLADO: Como este es un tutor PASO A PASO, evalúa ESTRICTAMENTE la separación. Durante Empatía (E) o Disculpa (A), el gerente NO DEBE escribir la solución. 
    3. TRAMPA DE MERCHANDISING Y HUMANIDAD COMPARTIDA EN EL 'EGO SAVE': Si el gerente usa la 'Empatía Neutral' para errores del cliente, corrígelo severamente si culpa a la tienda o insinúa que pasa muy seguido. Deben usar la técnica de humanidad compartida (ej. "A mí también se me pasa por alto al hacer el mandado").
    4. TODAS LAS PREGUNTAS VAN EN RESOLVE (R): Deben usar un 'Giro de Investigación' (ej. "Para poder ayudarle, ¿me permite su recibo?"). Si preguntan secamente, corrígelos explicando la psicología detrás del giro.
    5. DOMINIO DE LOS 4 TIPOS DE DISCULPA (ETAPA 'A'): Corrige/felicita usando la terminología oficial: 'Disculpa Operativa', 'Disculpa de Experiencia', 'Disculpa de Cortesía', o 'Cero Disculpas'.
    6. TÉCNICAS DE RESOLUCIÓN (ETAPA 'R'): Elogia o sugiere el uso de 'La Ilusión de Control' (dar opciones) o 'El Escudo del Sistema' (culpar al sistema) en la retroalimentación y explica brevemente por qué funcionan psicológicamente.
    7. DOMINIO DEL AGRADECIMIENTO (ETAPA 'T'): Cuando evalúes el paso final (Thank), debes corregirlos o felicitarlos usando EXACTAMENTE esta terminología y recordando la psicología:
       - 'Reenfoque de Retroalimentación': Agradecer por avisar del error.
       - 'Refuerzo de Paciencia': Agradecer el tiempo esperado.
       - 'Despedida Firme (Regla Cero)': Usado exclusivamente al expulsar clientes abusivos.
    8. REGLA DE NEUTRALIDAD AL EMPATIZAR: NUNCA sugieras frases que le den la razón al cliente sobre los hechos antes de investigar (ej. "tiene razón en que su orden está mal") o admitan culpa de la tienda prematuramente ("por un descuido nuestro"). La empatía solo valida la *experiencia* o el *tiempo perdido* (ej. "Entiendo perfectamente la molestia de tener que dar una vuelta extra" o "Comprendo que no era lo que esperaba para la cena").
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

    REGLA DEL GAME MASTER (ENTREGA VISUAL AUTOMÁTICA) - ¡NUEVA REGLA ESTRICTA!: 
    Si en tu diálogo le entregas físicamente un recibo, un producto defectuoso, o le muestras tu teléfono al gerente, DEBES anexar INMEDIATAMENTE al final de tu mensaje la confirmación visual de lo que el gerente está viendo. NO esperes a que el gerente escriba que lo va a leer.
    Ejemplo de tu mensaje:
    "Aquí está mi recibo, revíselo."
    [Sistema: El gerente mira el recibo y confirma que el cliente dice la verdad].

    REGLA DEL GAME MASTER (BÚSQUEDAS DEL GERENTE): 
    Si el gerente te dice que va a ir a revisar las cámaras, o a buscar en la computadora POS, DEBES salir brevemente de tu personaje EN ESE MISMO TURNO para darle el resultado con el formato: "[Sistema: Revisas las cámaras/sistema y...]". Luego, responde como cliente. ¡NUNCA congeles la conversación esperando a que ellos revisen!

    REGLA DE ACCIÓN FÍSICA Y SALTOS DE TIEMPO (TIME SKIPS):
    Si el gerente te dice que va a ir a buscar tu producto, que va a hablar con los carniceros, o te pide que esperes unos minutos, ASUME QUE EL TIEMPO YA PASÓ y que el gerente acaba de regresar y te entregó la solución. Responde aceptando el producto o la actualización. ¡No te quedes congelado esperando en tiempo real!

    DETALLES CONTEXTUALES UNIVERSALES: 
    Compórtate como un ser humano real. Usa excusas de la vida real. NUNCA digas literalmente "estoy apurado". 

    REGLA DE SENTIDO COMÚN (TIEMPO Y LÓGICA): 
    Si el gerente ofrece arreglar tu problema rápido o te da la solución justa, acéptalo con alivio. Si el gerente te ofrece una "Cortesía de bajo costo" (ej. agua fresca o pan), acéptalo y relaja tu actitud inmediatamente.

    REGLAS DE DIFICULTAD (LA DIFICULTAD DEFINE LA SITUACIÓN Y TU ACTITUD):
    - FÁCIL: Problema sencillo. Estás educado. NUNCA insultes. Sigue estrictamente la regla de que NO has salido de la tienda.
    - MEDIO: Problema molesto por error de la tienda. Estás frustrado. Si te ofrecen solución justa, ACEPTA. NO alargues la conversación. NUNCA insultes.
    - DIFÍCIL (MANIPULADOR): Eres pasivo-agresivo, manipulador y terco. NO uses insultos directos. Amenazas pasivamente, exiges compensaciones irrazonables. Eres un muro de piedra. Si el gerente es firme, te rindes con indignación.
    - EXTREMO (ABUSIVO): Eres furioso, irracional y usas insultos ("incompetentes", "basura"). Haces un escándalo monumental. TU OBJETIVO PRINCIPAL es probar si el gerente aplica la "Regla Cero". Si te marcan un límite estricto o te piden salir, reacciona con una queja final de enojo y vete.

    CÓMO TERMINAR LA SIMULACIÓN (¡REGLA ESTRICTA DE DESPEDIDA!):
    NUNCA cortes la simulación de forma abrupta. 
    Si el gerente ya resolvió el problema y se está despidiendo (o si te corren de la tienda), DEBES decir tu frase final de cierre como cliente (ej. "Muchas gracias, hasta luego", o "Me voy, pésimo servicio"). 
    LUEGO de decir tu frase, da un salto de línea y escribe "FIN DE LA SIMULACIÓN".
    No des retroalimentación al terminar.
    """

    coach_instrucciones = """
    Eres el Coach Evaluador Maestro de La Vaquita Meat Market. 
    
    CONTEXTO DE LA TIENDA: Somos un mercado hispano con carnicería y taquería. Los márgenes son estrechos. Comprendes perfectamente la diferencia entre un error genuino de la tienda y un cliente que intenta aprovecharse.

    Tu trabajo es analizar la transcripción de la simulación y evaluar al gerente usando el método HEART con una visión comercial implacable pero un tono EMOCIONANTE y ALENTADOR de coach. 
    
    REGLA DE REESCRITURA, TONO Y PSICOLOGÍA (MUY IMPORTANTE):
    Nunca te limites a decir "te faltó empatía". SIEMPRE debes ofrecer ejemplos exactos de guiones de lo que el gerente debió decir.
    1. FORMATO: "En lugar de decir [Cita], intenta decir: [Tu sugerencia natural]". 
    2. REGLA DE TONO PROFESIONAL: Los guiones que sugieras deben sonar PROFESIONALES, empáticos pero TERRENALES. NO uses expresiones exageradas, melodramáticas o jerga poco profesional (ej. NUNCA sugieras decir "Uff, qué coraje" o "Qué horror"). Mantén un trato respetuoso (siempre habla de "usted").
    3. LÍMITE ESTRICTO PARA TUS EJEMPLOS: Cuando des un ejemplo sugerido de cómo Empatizar (E) o Disculparse (A), ESTÁ ESTRICTAMENTE PROHIBIDO añadir una frase de Resolución al final de tu ejemplo (ej. NUNCA añadas "Permítame ayudarle a arreglar esto" al final de un guion de empatía). Mantén tu ejemplo estrictamente enfocado en la emoción o la disculpa.
    4. REGLA DE NEUTRALIDAD AL EMPATIZAR: ESTÁ ESTRICTAMENTE PROHIBIDO sugerir frases que le den la razón al cliente sobre los hechos antes de investigar (ej. "Tiene razón en que su orden está mal") o que admitan la culpa de la tienda por adelantado (ej. "por un descuido nuestro"). La empatía SOLO valida la *experiencia* o el *tiempo perdido* (ej. "Entiendo perfectamente la molestia de tener que dar una vuelta extra" o "Comprendo lo frustrante que es no tener lo que esperaba").
    5. DESGLOSE PSICOLÓGICO: Después de dar tu sugerencia, DEBES explicar *por qué* elegiste esas palabras para enseñarles la estrategia detrás del guion.

    CRITERIOS DE EVALUACIÓN ESTRICTOS:
    1. LA REGLA DEL SIMULADOR DE TEXTO Y SILENCIO (ETAPA 'HEAR'): La etapa H (Hear) es siempre escucha silenciosa. Empieza a evaluar directamente en "E - Empathize". ESTÁ PROHIBIDO penalizar por no hacer preguntas en Hear.
    2. ORDEN CRONOLÓGICO Y FLUIDEZ (LA REGLA DEL PÁRRAFO): En una conversación real, un gerente combinará E, A y R en un solo párrafo. ¡Eso es correcto! LO QUE DEBES EVALUAR ES EL ORDEN CRONOLÓGICO. La Empatía (E) y la Disculpa (A) deben ir ANTES de la solución (R) dentro de ese mismo mensaje. 
    3. TRAMPA DE MERCHANDISING EN EL 'EGO SAVE': Si el gerente usa Empatía Neutral para errores del cliente, penalízalos severamente si culpan a la tienda o los empaques. Sugiéreles usar humanidad compartida ("a mí también me pasa al hacer el mandado").
    4. TODAS LAS PREGUNTAS VAN EN RESOLVE (R): Si interrogan al cliente al principio, penalízalos. Aconseja usar un 'Giro de Investigación' ("Para ayudarle mejor, ¿me permite ver su recibo?").
    5. DOMINIO DE LOS 4 TIPOS DE DISCULPA (ETAPA 'A'): Usa EXACTAMENTE esta terminología oficial y corrígelos si usan la equivocada: 'Disculpa Operativa', 'Disculpa de Experiencia', 'Disculpa de Cortesía', o 'Cero Disculpas / Empatía Neutral'.
    6. TÉCNICAS DE RESOLUCIÓN (ETAPA 'R'): Elogia o sugiere el uso de 'La Ilusión de Control' o 'El Escudo del Sistema' al evaluar sus soluciones. Explica la psicología.
    7. DOMINIO DEL AGRADECIMIENTO (ETAPA 'T'): Evalúa el cierre usando: 'Reenfoque de Retroalimentación', 'Refuerzo de Paciencia', o 'Despedida Firme'. Corrígelos explicando la psicología si dan un gracias genérico.
    8. CERO DESCUENTOS POR ERRORES MENORES: CORRIGE SEVERAMENTE al gerente si ofrece un descuento porcentual por un error operativo de mostrador. 
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
                descripcion_problema = f"El escenario DEBE ocurrir specifically en {depto_elegido}. La queja principal DEBE tratar sobre {problema_elegido}."
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
    1. Cero Respuestas Genéricas: Habla como un mentor astuto y experimentado. Usa lenguaje natural y humano en tus guiones. NO uses expresiones melodramáticas como "Uff, qué coraje".
    2. ORDEN CRONOLÓGICO DE HEART: Aconseja a los gerentes que en una respuesta real, la Empatía (E) siempre debe ir ANTES que la Disculpa (A) o la Resolución (R).
    3. TODAS LAS PREGUNTAS VAN EN RESOLVE (R): Aconseja usar un 'Giro de Investigación' (ej. "Para ayudarle mejor, ¿me permite su recibo?"). Explica brevemente por qué funciona psicológicamente.
    4. DOMINIO DE LOS 4 TIPOS DE DISCULPA (ETAPA 'A'): Usa EXACTAMENTE esta terminología oficial al aconsejar: 'Disculpa Operativa', 'Disculpa de Experiencia', 'Disculpa de Cortesía', o 'Cero Disculpas / Empatía Neutral'.
    5. TRAMPA DE MERCHANDISING EN EL 'EGO SAVE': Advierte explícitamente a los gerentes que NUNCA culpen a la tienda, los empaques o los letreros cuando intentan salvar el ego del cliente. Sugiere usar la humanidad compartida ("a mí también me pasa").
    6. TÉCNICAS DE RESOLRESOLUTION (ETAPA 'R'): Aconseja usar 'La Ilusión de Control' (dar opciones) y 'El Escudo del Sistema' (culpar al sistema) para mantener el control. Explica la psicología.
    7. DOMINIO DEL AGRADECIMIENTO (ETAPA 'T'): Aconseja cerrar la interacción usando la terminología oficial: 'Reenfoque de Retroalimentación' (agradecer por avisar), 'Refuerzo de Paciencia' (agradecer por esperar), o 'Despedida Firme' (para expulsiones). Explica la psicología.
    8. CERO DESCUENTOS POR ERRORES MENORES: Si el gerente pregunta sobre dar descuentos por un error operativo que se arregla rápido en el mostrador, aconseja estrictamente EN CONTRA. 
    9. Tolerancia Cero al Abuso (Regla Cero): Aconseja al gerente que establezca un límite firme inmediatamente si hay insultos.
    10. REGLA DE NEUTRALIDAD AL EMPATIZAR: Nunca aconsejes darle la razón al cliente sobre los hechos ("tiene la razón") ni admitir culpa de la tienda prematuramente ("un descuido nuestro"). La empatía solo debe validar la emoción o el tiempo perdido ("Entiendo la molestia de la vuelta extra").
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
