import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.title("Aplikasi Turunan Parsial")

# Input fungsi
x, y = sp.symbols('x y')
user_input = st.text_input("Masukkan fungsi f(x, y):", "x**2 + y**2")

# Parsing fungsi
try:
    f = sp.sympify(user_input)
    st.latex(f"f(x, y) = {sp.latex(f)}")
    
    # Turunan parsial
    fx = sp.diff(f, x)
    fy = sp.diff(f, y)
    
    st.write("### Turunan Parsial")
    st.latex(f"\\frac{{\\partial f}}{{\\partial x}} = {sp.latex(fx)}")
    st.latex(f"\\frac{{\\partial f}}{{\\partial y}} = {sp.latex(fy)}")
    
    # Titik untuk bidang singgung
    x0 = st.number_input("Nilai x0:", value=1.0)
    y0 = st.number_input("Nilai y0:", value=1.0)
    
    f_lamb = sp.lambdify((x, y), f, "numpy")
    fx_lamb = sp.lambdify((x, y), fx, "numpy")
    fy_lamb = sp.lambdify((x, y), fy, "numpy")
    
    # Hitung nilai f(x0, y0) dan gradien
    z0 = f_lamb(x0, y0)
    fx0 = fx_lamb(x0, y0)
    fy0 = fy_lamb(x0, y0)

    st.write(f"f({x0}, {y0}) = {z0}")
    
    # Plot permukaan dan bidang singgung
    st.write("### Grafik 3D")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    X = np.linspace(x0-2, x0+2, 50)
    Y = np.linspace(y0-2, y0+2, 50)
    X, Y = np.meshgrid(X, Y)
    Z = f_lamb(X, Y)
    
    # Bidang singgung z = z0 + fx0*(x - x0) + fy0*(y - y0)
    Z_tangent = z0 + fx0*(X - x0) + fy0*(Y - y0)

    ax.plot_surface(X, Y, Z, alpha=0.6, cmap='viridis')
    ax.plot_surface(X, Y, Z_tangent, alpha=0.5, color='red')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f(x, y)')
    st.pyplot(fig)

except Exception as e:
    st.error(f"Terjadi kesalahan dalam membaca fungsi: {e}")
