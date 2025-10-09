import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuración de la página ---
st.set_page_config(page_title="Salary Data Dashboard", layout="wide")

# --- Cargar datos ---
@st.cache_data
def load_data():
    return pd.read_csv("Salary_Data_clean.csv")

df = load_data()

# --- Sidebar ---
st.sidebar.header("Filtros")

education_filter = st.sidebar.multiselect(
    "Nivel educativo",
    options=df['Education Level'].unique(),
    default=df['Education Level'].unique()
)

gender_filter = st.sidebar.multiselect(
    "Género",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

filtered_df = df[
    (df['Education Level'].isin(education_filter)) &
    (df['Gender'].isin(gender_filter))
]
salary_range = st.sidebar.slider("Rango de salario", 
                                 int(filtered_df['Salary'].min()), 
                                 int(filtered_df['Salary'].max()), 
                                 (int(filtered_df['Salary'].min()), int(filtered_df['Salary'].max())))

filtered_df = filtered_df[(filtered_df['Salary'] >= salary_range[0]) & (filtered_df['Salary'] <= salary_range[1])]

# --- KPIs ---
total_people = len(filtered_df)
avg_salary = filtered_df['Salary'].mean()
unique_education_level = filtered_df['Education Level'].nunique()

st.title("💰 Salary Data Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Personas totales", total_people)
col2.metric("Salario promedio", f"${avg_salary:,.2f}")
col3.metric("Niveles educativos únicos", unique_education_level)

st.markdown("---")

# --- Gráficos ---
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        filtered_df['Gender'].value_counts(),
        title="Distribución por género",
        labels={'index': 'Género', 'value': 'Cantidad'}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(
        filtered_df,
        names='Education Level',
        title="Distribución por nivel educativo"
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Tabla de datos ---
st.markdown("### 📋 Detalle de roles y salarios")

st.dataframe(
    filtered_df[['Age', 'Gender', 'Education Level', 'Job Title', 'Years of Experience', 'Salary']],
    use_container_width=True
)

# --- Gráficas ---
st.markdown("### 💼 Top 10 puestos de trabajo mejor pagados")

top10 = filtered_df.sort_values(by='Salary', ascending=False).head(10)

fig3 = px.bar(
    top10,
    x='Salary',
    y='Job Title',
    orientation='h',
    title="Top 10 puestos mejor pagados",
    labels={'Salary': 'Salario', 'Job Title': 'Puesto'}
)

st.plotly_chart(fig3, use_container_width=True)

avg_salary_edu = filtered_df.groupby('Education Level')['Salary'].mean().sort_values(ascending=False)
fig4 = px.bar(
    avg_salary_edu,
    x=avg_salary_edu.index,
    y=avg_salary_edu.values,
    title="Salario promedio por nivel educativo",
    labels={'x': 'Nivel educativo', 'y': 'Salario promedio'}
)
st.plotly_chart(fig4, use_container_width=True)

avg_salary_gender = filtered_df.groupby('Gender')['Salary'].mean()
fig5 = px.bar(
    avg_salary_gender,
    x=avg_salary_gender.index,
    y=avg_salary_gender.values,
    title="Salario promedio por género",
    labels={'x':'Género', 'y':'Salario promedio'}
)
st.plotly_chart(fig5, use_container_width=True)

fig6 = px.histogram(filtered_df, x='Salary', nbins=20, title="Distribución de salarios")
st.plotly_chart(fig6, use_container_width=True)

