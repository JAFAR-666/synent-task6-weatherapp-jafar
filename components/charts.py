import plotly.express as px
import pandas as pd


def create_temperature_chart(forecast_data):

    records = []

    for item in forecast_data["list"][:10]:

        records.append(
            {
                "Date": item["dt_txt"],
                "Temperature": item["main"]["temp"]
            }
        )

    df = pd.DataFrame(records)

    fig = px.line(
        df,
        x="Date",
        y="Temperature",
        title="Temperature Forecast"
    )

    return fig