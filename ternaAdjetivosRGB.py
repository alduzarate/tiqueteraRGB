import random
import subprocess


def leer_adjetivos(nombre_archivo):
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
        ^FO80,80^A0N,40,40^FD{palabra_r}^FS
        ^FO80,140^A0N,40,40^FD{palabra_g}^FS
        ^FO80,200^A0N,40,40^FD{palabra_b}^FS
        ^XZ
        """


def imprimir_zpl(nombre_impresora, zpl):
    subprocess.run(
        ["lp", "-d", nombre_impresora, "-o", "raw"],
        input=zpl,
        text=True,
        check=True
    )


terna = obtener_terna_adjetivos()
zpl = generar_zpl(terna)
print(zpl)

# imprimir_zpl("Zebra_GC420t", zpl)