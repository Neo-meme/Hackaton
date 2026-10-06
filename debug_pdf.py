from api.factus.facturas import descargar_pdf

contenido, nombre = descargar_pdf("SETP990023521")
print("Nombre:", nombre, "| bytes:", len(contenido))
with open("/tmp/prueba.pdf", "wb") as f:
    f.write(contenido)
