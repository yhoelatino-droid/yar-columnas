import streamlit as st
import math

# 1. CONFIGURACIÓN DE TU SEGUNDA APP (Logo de grúa torre unificado para tu marca)
st.set_page_config(
    page_title="YAR Columnas", 
    page_icon="https://githubusercontent.com", 
    layout="centered"
)

# Título de tu segunda marca de ingeniería
st.title("🧱 YAR Structural - Columnas")
st.write("Predimensionamiento normativo basado en el RNE E.030 y criterios sismorresistentes.")
st.write("---")

st.subheader("Esquema Geométrico de Columna (3D)")

# Ilustración isométrica 3D nativa de una columna de concreto armado (Peralte cambiado por Fondo)
columna_3d_svg = """
<svg xmlns="http://w3.org" viewBox="0 0 600 350" width="100%">
  <rect width="600" height="350" fill="#11151c" rx="10"/>
  <polygon points="200,80 200,280 280,310 280,110" fill="#4a5568" opacity="0.85" stroke="#cbd5e1" stroke-width="2"/>
  <polygon points="280,110 280,310 380,260 380,60" fill="#2d3748" opacity="0.85" stroke="#cbd5e1" stroke-width="2"/>
  <polygon points="200,80 280,110 380,60 300,30" fill="#718096" stroke="#cbd5e1" stroke-width="1.5"/>
  <line x1="215" y1="85" x2="215" y2="285" stroke="#e11d48" stroke-width="4" stroke-linecap="round"/>
  <line x1="280" y1="110" x2="280" y2="310" stroke="#e11d48" stroke-width="4" stroke-linecap="round"/>
  <line x1="365" y1="68" x2="365" y2="268" stroke="#e11d48" stroke-width="4" stroke-linecap="round"/>
  <line x1="295" y1="42" x2="295" y2="242" stroke="#e11d48" stroke-width="3" stroke-dasharray="2,2" opacity="0.6"/>
  <polygon points="215,115 280,140 365,98 295,72" fill="none" stroke="#38bdf8" stroke-width="2"/>
  <polygon points="215,165 280,190 365,148 295,122" fill="none" stroke="#38bdf8" stroke-width="2"/>
  <polygon points="215,215 280,240 365,198 295,172" fill="none" stroke="#38bdf8" stroke-width="2"/>
  <polygon points="215,265 280,290 365,248 295,222" fill="none" stroke="#38bdf8" stroke-width="2"/>
  <line x1="190" y1="285" x2="270" y2="315" stroke="#f8fafc" stroke-width="1.5"/>
  <line x1="190" y1="280" x2="190" y2="290" stroke="#f8fafc" stroke-width="1.5"/>
  <line x1="270" y1="310" x2="270" y2="320" stroke="#f8fafc" stroke-width="1.5"/>
  <text x="225" y="315" fill="#f8fafc" font-family="Arial" font-size="14" font-weight="bold" transform="rotate(20, 225, 315)">Ancho (b)</text>
  <line x1="290" y1="315" x2="390" y2="265" stroke="#f8fafc" stroke-width="1.5"/>
  <line x1="290" y1="310" x2="290" y2="320" stroke="#f8fafc" stroke-width="1.5"/>
  <line x1="390" y1="260" x2="390" y2="270" stroke="#f8fafc" stroke-width="1.5"/>
  <text x="345" y="300" fill="#f8fafc" font-family="Arial" font-size="14" font-weight="bold" transform="rotate(-26, 345, 300)">Fondo (t)</text>
</svg>
"""

st.markdown(columna_3d_svg, unsafe_allow_html=True)
st.write("---")

st.subheader("Datos de Entrada")

num_pisos = st.number_input("Número de Pisos de la edificación", min_value=1, max_value=20, value=3, step=1)
area_trib = st.number_input("Área Tributaria de la columna (m²)", min_value=1.0, max_value=100.0, value=16.0, step=0.5)
fc = st.number_input("Resistencia del concreto f'c (kg/cm²)", min_value=140, max_value=420, value=210, step=70)

categoria = st.selectbox(
    "Categoría de la Edificación (Norma E.030):",
    ("Categoría C: Comunes (Viviendas, Hoteles, Oficinas) - 1000 kg/m²", 
     "Categoría B: Importantes (Centros Comerciales, Teatros) - 1250 kg/m²", 
     "Categoría A: Esenciales (Hospitales, Universidades, Colegios) - 1500 kg/m²")
)

col1, col2 = st.columns(2)
with col1:
    tipo_columna = st.radio("Ubicación en Planta:", ("Central", "Excéntrica / Esquinera"))
with col2:
    forma_columna = st.radio("Forma Geométrica:", ("Cuadrada", "Circular"))

