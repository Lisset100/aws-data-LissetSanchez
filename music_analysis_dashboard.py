# =====================================================
# DASHBOARD DE ANÁLISIS MUSICAL - SPOTIFY & LAST.FM

import boto3
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import io

# CONFIGURACIÓN DE STREAMLIT
st.set_page_config(
    page_title="Análisis Musical Global",
    page_icon="🎵",
    layout="wide"
)

# CONEXIÓN CON AWS S3
s3 = boto3.client("s3")

BUCKET_NAME = "xideralaws-curso-lisset"
CARPETA_CLEAN = "clean/"

# =====================================================
# FUNCIONES PARA CARGAR DATOS DESDE PARQUET

@st.cache_data
def cargar_artists_combined():
    key = f"{CARPETA_CLEAN}artists_combined.parquet"
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        body = obj["Body"].read()
        df = pd.read_parquet(io.BytesIO(body))
        return df
    except Exception as e:
        st.error(f"Error cargando artists_combined: {str(e)}")
        return None

@st.cache_data
def cargar_tracks_lastfm():
    key = f"{CARPETA_CLEAN}tracks_lastfm.parquet"
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        body = obj["Body"].read()
        df = pd.read_parquet(io.BytesIO(body))
        return df
    except Exception as e:
        st.error(f"Error cargando tracks_lastfm: {str(e)}")
        return None

@st.cache_data
def cargar_genres_lastfm():
    key = f"{CARPETA_CLEAN}genres_lastfm.parquet"
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        body = obj["Body"].read()
        df = pd.read_parquet(io.BytesIO(body))
        return df
    except Exception as e:
        st.error(f"Error cargando genres_lastfm: {str(e)}")
        return None

@st.cache_data
def cargar_new_releases():
    key = f"{CARPETA_CLEAN}spotify_new_releases.parquet"
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        body = obj["Body"].read()
        df = pd.read_parquet(io.BytesIO(body))
        return df
    except Exception as e:
        st.error(f"Error cargando spotify_new_releases: {str(e)}")
        return None

@st.cache_data
def cargar_tracks_enriched():
    key = f"{CARPETA_CLEAN}tracks_enriched_cross_platform.parquet"
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        body = obj["Body"].read()
        df = pd.read_parquet(io.BytesIO(body))
        return df
    except Exception as e:
        st.error(f"Error cargando tracks_enriched: {str(e)}")
        return None

# =====================================================
# SIDEBAR

with st.sidebar:
    st.header("Filtra por análisis o Actualiza los datos")
    
    if st.button("🔄 Actualizar Datos"):
        st.cache_data.clear()
        st.rerun()
    
    st.subheader("📊 Selecciona un Análisis")
    
    analisis_seleccionado = st.radio(
        "Elige el análisis:",
        options=[
            "🏠 Vista General",
            "📈 Análisis 1: Ranking Global",
            "🔄 Análisis 2: Comparación Plataformas",
            "🎸 Análisis 3: Géneros Globales",
            "⭐ Análisis 4: Artistas Emergentes",
            "🆕 Análisis 5: Nuevos Lanzamientos"
        ],
        index=0
    )
    
    st.markdown("---")

# =====================================================
# CARGA DE DATOS

st.title("🎵 Análisis Musical Global")
st.markdown("### Spotify & Last.fm - Tendencias y Comparativas")

with st.spinner("⏳ Cargando datos desde S3..."):
    df_artists = cargar_artists_combined()
    df_tracks_lastfm = cargar_tracks_lastfm()
    df_genres = cargar_genres_lastfm()
    df_new_releases = cargar_new_releases()
    df_tracks_enriched = cargar_tracks_enriched()

if df_artists is None:
    st.error("❌ No se pudieron cargar los datos. Verifica tu bucket S3.")
    st.stop()

# KPIs GENERALES
st.subheader("📊 Resumen de los Datasets Disponibles")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🎤 Artistas", len(df_artists))

with col2:
    cantidad_tracks = len(df_tracks_lastfm) if df_tracks_lastfm is not None else 0
    st.metric("🎵 Tracks Last.fm", cantidad_tracks)

with col3:
    cantidad_generos = len(df_genres) if df_genres is not None else 0
    st.metric("🎸 Géneros", cantidad_generos)

