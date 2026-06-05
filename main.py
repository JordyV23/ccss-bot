from playwright.sync_api import sync_playwright
import time
import requests
from datetime import datetime
import pytz
import schedule
import os


# Configuración de Telegram desde variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

formulario_css = "https://serviciosweb.ccss.sa.cr/pls/APEXPRD/APEX/r/servicios_ccss/sgap361/formulario?session=4477887394136"

locaciones = [
    {
        "zona": "GAM / REGIÓN CENTRAL",
        "subzonas": [
            "ÁREA DE SALUD ASERRÍ",
            "ÁREA DE SALUD CARTAGO",
            "ÁREA DE SALUD TURRIALBA",
            "ÁREA DE SALUD DESAMPARADOS 3",
            "ÁREA DE SALUD GOICOECHEA 2",
            "ÁREA DE SALUD MATA REDONDA",
            "ÁREA DE SALUD MORA PALMICHAL",
            "ÁREA DE SALUD ZAPOTE CATEDRAL",
        ],
    },
    {
        "zona": "HEREDIA Y ALAJUELA",
        "subzonas": [
            "ÁREA DE SALUD ALAJUELA NORTE",
            "ÁREA DE SALUD TIBÁS URUCA MERCED",
            "ÁREA DE SALUD GRECIA",
            "ÁREA DE SALUD HEREDIA CUBUJUQUÍ",
        ],
    },
]


def enviar_notificacion_telegram(zona, subzona, fecha, horas):
    """Envía una notificación por Telegram cuando hay citas disponibles"""
    try:
        mensaje = (
            f"¡CITAS DISPONIBLES!\n\n"
            f"Zona: {zona}\n"
            f"Subzona: {subzona}\n"
            f"Fecha: {fecha}\n"
            f"Horas disponibles:\n"
        )
        for hora in horas:
            mensaje += f"   • {hora}\n"
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        datos = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": mensaje
        }
        response = requests.post(url, json=datos)
        if response.status_code == 200:
            print("✓ Notificación enviada a Telegram")
        else:
            print(f"✗ Error al enviar notificación: {response.status_code}")
    except Exception as e:
        print(f"✗ Error en Telegram: {e}")


def enviar_sin_citas_disponibles():
    """Envía una notificación por Telegram cuando NO hay citas"""
    try:
        mensaje = (
            "SIN CITAS DISPONIBLES\n\n"
            "No se encontraron citas disponibles en este momento.\n"
            "Se volverá a revisar en el próximo ciclo."
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        datos = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": mensaje
        }
        response = requests.post(url, json=datos)
        if response.status_code == 200:
            print("✓ Notificación (sin citas) enviada a Telegram")
        else:
            print(f"✗ Error al enviar notificación: {response.status_code}")
    except Exception as e:
        print(f"✗ Error en Telegram: {e}")


def esta_en_horario_valido():
    """Verifica si estamos dentro del horario de 6 AM a 8 PM (hora Costa Rica)"""
    tz_cr = pytz.timezone('America/Costa_Rica')
    hora_actual = datetime.now(tz_cr)
    hora_int = hora_actual.hour
    
    en_horario = 6 <= hora_int < 20
    estado = "✓ En horario" if en_horario else "✗ Fuera de horario"
    print(f"{estado} - Hora actual Costa Rica: {hora_actual.strftime('%H:%M:%S')}")
    
    return en_horario


def seleccionar_subzonas(page, zona, sub_zonas):
    resultados = []

    for sub_zona in sub_zonas:
        page.locator("select[name='P10_AREA_SEGUN_ZONA']").select_option(label=sub_zona)
        time.sleep(3)
        resultados.extend(validar_fechas(page, zona, sub_zona))
        return resultados


def validar_fechas(page, zona, subzona):

    resultados = []

    fechas = page.locator("#P10_FEC_CITA option")
    total_fechas = fechas.count()

    for i in range(1, total_fechas):  # omitir opción vacía
        fecha = fechas.nth(i).inner_text().strip()

        print(f"Revisando caso {zona} | {subzona} | {fecha}")

        page.locator("#P10_FEC_CITA").select_option(index=i)

        time.sleep(3)

        radios = page.locator("#P10_DSC_HORA_CITA .apex-item-option")

        if radios.count() == 0:
            continue

        texto = radios.first.inner_text().strip()

        # Caso sin citas
        if "ya gestionó todas las citas disponibles" in texto.lower():
            print("Ya se gestionaron todas las citas")
            continue

        horas = []

        for j in range(radios.count()):
            hora = radios.nth(j).inner_text().strip()

            if hora:
                horas.append(hora)

        resultado = {
            "zona": zona,
            "subzona": subzona,
            "fecha": fecha,
            "horas": horas,
        }

        resultados.append(resultado)

        # Enviar notificación por Telegram
        enviar_notificacion_telegram(zona, subzona, fecha, horas)

        print(f"{zona} | {subzona} | {fecha}")
        print(horas)

    return resultados


def main():
    todos_los_resultados = []

    # Verificar si estamos en horario válido
    if not esta_en_horario_valido():
        return

    print("\n🔍 Iniciando búsqueda de citas...\n")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto(formulario_css)
            time.sleep(5)
            for locacion in locaciones:
                page.locator("select[name='P10_ZONA_HABILITADA']").select_option(
                    label=locacion.get("zona")
                )

                time.sleep(5)
                sub_zonas = locacion.get("subzonas")
                resultados = seleccionar_subzonas(page, locacion.get("zona"), sub_zonas)
                
                todos_los_resultados.extend(resultados)
                
            print("\n=== RESUMEN DE BÚSQUEDA ===\n")

        if todos_los_resultados:
            print(f"✓ Se encontraron {len(todos_los_resultados)} coincidencias\n")
            for cita in todos_los_resultados:
                print(
                    f"{cita['zona']} | "
                    f"{cita['subzona']} | "
                    f"{cita['fecha']} | "
                    f"{', '.join(cita['horas'])}"
                )
        else:
            print("✗ No se encontraron citas disponibles")
            enviar_sin_citas_disponibles()
            
    except Exception as e:
        print(f"\n✗ Error durante la ejecución: {e}")
        mensaje_error = f"⚠️ ERROR EN EL BOT\n\n{str(e)}"
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            datos = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje_error}
            requests.post(url, json=datos)
        except Exception as e:
            print(e)


def ejecutar_en_loop():
    """Ejecuta el script en un loop continuamente usando schedule"""
    print("🤖 Bot iniciado - Ejecutando de 6 AM a 8 PM (Hora Costa Rica)")
    print("Presiona Ctrl+C para detener\n")
    
    # Programar la tarea cada 10 minutos entre las 6 AM y 8 PM
    schedule.every(10).minutes.do(main)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Revisar cada segundo si hay tarea pendiente
    except KeyboardInterrupt:
        print("\n\n👋 Bot detenido por el usuario")
        schedule.clear()  # Limpiar todas las tareas programadas


if __name__ == "__main__":
    ejecutar_en_loop()
