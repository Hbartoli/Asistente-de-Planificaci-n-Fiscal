import streamlit as st
import pandas as pd
from fpdf import FPDF

# Configuración de página con enfoque profesional
st.set_page_config(
    page_title="Asistente de Planificación Fiscal ARCA",
    page_icon="📈",
    layout="centered"
)

# Constantes Fiscales Actualizadas
TOPE_MONOTRIBUTO_ANUAL = 108300000.00  # Límite Máximo Categoría K
CUOTA_AUTONOMOS_CAT1 = 74003.80       # Aporte mensual básico trabajadores independientes
CUOTA_AUTONOMOS_CAT2 = 103603.74      # Aporte mensual comerciantes

# Definición global de las tareas para que las lea tanto la interfaz como el PDF
LISTA_TAREAS_GLOBAL = [
    "1. Vincular un Contador/a Matriculado al Administrador de Relaciones de ARCA para delegar las liquidaciones mensuales.",
    "2. Gestionar el alta formal en los impuestos de IVA (Regimen General) e Impuesto a las Ganancias.",
    "3. Registrarse en el regimen previsional de Autonomos en la categoria minima que corresponda a tu actividad.",
    "4. Dar de alta un nuevo punto de venta web especifico para Facturacion Electronica tipo 'A' y 'B'.",
    "5. Informar el cambio de condicion fiscal a todos tus proveedores recurrentes para exigir la emision de Facturas 'A'.",
    "6. Actualizar tu estructura de costos y precios finales al publico integrando el impacto del Impuesto al Valor Agregado.",
    "7. Readecuar la situacion en Ingresos Brutos (Alta en Convenio Multilateral si comercializas bienes o servicios fuera de tu provincia)."
]

 # Tabla de Datos Fiscales con márgenes corregidos y tabulación limpia hacia la derecha
    for k, v in datos_fiscales.items():
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(90, 8, f"{k}:", border=0) # Ampliamos a 90mm para que la etiqueta tenga espacio
        
        # Forzamos la posición del valor numérico bien hacia la derecha (columna fija a los 100mm)
        pdf.set_x(105) 
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, f"{v}", border=0, ln=True)
    
    # Título Principal
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(31, 119, 180) # Azul corporativo
    pdf.cell(0, 10, "Reporte de Planificacion Fiscal", ln=True, align="C")
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Transicion de Monotributo a Responsable Inscripto", ln=True, align="C")
    pdf.ln(10)
    
    # Sección 1: Radiografía Fiscal
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "1. Radiografia Fiscal Mensual Estimada", ln=True)
    pdf.set_font("Helvetica", "", 11)
    
    # Tabla de Datos Fiscales
    for k, v in datos_fiscales.items():
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(60, 8, f"{k}:", border=0)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, f" {v}", border=0, ln=True)
        
    pdf.ln(10)
    
    # Sección 2: Hoja de Ruta
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "2. Hoja de Ruta / Plan de Accion", ln=True)
    pdf.set_font("Helvetica", "", 10)
    
    for tarea in checklist_tareas:
        # Reemplazar caracteres con tildes para evitar errores de codificación
        tarea_limpia = tarea.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n").replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
        pdf.multi_cell(0, 6, f"[ ] {tarea_limpia}")
        pdf.ln(2)
        
    # Pie de página o nota final
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(0, 5, "Nota: Este reporte es una simulacion pedagogica basada en los parametros fiscales vigentes. No reemplaza la consulta vinculante con un Contador Publico matriculado.")
    
    return bytes(pdf.output())

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
    st.header("🔍 Diagnóstico de Situación Actual")
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
    st.header("📊 Simulador de Estructura Impositiva")
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
    
    if utilidad_neta_pre_ganancias > 0:
        ganancias_estimado = utilidad_neta_pre_ganancias * 0.25  
    else:
        ganancias_estimado = 0.0
        utilidad_neta_pre_ganancias = 0.0

    ingreso_de_bolsillo = utilidad_neta_pre_ganancias - ganancias_estimado

    # Guardar en diccionario para usar en el PDF de manera limpia
    datos_reporte = {
        "Facturacion Mensual (Neto)": f"${ingresos_mensuales:,.2f}",
        "Gastos Declarados (Factura A)": f"${gastos_mensuales:,.2f}",
        "IVA Neto a Pagar Mensual": f"${iva_neto:,.2f}",
        "Impuesto Ingresos Brutos": f"${iibb_estimado:,.2f}",
        "Aporte Autonomos": f"${cuota_autonomos:,.2f}",
        "Estimado Impuesto a las Ganancias": f"${ganancias_estimado:,.2f}",
        "Utilidad de Bolsillo Efectiva": f"${ingreso_de_bolsillo:,.2f}"
    }

    st.markdown("---")
    st.subheader("📋 Radiografía de Carga Fiscal Mensual")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="IVA Neto a Pagar", value=f"${iva_neto:,.2f}")
        st.metric(label="Ingresos Brutos", value=f"${iibb_estimado:,.2f}")
    with c2:
        st.metric(label="Autónomos (SIPA)", value=f"${cuota_autonomos:,.2f}")
        st.metric(label="Est. Ganancias", value=f"${ganancias_estimado:,.2f}")
    with c3:
        st.metric(label="Utilidad de Bolsillo", value=f"${ingreso_de_bolsillo:,.2f}", delta=f"{((ingreso_de_bolsillo/ingresos_mensuales)*100):.1f}% del total")

    st.subheader("💡 Distribución de tu Facturación Mensual")
    datos_grafico = pd.DataFrame({
        "Concepto": ["Gastos Operativos", "IVA Neto", "Ingresos Brutos", "Autónomos", "Imp. Ganancias", "Ganancia Neta"],
        "Monto ($)": [gastos_mensuales, iva_neto, iibb_estimado, cuota_autonomos, ganancias_estimado, ingreso_de_bolsillo]
    })
    st.bar_chart(data=datos_grafico, x="Concepto", y="Monto ($)", color="#1F77B4")

