# RPA - Verificador de Citas CCSS 🏥

Bot automatizado que verifica la disponibilidad de citas en el sistema CCSS de Costa Rica y notifica por Telegram.

## 🚀 Características

- ✅ Revisa citas cada 10 minutos
- ✅ Se ejecuta de 6 AM a 8 PM (hora Costa Rica)
- ✅ Notifica por Telegram cuando hay citas disponibles
- ✅ Notifica cuando NO hay citas
- ✅ Se ejecuta en GitHub Actions (sin necesidad de servidor)
- ✅ Manejo de errores con notificaciones

## 📋 Requisitos Previos

1. Crear un bot en Telegram:
   - Habla con [@BotFather](https://t.me/botfather) en Telegram
   - Crea un nuevo bot y obtén el TOKEN
   - Copia el token (ejemplo: `8790717161:AAERUviXMIhAkwkW_AosQZCB-ZeZmoG68jo`)

2. Obtener tu CHAT_ID:
   - Habla con [@userinfobot](https://t.me/userinfobot) en Telegram
   - Copia tu ID numérico

## 🔧 Configuración en GitHub Actions

### 1. Pushear el código a GitHub

```bash
git init
git add .
git commit -m "Agregar bot CCSS"
git remote add origin https://github.com/tu_usuario/rpa-vacuna.git
git branch -M main
git push -u origin main
```

### 2. Agregar Secrets en GitHub

Ve a tu repositorio → **Settings** → **Secrets and variables** → **Actions**

Agrega dos secrets:

| Nombre | Valor |
|--------|-------|
| `TELEGRAM_TOKEN` | Tu token del bot |
| `TELEGRAM_CHAT_ID` | Tu CHAT_ID |

### 3. ¡Listo! ✅

El workflow se ejecutará automáticamente cada 10 minutos. Puedes:

- Ver los logs en **Actions** → **RPA - Verificar Citas CCSS**
- Ejecutarlo manualmente: **Actions** → **RPA - Verificar Citas CCSS** → **Run workflow**

## 🖥️ Ejecución Local

Si quieres ejecutar en tu computadora:

```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python main.py
```

## 📊 Horario de Ejecución

- **Inicio:** 6:00 AM (Hora Costa Rica)
- **Fin:** 8:00 PM (Hora Costa Rica)
- **Intervalo:** Cada hora
- **Zona Horaria:** UTC-6 (América/Costa_Rica)

## 🔍 Zonas Monitoreadas

### GAM / REGIÓN CENTRAL
- ÁREA DE SALUD ASERRÍ
- ÁREA DE SALUD CARTAGO
- ÁREA DE SALUD TURRIALBA
- ÁREA DE SALUD DESAMPARADOS 3
- ÁREA DE SALUD GOICOECHEA 2
- ÁREA DE SALUD MATA REDONDA
- ÁREA DE SALUD MORA PALMICHAL
- ÁREA DE SALUD ZAPOTE CATEDRAL

### HEREDIA Y ALAJUELA
- ÁREA DE SALUD ALAJUELA NORTE
- ÁREA DE SALUD TIBÁS URUCA MERCED
- ÁREA DE SALUD GRECIA
- ÁREA DE SALUD HEREDIA CUBUJUQUÍ

## 📬 Notificaciones

Recibirás mensajes en Telegram como:

### ✅ Con citas disponibles:
```
🎉 ¡CITAS DISPONIBLES!

📍 Zona: GAM / REGIÓN CENTRAL
🏥 Subzona: ÁREA DE SALUD CARTAGO
📅 Fecha: 10 de junio de 2026
⏰ Horas disponibles:
   • 08:00 AM - 09:00 AM
   • 02:00 PM - 03:00 PM
```

### ❌ Sin citas disponibles:
```
❌ SIN CITAS DISPONIBLES

No se encontraron citas disponibles en este momento.
Se volverá a revisar en el próximo ciclo.
```

## 🐛 Solución de Problemas

### El workflow no se ejecuta
- Verifica que los Secrets están configurados correctamente
- Revisa que el código está en la rama `main`
- GitHub Actions puede tener retrasos en la ejecución

### No recibo notificaciones
- Verifica que el TELEGRAM_CHAT_ID es correcto (usa @userinfobot)
- Confirma que el bot tiene permiso para enviarte mensajes
- Inicia una conversación con el bot primero

### Errores de Playwright
- GitHub Actions instala automáticamente los navegadores
- Si aún hay errores, revisa los logs en **Actions**

## 📝 Personalización

Para cambiar el intervalo de tiempo (ahora es cada hora):

**En `.github/workflows/rpa-citas.yml`**, modifica la línea del cron:

```yaml
- cron: '*/15 * * * *'  # Cambiar a cada 15 minutos
```

Para cambiar el horario (ahora 6 AM - 8 PM):

**En `main.py`**, modifica la función `esta_en_horario_valido()`:

```python
en_horario = 8 <= hora_int < 18  # Cambiar a 8 AM - 6 PM
```

## 📄 Licencia

Proyecto de uso personal

## 🤝 Soporte

Si tienes problemas, revisa:
1. Los logs en GitHub Actions
2. Que los Secrets están correctos
3. Que tienes permisos en el repositorio
