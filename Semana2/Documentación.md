# 🎵 Análisis Musical Global - Spotify & Last.fm

Dashboard interactivo para análisis de tendencias musicales combinando datos de comportamiento real de usuarios (Last.fm) con métricas algorítmicas de popularidad (Spotify).

## Descripción

Es un sistema automatizado que extrae, transforma y analiza datos musicales de dos plataformas complementarias para identificar:

- Tendencias globales
- Artistas emergentes  
- Patrones de consumo musical
- Comparativas entre plataformas

## Arquitectura

```
APIs (Spotify + Last.fm)
         ↓
 Tres AWS Lambdas (ETL) 
         ↓
Amazon S3 (Storage)
         ↓
Streamlit Dashboard (Visualización)
```

### Componentes:

1. **Extracción**: AWS Lambda obtiene datos de ambas APIs
2. **Transformación**: Limpieza y combinación de datasets
3. **Almacenamiento**: S3 bucket con archivos Parquet
4. **Visualización**: Dashboard Streamlit con Docker

## Deployment

### Requisitos Previos

- Servidor con Docker y docker-compose instalado
- GitHub self-hosted runner configurado
- Credenciales de AWS con acceso a S3

### Variables de Entorno Necesarias

Configurar en **GitHub → Settings → Environments → prod → Secrets**:

```
AWS_ACCESS_KEY_ID          # Access key de AWS
AWS_SECRET_ACCESS_KEY      # Secret key de AWS
AWS_DEFAULT_REGION         # Región (us-west-1)
S3_BUCKET_NAME            # Nombre del bucket S3
```

### Deployment Automático

El proyecto usa GitHub Actions para deployment automático:

```yaml
# Push a main activa el deployment
git push origin main
```

El workflow:
1. Crea archivo `.env` con credenciales AWS
2. Construye imagen Docker
3. Levanta contenedor con docker-compose
4. Expone dashboard en puerto 8502

### Deployment Manual

```bash
# 1. Crear archivo .env
cat > .env << EOF
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_DEFAULT_REGION=us-west-1
S3_BUCKET_NAME=xideralaws-curso-lisset
EOF

# 2. Levantar servicios
docker-compose up -d --build

# 3. Ver logs
docker logs music_dashboard -f
```

## 📊 Datasets

El sistema genera 5 datasets en S3:

| Dataset | Descripción |
|---------|-------------|
| `artists_combined.parquet` | Artistas con datos de ambas plataformas |
| `tracks_lastfm.parquet` | Canciones más reproducidas |
| `genres_lastfm.parquet` | Géneros/tags populares |
| `spotify_new_releases.parquet` | Nuevos lanzamientos |
| `tracks_enriched_cross_platform.parquet` | Canciones con métricas combinadas |

## 📈 Análisis Disponibles

### 1. Ranking Global
Top artistas más escuchados con análisis de concentración de reproducciones.

### 2. Comparación Plataformas
Oyentes (Last.fm) vs Seguidores (Spotify) - Consumo real vs popularidad algorítmica.

### 3. Géneros Globales
Distribución de géneros musicales dominantes a nivel mundial.

### 4. Artistas Emergentes
Detección de artistas con alto potencial de crecimiento usando filtros ajustables.

### 5. Nuevos Lanzamientos
Tendencias en releases recientes por tipo (single, álbum, EP).

## 🛠️ Stack Tecnológico

**Backend**:
- Python 3.11
- AWS Lambda (ETL)
- boto3 (AWS SDK)
- pandas (procesamiento de datos)

**Frontend**:
- Streamlit
- Plotly (visualizaciones)

**Infraestructura**:
- Docker + docker-compose
- Amazon S3
- Amazon EventBridge (automatización)
- GitHub Actions (CI/CD)

## 📁 Estructura del Proyecto

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml          # Workflow de deployment
├── music_analysis_dashboard.py # Dashboard Streamlit
├── docker-compose.yml          # Orquestación de servicios
├── Dockerfile                  # Imagen del dashboard
└── README.md                   # Esta documentación
```

## 🔧 Configuración Local

Para desarrollo local:

```bash
# 1. Instalar dependencias
pip install streamlit pandas boto3 plotly pyarrow

# 2. Configurar credenciales AWS
export AWS_ACCESS_KEY_ID=tu_key
export AWS_SECRET_ACCESS_KEY=tu_secret
export AWS_DEFAULT_REGION=us-west-1
export S3_BUCKET_NAME=xideralaws-curso-lisset

# 3. Ejecutar dashboard
streamlit run music_analysis_dashboard.py
```

## 🔍 Troubleshooting

### Error: No se pueden cargar los datos

**Causa**: Falta configuración de credenciales AWS

**Solución**: 
```bash
# Verificar variables de entorno en el contenedor
docker exec music_dashboard env | grep AWS

# Si faltan, revisar archivo .env y secrets de GitHub
```

### Error: Container no inicia

**Causa**: Puerto 8502 ocupado o error en credenciales

**Solución**:
```bash
# Ver logs detallados
docker logs music_dashboard --tail 100

# Verificar puertos
netstat -tulpn | grep 8502
```

## 📝 Notas Importantes

- ⚠️ **No subir archivo `.env` a GitHub** - Está en `.gitignore`
- 🔄 El ETL Lambda se ejecuta semanalmente (domingos 12:00 UTC)
- 📊 Los datos se actualizan automáticamente en el dashboard
- 🔒 Las credenciales se manejan vía GitHub Secrets (producción) o `.env` (local)

## 👥 Autor

**Lisset** - Xideral AWS Curso

## 📄 Licencia

Proyecto educativo - Xideral AWS Training

---

**Última actualización**: Octubre 2025
