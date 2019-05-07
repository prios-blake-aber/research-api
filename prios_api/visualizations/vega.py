
import pandas as pd
import altair as alt


def plot_timeseries_from_df(
    df: pd.DataFrame = None, x: str = None, y: str = None, title: str = None,
    notebook_render=False
):
    assert (
        isinstance(df, pd.DataFrame) and not df.empty and x and y
    ), 'Must specify dataframe and column names for x, y axes!'

    if notebook_render:
        alt.renderers.enable('notebook')

    chart = alt.Chart(df)
    return chart.mark_line().encode(
        x=x,
        y=y
    ).properties(title=title)
