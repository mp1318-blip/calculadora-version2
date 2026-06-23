import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import symbols, sympify, limit, diff, integrate, latex
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
#pagina inicio 
st.set_page_config(page_title="Calculadora Matemática Completa", layout="wide")
st.sidebar.title(" Menú Principal")
menu = st.sidebar.radio(
    "Seleccione una opción",
    ["Inicio", "Límites", "Integrales", "Geometría Analítica"]
)
#wea de x importante no toques
x = symbols("x")

# wea del pdf
def generar_pdf(titulo, funcion, procedimiento, resultado, imagen="grafico.png"):
    pdf = "resultado.pdf"
    doc = SimpleDocTemplate(pdf)
    estilos = getSampleStyleSheet()
    contenido = []
    contenido.append(Paragraph(titulo, estilos["Title"]))
    contenido.append(Paragraph(f"Función: {funcion}", estilos["BodyText"]))
    contenido.append(Paragraph("Procedimiento", estilos["Heading2"]))
    contenido.append(Paragraph(procedimiento, estilos["BodyText"]))
    contenido.append(Paragraph(f"Resultado: {resultado}", estilos["BodyText"]))
    contenido.append(Spacer(1, 12))
    try:
        contenido.append(Image(imagen, width=350, height=250))
    except:
        pass
    doc.build(contenido)
    return pdf

# wea del menu de inicio
if menu == "Inicio":
    st.title(" Calculadora Matemática Completa")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://miprofe.com/evaluacion-de-limites.png")
        st.caption("LÍMITES")
    with col2:
        st.image(r"C:\Users\mp1318\Desktop\weas de c++\unidad 5\inte.png", width=400)
        st.caption("INTEGRALES") 
    with col3:
        st.image(r"C:\Users\mp1318\Desktop\weas de c++\unidad 5\geo.png", width=700)
        st.caption("GEOMETRÍA ANALÍTICA")

# menu de limites 
elif menu == "Límites":
    st.title("Límites y Regla de L'Hôpital")
    
    metodo = st.selectbox(
        "Seleccione el caso",
        ["Límite Directo", "L'Hôpital 0/0", "L'Hôpital ∞/∞"]
    )
    #entrada de los limites
    expr = st.text_input("Función", "sin(x)/x")
    if expr.strip() == "":
        st.warning("Ingrese una función")
        st.stop()
    
    punto_txt = st.text_input("Punto", "0")
    if punto_txt.strip() == "":
        st.warning("Ingrese un punto")
        st.stop()
#wea de slider
    zoom = st.slider("Zoom del gráfico", min_value=1, max_value=20, value=5)
#parte del ejercicio 
    if st.button("Resolver límite"):
        try:
            f = sympify(expr)
            punto = sympify(punto_txt)            
            st.subheader("Procedimiento")
            resultado = limit(f, x, punto)
            
            if metodo == "Límite Directo":
                st.subheader("Evaluación Directa")
                st.latex(latex(resultado))
            
            else:  # L'Hôpital
                num, den = f.as_numer_denom()
                st.subheader("Expresión Original")
                st.latex(r"\frac{" + latex(num) + "}{" + latex(den) + "}")
                
                st.subheader("Evaluación en el punto")
                valor_num = num.subs(x, punto)
                valor_den = den.subs(x, punto)
                st.latex(r"\frac{" + latex(valor_num) + "}{" + latex(valor_den) + "}")
                st.subheader("Aplicando Regla de L'Hôpital")
#wea del infinito
                es_00 = (valor_num == 0 and valor_den == 0)
                es_inf_inf = (valor_num in [sp.oo, -sp.oo] and valor_den in [sp.oo, -sp.oo])
                if not (es_00 or es_inf_inf):
                    st.warning("No hay indeterminación 0/0 o ∞/∞")
                else:
                    if es_00:
                        st.success("Indeterminación 0/0 detectada")
                    else:
                        st.success("Indeterminación ∞/∞ detectada")
#veces que deriba
                    for i in range(1, 6):
                        num = diff(num, x)
                        den = diff(den, x)
                        st.write(f"Paso {i}:")
                        st.latex(r"\frac{" + latex(num) + "}{" + latex(den) + "}")       
                        res_temp = limit(num/den, x, punto)
                        if res_temp not in [sp.nan, sp.zoo]:
                            resultado = res_temp
                            break
            
            st.subheader("Resultado Final")
            st.success(f"Resultado = {resultado}")
            st.latex(latex(resultado))
