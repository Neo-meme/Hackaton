# 🚀 SAIAYIN — Plataforma de Pagos y Facturación

<div align="center">

# 💳 PAGOS + FACTURACIÓN AUTOMÁTICA

### Una experiencia de compra simple, rápida y conectada.

**Factus Pay + Factus**

<br>

# 👥 EQUIPO

### **Juan David Merchan González**

### **Javier Alexander Buitrago Torres**

### **Samuel Andrés Rojas Escobar**

### **Reynel Felipe Amezquita Puentes**

<br>

🌐 **[PLATAFORMA ONLINE](https://saiayinesfactus.online/)**

<br>

[![Django](https://img.shields.io/badge/Django-6.1.1-092E20?style=for-the-badge\&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge\&logo=python)](https://www.python.org/)
[![Factus](https://img.shields.io/badge/Factus-API-orange?style=for-the-badge)](https://www.factus.com.co/)

</div>

---

## 🎯 ¿Qué construimos?

SAIAYIN es una plataforma web de comercio electrónico que conecta **el proceso de compra, el pago y la facturación electrónica en un único flujo**.

El usuario selecciona sus productos, realiza el pago mediante **Factus Pay** y, una vez confirmado el pago, la plataforma genera automáticamente la factura electrónica mediante **Factus**.

### 🔄 Flujo principal

```text
🛒 PRODUCTO
     ↓
🛍️ CARRITO
     ↓
💰 CHECKOUT
     ↓
🔗 FACTUS PAY
     ↓
📱 QR / PAGO
     ↓
✅ CONFIRMACIÓN
     ↓
🧾 FACTUS
     ↓
📄 FACTURA ELECTRÓNICA
```

El objetivo fue demostrar una integración real entre ambas APIs dentro de una aplicación funcional.

---

# ⚡ IMPLEMENTACIÓN

## 1. Clonar el repositorio

```bash
git clone https://github.com/Neo-meme/Hackaton.git
cd Hackaton
```

---

## 2. Crear el entorno virtual

Crear el entorno virtual dentro del proyecto:

```bash
python3 -m venv venv
```

Activarlo:

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Instalar las dependencias

Con el entorno virtual activo:

```bash
pip install -r requirements.txt
```

---

## 4. Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```text
Hackaton/
├── api/
├── config/
├── venv/
├── .env
├── manage.py
└── requirements.txt
```

El archivo `.env` debe contener las credenciales correspondientes al entorno Sandbox:

```env
FACTUS_URL=
FACTUS_CLIENT_ID=
FACTUS_CLIENT_SECRET=
FACTUS_USERNAME=
FACTUS_PASSWORD=

FACTUS_PAY_EMAIL=
FACTUS_PAY_PASSWORD=

FACTUS_RANGO_ID=
```

> ⚠️ **Nunca subir el archivo `.env` al repositorio.**
>
> Las credenciales utilizadas durante la Hackathon corresponden únicamente al entorno Sandbox.

---

# 🗄️ BASE DE DATOS

El proyecto utiliza **SQLite** para facilitar su ejecución y demostración.

Después de clonar el proyecto, ejecutar:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 👤 CREAR USUARIOS

Para crear los usuarios utilizados durante la demostración:

```bash
python manage.py shell
```

Dentro de la consola de Django:

```python
from django.contrib.auth.models import User

User.objects.create_user(
    username="admin",
    password="admin123",
    is_staff=True
)

User.objects.create_user(
    username="user",
    password="user123"
)
```

Salir:

```python
exit()
```

### 🔐 Credenciales de demostración

| Rol                 | Usuario | Contraseña |
| ------------------- | ------- | ---------- |
| 👨‍💼 Administrador | `admin` | `admin123` |
| 🛒 Cliente          | `user`  | `user123`  |

---

# ▶️ EJECUTAR EL PROYECTO

Con el entorno virtual activo:

```bash
python manage.py runserver
```

Abrir:

```text
http://127.0.0.1:8000/
```

La plataforma también se encuentra desplegada en:

### 🌐 https://saiayinesfactus.online/

---

# 💳 INTEGRACIÓN FACTUS PAY

La plataforma utiliza **Factus Pay** para crear y consultar los recaudos.

El proceso implementado es:

1. El cliente agrega productos al carrito.
2. Se calcula el total de la compra.
3. Se genera una referencia única.
4. Se crea el recaudo en Factus Pay.
5. Se obtiene el código QR.
6. El cliente realiza el pago en el entorno Sandbox.
7. La plataforma consulta el estado del recaudo.
8. Cuando el estado es `paid`, el pago se considera confirmado.

```text
Django
   │
   ├── Crear recaudo
   ↓
Factus Pay
   │
   ├── QR
   ↓
Cliente realiza el pago
   │
   ↓
Consultar estado
   │
   └── paid
```

---

# 🧾 INTEGRACIÓN FACTUS

Una vez confirmado el pago, la plataforma utiliza la API de **Factus** para generar automáticamente la factura electrónica.

El flujo implementado es:

```text
Pago confirmado
      ↓
Transacción → PAGADO
      ↓
Construcción del documento
      ↓
Factus API
      ↓
Factura validada
      ↓
Número de factura almacenado
      ↓
Consulta / descarga del PDF
```

La factura queda asociada a la transacción realizada por el cliente.

---

# 🛠️ FUNCIONALIDADES

### 👤 Cliente

* Inicio de sesión.
* Visualización de productos.
* Carrito de compras.
* Aumentar y disminuir cantidades.
* Checkout.
* Generación de recaudo.
* Pago mediante Factus Pay.
* Confirmación del pago.
* Generación automática de factura.
* Historial de compras.
* Consulta y descarga de factura.

### 👨‍💼 Administrador

* Gestión de productos.
* Crear productos.
* Editar productos.
* Eliminar productos.
* Visualizar todas las compras.
* Consultar transacciones.
* Verificar pagos.
* Acceder a las facturas generadas.

---

# 🧰 TECNOLOGÍAS

## Aplicación

* **Python 3.12**
* **Django 6.1.1**
* **SQLite**
* **HTML5**
* **CSS3**
* **Bootstrap**
* **Animate.css**
* **Requests**
* **Pillow**
* **python-dotenv**

## APIs

* **Factus Pay**
* **Factus**

## Servidor

* **Ubuntu Server**
* **Apache 2**
* **mod_wsgi**
* **Python Virtual Environment**
* **HTTPS / SSL mediante Let's Encrypt**
* **Dominio propio**

---

# 🌐 DESPLIEGUE

La aplicación se encuentra desplegada en un servidor Ubuntu mediante:

```text
Internet
   │
   ↓
saiayinesfactus.online
   │
   ↓
Apache
   │
   ↓
mod_wsgi
   │
   ↓
Django
   │
   ↓
SQLite
```

El servidor permite ejecutar la misma aplicación utilizada durante la demostración de la Hackathon.

---

# 🔐 SEGURIDAD

Las credenciales de las APIs **no forman parte del código fuente**.

Se utilizan variables de entorno mediante `.env`.

El repositorio contiene únicamente la estructura necesaria para ejecutar el proyecto.

> Para ejecutar la integración real es necesario proporcionar las credenciales Sandbox correspondientes.

---

# 🧪 ENTORNO SANDBOX

Toda la integración con Factus y Factus Pay fue desarrollada utilizando el **entorno Sandbox**, permitiendo realizar pruebas del flujo completo sin utilizar dinero real.

```text
Compra
  ↓
Factus Pay Sandbox
  ↓
Pago de prueba
  ↓
Confirmación
  ↓
Factus Sandbox
  ↓
Factura electrónica de prueba
```

---

# 👥 EQUIPO

Proyecto desarrollado durante **API WARS 2026** por estudiantes de Ingeniería de Sistemas.

### 💙 Nuestro objetivo

Como futuros ingenieros de sistemas, buscamos demostrar que una idea puede convertirse en una solución funcional cuando combinamos **aprendizaje, creatividad, tecnología y trabajo en equipo**.

---

# ❤️ AGRADECIMIENTO

> **Gracias, Halltec, por darnos el reto de convertir nuestras ideas en tecnología real. Como futuros ingenieros de sistemas, nos llevamos una experiencia retadora, en la que pusimos a prueba nuestra pasión, aprendizaje y conocimientos para construir una solución que nos acerca un paso más a la vida que soñamos tener. ¡La buena!**

---

<div align="center">

# 🚀 SAIAYIN

### Del reto → a la idea → al código → a una solución real.

**API WARS 2026**

🌐 **https://saiayinesfactus.online/**

</div>
