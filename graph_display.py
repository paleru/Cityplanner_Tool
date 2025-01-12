import plotly.graph_objects as go
import plotly.express as px
import dataframe_helper as dh


def colors(emission_sources):

    color_palette = colors_pie()

    return color_palette[emission_sources]


def colors_pie():

    color_palette = {
        "Waste And Sewage": "#FF6692",
        "Machinery": '#00CC96',
        "Electricity And District Heating": '#636EFA',
        "Other Heating": '#AB63FA',
        "Agriculture": '#FFA15A',
        "Industry": '#19D3F3',
        "Transportation": '#EF553B'
    }

    return color_palette


def bar(df, fig):

    emission_sources = [
        'Waste And Sewage', 'Machinery', 'Electricity And District Heating',
        'Other Heating', 'Agriculture', 'Transportation', 'Industry'
    ]

    for emission_source in emission_sources:
        if emission_source in df.columns:
            fig.add_trace(go.Bar(
                x=df.index,
                y=df[emission_source],
                name=emission_source,
                marker_color=colors(emission_source)
            ))

    fig.update_layout(
        barmode='stack',
        xaxis_title='Region',
        yaxis_title='Total Emissions in 2022 (kt CO2e)',
        margin=dict(l=22, r=22, t=3, b=22),
        legend_title='Emission Sources'
    )

    return fig


def pie(df, fig):

    fig = px.pie(
        df,
        values='Total Emissions 2022',
        names='Hinku calculation without emission credits',
        hole=.5,
        title='Total Emissions by Source (2022)',
        color='Hinku calculation without emission credits',
        color_discrete_map=colors_pie()
    )

    fig.update_traces(hovertemplate='%{label}', textinfo='none')
    fig.update_layout(showlegend=False)

    return fig


def line(df, input_value, fig):

    input_value_spec_rm = dh.replace_special_chars(input_value)

    df_before_2022 = df[df['Year'] <= 2022]
    df_after_2022 = df[df['Year'] >= 2022]

    # Create the figure with two line traces
    fig = go.Figure()

    # Add the trace for years from 2022 onwards
    fig.add_trace(go.Scatter(
        x=df_after_2022['Year'],
        y=df_after_2022[input_value_spec_rm],
        mode='lines+markers',
        name='Predicted Data',
        line=dict(color='red'),
        marker=dict(color='red')
    ))

    # Add the trace for years before 2022
    fig.add_trace(go.Scatter(
        x=df_before_2022['Year'],
        y=df_before_2022[input_value_spec_rm],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='blue'),
        marker=dict(color='blue')
    ))

    fig.update_layout(
        title=f'Total Yearly Emissions for {input_value.capitalize()}',
        xaxis=dict(
            title='Year',
            type='category',  # Treat 'Year' as a category
            categoryorder='array',
            categoryarray=sorted(df['Year'].unique(), key=lambda x: int(x))
        ),
        yaxis=dict(title='Total Emissions')
    )

    # marker_colors = ['red' if year > 2022 else 'blue' for year in df['Year']]

    # fig = px.line(
    #                 df,
    #                 x='Year',
    #                 y=input_value,
    #                 markers='o',
    #                 title=f'Total Yearly Emissions for {input_value.capitalize()}',
    #                 category_orders={'Year': sorted(df['Year'].unique(), key=lambda x: int(x))}  # Ensures years are sorted correctly
    #             )

    # fig.update_traces(marker=dict(color=marker_colors))

    # fig.update_xaxes(
    #                 type='category',  # Treat 'Year' as a category
    #                 #tickangle=75
    #             )

    # fig.update_layout(yaxis_title = 'Total Emissions')
    return fig


def pie_city(df, input_value, fig):
    fig = px.pie(
        df,
        values='Emissions',
        names='Source',
        hole=.5,
        title=f'Emissions by Sector in {input_value.capitalize()} in 2022',
        color='Source',
        color_discrete_map=colors_pie()
    )

    fig.update_traces(hovertemplate='%{label}', textinfo='none')  # remove percentages from figure
    # fig.update_layout(width=700, height=500)

    return fig


def tree_co2(df, fig):
    fig.add_trace(go.Bar(
        x=df["Tree"],
        y=df["Average CO2 Consumption"],
        name="Average CO2 Consumption",
        marker_color='#a7d2ac'
    ))
    fig.update_layout(
        title='Average CO2 Consumption by Tree Species',
        xaxis_title='Trees',
        yaxis_title='Average CO2 Consumption'
    )

    return fig


def tree_rec(df, input_value, fig):
    fig.add_trace(go.Bar(
        x=df["Tree"],
        y=df['Recommended Tree Amount'],
        name='Recommended Tree Amount',
        text=df['Recommended Tree Amount'],
        textposition='inside',
        insidetextanchor='middle',
        marker_color='#8eb892'  # 5d8e62
    ))
    fig.add_trace(go.Bar(
        x=df["Tree"],
        y=df['Recommended Tree Amount with Net Offset'],
        name='Recommended Tree Amount with Net Offset',
        text=df['Recommended Tree Amount with Net Offset'],
        textposition='inside',
        insidetextanchor='middle',
        marker_color='#5d8e62'  # 5d8e62
    ))
    fig.update_layout(
        title=f'Tree Amount Needed to Offset Emissions for Predicted Year by Species for {
            str(input_value.capitalize())}',
        font=dict(
                    family='Open Sans, verdana, arial, sans-serif',
                    size=12,  # Set the font size here
                    color="#000000"
        )
    )

    return fig
