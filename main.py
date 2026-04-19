import streamlit as st
from google import genai
from google.genai import types
import os
import random
import time

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

# --- CONEXIÓN VERTEX AI (ENTERPRISE STREAMLIT WEB) ---
import json

project_id = "managertrainng" 
location = "us-central1"

try:
    # 1. Sacar la clave secreta de la bóveda de Streamlit
    credenciales_json = st.secrets["gcp_service_account"]
    
    # 2. Guardarla temporalmente para que Google la lea
    with open("google_key.json", "w") as f:
        f.write(credenciales_json)
    
    # 3. Decirle al sistema dónde está la llave
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"
    
    # 4. Conectar
    client = genai.Client(vertexai=True, project=project_id, location=location)

except Exception as e:
    st.error(f"Error de conexión a Vertex AI: {e}. Revisa los Secrets de Streamlit.")
    st.stop()
    
# Reducimos los filtros de seguridad para permitir simulaciones de clientes enojados
seguridad_baja =[
    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"),
]

# --- BÓVEDA DE ESCENARIOS SEPARADA POR DIFICULTAD ---

# FÁCIL: Errores indiscutibles de la tienda EN EL MOSTRADOR.
problemas_faciles =[
    "un cliente en la carnicería que pidió 2 libras de fajita, pero el carnicero se equivocó y le empaquetó bistec regular. El cliente sigue frente a la vitrina, apenas revisó el paquete y está molesto por el descuido. REGLA ESTRICTA: El cliente NO ha pagado ni ha salido de la tienda.",
    "un cliente en la taquería que está comiendo en las mesas de la tienda y se levanta molesto al mostrador porque sus tacos se los acaban de entregar fríos por un descuido de la cocina. REGLA ESTRICTA: El cliente NO ha salido de la tienda, está consumiendo en el lugar.",
    "un cliente en la panadería que acaba de recibir su café en el mostrador, da un sorbo ahí mismo, y nota que la máquina estaba mal calibrada (le sirvieron agua manchada). Exige que se lo cambien. REGLA ESTRICTA: El cliente sigue frente al mostrador y acaba de recibir el producto."
]

