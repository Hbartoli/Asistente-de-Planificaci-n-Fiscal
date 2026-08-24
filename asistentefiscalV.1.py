import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Asistente de Planificación Fiscal",
    page_icon="📊",
    layout="centered"
)

# Título principal y bienvenida
st.title("📊 Asistente de Planificación Fiscal")
st.subheader("Guía interactiva: Pasar de Monotributo a Responsable Inscripto sin morir en el intento")
st.write("El salto al Régimen General da miedo, pero con números claros es solo un paso más para hacer crecer tu negocio. ¡Vamos a analizar tu situación!")

# Estructura de pestañas para guiar al usuario paso a paso
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 1. ¿Por qué el cambio?", 
    "📈 2. Simulador de Impacto", 
    "🛡️ 3. Alivio Fiscal (Puente)", 
    "📋 4. Plan de Acción"
])

# -------------------------------------------------------------------------
# PESTAÑA 1: DIAGNÓSTICO
# -------------------------------------------------------------------------
with tab1:
    st.header("¿Por qué te vas del Monotributo?")
    st.write("Identificar la causa te ayuda a saber si es una transición obligatoria o voluntaria.")
    
    motivo = st.radio(
        "Seleccioná tu situación actual:",
        (
            "Excedí la facturación máxima de la última categoría.",
            "El precio unitario de mis productos supera el límite permitido.",
            "Quiero importar, tener más de 3 unidades de explotación o crecer sin tope.",
            "Mis clientes me piden factura 'A' para computar IVA."
        )
    )
    
    if "Excedí" in motivo or "precio unitario" in motivo:
        st.warning("⚠️ **Alerta:** Estás ante una exclusión de pleno derecho. Es clave que hagas la transición antes de que AFIP te excluya de oficio para evitar multas y recargos retroactivos.")
    else:
        st.info("💡 **Buen camino:** Es una transición voluntaria. Hacerlo de forma planificada te permite aprovechar al máximo los beneficios del 'Puente Fiscal'.")

# -------------------------------------------------------------------------
# PESTAÑA 2: SIMULADOR NUMÉRICO SIMPLE
# -------------------------------------------------------------------------
with tab2:
    st.header("Simulador de Impacto Fiscal")
    st.write("En el Monotributo pagás una cuota fija. Como Responsable Inscripto, tu realidad cambia. Ingresá tus números estimados mensuales:")

    # Inputs del usuario
    ingresos = st.number_input("Ingresos mensuales estimados (sin IVA):", min_value=0, value=500000, step=50000)
    gastos_blancos = st.number_input("Gastos mensuales facturados con Factura A (compras, alquiler, servicios):", min_value=0, value=200000, step=20000)
    
    # Cálculos express (Metodología simplificada para concientizar)
    iva_debito = ingresos * 0.21
    iva_credito = gastos_blancos * 0.21
    iva_a_pagar = max(0.0, iva_debito - iva_credito)
    
    ganancia_neta_estimada = ingresos - gastos_blancos
    
    st.markdown("---")
    st.subheader("📊 Radiografía de tu nueva estructura:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="IVA Débito (Lo que cobrás)", value=f"${iva_debito:,.2f}")
        st.metric(label="IVA Crédito (Lo que recuperás)", value=f"${iva_credito:,.2f}")
    with col2:
        st.metric(label="Estimado de IVA mensual a pagar", value=f"${iva_a_pagar:,.2f}", delta=f"${iva_a_pagar:,.2f}", delta_color="inverse")
        st.metric(label="Base para Ganancias (Mensual)", value=f"${ganancia_neta_estimada:,.2f}")

    st.subheader("💡 La regla de oro del Responsable Inscripto:")
    st.error("**El IVA no es tu plata.** Cuando factures, sumale el 21% a tus precios. Guardá ese dinero en una cuenta separada; solo sos un intermediario que se lo recauda a la AFIP.")
    st.success("**Pedí siempre Factura A:** Cada gasto en blanco que tenga que ver con tu actividad reduce directamente el IVA y el Impuesto a las Ganancias que vas a pagar.")

# -------------------------------------------------------------------------
# PESTAÑA 3: EL PUENTE FISCAL (Beneficios de la Ley 27.618)
# -------------------------------------------------------------------------
with tab3:
    st.header("🛡️ Tu salvavidas: El Puente Fiscal")
    st.write("Si pasás a Responsable Inscripto de forma voluntaria (o si tus ingresos no se excedieron en más de un 50% del tope del Monotributo), la ley te da un beneficio enorme para que el golpe no sea duro:")
    
    st.markdown("""
    *   **Crédito Fiscal Presunto:** Podés computar como IVA crédito las facturas de compras de bienes e insumos que te hicieron cuando eras monotributista (Facturas B).
    *   **Deducción Especial en Ganancias:** Un beneficio equivalente en el impuesto a las ganancias para amortiguar el primer año.
    *   **Reducción del saldo de IVA:** Descuentos decrecientes en el IVA a pagar durante los primeros 3 años (50%, 30% y 10% de reducción).
    """)
    
    cumple_puente = st.checkbox("Mis ingresos anuales NO superan en más del 50% el límite máximo del Monotributo.")
    if cumple_puente:
        st.balloons()
        st.success("🎉 ¡Excelente! Podés aplicar a los beneficios de la transición pacífica. Esto reduce drásticamente tus primeros pagos de impuestos.")
    else:
        st.warning("📋 Si te excediste por mucho, la transición será directa y sin estos créditos presuntos. Revisá urgente las fechas de exclusión con tu contador.")

# -------------------------------------------------------------------------
# PESTAÑA 4: CHECKLIST Y PLAN DE ACCIÓN
# -------------------------------------------------------------------------
with tab4:
    st.header("📋 Tu hoja de ruta para no morir en el intento")
    st.write("Marcá las tareas que vas completando para organizar tu mudanza fiscal:")

    st.checkbox("1. Contratar un contador/a de confianza (El Régimen General requiere liquidaciones mensuales obligatorias).")
    st.checkbox("2. Dar de alta los nuevos impuestos en AFIP (IVA y Ganancias).")
    st.checkbox("3. Modificar el punto de venta para empezar a emitir Facturas A y B.")
    st.checkbox("4. Notificar a tus proveedores para que te emitan Facturas A (y dejen de hacerte Factura B).")
    st.checkbox("5. Recalcular la lista de precios sumando el impacto del IVA.")
    st.checkbox("6. Dar de alta el régimen correspondiente de Ingresos Brutos (Convenio Multilateral si vendés a otras provincias).")
    st.checkbox("7. Configurar una cuenta bancaria o billetera digital exclusiva para separar el IVA de tus ganancias reales.")

    st.markdown("---")
    st.info("📌 **Reflexión final:** Ser Responsable Inscripto no es un castigo, es el síntoma de que tu negocio está facturando a gran escala. Con orden, previsión y un buen contador, es el inicio de una estructura empresarial real.")
