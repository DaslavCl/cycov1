import streamlit as st
import csv
import os
import sys

def main():


    # Solicitar la ruta de la carpeta al usuario
    folder = st.text_input("Por favor, ingrese la ruta de la carpeta donde se encuentran las imágenes")

    # Solicitar SKU al usuario
    user_input_sku = st.text_input("Por favor, ingrese el SKU inicial (Debe comenzar con 'SKU')")

    # Solicitar la carga al usuario
    user_input_carga = st.text_input("Por favor, ingrese el número de la carga")

    # Solicitar color de la polera al usuario
    color = st.selectbox("Por favor, elige el color de la polera", options=["Blanco", "Negro"])

    # Cuando se presione el botón, proceder con la generación del archivo CSV
    if st.button("Generar CSV"):
        # Verificar si SKU es válido
        if user_input_sku and user_input_sku.startswith('SKU') and len(user_input_sku) > 3:
            # Extraer el número del SKU y convertirlo a un entero
            sku = int(user_input_sku[3:])
        else:
            st.error("Por favor, introduce un SKU válido.")
            return

        if not os.path.isdir(folder):
            st.error("La ruta proporcionada no es válida o no se puede acceder a ella.")
            return

        # Definir las variantes de tallas
        sizes = ['S', 'M', 'L', 'XL', 'XXL', '10', '12', '14']

        # Abra el archivo CSV en modo escritura
        with open('product-bulk-load-CARGA{}.csv'.format(user_input_carga), 'w', newline='') as file:
            writer = csv.writer(file)
            # Escribir la fila de encabezado
            writer.writerow(["SKU_PADRE", "SKU_HIJO", "PRODUCTO", "DESCRIPCION", "MODELO", "MARCA", "CATEGORIA", "COLOR", "TAMANO", "TEMPORADA", "ANCHO", "LARGO", "ALTO", "PESO", "POSICION", "CANTIDAD_BODEGA_MERCADOLIBRE_FULLFILMENT", "CANTIDAD_BODEGA_ONLINE", "MONEDA", "PRECIO_VENTA", "PRICING_PRICE_WITH_DISCOUNT", "TAGS"])

            # Crear una lista de los nombres de los archivos en la carpeta
            filenames = [filename for filename in os.listdir(folder) if filename.endswith('.jpg') or filename.endswith('.png')]

            # Recorrer todos los archivos en la lista
            for filename in filenames:
                # Incrementar el SKU para el próximo archivo
                sku += 1
                # Para cada tamaño, crear una entrada
                for i, size in enumerate(sizes, start=1):
                    # Crear un nuevo nombre de archivo basado en el SKU y la talla
                    new_filename = 'p-SK{}-{}.jpg'.format(sku, i)
                    # Si estamos en la primera talla, renombrar el archivo
                    if size == sizes[0]:
                        os.rename(os.path.join(folder, filename), os.path.join(folder, new_filename))
                    # Escribir una nueva fila en el archivo CSV
                    writer.writerow(['SK{}'.format(sku), '', filename.split('.')[0], 'Descripción {}'.format(sku), 'Modelo {}'.format(sku), 'Marca', 'Poleras', color, size, '', '20', '25', '5', '0.25', '5', '0', '30', 'CLP', '15500', '0', 'CARGA{}'.format(user_input_carga)])

        st.success('Archivo de carga masiva generado con éxito.')

if __name__ == "__main__":
    main()