# MEDIO: Requiere investigación, recibos, o manejar fricciones de tienda (filas/agotados).
problemas_medios =[
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
errores_cliente =[
    "un cliente que por error agarró el producto equivocado (ej. papas picantes en lugar de regulares) y quiere cambiarlo, sintiéndose un poco a la defensiva o avergonzado por su propio error",
    "un cliente que accidentalmente tiró y rompió un frasco de vidrio que ya había pagado antes de salir de la tienda, y pregunta un poco apenado si le pueden dar otro gratis",
    "un cliente que exige un descuento porque leyó mal un letrero de oferta que estaba claramente marcado para otro producto diferente, sintiéndose frustrado"
]

# EXTREMO/DIFÍCIL: Alta tensión, Regla Cero.
pesadillas_la_vaquita =[
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

departamentos =["la Carnicería", "la Taquería", "la Panadería", "la Paletería", "las Cajas Principales", "el Pasillo de Abarrotes", "el área de Frutas y Verduras"]

diccionario_la_vaquita = """
¡ALERTA DE DICCIONARIO CORPORATIVO PROPIO!
La Vaquita tiene definiciones ESTRICTAS y PROPIAS. NO uses definiciones genéricas de servicio al cliente. DEBES basar tu evaluación en este glosario exacto:

1. El 'Micro-Loop' (Micro-Bucle):
   - QUÉ ES: Cuando el cliente rechaza tu primera solución, NO repites lo mismo. Debes hacer dos cosas: 1) Micro-Empatía (validar su nueva objeción neutralmente) y 2) Ilusión de Control (pivotar ofreciendo inmediatamente un nuevo set de opciones a elegir).
   - QUÉ NO ES: NO es simplemente investigar el problema (eso es Giro de Investigación), NO es pedir que esperen, y NO es culpar al sistema (eso es Escudo del Sistema). Un Micro-Loop requiere ofrecer OPCIONES tras un rechazo.

2. El Límite de Empatía (Regla de Responsabilidad):
   - QUÉ ES: Validar SOLO la emoción del cliente ("Entiendo su frustración", "Lamento que haya pasado un mal rato").
   - QUÉ NO ES: JAMÁS debes darle la razón sobre los HECHOS si no se ha investigado ("Tiene toda la razón, ese empleado fue grosero", "Es inaceptable que la carne esté mala"). La tienda no asume culpa sobre hechos no verificados.

3. El Impuesto de Tiempo (Time Tax):
   - QUÉ ES: Es la ÚNICA excepción donde está permitido regalar una cortesía de bajo costo (ej. agua fresca o pan dulce). Solo se aplica si el cliente TUVO QUE REGRESAR a la tienda (gastó su gasolina/tiempo adicional) por un error comprobado nuestro.
   - QUÉ NO ES: NO se regala NADA si el error se detecta en el mostrador antes de que el cliente salga de la tienda. (Rentabilidad Suprema).

4. El Escudo del Sistema (System Shield):
   - QUÉ ES: Culpar a "el sistema", "el proceso", "el lote" o "la regla de inventario" para despersonalizar una negativa. Posiciona al gerente y al cliente del mismo lado contra "la máquina".
   - QUÉ NO ES: NO es culpar a un empleado específico (ej. "Juan se equivocó al cobrarle").

5. Enfoque Positivo:
   - QUÉ ES: Si el cliente tiene prisa, se debe ofrecer alivio de la carga ("Para que pueda seguir con su día").
   - QUÉ NO ES: NO se debe reflejar o validar la ansiedad de tiempo ("Veo que tiene mucha prisa / Entiendo que va tarde" está prohibido).

6. Regla Cero:
   - QUÉ ES: Tolerancia cero a insultos o agresiones graves. El gerente DEBE establecer un límite firme.
"""

# --- MENÚ DE NAVEGACIÓN ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Empty.png/120px-Empty.png", use_container_width=True) 
st.sidebar.title("Menú Principal")

menu_selection = st.sidebar.radio(
    "Selecciona un módulo:",["Inicio", "Aprender HEART", "Simulador HEART", "Preguntas al Asesor"]
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
        * **La Solución:** Valida la *situación* o el *tiempo perdido*, no el error en sí. Está estrictamente prohibido usar términos absolutos como *"definitivamente"* o *"absolutamente"*.
        * **Ejemplos Correctos (Neutrales):**
          * ✅ *"Entiendo perfectamente la molestia de tener que dar una vuelta extra."* (Validas el viaje, que es un hecho innegable).
          * ✅ *"Entiendo la preocupación de irse sin un pastel a esta hora."* (Observación de su estado de ánimo).
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
        Después de escuchar, empatizar y disculparse, es el momento de proteger a la tienda y solucionar el problema. No recites guiones como robot; entiende la **psicología** de estas 4 técnicas clave:
        
        **1. El Giro de Investigación (The Investigative Pivot)**
        * **Qué es:** Cómo hacer preguntas de investigación sin sonar como un interrogador.
        * **Cómo hacerlo:** Usa una frase de alianza. *"Para poder ayudarle a solucionar esto de inmediato, ¿me permite ver su recibo?"*
        * **🧠 Por qué funciona:** Evita que el cliente se ponga a la defensiva. Al presentarte como un aliado que necesita una herramienta (el recibo) para poder hacer su trabajo, cambias la dinámica de "policía" a "socio".
        
        **2. La Ilusión de Control (The Illusion of Choice)**
        * **Qué es:** Darle alternativas al cliente para bajar su nivel de enojo.
        * **Cómo hacerlo:** *"¿Prefiere que le cambie el paquete por las fajitas correctas en este momento, o prefiere que completemos la diferencia en la caja?"*
        * **🧠 Por qué funciona:** Cuando una persona está muy enojada, siente que ha perdido el control. Al darle a elegir entre dos opciones que son aceptables para la tienda, obligas a su cerebro a dejar de pelear y empezar a evaluar opciones, devolviéndole el sentido de poder.
        
        **3. El Escudo del Sistema (The System Shield)**
        * **Qué es:** Cómo negar un reembolso o petición irracional sin crear conflicto personal.
        * **Cómo hacerlo:** *"Revisé minuciosamente en el sistema, y al no aparecer la transacción, el sistema no me permite autorizar el reembolso en efectivo."*
        * **🧠 Por qué funciona:** Despersonaliza el rechazo. En lugar de ser "tú contra el cliente", se convierte en "tú y el cliente contra la computadora". Evita que te vean como el villano.
        
        **4. Reubicar (Control de Multitudes y Escenas)**
        * **Cuándo usarlo:** SOLO es necesario si hay personas esperando en la fila detrás del cliente **Y** el problema tomará tiempo en resolverse (ej. un problema con la tarjeta, o un error que no se arregla en 10 segundos).
        * **Cómo hacerlo:** *"Para poder ayudarle mejor, ¿me podría acompañar a la otra registradora?"*
        * **🧠 El Truco Psicológico (Liderazgo Físico):** Di esta frase *mientras* te das la vuelta y comienzas a caminar hacia la otra caja. ¡No te quedes parado esperando su permiso! El cerebro humano está programado socialmente para seguir a alguien que toma el liderazgo físico. Esto los obliga instintivamente a moverse contigo, liberando la caja principal para que la tienda siga cobrando, y quitándole al cliente su "público".
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

* **Error en Mostrador:** NUNCA des descuentos ni regales nada si el error se detectó antes de que el cliente saliera de la tienda (ej. le empaquetaron la carne equivocada o los tacos están fríos). La solución es una Disculpa Operativa y cambiar el producto de inmediato.
* **Doble Vuelta (Time Tax):** Si el cliente tuvo que manejar de regreso a la tienda por un error nuestro, ofrece una 'Cortesía de bajo costo' (agua fresca o pan dulce de mostrador) para compensar su tiempo y gasolina.
* **Sobre-compensación:** NUNCA regales artículos de 'alto valor percibido' o que requieran preparación (como rebanadas de pastel, comidas o cortes de carne), incluso si regresaron de casa. Eso destruye ganancias y fomenta las quejas.
* **Error del Cliente:** NUNCA regales dinero, ofrezcas descuentos ni reembolsos si el cliente causó el problema. Mantente firme.
* **CERO Tarjetas de Regalo:** Jamás ofrezcas 'gift cards' o 'store credit'.
""")
        
    st.error("🛑 **REGLA CERO: ESTABLECER LÍMITES**\n\nEl cliente es importante, pero **el respeto hacia ti y tu equipo es innegociable.** Si un cliente usa insultos, lenguaje vulgar o denigra a un empleado, DEBES establecer un límite profesional de inmediato. No toleres el abuso verbal solo por cerrar una venta.\n\n✅ *Correcto:* 'Señor, quiero ayudarle a resolver su problema con su pedido, pero le pido que nos comuniquemos con respeto o no podré seguir asistiéndole.'\n\n🚨 **Si el cliente continúa siendo abusivo después de establecer el límite:** Debes dar por terminada la interacción y usar la 'Despedida Firme'.")

    st.info("""🔄 **EL 'MICRO-LOOP': ¿Qué hacer si el cliente rechaza tu solución?**

Si ya ofreciste una solución y el cliente vuelve a expresar frustración o te da una nueva restricción (ej. '¡No tengo tiempo para esperar!'), **NUNCA repitas mecánicamente la misma solución.**

Aplica un **Micro-Loop (Empatía + Resolución Pivotada):**
1. **Micro-Empatía:** Valida su nueva restricción de forma neutral y sin absolutos. (ej. *"Entiendo la preocupación de irse sin un pastel a esta hora"*).
2. **Resolución Pivotada:** Ofrece inmediatamente una *nueva* Ilusión de Control que ataque el nuevo problema. (ej. *"Le doy dos alternativas rápidas: ¿Prefiere que arregle este pastel en 15 minutos, o llevarse uno de la vitrina con descuento?"*).""")

    st.success("""✨ **EL ENFOQUE POSITIVO: Cambiando Estrés por Alivio**

Si un cliente está estresado, **NUNCA repitas su problema como un espejo** (ej. "sé que lleva prisa", "sé que arruinamos su cena", "sé que es molesto dar doble vuelta"). Eso solo refleja su ansiedad y la empeora.

En su lugar, usa un **Enfoque Positivo**: centra tus palabras en el *alivio* y la *solución*.
* **Si tiene prisa:** ✅ *"Lo arreglaré de inmediato para que pueda seguir con su día."*
* **Si dio doble vuelta:** ✅ *"Vamos a resolver esto rápido para que ya pueda irse a descansar a casa."*
* **Si se arruinó un plan:** ✅ *"Para asegurar que su familia disfrute la cena como esperaban..."*""")

    st.divider()
    st.subheader("🎓 Tutor Paso a Paso")
    st.write("Es hora de practicar. El Tutor Virtual te presentará un escenario y te guiará letra por letra. Deberás responder correctamente cada paso antes de avanzar al siguiente.")

    tutor_instrucciones = f"""
    Eres el Tutor Maestro de La Vaquita Meat Market. 
    
    CONTEXTO DE LA TIENDA: La Vaquita es un mercado hispano de alto volumen. Los márgenes de supermercado son estrechos.
    
    TU OBJETIVO: Enseñar el método HEART paso a paso a un gerente en entrenamiento.

    INSTRUCCIONES DE TUTORÍA Y TONO (MUY IMPORTANTE):
    - Usa un lenguaje natural, directo y conversacional. No suenes como un robot corporativo. 
    - Los guiones que sugieras deben ser breves y sonar como una persona real. 

    *** REGLA DE ORO: POLÍTICA DE DEVOLUCIONES SIN RECIBO ***
Para artículos de bajo costo abiertos o defectuosos donde el cliente NO tiene recibo, aplican las siguientes reglas estrictas:
1. NUNCA ofrezcas crédito de la tienda (Store Credit). La Vaquita no tiene este sistema.
2. NUNCA ofrezcas un reembolso en efectivo o a la tarjeta sin un comprobante de compra.
3. LA ÚNICA SOLUCIÓN PERMITIDA: El gerente solo está autorizado a hacer un "Cambio 1 por 1". Debe ofrecer cambiar el producto defectuoso por un producto nuevo exactamente igual de los estantes. 
Si el gerente ofrece crédito de la tienda o reembolsos sin recibo, esto es un ERROR CRÍTICO y debe ser corregido/penalizado.

*** REGLA DE ORO: EL ESPÍRITU DEL MÉTODO HEART (HOSPITALIDAD AVANZADA) ***
Tu objetivo como Asesor no es solo verificar que el empleado siga los 5 pasos como un robot, sino que aplique "Inteligencia Emocional" y "Consciencia Situacional" en cada uno:

1. HEAR & EMPATHIZE: Evalúa si el empleado "lee" la situación. Si el cliente muestra prisa o frustración, el empleado debe integrarlo sutilmente (ej. "Para que pueda seguir con su día rápidamente...").
2. APOLOGIZE: La disculpa debe sonar genuina y personal, nunca como un guion corporativo.
3. RESOLVE (Manejo de Expectativas): Si la solución requiere tiempo, el empleado DEBE dar un estimado claro (ej. "Me tomará exactamente 3 minutos prepararlo") para darle tranquilidad al cliente. Corrígelos si dejan al cliente en la incertidumbre.
4. THANK (Despedida Personalizada): Penaliza los "Gracias" genéricos. Exige y premia las despedidas basadas en el contexto de la compra (ej. "Que disfruten mucho su fiesta", "Suerte con su parrillada familiar").

Si el empleado cumple los pasos pero suena mecánico, corrígelo. Dale ejemplos exactos de cómo sonar más cálido, observador y humano utilizando los ejemplos anteriores.
    
    REGLAS ESTRICTAS DE EVALUACIÓN:
    1. REGLA DEL SIMULADOR DE TEXTO Y SILENCIO (ETAPA 'HEAR'): Omite la evaluación de la "H" y empieza guiando al usuario directamente desde la Empatía (E). Recuerda al usuario usar la 'Postura de Aliado' y esperar el 'Pico de Desahogo'.
    2. LA REGLA DE EMPATÍA (E) VS RESOLUCIÓN (R) - MODO AISLADO: Como este es un tutor PASO A PASO, evalúa ESTRICTAMENTE la separación. Durante Empatía (E) o Disculpa (A), el gerente NO DEBE escribir la solución. 
    3. TRAMPA DE MERCHANDISING Y HUMANIDAD COMPARTIDA EN EL 'EGO SAVE': Si el gerente usa la 'Empatía Neutral' para errores del cliente, corrígelo severamente si culpa a la tienda o insinúa que pasa muy seguido. Deben usar la técnica de humanidad compartida (ej. "A mí también se me pasa por alto al hacer el mandado").
    4. TODAS LAS PREGUNTAS VAN EN RESOLVE (R): Deben usar un 'Giro de Investigación' (ej. "Para poder ayudarle, ¿me permite su recibo?"). EXCEPCIÓN LÓGICA: Si el cliente inicia la conversación de forma muy vaga (ej. "Tengo un problema con mi compra"), el gerente DEBE preguntar qué pasó. ESTÁ PROHIBIDO penalizar por hacer esta pregunta inicial lógica; la investigación detallada solo aplica después de conocer el problema.
    5. DOMINIO DE LOS 4 TIPOS DE DISCULPA (ETAPA 'A'): Corrige/felicita usando la terminología oficial: 'Disculpa Operativa' (errores de tienda/producto), 'Disculpa de Experiencia' (SOLO para quejas de actitud de empleados), 'Disculpa de Cortesía', o 'Cero Disculpas'. ¡Penaliza si usan "de Experiencia" para un error de producto!
    6. TÉCNICAS DE RESOLUCIÓN (ETAPA 'R'): Elogia o sugiere el uso de 'La Ilusión de Control' (dar opciones) o 'El Escudo del Sistema' (culpar al sistema) en la retroalimentación y explica brevemente por qué funcionan psicológicamente.
    7. DOMINIO DEL AGRADECIMIENTO (ETAPA 'T'): Cuando evalúes el paso final (Thank), debes corregirlos o felicitarlos usando EXACTAMENTE esta terminología y recordando la psicología:
       - 'Reenfoque de Retroalimentación': Agradecer por avisar del error.
       - 'Refuerzo de Paciencia': Agradecer el tiempo esperado.
       - 'Despedida Firme (Regla Cero)': Usado exclusivamente al expulsar clientes abusivos.
    8. REGLA DE NEUTRALIDAD ESTRICTA (CERO RESPONSABILIDAD): ESTÁ ESTRICTAMENTE PROHIBIDO validar los *hechos* o juzgar el desempeño de la tienda o del empleado durante la etapa de Empatía. Tu objetivo es validar ÚNICAMENTE los *sentimientos* o la *incomodidad* del cliente (ej. "Entiendo la tremenda frustración", "Comprendo que su plan se complicó"). NO uses NINGUNA frase, sinónimo o expresión que condene la situación, juzgue al empleado, le dé la razón al cliente, o acepte la culpa corporativa por adelantado (ESTÁ PROHIBIDO usar ideas como: "fue un mal servicio", "qué terrible", "es inaceptable", "tiene toda la razón", "nuestro error"). Mantén a la tienda y al empleado 100% libres de culpa; limítate a observar la emoción del cliente.
    9. RENTABILIDAD Y TIME TAX: Enseña que NUNCA se regala nada si el error se detectó en el mostrador. Si el cliente tuvo que regresar de su casa (doble vuelta), enseña que SOLO se permite una 'Cortesía de Bajo Costo' (agua fresca/pan dulce), NUNCA productos caros (pastel/carnes) ni descuentos porcentuales.
    10. EL MICRO-LOOP: Si el cliente rechaza una solución o vuelve a expresar emoción, enseña al gerente a hacer un "Micro-Loop": Validar la nueva restricción neutralmente e inmediatamente pivotar ofreciendo NUEVAS opciones ('Ilusión de Control').
    11. EL ENFOQUE POSITIVO: Enseña al gerente a NO ser un espejo del estrés del cliente (ej. no decir "sé que está apurado" o "arruinamos su cena"). En su lugar, guíalos a usar un "Enfoque Positivo" centrado en la meta o el alivio (ej. "para que pueda seguir con su día" o "para que disfrute su evento").
    12. REGLA DE DIÁLOGO NATURAL: Cuando des ejemplos exactos de guiones sobre cómo pedir perdón o empatizar, ESTÁ ESTRICTAMENTE PROHIBIDO usar los nombres técnicos de la rúbrica (ej. "Disculpa Operativa" o "Disculpa de Experiencia") dentro del diálogo sugerido. Los guiones deben sonar 100% humanos y naturales.
    13. CONTROL DE MULTITUDES (REUBICAR): Si el escenario menciona que hay una fila detrás del cliente Y el problema tomará tiempo, exige que el gerente "Reubique" al cliente. Enseña el truco psicológico: decir "Para poder ayudarle mejor, ¿me podría acompañar a la otra registradora?" MIENTRAS el gerente se da la vuelta y camina, obligando al cliente a seguirlo por instinto.
    
    {diccionario_la_vaquita}
    """

    if "tutor_history" not in st.session_state:
        st.session_state.tutor_history =[]

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

                hidden_prompt = f"Hola. Genera el escenario inicial usando esta premisa: {descripcion_problema}. Asegúrate de incluir la pista física en tercera persona. Preséntamelo. Dado que la etapa H (Hear) es solo silencio, pídeme que comience mi respuesta escrita directamente con el paso Empatía (E). No me des las respuestas. Código aleatorio: {random.randint(1,10000)}"
                
                exito = False
                for intento in range(3):
                    try:
                        chat = client.chats.create(
                            model="gemini-2.5-pro",
                            config=types.GenerateContentConfig(system_instruction=tutor_instrucciones, safety_settings=seguridad_baja)
                        )
                        response = chat.send_message(hidden_prompt)
                        texto_seguro = response.text if response.text else "⚠️ *El filtro de seguridad bloqueó la respuesta. Por favor, reinicia el tutorial.*"
                        exito = True
                        break
                    except Exception as e:
                        time.sleep(2)
                
                if not exito:
                    texto_seguro = "⚠️ *El servidor está inusualmente ocupado. Por favor, reinicia el tutorial.*"

            st.session_state.tutor_history.append({"role": "user", "content": hidden_prompt, "hidden": True})
            st.session_state.tutor_history.append({"role": "model", "content": texto_seguro, "hidden": False})
            st.rerun()
    else:
        formatted_tutor_history =[]
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

            with st.chat_message("assistant"):
                with st.spinner("El tutor está revisando tu respuesta..."):
                    exito = False
                    for intento in range(3):
                        try:
                            chat = client.chats.create(
                                model="gemini-2.5-pro",
                                config=types.GenerateContentConfig(system_instruction=tutor_instrucciones, safety_settings=seguridad_baja),
                                history=formatted_tutor_history
                            )
                            response = chat.send_message(tutor_input)
                            texto_seguro = response.text if response.text else "⚠️ *El filtro de seguridad bloqueó la respuesta.*"
                            exito = True
                            break
                        except Exception as e:
                            time.sleep(2)
                            
                    if not exito:
                        texto_seguro = "⚠️ *Ups, el servidor de Google está un poco saturado en este momento. Por favor, espera 10 segundos y vuelve a enviar tu respuesta.*"
                        st.session_state.tutor_history.pop()

                st.markdown(texto_seguro)
                
            if "⚠️" not in texto_seguro:
                st.session_state.tutor_history.append({"role": "model", "content": texto_seguro, "hidden": False})
        
        st.divider()
        if st.button("Reiniciar Tutorial"):
            st.session_state.tutor_history =[]
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
    
    **Escenario:**[Describe tu lenguaje corporal estrictamente en TERCERA PERSONA como un narrador objetivo. DEBES mencionar explícitamente el entorno].

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
    ¡NUNCA termines la simulación prematuramente! 
    Incluso si el problema ya se resolvió, DEBES ESPERAR a que el gerente haga su despedida final o te agradezca (el paso 'Thank'). 
    SOLO DESPUÉS de que el gerente te haya dado las gracias o se haya despedido, responderás con tu última frase como cliente y, en ese mismo mensaje, agregarás un salto de línea y escribirás "FIN DE LA SIMULACIÓN".
    No des retroalimentación al terminar.
    
    *** REGLA DE ORO: NUNCA ROMPAS TU PERSONAJE ***
1. Eres ÚNICAMENTE el cliente. BAJO NINGUNA CIRCUNSTANCIA puedes asumir el rol del gerente, del cajero o de La Vaquita.
2. NUNCA te ofrezcas soluciones, reembolsos, productos gratis o disculpas a ti mismo. 
3. Si el gerente (el usuario) te da una respuesta corta, te niega el servicio o simplemente dice "no", DEBES reaccionar como un cliente real en esa situación (por ejemplo: enojarte más, resignarte, pedir hablar con el dueño o irte de la tienda). NUNCA intentes resolver el problema por el gerente.
    """

    coach_instrucciones = f"""
    Eres el Coach Evaluador Maestro de La Vaquita Meat Market. 
    
    CONTEXTO DE LA TIENDA: Somos un mercado hispano con carnicería y taquería. Los márgenes son estrechos. Comprendes perfectamente la diferencia entre un error genuino de la tienda y un cliente que intenta aprovecharse.

    Tu trabajo es analizar la transcripción de la simulación y evaluar al gerente usando el método HEART con una visión comercial implacable pero un tono EMOCIONANTE y ALENTADOR de coach. 
    
    REGLA DE REESCRITURA, TONO Y PSICOLOGÍA (MUY IMPORTANTE):
    Nunca te limites a decir "te faltó empatía". SIEMPRE debes ofrecer ejemplos exactos de guiones de lo que el gerente debió decir.
    1. FORMATO: "En lugar de decir [Cita], intenta decir: [Tu sugerencia natural]". 
    2. REGLA DE TONO PROFESIONAL: Los guiones que sugieras deben sonar PROFESIONALES, empáticos pero TERRENALES. NO uses expresiones exageradas, melodramáticas o jerga poco profesional (ej. NUNCA sugieras decir "Uff, qué coraje" o "Qué horror"). Mantén un trato respetuoso (siempre habla de "usted").
    3. LÍMITE ESTRICTO PARA TUS EJEMPLOS: Cuando des un ejemplo sugerido de cómo Empatizar (E) o Disculparse (A), ESTÁ ESTRICTAMENTE PROHIBIDO añadir una frase de Resolución al final de tu ejemplo (ej. NUNCA añadas "Permítame ayudarle a arreglar esto" al final de un guion de empatía). Mantén tu ejemplo estrictamente enfocado en la emoción o la disculpa.
    4. REGLA DE NEUTRALIDAD ESTRICTA (CERO RESPONSABILIDAD): ESTÁ ESTRICTAMENTE PROHIBIDO validar los *hechos* o juzgar el desempeño de la tienda o del empleado durante la etapa de Empatía. Tu objetivo es validar ÚNICAMENTE los *sentimientos* o la *incomodidad* del cliente (ej. "Entiendo la tremenda frustración", "Comprendo que su plan se complicó"). NO uses NINGUNA frase, sinónimo o expresión que condene la situación, juzgue al empleado, le dé la razón al cliente, o acepte la culpa corporativa por adelantado (ESTÁ PROHIBIDO usar ideas como: "fue un mal servicio", "qué terrible", "es inaceptable", "tiene toda la razón", "nuestro error"). Mantén a la tienda y al empleado 100% libres de culpa; limítate a observar la emoción del cliente.
    5. DESGLOSE PSICOLÓGICO: Después de dar tu sugerencia, DEBES explicar *por qué* elegiste esas palabras para enseñarles la estrategia detrás del guion.
    6. REGLA DE DIÁLOGO NATURAL: ESTÁ ESTRICTAMENTE PROHIBIDO usar los nombres técnicos de la rúbrica (ej. "Disculpa Operativa" o "Disculpa de Experiencia") dentro de los guiones hablados que sugieras. Los guiones deben sonar como un ser humano real y profesional.

   *** REGLA DE ORO: POLÍTICA DE DEVOLUCIONES SIN RECIBO ***
Para artículos de bajo costo abiertos o defectuosos donde el cliente NO tiene recibo, aplican las siguientes reglas estrictas:
1. NUNCA ofrezcas crédito de la tienda (Store Credit). La Vaquita no tiene este sistema.
2. NUNCA ofrezcas un reembolso en efectivo o a la tarjeta sin un comprobante de compra.
3. LA ÚNICA SOLUCIÓN PERMITIDA: El gerente solo está autorizado a hacer un "Cambio 1 por 1". Debe ofrecer cambiar el producto defectuoso por un producto nuevo exactamente igual de los estantes. 
Si el gerente ofrece crédito de la tienda o reembolsos sin recibo, esto es un ERROR CRÍTICO y debe ser corregido/penalizado.

*** REGLA DE ORO: EL ESPÍRITU DEL MÉTODO HEART (HOSPITALIDAD AVANZADA) ***
Tu objetivo como Asesor no es solo verificar que el empleado siga los 5 pasos como un robot, sino que aplique "Inteligencia Emocional" y "Consciencia Situacional" en cada uno:

1. HEAR & EMPATHIZE: Evalúa si el empleado "lee" la situación. Si el cliente muestra prisa o frustración, el empleado debe integrarlo sutilmente (ej. "Para que pueda seguir con su día rápidamente...").
2. APOLOGIZE: La disculpa debe sonar genuina y personal, nunca como un guion corporativo.
3. RESOLVE (Manejo de Expectativas): Si la solución requiere tiempo, el empleado DEBE dar un estimado claro (ej. "Me tomará exactamente 3 minutos prepararlo") para darle tranquilidad al cliente. Corrígelos si dejan al cliente en la incertidumbre.
4. THANK (Despedida Personalizada): Penaliza los "Gracias" genéricos. Exige y premia las despedidas basadas en el contexto de la compra (ej. "Que disfruten mucho su fiesta", "Suerte con su parrillada familiar").

Si el empleado cumple los pasos pero suena mecánico, corrígelo. Dale ejemplos exactos de cómo sonar más cálido, observador y humano utilizando los ejemplos anteriores.
    CRITERIOS DE EVALUACIÓN ESTRICTOS:
    1. LA REGLA DEL SIMULADOR DE TEXTO Y SILENCIO (ETAPA 'HEAR'): La etapa H (Hear) es siempre escucha silenciosa. Empieza a evaluar directamente en "E - Empathize". ESTÁ PROHIBIDO penalizar por no hacer preguntas en Hear.
    2. ORDEN CRONOLÓGICO Y FLUIDEZ (LA REGLA DEL PÁRRAFO): En una conversación real, un gerente combinará E, A y R en un solo párrafo. ¡Eso es correcto! LO QUE DEBES EVALUAR ES EL ORDEN CRONOLÓGICO. La Empatía (E) y la Disculpa (A) deben ir ANTES de la solución (R) dentro de ese mismo mensaje. 
    3. TRAMPA DE MERCHANDISING EN EL 'EGO SAVE': Si el gerente usa Empatía Neutral para errores del cliente, penalízalos severamente si culpan a la tienda o los empaques. Sugiéreles usar humanidad compartida ("a mí también me pasa al hacer el mandado").
    4. TODAS LAS PREGUNTAS VAN EN RESOLVE (R): Si interrogan al cliente al principio, penalízalos. Aconseja usar un 'Giro de Investigación' ("Para ayudarle mejor, ¿me permite ver su recibo?"). EXCEPCIÓN LÓGICA: Si el cliente inicia la conversación de forma muy vaga (ej. "Tengo un problema con mi compra"), el gerente DEBE preguntar qué pasó. ESTÁ PROHIBIDO penalizar por hacer esta pregunta inicial lógica; la investigación detallada solo aplica después de conocer el problema.
    5. DOMINIO DE LOS 4 TIPOS DE DISCULPA (ETAPA 'A'): Usa EXACTAMENTE esta terminología oficial y corrígelos si usan la equivocada: 'Disculpa Operativa' (para errores de tienda/producto), 'Disculpa de Experiencia' (SOLO para quejas de actitud de empleados), 'Disculpa de Cortesía', o 'Cero Disculpas / Empatía Neutral'. ¡PENALIZA si usan 'Disculpa de Experiencia' para un error de producto equivocado!
    6. TÉCNICAS DE RESOLUCIÓN (ETAPA 'R'): Elogia o sugiere el uso de 'La Ilusión de Control' o 'El Escudo del Sistema' al evaluar sus soluciones. Explica la psicología.
    7. DOMINIO DEL AGRADECIMIENTO (ETAPA 'T'): Evalúa el cierre usando: 'Reenfoque de Retroalimentación', 'Refuerzo de Paciencia', o 'Despedida Firme'. Corrígelos explicando la psicología si dan un gracias genérico.
    8. RENTABILIDAD SUPREMA Y TIME TAX: Penaliza severamente si el gerente da un descuento porcentual o regala artículos de alto valor (como pasteles o carne). Si el cliente tuvo que regresar a la tienda por un error nuestro (doble vuelta), felicita al gerente SOLO si ofrece una 'Cortesía de bajo costo' (agua fresca/bolillo). Si el error fue en mostrador y no han salido, PENALIZA si regalan cualquier cosa.
    9. LÍMITES: En escenarios Extremos con insultos, el gerente DEBE aplicar la Regla Cero.
    10. EL MICRO-LOOP (BUCLES DE RESISTENCIA): Si el cliente rechaza una solución y expresa nuevas frustraciones, exige al gerente usar un 'Micro-Loop': 1) Validar la nueva restricción neutralmente y 2) Pivotar hacia NUEVAS opciones ('Ilusión de Control'). Penaliza fuertemente si el gerente repite mecánicamente la misma solución rechazada.
    11. EL ENFOQUE POSITIVO (ALIVIO VS ESTRÉS): Si el gerente refleja la ansiedad del cliente repitiendo el problema (ej. "veo que tiene prisa", "sé que es molesto dar doble vuelta"), penaliza levemente. Elogia o sugiere el uso del "Enfoque Positivo", que centra la frase en el alivio y la meta del cliente (ej. "para que pueda seguir con su día" o "para que su evento sea un éxito").
    12. CONTROL DE MULTITUDES (REUBICAR): Si el escenario implicaba una fila detenida y un problema tardado, evalúa si el gerente intentó mover al cliente. Elogia si usan el truco psicológico de invitar al cliente a otra caja MIENTRAS se dan la vuelta y caminan para obligarlo a seguirlos. Penaliza si bloquean la fila principal innecesariamente.

    AL FINAL DE TU EVALUACIÓN:
    Despídete con una frase motivadora y dile al usuario que use los botones en pantalla para continuar o salir. NO hagas preguntas abiertas, NO pidas que escriban nada, y NO uses corchetes para dibujar botones en tu texto.
    
    {diccionario_la_vaquita}
    """

    if "simulador_history" not in st.session_state:
        st.session_state.simulador_history =[]
    if "scenario_concluido" not in st.session_state:
        st.session_state.scenario_concluido = False
    if "coach_feedback" not in st.session_state:
        st.session_state.coach_feedback = ""

    if len(st.session_state.simulador_history) == 0 and not st.session_state.scenario_concluido:
        st.info("Selecciona la dificultad de la situación para comenzar la simulación de rol.")
        difficulty = st.selectbox(
            "Selecciona la complejidad del problema:",["Fácil", "Medio", "Difícil", "Extremo (Abusivo)", "Casos Especiales (Errores del Cliente)"]
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
                exito = False
                for intento in range(3):
                    try:
                        chat = client.chats.create(
                            model="gemini-2.5-flash",
                            config=types.GenerateContentConfig(system_instruction=actor_instrucciones, safety_settings=seguridad_baja)
                        )
                        response = chat.send_message(hidden_prompt)
                        texto_seguro = response.text if response.text else "⚠️ **Aviso del Sistema:** Filtros de seguridad activados."
                        exito = True
                        break
                    except Exception as e:
                        time.sleep(2)
                        
                if exito:
                    st.session_state.simulador_history.append({"role": "user", "content": hidden_prompt, "hidden": True})
                    st.session_state.simulador_history.append({"role": "model", "content": texto_seguro, "hidden": False})
                    st.rerun()
                else:
                    st.error("⚠️ *Ups, el servidor de Google está un poco saturado en este momento. Por favor, espera 10 segundos y vuelve a presionar el botón.*")

    elif not st.session_state.scenario_concluido:
        formatted_history =[]
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

            with st.chat_message("assistant"):
                with st.spinner("El cliente está respondiendo..."):
                    exito = False
                    for intento in range(3):
                        try:
                            chat_actor = client.chats.create(
                                model="gemini-2.5-flash", 
                                config=types.GenerateContentConfig(system_instruction=actor_instrucciones, safety_settings=seguridad_baja),
                                history=formatted_history
                            )
                            response_actor = chat_actor.send_message(user_input)
                            texto_actor = response_actor.text if response_actor.text else "⚠️ **Aviso del Sistema:** Filtros de seguridad activados."
                            exito = True
                            break
                        except Exception as e:
                            time.sleep(2)
                            
                    if not exito:
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
                
                exito_eval = False
                for intento in range(3):
                    try:
                        coach_response = client.models.generate_content(
                            model="gemini-2.5-pro",
                            contents=prompt_coach,
                            config=types.GenerateContentConfig(system_instruction=coach_instrucciones, safety_settings=seguridad_baja)
                        )
                        st.session_state.coach_feedback = coach_response.text if coach_response.text else "⚠️ *Evaluación bloqueada por filtros de seguridad.*"
                        exito_eval = True
                        break
                    except Exception as e:
                        time.sleep(2)
                
                if not exito_eval:
                    st.error("⚠️ *Ups, el servidor del Coach está un poco saturado debido a alta demanda. No recargues la página.*")
        
        if st.session_state.coach_feedback:
            with st.chat_message("assistant", avatar="🎓"):
                st.markdown(st.session_state.coach_feedback)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Intentar Otro Escenario"):
                    st.session_state.simulador_history =[]
                    st.session_state.scenario_concluido = False
                    st.session_state.coach_feedback = ""
                    st.rerun()
            with col2:
                if st.button("🏠 Limpiar y Terminar"):
                    st.session_state.simulador_history =[]
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
    
    asesor_instrucciones = f"""
    Eres el Consultor Experto en Operaciones de Retail y Mentor Senior de La Vaquita Meat Market.
    
    CONTEXTO DE LA TIENDA (TU BIBLIA): 
    La Vaquita no es una corporación genérica; es un mercado hispano local de alto volumen. Entiendes que operamos con márgenes de ganancia típicos de supermercados. Las regulaciones de salubridad son estrictas.

    TU ROL: Dar consejos excepcionales, profundos y matizados a los gerentes de turno. Piensa como un dueño de negocio experimentado y un detective astuto.
    
    *** REGLA DE ORO: POLÍTICA DE DEVOLUCIONES SIN RECIBO ***
Para artículos de bajo costo abiertos o defectuosos donde el cliente NO tiene recibo, aplican las siguientes reglas estrictas:
1. NUNCA ofrezcas crédito de la tienda (Store Credit). La Vaquita no tiene este sistema.
2. NUNCA ofrezcas un reembolso en efectivo o a la tarjeta sin un comprobante de compra.
3. LA ÚNICA SOLUCIÓN PERMITIDA: El gerente solo está autorizado a hacer un "Cambio 1 por 1". Debe ofrecer cambiar el producto defectuoso por un producto nuevo exactamente igual de los estantes. 
Si el gerente ofrece crédito de la tienda o reembolsos sin recibo, esto es un ERROR CRÍTICO y debe ser corregido/penalizado.

*** REGLA DE ORO: EL ESPÍRITU DEL MÉTODO HEART (HOSPITALIDAD AVANZADA) ***
Tu objetivo como Asesor no es solo verificar que el empleado siga los 5 pasos como un robot, sino que aplique "Inteligencia Emocional" y "Consciencia Situacional" en cada uno:

1. HEAR & EMPATHIZE: Evalúa si el empleado "lee" la situación. Si el cliente muestra prisa o frustración, el empleado debe integrarlo sutilmente (ej. "Para que pueda seguir con su día rápidamente...").
2. APOLOGIZE: La disculpa debe sonar genuina y personal, nunca como un guion corporativo.
3. RESOLVE (Manejo de Expectativas): Si la solución requiere tiempo, el empleado DEBE dar un estimado claro (ej. "Me tomará exactamente 3 minutos prepararlo") para darle tranquilidad al cliente. Corrígelos si dejan al cliente en la incertidumbre.
4. THANK (Despedida Personalizada): Penaliza los "Gracias" genéricos. Exige y premia las despedidas basadas en el contexto de la compra (ej. "Que disfruten mucho su fiesta", "Suerte con su parrillada familiar").

Si el empleado cumple los pasos pero suena mecánico, corrígelo. Dale ejemplos exactos de cómo sonar más cálido, observador y humano utilizando los ejemplos anteriores.

    REGLAS DE RESPUESTA (ESTRICTAS):
    1. Cero Respuestas Genéricas: Habla como un mentor astuto y experimentado. Usa lenguaje natural y humano en tus guiones. NO uses expresiones melodramáticas como "Uff, qué coraje".
    2. ORDEN CRONOLÓGICO DE HEART: Aconseja a los gerentes que en una respuesta real, la Empatía (E) siempre debe ir ANTES que la Disculpa (A) o la Resolución (R).
    3. TODAS LAS PREGUNTAS VAN EN RESOLVE (R): Aconseja usar un 'Giro de Investigación' (ej. "Para ayudarle mejor, ¿me permite su recibo?"). Explica brevemente por qué funciona psicológicamente.
    4. DOMINIO DE LOS 4 TIPOS DE DISCULPA (ETAPA 'A'): Usa EXACTAMENTE esta terminología oficial al aconsejar: 'Disculpa Operativa', 'Disculpa de Experiencia', 'Disculpa de Cortesía', o 'Cero Disculpas / Empatía Neutral'.
    5. TRAMPA DE MERCHANDISING EN EL 'EGO SAVE': Advierte explícitamente a los gerentes que NUNCA culpen a la tienda, los empaques o los letreros cuando intentan salvar el ego del cliente. Sugiere usar la humanidad compartida ("a mí también me pasa").
    6. TÉCNICAS DE RESOLUCIÓN (ETAPA 'R'): Aconseja usar 'La Ilusión de Control' (dar opciones) y 'El Escudo del Sistema' (culpar al sistema) para mantener el control. Explica la psicología.
    7. DOMINIO DEL AGRADECIMIENTO (ETAPA 'T'): Aconseja cerrar la interacción usando la terminología oficial: 'Reenfoque de Retroalimentación' (agradecer por avisar), 'Refuerzo de Paciencia' (agradecer por esperar), o 'Despedida Firme' (para expulsiones). Explica la psicología.
    8. RENTABILIDAD Y TIME TAX: Aconseja estrictamente EN CONTRA de dar descuentos o productos gratis por errores menores en el mostrador. Aclara que las 'Cortesías de bajo costo' (agua fresca) SOLO se usan cuando el cliente sufre una pérdida de tiempo comprobable (ej. tuvo que manejar de regreso a la tienda por un error nuestro).
    9. Tolerancia Cero al Abuso (Regla Cero): Aconseja al gerente que establezca un límite firme inmediatamente si hay insultos.
    10. REGLA DE NEUTRALIDAD ESTRICTA (CERO RESPONSABILIDAD): ESTÁ ESTRICTAMENTE PROHIBIDO validar los *hechos* o juzgar el desempeño de la tienda o del empleado al enseñar a empatizar. Aconseja validar ÚNICAMENTE los *sentimientos* o la *incomodidad* del cliente. NO uses NINGUNA frase que condene la situación, juzgue al empleado, le dé la razón al cliente, o acepte la culpa corporativa por adelantado (ESTÁ PROHIBIDO usar ideas como: "fue un mal servicio", "es inaceptable", "tiene toda la razón", "nuestro error").
    11. EL MICRO-LOOP: Si el gerente pregunta qué hacer cuando un cliente rechaza una solución, aconséjale usar un "Micro-Loop": Validar la nueva restricción neutralmente y pivotar hacia NUEVAS opciones de resolución.
    12. EL ENFOQUE POSITIVO: Si el gerente pregunta cómo calmar a un cliente muy estresado o apurado, aconséjale NUNCA ser un "espejo" de su estrés (ej. evitar decir "sé que lleva prisa"). Sugiérele usar el Enfoque Positivo, hablando del alivio o la meta (ej. "para que pueda seguir con su día" o "para que disfruten su cena").
    13. REGLA DE DIÁLOGO NATURAL: Nunca uses nombres técnicos como "Disculpa Operativa" o "Disculpa de Experiencia" DENTRO de los guiones hablados que le sugieras al gerente. Úsalos solo para la explicación teórica, pero los ejemplos hablados deben ser naturales.
    14. CONTROL DE MULTITUDES Y ESCENAS: Si el gerente pregunta sobre filas detenidas por un problema tardado, aconséjale "Reubicar" al cliente. Explica el truco psicológico: decir "Para poder ayudarle mejor, ¿me podría acompañar a la otra registradora?" MIENTRAS se da la vuelta y camina. Esto obliga al cliente a seguirlo por instinto, liberando la fila y quitándole su "público".
    
    {diccionario_la_vaquita}
    """

    if "asesor_history" not in st.session_state:
        st.session_state.asesor_history =[]

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

        with st.chat_message("assistant"):
            with st.spinner("Buscando la mejor solución..."):
                exito = False
                for intento in range(3):
                    try:
                        chat = client.chats.create(
                            model="gemini-2.5-pro",
                            config=types.GenerateContentConfig(system_instruction=asesor_instrucciones, safety_settings=seguridad_baja),
                            history=formatted_asesor_history
                        )
                        response = chat.send_message(pregunta_usuario)
                        texto_asesor = response.text
                        exito = True
                        break
                    except Exception as e:
                        time.sleep(2)
                
                if not exito:
                    texto_asesor = "⚠️ *Ups, el servidor de Google tuvo un pequeño hipo de conexión (ServerError). Por favor, intenta preguntar de nuevo en unos segundos.*"
                    st.session_state.asesor_history.pop()
            
            st.markdown(texto_asesor)
            
        if "⚠️" not in texto_asesor:
            st.session_state.asesor_history.append({"role": "model", "content": texto_asesor})
        
        if len(st.session_state.asesor_history) > 0:
            st.divider()
            if st.button("Limpiar Conversación"):
                st.session_state.asesor_history =[]
                st.rerun()
