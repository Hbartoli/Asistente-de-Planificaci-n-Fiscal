import streamlit as st
import pandas as pd

# Configuración de página con enfoque profesional
st.set_page_config(
    page_title="Asistente de Planificación Fiscal ARCA - Actualizado Agosto 2026",
    page_icon="📈",
    layout="centered"
)

# Constantes Fiscales Actualizadas (Agosto 2026)
TOPE_MONOTRIBUTO_ANUAL = 108300000.00  # Límite Máximo Categoría K
CUOTA_AUTONOMOS_CAT1 = 74003.80       # Aporte mensual básico trabajadores independientes
CUOTA_AUTONOMOS_CAT2 = 103603.74      # Aporte mensual comerciantes

# Título e Introducción
st.title("📈 Asistente de Planificación Fiscal")
st.subheader("Transición interactiva de Monotributo a Responsable Inscripto sin morir en el intento")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 1. Diagnóstico de Exclusión", 
    "📊 2. Simulador Financiero", 
    "🛡️ 3. Beneficios Puente Fiscal", 
    "📋 4. Hoja de Ruta"
])

# -------------------------------------------------------------------------
# PESTAÑA 1: DIAGNÓSTICO
# -------------------------------------------------------------------------
with tab1:
    st.header("### 🔍 Diagnóstico de Situación Actual")
    st.write("Identificar con precisión la causa de tu salida del Régimen Simplificado previene exclusiones de oficio por parte de ARCA.")
    
    motivo = st.radio(
        "**Seleccioná el motivo principal de tu consulta:**",
        (
            "Mis ingresos acumulados últimos 12 meses están cerca o superaron los $108.3M.",
            "El precio unitario de venta de mis productos supera el límite legal de ARCA.",
            "Necesito expandir mi negocio (más de 3 locales/unidades de explotación o importar).",
            "Mis clientes corporativos me exigen Factura 'A' para computar crédito fiscal."
        )
    )
    
    if "ingresos acumulados" in motivo or "precio unitario" in motivo:
        st.warning("⚠️ **Alerta Crítica:** Te encontrás frente a causales de exclusión de pleno derecho. Planificar la transición inmediatamente evitará determinaciones de oficio, multas e intereses retroactivos por parte del fisco.")
    else:
        st.info("💡 **Transición Voluntaria:** Tu salida obedece a razones operativas o de crecimiento. Hacerlo por motu proprio te habilita a gozar de los beneficios máximos del 'Puente Fiscal' Ley 27.618.")

# -------------------------------------------------------------------------
# PESTAÑA 2: SIMULADOR FINANCIERO INTERACTIVO
# -------------------------------------------------------------------------
with tab2:
    st.header("### 📊 Simulador de Estructura Impositiva")
    st.write("Como Responsable Inscripto el impuesto se calcula mes a mes sobre el valor agregado y tus utilidades netas reales.")

    col_in_1, col_in_2 = st.columns(2)
    with col_in_1:
        ingresos_mensuales = st.number_input("Facturación mensual estimada (Neto sin IVA):", min_value=0, value=6500000, step=100000, format="%d")
        actividad = st.selectbox("Tipo de actividad principal:", ["Servicios / Freelancer", "Venta de Bienes / Comercio"])
    with col_in_2:
        gastos_mensuales = st.number_input("Gastos mensuales con Factura 'A' (Mercadería, insumos, servicios):", min_value=0, value=3000000, step=100000, format="%d")
        alicuota_iibb = st.slider("Alícuota estimada de Ingresos Brutos (%):", min_value=0.0, max_value=5.0, value=3.5, step=0.5)

    # Cálculos Impositivos Precisos
    iva_debito = ingresos_mensuales * 0.21
    iva_credito = gastos_mensuales * 0.21
    iva_neto = max(0.0, iva_debito - iva_credito)
    
    # Cálculo Autónomos según actividad
    cuota_autonomos = CUOTA_AUTONOMOS_CAT1 if actividad == "Servicios / Freelancer" else CUOTA_AUTONOMOS_CAT2
    
    # Cálculo Simplificado de Ingresos Brutos e Impuesto a las Ganancias
    iibb_estimado = ingresos_mensuales * (alicuota_iibb / 100)
    utilidad_neta_pre_ganancias = ingresos_mensuales - gastos_mensuales - cuota_autonomos - iibb_estimado
    
    # Simulación de escala progresiva de ganancias mensualizada
    if utilidad_neta_pre_ganancias > 0:
        ganancias_estimado = utilidad_neta_pre_ganancias * 0.25  # Tasa efectiva promedio ponderada simulada
    else:
        ganancias_estimado = 0.0
        utilidad_neta_pre_ganancias = 0.0

    ingreso_de_bolsillo = utilidad_neta_pre_ganancias - ganancias_estimado

    st.markdown("---")
    st.subheader("📋 Radiografía de Carga Fiscal Mensual")
    
    # Métricas clave organizadas en columnas
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="IVA Neto a Pagar", value=f"${iva_neto:,.2f}")
        st.metric(label="Ingresos Brutos", value=f"${iibb_estimado:,.2f}")
    with c2:
        st.metric(label="Autónomos (SIPA)", value=f"${cuota_autonomos:,.2f}")
        st.metric(label="Est. Ganancias", value=f"${ganancias_estimado:,.2f}")
    with c3:
        st.metric(label="Utilidad de Bolsillo", value=f"${ingreso_de_bolsillo:,.2f}", delta=f"{((ingreso_de_bolsillo/ingresos_mensuales)*100):.1f}% del total bruto")

    # Gráfico interactivo nativo
    st.subheader("💡 Distribución de tu Facturación Mensual")
    
    datos_grafico = pd.DataFrame({
        "Concepto": ["Gastos Operativos", "IVA Neto", "Ingresos Brutos", "Autónomos", "Imp. Ganancias", "Ganancia Neta (Tu plata)"],
        "Monto ($)": [gastos_mensuales, iva_neto, iibb_estimado, cuota_autonomos, ganancias_estimado, ingreso_de_bolsillo]
    })
    
    st.bar_chart(data=datos_grafico, x="Concepto", y="Monto ($)", color="#1F77B4")

    st.error("**⚠️ Regla de Oro Impositiva:** El IVA Débito no es parte de tus ingresos ni de tu rentabilidad. Es dinero de ARCA que recaudás temporalmente. Separalo en una cuenta bancaria distinta apenas cobres tus facturas.")