with col4:
    cantidad_releases = len(df_new_releases) if df_new_releases is not None else 0
    st.metric("🆕 Lanzamientos", cantidad_releases)

with col5:
    cantidad_enriched = len(df_tracks_enriched) if df_tracks_enriched is not None else 0
    st.metric("🔗 Tracks Enriched", cantidad_enriched)
st.markdown("---")
# =====================================================
# VISTA GENERAL

if analisis_seleccionado == "🏠 Vista General":
    
    st.markdown("""
    Bienvenido al **Dashboard de Análisis Musical Global**. Este dashboard analiza datos de:
    - 🎧 **Last.fm**: Comportamiento real de usuarios
    - 💚 **Spotify**: Popularidad algorítmica
    
    ### 📋 Análisis Disponibles:
    
    **1️⃣ Ranking Global** - Top artistas más escuchados
    
    **2️⃣ Comparación Plataformas** - Oyentes vs Seguidores
    
    **3️⃣ Géneros Globales** - Distribución de géneros populares
    
    **4️⃣ Artistas Emergentes** - Detección de alto potencial
    
    **5️⃣ Nuevos Lanzamientos** - Tendencias recientes
    
    """)
    
    st.info("👈 **Selecciona un análisis en el menú lateral para comenzar**")
    
    st.markdown("---")
    st.subheader("👀 Vista Previa: Top 10 Artistas")
    st.dataframe(
        df_artists.head(10)[['artist_name', 'lastfm_playcount', 'lastfm_listeners', 
                              'spotify_followers', 'spotify_popularity']],
        use_container_width=True
    )

# =====================================================
# ANÁLISIS 1: RANKING GLOBAL