# -------------------------------------------------------------------------
# PESTAÑA 3: EL PUENTE FISCAL (Beneficios Ley 27.618)
# -------------------------------------------------------------------------
with tab3:
    st.header("🛡️ Beneficios del Régimen de Puente Fiscal")
    st.write("Si tu transición es planificada y ordenada, la normativa vigente mitiga el impacto financiero mediante créditos fiscales adicionales:")
    
    st.markdown("""
    - **Crédito Fiscal Presunto de IVA:** Podés computar el IVA contenido en las compras hechas a proveedores en los 12 meses anteriores al cambio.
    - **Deducción Especial de Transición:** Reducción de la base imponible del Impuesto a las Ganancias.
    - **Reducción Progresiva de IVA:** Descuento directo sobre el saldo técnico de IVA del **50% el primer año**, **30% el segundo año** y **10% el tercer año**.
    """)
    
    ingresos_anuales_est = ingresos_mensuales * 12
    st.write(f"Tu proyección de ingresos anuales estimados es de: **${ingresos_anuales_est:,.2f}**")
    
    if ingresos_anuales_est <= (TOPE_MONOTRIBUTO_ANUAL * 1.5):
        st.success("🎉 Calificás para el Puente Fiscal: Tus ingresos estimados se encuentran dentro del límite del beneficio.")
    else:
        st.warning("⚠️ Excedido de Parámetros: Tus ingresos anuales estimados superan el límite extendido. Tu alta será directa.")

# -------------------------------------------------------------------------
# PESTAÑA 4: CHECKLIST Y HOJA DE RUTA + EXPORTACIÓN
# -------------------------------------------------------------------------    
with tab4:
    st.header("📋 Plan de Acción Estructurado")
    st.write("Seguí estos pasos cronológicos para formalizar tu traspaso sin contingencias impositivas:")
    
    # Renderizado manual de la lista visual en la app
    st.checkbox("1. Vincular un Contador/a Matriculado al Administrador de Relaciones de ARCA para delegar las liquidaciones mensuales.")
    st.checkbox("2. Gestionar el alta formal en los impuestos de IVA (Régimen General) e Impuesto a las Ganancias.")
    st.checkbox("3. Registrarse en el régimen previsional de Autónomos en la categoría mínima que corresponda a tu actividad.")
    st.checkbox("4. Dar de alta un nuevo punto de venta web específico para Facturación Electrónica tipo 'A' y 'B'.")
    st.checkbox("5. Informar el cambio de condición fiscal a todos tus proveedores recurrentes para exigir la emisión de Facturas 'A'.")
    st.checkbox("6. Actualizar tu estructura de costos y precios finales al público integrando el impacto del Impuesto al Valor Agregado.")
    st.checkbox("7. Readecuar la situación en Ingresos Brutos (Alta en Convenio Multilateral si comercializás bienes o servicios fuera de tu provincia).")

    st.markdown("---")
    st.subheader("💾 Descargar Reporte Completo")
    st.write("Hacé clic en el botón de abajo para generar tu documento PDF personalizado con la radiografía financiera y tu plan de acción estructurado.")
    
    # LLAMADA CORRECTA: Usa 'datos_reporte' y 'LISTA_TAREAS_GLOBAL'
    pdf_bytes = generar_pdf(datos_reporte, LISTA_TAREAS_GLOBAL)
         
    st.download_button(
        label="📥 Descargar Radiografía y Hoja de Ruta en PDF",
        data=pdf_bytes,
        file_name="Planificacion_Fiscal_RI.pdf",
        mime="application/pdf"
    )