# -------------------------------------------------------------------------
# PESTAÑA 3: EL PUENTE FISCAL (Beneficios Ley 27.618)
# -------------------------------------------------------------------------
with tab3:
    st.header("### 🛡️ Beneficios del Régimen de Puente Fiscal")
    st.write("Si tu transición es planificada y ordenada, la normativa vigente mitiga el impacto financiero mediante créditos fiscales adicionales:")
    
    st.markdown("""
    - **Crédito Fiscal Presunto de IVA:** Podés computar el IVA contenido en las compras hechas a proveedores en los 12 meses anteriores al cambio, aunque fuesen Facturas 'B'.
    - **Deducción Especial de Transición:** Reducción de la base imponible del Impuesto a las Ganancias aplicable durante el primer ejercicio fiscal completo.
    - **Reducción Progresiva de IVA (Beneficio de Continuidad):** Descuento directo sobre el saldo técnico de IVA del **50% el primer año**, **30% el segundo año** y **10% el tercer año**.
    """)
    
    ingresos_anuales_est = ingresos_mensuales * 12
    st.write(f"Tu proyección de ingresos anuales estimados es de: **${ingresos_anuales_est:,.2f}**")
    
    if ingresos_anuales_est <= (TOPE_MONOTRIBUTO_ANUAL * 1.5):
        st.balloons()
        st.success("🎉 **Calificás para el Puente Fiscal:** Tus ingresos estimados se encuentran dentro del límite del beneficio (no exceden el 50% del tope del régimen simplificado). Vas a poder computar reducciones de IVA y créditos presuntos.")
    else:
        st.warning("⚠️ **Excedido de Parámetros:** Tus ingresos anuales estimados superan el límite extendido. Tu alta en el Régimen General será directa y sin reducciones de IVA escalonadas. Es crítico trabajar junto a un profesional contable.")

# -------------------------------------------------------------------------
# PESTAÑA 4: CHECKLIST Y HOJA DE RUTA
# -------------------------------------------------------------------------
with tab4:
    st.header("### 📋 Plan de Acción Estructurado")
    st.write("Seguí estos pasos cronológicos para formalizar tu traspaso sin contingencias impositivas:")

    st.checkbox("1. Vincular un Contador/a Matriculado al Administrador de Relaciones de ARCA para delegar las liquidaciones mensuales.")
    st.checkbox("2. Gestionar el alta formal en los impuestos de IVA (Régimen General) e Impuesto a las Ingresos Personales / Ganancias.")
    st.checkbox("3. Registrarse en el régimen previsional de Autónomos en la categoría mínima que corresponda a tu actividad.")
    st.checkbox("4. Dar de alta un nuevo punto de venta web específico para Facturación Electrónica tipo 'A' y 'B'.")
    st.checkbox("5. Informar el cambio de condición fiscal a todos tus proveedores recurrentes para exigir la emisión de Facturas 'A'.")
    st.checkbox("6. Actualizar tu estructura de costos y precios finales al público integrando el impacto del Impuesto al Valor Agregado.")
    st.checkbox("7. Readecuar la situación en Ingresos Brutos (Alta en Convenio Multilateral si comercializás bienes o servicios digitalmente fuera de tu provincia natal).")

    st.markdown("---")
    st.info("💡 **Perspectiva Empresarial:** Dejar atrás el Monotributo no es un castigo impositivo; es la confirmación de que tu modelo de negocios escaló y superó la etapa de microemprendimiento. Con orden financiero y previsión de flujo, representa el inicio de una estructura corporativa sólida.")
