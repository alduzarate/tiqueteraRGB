import random
import subprocess
from gpiozero import Button
from signal import pause
from pathlib import Path

NOMBRE_IMPRESORA = "Zebra_GC420t"

# GPIO BCM 17.
# Cableado esperado: botón entre GPIO 17 y GND
GPIO_BOTON = 17

# Evita doble impresión si el botón rebota o si alguien lo mantiene presionado
imprimiendo = False

def leer_adjetivos(nombre_archivo):
    ruta = Path(nombre_archivo)

    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {nombre_archivo}")

    adjetivos = []
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            palabra = linea.strip()

            if palabra:
                adjetivos.append(palabra)

    if not adjetivos:
        raise ValueError(f"El archivo {nombre_archivo} está vacío o no contiene palabras válidas.")

    return adjetivos


def obtener_terna_adjetivos():
    return (
        random.choice(leer_adjetivos("adjetivosR.txt")),
        random.choice(leer_adjetivos("adjetivosG.txt")),
        random.choice(leer_adjetivos("adjetivosB.txt"))
    )


def generar_zpl(terna):
    palabra_r, palabra_g, palabra_b = terna

    return f"""
^XA

^FO165,0^GFA,935,935,11,,:::T04,P03I0E,P07I0C,P07801C18,P0E001C38,P0F0038383,O01E003078F,O01C007071F,O03C0070E1D,O0380060C39C,O07I0E1C39C,O0F700E3871C,O0FF00ED8738,O0FF31C3873,O0FE31C3073,O0EE79C3077,N01ECF1C303E,N01CCE1C301C,I0CK08CE1C308,001FL09C1C31,003F8001C09C1C3A,003F80CFC01C1C9C1,007F80IF01C1F8018,00FF00IF01C070038,00FF00IF00CJ078,01FE0073C007J07,01FE003O0FI08,01FC7018N0E001C,03FC7C18M01E001C,03FC7E18M01C001C,03FCFE08M03C001C,03FCFE08M038003C,03F8FE0C0180600380038,07F8FE0803C0F10780038,07F8FE0C0FC0F387I038,07F8FE0C0FC0F787I078,07F0FE041F61FF8F007F8,07F0FE441E6BFF8F01E78,07F0FE443C7IF8F03C7,07F1FE443C78FF1F07C7,07F1FF4C7C781F1E078F,07F1FFC878781E1E0F8F,07F1FFC878F83E1E0F9F0807F3FFC878E83E1E0F1F0807F3FFD878E03C1E1F371807FE7FF878E03C1E1F373,03FE7FF879E03C0EAF63E,03FC7FF879C03C0FEFC1C,01FC3FF87FC01C0FCF8,01FC1FF03F8J018,00FC0FC00E,,:U04,:T024,P0180364,M0800380D6C,M0C00243978,M0E00247278,M0F0074F66,M07C074FC,M07F078F8,M03FC78F,N0IF080FC,N07FF8FBF8,N01IFE7C,O03FF8FF8,S0FF,Q0147E,Q01F,Q0198,R0CC,R0E4,R0FE,R032,,::::^FS

^FO165,100^A0N,30,30^FD{palabra_r}^FS
^FO165,145^A0N,30,30^FD{palabra_g}^FS
^FO165,190^A0N,30,30^FD{palabra_b}^FS

^XZ"""

# Envío a impresora

def imprimir_zpl(zpl):
    subprocess.run(
        ["lp", "-d", NOMBRE_IMPRESORA, "-o", "raw"],
        input=zpl,
        text=True,
        check=True
    )


# Monitoreo del botón

def ejecutar_impresion():
    global imprimiendo

    if imprimiendo:
        print("Ya se está imprimiendo una etiqueta.")
        return

    imprimiendo = True

    try:
        print("Botón presionado. Generando etiqueta...")

        terna = obtener_terna_adjetivos()
        zpl = generar_zpl(terna)
        print(zpl)
        imprimir_zpl(zpl)

        print("Etiqueta enviada a la impresora.")

    except Exception as error:
        print(f"Error durante la impresión: {error}")

    finally:
        imprimiendo = False


if __name__ == "__main__":
    ejecutar_impresion()  # Para pruebas sin botón
    # boton = Button(GPIO_BOTON, pull_up=True, bounce_time=0.3)

    # boton.when_pressed = ejecutar_impresion

    # print("Sistema listo.")
    # print(f"Esperando botón en GPIO {GPIO_BOTON}...")

    # pause()