elif analisis_seleccionado == "📈 Análisis 1: Ranking Global":
    st.header("📈 Análisis 1: Ranking Global de Artistas")

    st.subheader("🎵 Top Artistas con Más Reproducciones")
    
    col_filtro, col_espacio = st.columns([1, 3])
    with col_filtro:
        top_n_artistas = st.selectbox("Mostrar top:", options=[10, 20, 30, 50], index=1)
    
    df_top = df_artists.sort_values(by='lastfm_playcount', ascending=False).head(top_n_artistas)
    
    grafica_top = px.bar(
        df_top, x='artist_name', y='lastfm_playcount',
        title=f'Top {top_n_artistas} Artistas Más Escuchados',
        labels={'artist_name': 'Artista', 'lastfm_playcount': 'Reproducciones'},
        color='lastfm_playcount', color_continuous_scale='Viridis', height=600
    )
    grafica_top.update_layout(xaxis_tickangle=-45, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(grafica_top, use_container_width=True)
    
    artista_top1 = df_top.iloc[0]['artist_name']
    reproducciones_top1 = df_top.iloc[0]['lastfm_playcount']
    st.info(f"🔍 **El artista más escuchado es {artista_top1} con {reproducciones_top1:,} reproducciones**")
    
    st.markdown("---")
    st.subheader("📈 Correlación: Reproducciones vs Oyentes")
    
    df_scatter = df_artists.sort_values(by='lastfm_playcount', ascending=False).head(50)
    
    grafica_scatter = px.scatter(
        df_scatter, x='lastfm_listeners', y='lastfm_playcount',
        size='lastfm_playcount', color='lastfm_playcount',
        hover_name='artist_name', color_continuous_scale='Viridis', height=600,
        title='Relación entre Oyentes y Reproducciones'
    )
    st.plotly_chart(grafica_scatter, use_container_width=True)
    
    correlacion = df_scatter['lastfm_listeners'].corr(df_scatter['lastfm_playcount'])
    ratio_promedio = (df_scatter['lastfm_playcount'] / df_scatter['lastfm_listeners']).mean()
    
    st.success(f"""
    **Análisis:** Cada oyente reproduce {ratio_promedio:.0f} veces
    """)
    
    st.markdown("---")
    st.subheader("📊 Concentración de Reproducciones")
    
    df_concentracion = df_artists.sort_values(by='lastfm_playcount', ascending=False).head(50)
    total_reproducciones = df_concentracion['lastfm_playcount'].sum()
    df_concentracion['porcentaje_individual'] = (df_concentracion['lastfm_playcount'] / total_reproducciones * 100)
    df_concentracion['porcentaje_acumulado'] = df_concentracion['porcentaje_individual'].cumsum()
    df_concentracion['ranking'] = range(1, len(df_concentracion) + 1)
    
    grafica_concentracion = px.line(
        df_concentracion,
        x='ranking',
        y='porcentaje_acumulado',
        title='Distribución Acumulativa de Reproducciones (Top 50)',
        labels={'ranking': 'Posición', 'porcentaje_acumulado': 'Porcentaje Acumulado (%)'},
        markers=True, height=600
    )
    grafica_concentracion.update_traces(
        line_color='#00CC96', line_width=3, marker=dict(size=8, color='#FF6692')
    )
    grafica_concentracion.add_hline(y=50, line_dash="dash", line_color="orange")
    grafica_concentracion.add_hline(y=80, line_dash="dash", line_color="red")
    
    st.plotly_chart(grafica_concentracion, use_container_width=True)
    
    porcentaje_top10 = df_concentracion.iloc[9]['porcentaje_acumulado']
    st.warning(f"🔥 El top 10 concentra {porcentaje_top10:.1f}% de todas las reproducciones")

# =====================================================
# ANÁLISIS 2: COMPARACIÓN PLATAFORMAS

elif analisis_seleccionado == "🔄 Análisis 2: Comparación Plataformas":
    st.header("🔄 Comparación Last.fm vs Spotify")
    
    with st.expander("ℹ️ ¿Cuál es la diferencia?"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🎧 OYENTES (Last.fm)** - Consumo real")
        with col2:
            st.markdown("**💚 SEGUIDORES (Spotify)** - Interés explícito")

    st.subheader("📊 Oyentes vs Seguidores")
    
    col1, col2 = st.columns(2)
    with col1:
        num_artistas = st.slider("Número de artistas:", 10, 30, 20, 5)
    with col2:
        metricas = st.multiselect(
            "Métricas:", 
            ["Oyentes Last.fm", "Seguidores Spotify"],
            default=["Oyentes Last.fm", "Seguidores Spotify"]
        )
    
    if len(metricas) > 0:
        df_comp = df_artists[
            (df_artists['lastfm_listeners'].notna()) &
            (df_artists['spotify_followers'].notna())
        ].sort_values('lastfm_listeners', ascending=False).head(num_artistas)
        
        df_grafica = pd.melt(
            df_comp[['artist_name', 'lastfm_listeners', 'spotify_followers']],
            id_vars=['artist_name'],
            value_vars=['lastfm_listeners', 'spotify_followers'],
            var_name='plataforma', value_name='cantidad'
        )
        
        df_grafica['plataforma'] = df_grafica['plataforma'].map({
            'lastfm_listeners': 'Oyentes Last.fm',
            'spotify_followers': 'Seguidores Spotify'
        })
        
        df_grafica = df_grafica[df_grafica['plataforma'].isin(metricas)]
        
        grafica_comp = px.bar(
            df_grafica, x='artist_name', y='cantidad', color='plataforma',
            barmode='group', title=f'Top {num_artistas} Artistas: Comparación',
            color_discrete_map={'Oyentes Last.fm': '#FF6692', 'Seguidores Spotify': '#1DB954'},
            height=600
        )
        grafica_comp.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(grafica_comp, use_container_width=True)
        
        # Métricas
        total_oyentes = df_comp['lastfm_listeners'].sum()
        total_seguidores = df_comp['spotify_followers'].sum()
        ratio_global = total_seguidores / total_oyentes
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎧 Total Oyentes", f"{total_oyentes:,.0f}")
        with col2:
            st.metric("💚 Total Seguidores", f"{total_seguidores:,.0f}")

# =====================================================
# ANÁLISIS 3: GÉNEROS GLOBALES

elif analisis_seleccionado == "🎸 Análisis 3: Géneros Globales":
    st.header("🎸 Análisis 3: Distribución de Géneros")
    
    if df_genres is not None and not df_genres.empty:
        st.subheader("🎵 Top Géneros Más Populares")
        
        top_n_generos = st.slider("Mostrar top géneros:", 10, 50, 20, 5)
        
        df_top_generos = df_genres.sort_values('tag_count', ascending=False).head(top_n_generos)
        
        fig_generos = px.bar(
            df_top_generos, x='tag_name', y='tag_count',
            title=f'Top {top_n_generos} Géneros Más Populares',
            labels={'tag_name': 'Género', 'tag_count': 'Popularidad'},
            color='tag_count', color_continuous_scale='Blues', height=600
        )
        fig_generos.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig_generos, use_container_width=True)
        
        total_tags = df_top_generos['tag_count'].sum()
        top_genero = df_top_generos.iloc[0]['tag_name']
        top_count = df_top_generos.iloc[0]['tag_count']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎸 Género #1", top_genero)
        with col2:
            st.metric("📊 Popularidad", f"{top_count:,}")
        with col3:
            porcentaje = (top_count / total_tags * 100)
            st.metric("📈 % del Top", f"{porcentaje:.1f}%")
        
        st.markdown("---")
        st.subheader("🥧 Distribución por Géneros")
        
        df_pie = df_top_generos.head(10)
        fig_pie = px.pie(
            df_pie, values='tag_count', names='tag_name',
            title='Top 10 Géneros - Distribución',
            hole=0.4, height=500
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    else:
        st.warning("⚠️ No hay datos de géneros disponibles")

# =====================================================
# ANÁLISIS 4: ARTISTAS EMERGENTES
elif analisis_seleccionado == "⭐ Análisis 4: Artistas Emergentes":
    st.header("⭐ Análisis 4: Artistas Emergentes")
    st.markdown("**Objetivo:** Identificar artistas con alto potencial de crecimiento")
        

    # Filtrar artistas con datos válidos
    df_emergentes = df_artists[
        (df_artists['lastfm_listeners'].notna()) &
        (df_artists['spotify_followers'].notna()) &
        (df_artists['spotify_popularity'].notna()) &
        (df_artists['lastfm_listeners'] > 0) &
        (df_artists['spotify_followers'] > 0)
    ].copy()

    
    if len(df_emergentes) == 0:
        st.error("❌ No hay artistas con datos completos de ambas plataformas.")
        st.info("""
        **Posibles causas:**
        - Lambda 2 no está combinando correctamente los datos
        - Los nombres de artistas no coinciden entre Last.fm y Spotify
        - Falta ejecutar el pipeline completo
        """)
    else:
        # Calcular engagement ratio
        df_emergentes['engagement_ratio'] = df_emergentes['lastfm_listeners'] / (df_emergentes['spotify_followers'] + 1)
        
        # CONTROLES DE FILTRADO
        st.subheader("🎛️ Ajustar Criterios de Emergentes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            min_popularity = st.slider(
                "Popularidad mínima en Spotify:",
                min_value=0,
                max_value=100,
                value=0,
                step=5,
                help="Artistas con al menos esta popularidad"
            )
        
        with col2:
            max_followers = st.slider(
                "Seguidores máximos (millones):",
                min_value=0.1,
                max_value=50.0,
                value=10.0,
                step=0.5,
                help="Artistas que aún no son mainstream"
            )
        
        # Aplicar filtros
        max_followers_valor = int(max_followers * 1_000_000)
        
        df_filtrado = df_emergentes[
            (df_emergentes['spotify_popularity'] >= min_popularity) &
            (df_emergentes['spotify_followers'] < max_followers_valor)
        ]
        
        # Mostrar cuántos artistas cumplen el criterio
        st.info(f"📊 **{len(df_filtrado)} artistas** cumplen con los criterios seleccionados")
        
        if len(df_filtrado) == 0:
            st.warning("⚠️ No hay artistas con estos criterios. Intenta ajustar los filtros.")
            
            # Mostrar estadísticas para ayudar
            st.write("**Estadísticas de los datos:**")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Popularidad mínima real", f"{df_emergentes['spotify_popularity'].min():.0f}")
                st.metric("Popularidad máxima real", f"{df_emergentes['spotify_popularity'].max():.0f}")
            with col2:
                st.metric("Seguidores mínimos", f"{df_emergentes['spotify_followers'].min():,.0f}")
                st.metric("Seguidores máximos", f"{df_emergentes['spotify_followers'].max():,.0f}")
        else:
            st.markdown("---")
            st.subheader("🚀 Artistas con Alto Potencial")
            
            # Ajustar slider según cantidad de datos disponibles
            num_disponibles = len(df_filtrado)
            
            if num_disponibles <= 10:
                # Si hay 10 o menos, mostrar todos sin slider
                top_emergentes = num_disponibles
                st.info(f"📊 Mostrando todos los {top_emergentes} artistas disponibles")
            else:
                # Si hay más de 10, permitir selección con slider
                max_valor = min(50, num_disponibles)
                valor_default = min(15, num_disponibles)
                top_emergentes = st.slider(
                    "Mostrar top artistas emergentes:", 
                    min_value=10, 
                    max_value=max_valor, 
                    value=valor_default, 
                    step=5
                )
            
            df_top_emergentes = df_filtrado.sort_values('spotify_popularity', ascending=False).head(top_emergentes)
            
            fig_emergentes = px.scatter(
                df_top_emergentes,
                x='spotify_followers', y='spotify_popularity',
                size='lastfm_listeners', color='spotify_popularity',
                hover_name='artist_name',
                hover_data={
                    'spotify_followers': ':,',
                    'spotify_popularity': True,
                    'lastfm_listeners': ':,'
                },
                title='Artistas Emergentes: Popularidad vs Seguidores',
                labels={'spotify_followers': 'Seguidores Spotify', 'spotify_popularity': 'Popularidad'},
                color_continuous_scale='Sunset', height=600
            )
            st.plotly_chart(fig_emergentes, use_container_width=True)
            
            # Métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                avg_pop = df_top_emergentes['spotify_popularity'].mean()
                st.metric("📈 Popularidad Promedio", f"{avg_pop:.1f}")
            with col2:
                avg_followers = df_top_emergentes['spotify_followers'].mean()
                st.metric("👥 Seguidores Promedio", f"{avg_followers:,.0f}")
            with col3:
                avg_listeners = df_top_emergentes['lastfm_listeners'].mean()
                st.metric("🎧 Oyentes Promedio", f"{avg_listeners:,.0f}")
            
            st.markdown("---")
            st.subheader("📋 Lista de Artistas Emergentes")
            
            df_display = df_top_emergentes[['artist_name', 'spotify_popularity', 'spotify_followers', 'lastfm_listeners']].copy()
            df_display.columns = ['Artista', 'Popularidad', 'Seguidores Spotify', 'Oyentes Last.fm']
            
            st.dataframe(df_display, use_container_width=True)

# =====================================================
# ANÁLISIS 5: NUEVOS LANZAMIENTOS
elif analisis_seleccionado == "🆕 Análisis 5: Nuevos Lanzamientos":
    st.header("🆕 Análisis 5: Tendencias de Nuevos Lanzamientos")
    
    if df_new_releases is not None and not df_new_releases.empty:
        st.subheader("📀 Distribución por Tipo de Lanzamiento")
        
        tipo_counts = df_new_releases['album_type'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_tipos = px.pie(
                values=tipo_counts.values,
                names=tipo_counts.index,
                title='Tipos de Lanzamientos',
                hole=0.4, height=400
            )
            st.plotly_chart(fig_tipos, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Estadísticas")
            for tipo, count in tipo_counts.items():
                st.metric(tipo.title(), count)
        
        st.markdown("---")
        st.subheader("🎵 Artistas con Más Lanzamientos Recientes")
        
        top_n_artists = st.slider("Mostrar top artistas:", 10, 30, 15, 5)
        
        artistas_releases = df_new_releases['artist_name'].value_counts().head(top_n_artists)
        
        fig_artists = px.bar(
            x=artistas_releases.index, y=artistas_releases.values,
            title=f'Top {top_n_artists} Artistas con Más Lanzamientos',
            labels={'x': 'Artista', 'y': 'Número de Lanzamientos'},
            color=artistas_releases.values, color_continuous_scale='Greens',
            height=500
        )
        fig_artists.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig_artists, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📋 Últimos Lanzamientos")
        
        st.dataframe(
            df_new_releases[['album_name', 'artist_name', 'album_type', 'release_date', 'total_tracks']].head(20),
            use_container_width=True
        )
        
    else:
        st.warning("⚠️ No hay datos de nuevos lanzamientos disponibles")