# Gráfico
            try:
                f_num = sp.lambdify(x, f, "numpy")
                xs = np.linspace(float(punto) - zoom, float(punto) + zoom, 1000)
                ys = f_num(xs)
                fig, ax = plt.subplots()
                ax.plot(xs, ys)
                ax.axvline(float(punto), linestyle="--", color='red')
                ax.grid(True)
                ax.set_title("Gráfico del Límite")
                st.pyplot(fig)
                fig.savefig("grafico.png")
            except:
                pass
#parte del pdf
            procedimiento = f"Función: {expr}\nPunto: {punto}\nMétodo: {metodo}"
            pdf = generar_pdf("Límite", expr, procedimiento, resultado)
            with open(pdf, "rb") as archivo:
                st.download_button(
                    "Descargar PDF",
                    archivo,
                    file_name="limite.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Error: {str(e)}")

# integrales menu
elif menu == "Integrales":
    st.title("Integrales con Gráfico y Métodos")
    metodo = st.selectbox("Selecciona el método de integración", 
                         ["Integración Directa", "Por Sustitución"])

    expr = st.text_input("Función a integrar", 
                        "x**2" if metodo == "Integración Directa" else "x * sin(x**2)",
                        help="Ej: x**2, sin(x), x*exp(x), x*sin(x**2)")
    if expr.strip() == "":
        st.warning("Ingresa una función")
        st.stop()
    try:
        f = sympify(expr)
    except Exception as e:
        st.error(f"Expresión inválida: {e}")
        st.stop()
    if metodo == "Por Sustitución":
        st.subheader("Integración por Sustitución")
        u_expr = st.text_input("Sustitución (u = ...)", "x**2",
                              help="Ejemplos: x**2, sin(x), 2*x+3")
        if u_expr.strip() == "":
            st.warning("Define la sustitución u")
            st.stop()
        try:
            u_expr_sym = sympify(u_expr)
            du = sp.diff(u_expr_sym, x)
        except Exception as e:
            st.error(f"Sustitución inválida: {e}")
            st.stop()
        u = symbols('u')
        if st.button("Realizar Integración por Sustitución", type="primary"):
            try:
                st.subheader("Procedimiento Paso a Paso")
                st.markdown("**Paso 1:** Integral original")
                st.latex(r"\int " + latex(f) + r"\ dx")
                st.markdown("**Paso 2:** Sustitución")
                col1, col2 = st.columns(2)
                with col1:
                    st.latex(r"u = " + latex(u_expr_sym))
                with col2:
                    st.latex(r"du = " + latex(du) + r"\ dx")
                
                st.markdown("**Paso 3:** Expresión en términos de u")
                try:
                    integrando_u = sp.simplify(f / du)
                    st.latex(r"\int " + latex(integrando_u) + r"\ du")
                except:
                    integrando_u = f / du
                    st.latex(r"\int ... \ du")
                
                st.markdown("**Paso 4:** Integramos respecto a u")
                try:
                    integral_u = integrate(integrando_u, u)
                    st.latex(latex(integral_u) + " + C")
                except:
                    st.warning("No se pudo integrar automáticamente respecto a u")
                    st.latex("... + C")
                st.markdown("**Paso 5:** Regresar a x")
                resultado = integrate(f, x)
                st.latex(latex(resultado) + r" + C") 
                st.subheader("Resultado Final")
                st.success(f"Integral = {resultado} + C")
                # Gráfico
                try:
                    f_num = sp.lambdify(x, f, "numpy")
                    xs = np.linspace(-5, 5, 500)
                    ys = f_num(xs)
                    fig, ax = plt.subplots()
                    ax.plot(xs, ys, label=f"${latex(f)}$")
                    ax.fill_between(xs, ys, alpha=0.3)
                    ax.grid(True)
                    ax.set_title("Gráfica de la función")
                    ax.legend()
                    st.pyplot(fig)
                    fig.savefig("grafico.png")
                except:
                    pass
                # PDF
                procedimiento = f"Función: {expr}\nSustitución: u = {u_expr}\nResultado: {resultado} + C"
                pdf = generar_pdf("Integral por Sustitución", expr, procedimiento, resultado)
                with open(pdf, "rb") as archivo:
                    st.download_button("Descargar PDF", archivo, file_name="integral_sustitucion.pdf")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    else:  # Directa
        if st.button("Integrar Directamente", type="primary"):
            try:
                resultado = integrate(f, x)
                st.subheader("Resultado")
                st.latex(latex(resultado) + r" + C")
                f_num = sp.lambdify(x, f, "numpy")
                xs = np.linspace(-5, 5, 500)
                ys = f_num(xs)
                fig, ax = plt.subplots()
                ax.plot(xs, ys)
                ax.fill_between(xs, ys, alpha=0.3)
                ax.grid(True)
                st.pyplot(fig)
                fig.savefig("grafico.png")
                pdf = generar_pdf("Integral Directa", expr, f"∫ {expr} dx = {resultado}", resultado)
                with open(pdf, "rb") as archivo:
                    st.download_button("Descargar PDF", archivo, file_name="integral_directa.pdf")
            except Exception as e:
                st.error(str(e))

