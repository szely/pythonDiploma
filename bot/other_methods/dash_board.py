import plotly.graph_objects as go
import os

y_list = [2451, 2, -397, 68, 132, -10]
x_list = ['Плановая<br>доходность', 'Парк', 'Выполнение<br>плана погрузки', 'Средняя ставка<br>на 1 груж в/о',
          'Порожние<br>ваг/отпр', 'Средняя ставка<br>на 1 пор в/о', 'Фактическая<br>доходность']
def paint_waterfall_chart(x_list, y_list, name):
    total = round(sum(y_list))
    y_list.append(total)

    text_list = []
    for index, item in enumerate(y_list):
        if item > 0 and index != 0 and index != len(y_list) - 1:
            text_list.append(f'+{str(y_list[index])}')
        else:
            text_list.append(str(y_list[index]))
    for index, item in enumerate(text_list):
        if item[0] == '+' and index != 0 and index != len(text_list) - 1:
            text_list[index] = '<span style="color:#2ca02c">' + text_list[index] + '</span>'
        elif item[0] == '-' and index != 0 and index != len(text_list) - 1:
            text_list[index] = '<span style="color:#d62728">' + text_list[index] + '</span>'
        if index == 0 or index == len(text_list) - 1:
            text_list[index] = '<b>' + text_list[index] + '</b>'

    dict_list = []
    for i in range(0, 2500, 250):
        dict_list.append(dict(
                type="line",
                line=dict(
                    color="#666666",
                    dash="dot"
                ),
                x0=-0.5,
                y0=i,
                x1=6,
                y1=i,
                line_width=1,
                layer="below"))

    fig = go.Figure(go.Waterfall(
        name = "e-commerce", orientation = "v",
        measure = ["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
        x = x_list,
        y = y_list,
        text = text_list,
        textposition = "outside",
        connector = {"line":{"color":'rgba(0,0,0,0)'}},
        increasing = {"marker":{"color":"#2ca02c"}},
        decreasing = {"marker":{"color":"#d62728"}},
        totals={'marker':{"color":"#9467bd"}},
        textfont={"family":"Open Sans, light",
                "color":"black"
                }
    ))

    fig.update_yaxes(range=[1000, 2700])
    fig.update_layout(
        title =
            {'text':'<b>Waterfall chart</b><br><span style="color:#666666">Факторный анализ влияния показателей на доходность</span>'},
        showlegend = False,
        height=650,
        font={
            'family':'Open Sans, light',
            'color':'black',
            'size':14
        },
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="руб./ваг./сут.",
        shapes=dict_list
    )
    fig.update_xaxes(tickangle=-45, tickfont=dict(family='Open Sans, light', color='black', size=14))
    fig.update_yaxes(tickangle=0, tickfont=dict(family='Open Sans, light', color='black', size=14))

    # fig.show()

    fig.write_image(f"{name}.png")


paint_waterfall_chart(x_list, y_list, 1111111)