if st.button("Calcular Sección de Columna ▶️", use_container_width=True):
    if "Categoría A" in categoria:
        peso_por_m2 = 1500
        cat_letra = "A (Esenciales)"
    elif "Categoría B" in categoria:
        peso_por_m2 = 1250
        cat_letra = "B (Importantes)"
    else:
        peso_por_m2 = 1000
        cat_letra = "C (Comunes)"
        
    P_servicio = area_trib * num_pisos * peso_por_m2
    factor_aci = 0.45 if tipo_columna == "Central" else 0.35
    area_concreto_cm2 = P_servicio / (factor_aci * fc)
    
    st.success("### 📊 MEMORIA DE RENDIMIENTO NORMATIVA")
    st.write(f"Peso asignado por norma: **{peso_por_m2} kg/m² por nivel**")
    st.write(f"Carga de Servicio Total ($P$): **{P_servicio:,.0f} kg**")
    st.write(f"Área Neta de Concreto Requerida ($A_c$): **{area_concreto_cm2:.2f} cm²**")
    
    if forma_columna == "Cuadrada":
        lado_exacto = math.sqrt(area_concreto_cm2)
        lado_final = math.ceil(lado_exacto / 5) * 5
        if lado_final < 25:
            lado_final = 25
        st.metric(label="🧱 Lado Mínimo Recomendado (b × t)", value=f"{lado_final} cm × {lado_final} cm")
        detalle_dimension = f"{lado_final} cm x {lado_final} cm (Sección Cuadrada)"
    else:
        diametro_exacto = math.sqrt((4 * area_concreto_cm2) / math.pi)
        diametro_final = math.ceil(diametro_exacto / 5) * 5
        if diametro_final < 25:
            diametro_final = 25
        st.metric(label="⭕ Diámetro Mínimo Recomendado (Ø)", value=f"{diametro_final} cm")
        detalle_dimension = f"Ø {diametro_final} cm (Sección Circular)"

    st.write("---")
    st.subheader("📄 Reporte y Exportación")
    
    html_reporte = f"""
    <div style="padding:20px; border:2px solid #333; font-family:Arial, sans-serif; background-color:white; color:black; border-radius:8px;">
        <h2 style="text-align:center; color:#1e3a8a; margin-bottom:5px;">MEMORIA DE CÁLCULO ESTRUCTURAL</h2>
        <p style="text-align:center; font-weight:bold; margin-top:0;">SOFTWARE: YAR STRUCTURAL</p>
        <hr style="border:1px solid #333;">
        
        <table style="width:100%; font-size:14px; margin-bottom:20px;">
            <tr><td><strong>Consultor estructural:</strong></td><td>Ing. Yhoel Aquino Reyes</td></tr>
            <tr><td><strong>Elemento:</strong></td><td>Columna de Concreto Armado</td></tr>
            <tr><td><strong>Ubicación de columna:</strong></td><td>Columna {tipo_columna}</td></tr>
        </table>
        
        <h4 style="color:#1e3a8a; border-bottom:1px solid #ccc; padding-bottom:5px;">1. PARÁMETROS DE DISEÑO (ENTRADA)</h4>
        <ul style="font-size:14px; line-height:1.6;">
            <li><strong>Número de pisos:</strong> {num_pisos} niveles</li>
            <li><strong>Área Tributaria (A_trib):</strong> {area_trib} m²</li>
            <li><strong>Resistencia del Concreto (f'c):</strong> {fc} kg/cm²</li>
            <li><strong>Categoría de Edificación (Norma E.030):</strong> Categoría {cat_letra}</li>
            <li><strong>Carga métrica asignada por norma:</strong> {peso_por_m2} kg/m² por nivel</li>
        </ul>
        
        <h4 style="color:#1e3a8a; border-bottom:1px solid #ccc; padding-bottom:5px;">2. PROCEDIMIENTO DETALLADO DE CÁLCULO</h4>
        <p style="font-size:14px; line-height:1.5;">
            <strong>Paso 2.1: Estimación de la Carga de Servicio Total (P)</strong><br>
            P = A_trib &times; N° Pisos &times; Peso_Normativo<br>
            P = {area_trib} m² &times; {num_pisos} &times; {peso_por_m2} kg/m² = <strong>{P_servicio:,.0f} kg</strong>
        </p>
        <p style="font-size:14px; line-height:1.5;">
            <strong>Paso 2.2: Área de Concreto Mínima Requerida (Ac)</strong><br>
            Ac = P / (&lambda; &times; f'c)<br>
            Ac = {P_servicio:,.0f} / ({factor_aci} &times; {fc}) = <strong>{area_concreto_cm2:.2f} cm²</strong>
        </p>
        
        <h4 style="color:#1e3a8a; border-bottom:1px solid #ccc; padding-bottom:5px;">3. CONCLUSIÓN Y DIMENSIONAMIENTO CONSTRUCTIVO</h4>
        <div style="background-color:#f3f4f6; padding:15px; border-radius:5px; font-size:15px; font-weight:bold; border-left:5px solid #1e3a8a;">
            Sección Final Sugerida Mínima (Redondeo comercial a 5cm): {detalle_dimension}
        </div>
        <p style="font-size:11px; color:#555; text-align:center; margin-top:30px;">
            Memoria técnica generada automáticamente por YAR Structural. Formato oficial conforme al RNE Perú.
        </p>
        <script>
            window.onload = function() {{ window.print(); }}
        </script>
    </div>
    """
    
    st.components.v1.html(html_reporte, height=480, scrolling=True)
    
    # Botón de descarga nativo de Streamlit
    st.download_button(
        label="📥 Descargar Memoria de Cálculo Oficial",
        data=html_reporte,
        file_name=f"Memoria_Columna_{tipo_columna}.html",
        mime="text/html",
        use_container_width=True
    )