#geometria analitica
elif menu == "Geometría Analítica":
    st.title("Geometría Analítica")

    tema = st.selectbox(
        "Tema",
        ["Distancia entre dos puntos", "Punto Medio", "Pendiente", 
         "Recta Punto-Pendiente", "Circunferencia", "Parábola", 
         "Elipse", "Hipérbola"]
    )

    if tema == "Distancia entre dos puntos":
        x1 = st.number_input("x1", value=0.0)
        y1 = st.number_input("y1", value=0.0)
        x2 = st.number_input("x2", value=3.0)
        y2 = st.number_input("y2", value=4.0)
        if st.button("Calcular"):
            d = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            st.success(f"Distancia = {d:.4f}")
            
            fig, ax = plt.subplots()
            ax.scatter([x1, x2], [y1, y2])
            ax.plot([x1, x2], [y1, y2])
            ax.grid(True)
            st.pyplot(fig)
            fig.savefig("grafico.png")
            
            # PDF
            procedimiento = f"Distancia entre P1({x1}, {y1}) y P2({x2}, {y2})"
            pdf = generar_pdf("Distancia entre dos puntos", f"P1({x1},{y1}) - P2({x2},{y2})", procedimiento, f"{d:.4f}")
            with open(pdf, "rb") as archivo:
                st.download_button("Descargar PDF", archivo, file_name="distancia.pdf")

    elif tema == "Punto Medio":
        x1 = st.number_input("x1 ", value=0.0)
        y1 = st.number_input("y1 ", value=0.0)
        x2 = st.number_input("x2 ", value=4.0)
        y2 = st.number_input("y2 ", value=6.0)
        if st.button("Mostrar"):
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            st.success(f"Punto Medio M = ({mx:.2f}, {my:.2f})")
            
            fig, ax = plt.subplots()
            ax.scatter([x1, x2, mx], [y1, y2, my])
            ax.plot([x1, x2], [y1, y2])
            ax.grid(True)
            st.pyplot(fig)
            fig.savefig("grafico.png")
            
            # PDF
            procedimiento = f"Punto Medio entre P1({x1}, {y1}) y P2({x2}, {y2})"
            pdf = generar_pdf("Punto Medio", f"P1({x1},{y1}) - P2({x2},{y2})", procedimiento, f"({mx:.2f}, {my:.2f})")
            with open(pdf, "rb") as archivo:
                st.download_button("Descargar PDF", archivo, file_name="punto_medio.pdf")

    elif tema == "Pendiente":
        x1 = st.number_input("x1  ", value=0.0)
        y1 = st.number_input("y1  ", value=0.0)
        x2 = st.number_input("x2  ", value=3.0)
        y2 = st.number_input("y2  ", value=4.0)
        if st.button("Resolver"):
            if (x2 - x1) == 0:
                m = "Indefinida (recta vertical)"
                st.success(f"Pendiente = {m}")
            else:
                m = (y2 - y1) / (x2 - x1)
                st.success(f"Pendiente = {m:.4f}")
            
            fig, ax = plt.subplots()
            ax.scatter([x1, x2], [y1, y2])
            ax.plot([x1, x2], [y1, y2])
            ax.grid(True)
            st.pyplot(fig)
            fig.savefig("grafico.png")
            
            # PDF
            procedimiento = f"Pendiente entre P1({x1}, {y1}) y P2({x2}, {y2})"
            pdf = generar_pdf("Pendiente", f"P1({x1},{y1}) - P2({x2},{y2})", procedimiento, str(m))
            with open(pdf, "rb") as archivo:
                st.download_button("Descargar PDF", archivo, file_name="pendiente.pdf")

    elif tema == "Recta Punto-Pendiente":
        x1 = st.number_input("x₁", value=0.0)
        y1 = st.number_input("y₁", value=0.0)
        m = st.number_input("Pendiente", value=1.0)
        if st.button("Graficar recta"):
            xs = np.linspace(-20, 20, 500)
            ys = m * (xs - x1) + y1
            fig, ax = plt.subplots()
            ax.plot(xs, ys)
            ax.scatter([x1], [y1], color='red')
            ax.grid(True)
            st.pyplot(fig)
            fig.savefig("grafico.png")
            
            # PDF
            procedimiento = f"Recta con punto ({x1}, {y1}) y pendiente {m}"
            pdf = generar_pdf("Recta Punto-Pendiente", f"y - {y1} = {m}(x - {x1})", procedimiento, "Ecuación generada")
            with open(pdf, "rb") as archivo:
                st.download_button("Descargar PDF", archivo, file_name="recta.pdf")

    elif tema == "Circunferencia":
        h = st.number_input("Centro h", value=0.0)
        k = st.number_input("Centro k", value=0.0)
        r = st.number_input("Radio", value=5.0)
        if st.button("Graficar circunferencia"):
            t = np.linspace(0, 2*np.pi, 500)
            xs = h + r * np.cos(t)
            ys = k + r * np.sin(t)
            fig, ax = plt.subplots()
            ax.plot(xs, ys)
            ax.scatter([h], [k], color='red')
            ax.axis("equal")
            ax.grid(True)
            st.pyplot(fig)
            fig.savefig("grafico.png")
            
            # PDF
            procedimiento = f"Circunferencia centro ({h}, {k}), radio {r}"
            pdf = generar_pdf("Circunferencia", f"(x-{h})² + (y-{k})² = {r}²", procedimiento, "Gráfica generada")
            with open(pdf, "rb") as archivo:
                st.download_button("Descargar PDF", archivo, file_name="circunferencia.pdf")

    elif tema == "Parábola":
        a = st.number_input("a", value=1.0)
        b = st.number_input("b", value=0.0)
        c = st.number_input("c", value=0.0)
        if st.button("Graficar parábola"):
            x_vals = np.linspace(-10, 10, 500)
            y_vals = a * x_vals**2 + b * x_vals + c
            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label="Parábola")
            ax.axhline(0, color="black")
            ax.axvline(0, color="black")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)
            fig.savefig("grafico.png")
            
            # PDF
            procedimiento = f"Parábola: y = {a}x² + {b}x + {c}"
            pdf = generar_pdf("Parábola", f"y = {a}x² + {b}x + {c}", procedimiento, "Gráfica generada")
            with open(pdf, "rb") as archivo:
                st.download_button("Descargar PDF", archivo, file_name="parabola.pdf")

    elif tema == "Elipse":
        a = st.number_input("Semieje a", value=5.0)
        b = st.number_input("Semieje b", value=3.0)
        if st.button("Graficar elipse"):
            t = np.linspace(0, 2*np.pi, 500)
            x_vals = a * np.cos(t)
            y_vals = b * np.sin(t)
            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals)
            ax.scatter([0], [0], color="red")
            ax.set_aspect("equal")
            ax.grid(True)
            st.pyplot(fig)
            fig.savefig("grafico.png")
            
            # PDF
            procedimiento = f"Elipse: x²/{a}² + y²/{b}² = 1"
            pdf = generar_pdf("Elipse", f"x²/{a}² + y²/{b}² = 1", procedimiento, "Gráfica generada")
            with open(pdf, "rb") as archivo:
                st.download_button("Descargar PDF", archivo, file_name="elipse.pdf")

    elif tema == "Hipérbola":
        a = st.number_input("a", value=2.0)
        b = st.number_input("b", value=1.0)
        if st.button("Graficar hipérbola"):
            x_vals = np.linspace(-10, 10, 1000)
            x_vals = x_vals[np.abs(x_vals) > a]
            y_vals_pos = b * np.sqrt((x_vals**2 / a**2) - 1)
            y_vals_neg = -y_vals_pos
            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals_pos)
            ax.plot(x_vals, y_vals_neg)
            ax.axhline(0, color="black")
            ax.axvline(0, color="black")
            ax.grid(True)
            st.pyplot(fig)
            fig.savefig("grafico.png")
            
            # PDF
            procedimiento = f"Hipérbola: x²/{a}² - y²/{b}² = 1"
            pdf = generar_pdf("Hipérbola", f"x²/{a}² - y²/{b}² = 1", procedimiento, "Gráfica generada")
            with open(pdf, "rb") as archivo:
                st.download_button("Descargar PDF", archivo, file_name="hiperbola.pdf")
