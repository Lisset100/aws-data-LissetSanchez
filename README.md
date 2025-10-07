# 🚀 Guía Completa de Instalación y Preparación del Entorno de Trabajo en EC2

## Tabla de Contenidos 📋 
1. [Introducción](#introducción)
2. [Prerrequisitos](#prerrequisitos)
3. [Conceptos Clave](#conceptos-clave)
4. [Configuración Paso a Paso](#configuración-paso-a-paso)
5. [Buenas Prácticas](#buenas-prácticas)

---

## Introducción 🎯

Esta guía te ayuda a configurar un servidor Ubuntu en AWS EC2 para trabajar con **Python, Docker, Docker Compose y análisis de datos**. Al finalizar, tendrás un entorno profesional y escalable para proyectos de ciencia de datos.

### ¿Por qué usar EC2?
- **Escalabilidad**: Ajusta recursos según necesites
- **Costo-efectivo**: Paga solo por lo que usas
- **Acceso remoto**: Trabaja desde cualquier lugar
- **Entorno consistente**: Mismo ambiente para todo el equipo
---

## Prerrequisitos 📦

### En tu computadora local:
- [ ] Windows PowerShell (o terminal en Mac/Linux)
- [ ] Clave privada `.pem` descargada de AWS
- [ ] Acceso a internet

### En AWS:
- [ ] Cuenta de AWS activa
- [ ] Instancia EC2 Ubuntu lanzada
- [ ] Security Group configurado 
- [ ] IP pública asignada

---

## Conceptos Clave ✨

### ¿Qué es EC2?
**Amazon Elastic Compute Cloud (EC2)** es un servicio que proporciona servidores virtuales en la nube.

**Ventajas:**
- No necesitas hardware físico
- Creas y destruyes servidores en minutos
- Múltiples configuraciones disponibles (CPU, RAM, almacenamiento)

### ¿Qué es Docker?
**Docker** permite empaquetar aplicaciones con todas sus dependencias en "contenedores". 

**¿Por qué usarlo?**
- **Portabilidad**: "Funciona en mi máquina" → "Funciona en cualquier máquina"
- **Aislamiento**: Cada contenedor es independiente
- **Eficiencia**: Más ligero que una máquina virtual completa
- **Consistencia**: Mismo entorno en desarrollo, pruebas y producción

### ¿Qué es un Entorno Virtual de Python?
Un **entorno virtual** es una carpeta que contiene una instalación de Python aislada con sus propios paquetes.

**Beneficios:**
- Evitas conflictos entre versiones de librerías
- Cada proyecto tiene sus dependencias específicas
- No "ensucias" el Python del sistema
- Fácil de replicar en otros servidores

### ¿Qué es Docker Compose?
**Docker Compose** orquesta múltiples contenedores Docker. Con un solo archivo YAML defines toda tu infraestructura.

**Ejemplo de uso:**
- Contenedor 1: Base de datos PostgreSQL
- Contenedor 2: API en Python
- Contenedor 3: Frontend en React
- Docker Compose los conecta y maneja todos a la vez

---

## Configuración Paso a Paso

### 1️⃣ Conexión al Servidor EC2

#### 1.1 Preparar la clave privada

En tu computadora local (Windows PowerShell):

```powershell
# Navega a la carpeta donde está tu archivo .pem
cd C:\Users\User\Downloads

# Establece permisos restrictivos (solo lectura para ti)
# Esto es un requisito de seguridad de SSH
icacls "aws-data-ejemplo.pem" /inheritance:r
icacls "aws-data-ejemplo.pem" /grant:r "%username%:R"
```

**🔍 ¿Por qué esto?**
SSH rechaza claves privadas con permisos muy abiertos por seguridad.

#### 1.2 Conectarte al servidor

```powershell
ssh -i "C:\Users\User\Downloads\aws-data-ejemplo.pem" ubuntu@ec2-54-219-169-96.us-west-1.compute.amazonaws.com
```

**Desglose del comando:**
- `ssh` → Protocolo de conexión segura y encriptada
- `-i "ruta_a_pem"` → Especifica tu clave privada de autenticación
- `ubuntu` → Usuario predeterminado en instancias Ubuntu de AWS
- `@ec2-...` → Dirección DNS pública de tu servidor

**✅ Conexión exitosa:**
Verás un prompt como:
```
ubuntu@ip-172-31-16-32:~$
```

**⚠️ Primera conexión:**
Si es tu primera vez, verás un mensaje sobre autenticidad del host. Escribe `yes` y presiona Enter.

---

### 2️⃣ Actualizar el Sistema Operativo

```bash
sudo apt update
```

**🔍 ¿Qué hace?**
- `sudo` → "Superuser Do" - ejecuta comandos como administrador
- `apt` → Advanced Package Tool - gestor de paquetes de Ubuntu
- `update` → Actualiza la lista de paquetes disponibles en los repositorios


```bash
sudo apt upgrade -y
```

**🔍 ¿Qué hace?**
- `upgrade` → Instala las versiones más recientes de los paquetes ya instalados
- `-y` → Responde "sí" automáticamente a todas las preguntas

**⚠️ Importante:**
Este proceso puede tardar varios minutos. Es crítico para:
- Parches de seguridad
- Corrección de bugs
- Compatibilidad con software nuevo

---

### 3️⃣ Instalar Docker y Docker Compose

#### 3.1 Instalar dependencias del sistema

```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
```

**🔍 ¿Qué instala cada paquete?**
- `apt-transport-https` → Permite a apt descargar paquetes vía HTTPS (conexión segura)
- `ca-certificates` → Certificados para verificar identidad de servidores
- `curl` → Herramienta para descargar archivos desde internet
- `software-properties-common` → Gestiona repositorios de software adicionales

#### 3.2 Agregar clave GPG de Docker

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

**🔍 ¿Por qué esto?**
Las claves GPG verifican que los paquetes que descargas realmente vienen de Docker (no de un atacante). Es como verificar el sello de calidad.

**Desglose:**
- `curl -fsSL URL` → Descarga el archivo de forma silenciosa
- `gpg --dearmor` → Convierte la clave a formato binario
- `>` → Guarda el resultado en un archivo específico

#### 3.3 Agregar repositorio oficial de Docker

```bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**🔍 ¿Qué hace?**
Agrega el repositorio oficial de Docker a la lista de fuentes de software de Ubuntu.

**Componentes:**
- `arch=amd64` → Arquitectura del procesador
- `signed-by=...` → Usa la clave GPG para verificar
- `$(lsb_release -cs)` → Detecta automáticamente tu versión de Ubuntu
- `stable` → Canal estable (no versiones experimentales)

#### 3.4 Actualizar e instalar Docker

```bash
sudo apt update
sudo apt install docker-ce -y
```

**🔍 ¿Qué es docker-ce?**
- **CE** = Community Edition (versión gratuita)
- Incluye el motor Docker completo
- Suficiente para la mayoría de proyectos

#### 3.5 Verificar instalación

```bash
sudo systemctl status docker
```

**🔍 ¿Qué verás?**
```
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
   Active: active (running) since...
```

**✅ "Active (running)" = Docker está funcionando correctamente**

Presiona `q` para salir.

#### 3.6 Permitir usar Docker sin sudo (Opcional pero recomendado)

```bash
sudo usermod -aG docker $USER
```

**🔍 ¿Qué hace?**
Agrega tu usuario al grupo `docker`, permitiéndote ejecutar comandos Docker sin `sudo`.

**⚠️ Importante:**
Debes cerrar sesión y volver a conectarte para que el cambio tome efecto:
```bash
exit
# Vuelve a conectarte con SSH
```

#### 3.7 Instalar Docker Compose

```bash
sudo apt install docker-compose -y
docker-compose --version
```

**Salida esperada:**
```
docker-compose version 1.29.2, build 5becea4c
```

**🔍 Alternativa moderna:**
Docker ahora incluye Compose V2 como plugin. Puedes usar `docker compose` (sin guión) en lugar de `docker-compose`.

---

### 4️⃣ Crear Entorno Virtual de Python

#### 4.1 Verificar instalación de Python

```bash
python3 --version
```

**Salida típica:**
```
Python 3.12.3
```

#### 4.2 Instalar herramienta de entornos virtuales

```bash
sudo apt install python3-venv -y
```

**🔍 ¿Por qué?**
Ubuntu no incluye `venv` por defecto en todas las versiones. Este paquete lo proporciona.

#### 4.3 Crear el entorno virtual

```bash
python3 -m venv entorno_ejemplo
```

#### 4.4 Activar el entorno

```bash
source entorno_ejemplo/bin/activate
```

**✅ Entorno activado:**
Tu prompt cambiará a:
```
(entorno_ejemplo) ubuntu@ip-172-31-16-32:~$
```

**🔍 ¿Qué significa?**
Ahora cualquier `pip install` o ejecución de Python usará este entorno aislado.

#### 4.5 Actualizar pip

```bash
pip install --upgrade pip
```

**🔍 ¿Por qué?**
El pip incluido en el entorno puede estar desactualizado. Actualizarlo previene errores de instalación.

#### 4.6 Instalar librerías para análisis de datos

```bash
pip install pandas openpyxl jupyter
```

**🔍 ¿Qué instala cada paquete?**
- `pandas` → Análisis y manipulación de datos (DataFrames)
- `openpyxl` → Leer/escribir archivos Excel (.xlsx)
- `jupyter` → Notebooks interactivos

#### 4.7 Desactivar el entorno (cuando termines)

```bash
deactivate
```

Tu prompt volverá a:
```
ubuntu@ip-172-31-16-32:~$
```

---

### 5️⃣ Transferir y Procesar Datasets

#### 5.1 Subir archivos desde tu computadora

**Desde Windows PowerShell (tu computadora local):**

```powershell
scp -i "C:\Users\User\Downloads\aws-data-ejemplo.pem" "C:\Users\User\Downloads\archive.zip" ubuntu@ec2-54-219-169-96.us-west-1.compute.amazonaws.com:~/
```

**🔍 Desglose del comando:**
- `scp` → Secure Copy Protocol (copia segura y encriptada)
- `-i "ruta_pem"` → Tu clave privada
- `"archivo_origen"` → Archivo en tu PC
- `ubuntu@ec2...:~/` → Destino (carpeta home del servidor)

**💡 Tips:**
- Para subir una carpeta completa: agrega `-r` después de `scp`
- Puedes subir múltiples archivos: `scp -i key.pem file1.csv file2.csv ubuntu@ec2...:/ruta/`

#### 5.2 Descomprimir archivos

**En el servidor EC2:**

```bash
# Instalar unzip si no está disponible
sudo apt install unzip -y

# Descomprimir
unzip archive.zip

# Ver archivos extraídos
ls -lh
```

**🔍 Comandos de compresión útiles:**
```bash
# Descomprimir .tar.gz
tar -xzvf archivo.tar.gz

# Descomprimir .gz
gunzip archivo.gz

# Crear un .zip
zip -r backup.zip mi_carpeta/
```

#### 5.3 Verificar el dataset

```bash
head -n 5 netflix_titles.csv
```

**🔍 ¿Qué hace `head`?**
Muestra las primeras líneas de un archivo. Útil para inspeccionar datasets grandes sin abrirlos completamente.

**Otros comandos útiles:**
```bash
# Ver número de líneas
wc -l netflix_titles.csv

# Ver tamaño del archivo
du -h netflix_titles.csv

# Ver columnas del CSV
head -n 1 netflix_titles.csv | tr ',' '\n'
```

---

## ✅ Buenas Prácticas

### 🔒 Seguridad

1. **Nunca compartas tu archivo .pem**
   - Es como la llave de tu casa
   - Si se compromete, crea una nueva key pair

2. **Configura Security Groups restrictivos**
   ```
   SSH (22): Solo tu IP
   HTTP (80): 0.0.0.0/0 (si necesitas servidor web)
   Custom: Solo IPs específicas
   ```

3. **Actualiza regularmente**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

4. **Usa firewalls adicionales**
   ```bash
   sudo ufw enable
   sudo ufw allow 22
   sudo ufw status
   ```

---

### 🧪 Separación de Entornos

```bash
# Desarrollo
python3 -m venv venv_dev
source venv_dev/bin/activate

# Producción
python3 -m venv venv_prod
source venv_prod/bin/activate

# Testing
python3 -m venv venv_test
source venv_test/bin/activate
```

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Python venv Documentation](https://docs.python.org/3/library/venv.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Tutoriales Recomendados
- [AWS EC2 Getting Started](https://aws.amazon.com/ec2/getting-started/)
- [Docker 101](https://www.docker.com/101-tutorial/)
- [Real Python - Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)


---

**¡Feliz análisis de datos! 🎉📊🐍**
