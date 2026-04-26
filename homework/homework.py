"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


import os
import pandas as pd

def clean_campaign_data():
    input_path = "files/input"
    output_path = "files/output"
    os.makedirs(output_path, exist_ok=True)

    # Leer todos los .csv.zip y concatenarlos
    files = [f for f in os.listdir(input_path) if f.endswith(".csv.zip")]
    dfs = []

    for f in files:
        full_path = os.path.join(input_path, f)
        df = pd.read_csv(full_path, compression="zip")
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)

    # Crear client_id
    df["client_id"] = range(len(df))

    # -------------------------
    # client.csv
    # -------------------------
    client = pd.DataFrame()
    client["client_id"] = df["client_id"]
    client["age"] = df["age"]

    client["job"] = df["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)

    client["marital"] = df["marital"]

    client["education"] = df["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].replace("unknown", pd.NA)

    client["credit_default"] = (df["credit_default"] == "yes").astype(int)
    client["mortgage"] = (df["mortgage"] == "yes").astype(int)

    # -------------------------
    # campaign.csv
    # -------------------------
    campaign = pd.DataFrame()
    campaign["client_id"] = df["client_id"]
    campaign["number_contacts"] = df["number_contacts"]
    campaign["contact_duration"] = df["contact_duration"]
    campaign["previous_campaign_contacts"] = df["previous_campaign_contacts"]

    campaign["previous_outcome"] = (df["previous_outcome"] == "success").astype(int)
    campaign["campaign_outcome"] = (df["campaign_outcome"] == "yes").astype(int)

    month_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }

    campaign["last_contact_date"] = (
        "2022-" +
        df["month"].map(month_map) + "-" +
        df["day"].astype(str).str.zfill(2)
    )

    # -------------------------
    # economics.csv
    # -------------------------
    economics = pd.DataFrame()
    economics["client_id"] = df["client_id"]
    economics["cons_price_idx"] = df["cons_price_idx"]
    economics["euribor_three_months"] = df["euribor_three_months"]

    # -------------------------
    # Guardar archivos
    # -------------------------
    client.to_csv(os.path.join(output_path, "client.csv"), index=False)
    campaign.to_csv(os.path.join(output_path, "campaign.csv"), index=False)
    economics.to_csv(os.path.join(output_path, "economics.csv"), index=False)
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    return


if __name__ == "__main__":
    clean_campaign_data()