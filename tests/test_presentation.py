import pandas as pd
from cloudtrack.presentation import selection_insights
from cloudtrack.presentation import category_colors, style_chart
import plotly.express as px


def test_insights_use_only_delivered_and_handle_ties_and_zero_sales():
    frame = pd.DataFrame({
        'status': ['entregado', 'entregado', 'cancelado'],
        'category': ['Hogar', 'Moda', 'Omitida'],
        'city': ['La Paz', 'Tarija', 'Otra'],
        'amount_bob': [100, 100, 9999],
        'on_time': [True, False, False],
    })
    category, city = selection_insights(frame)
    assert category['names'] == 'Hogar, Moda'
    assert 'empate' in category['title']
    assert category['share'] == 50
    assert city['names'] == 'Tarija'
    assert city['value'] == 0
    # Al filtrar, el resumen debe describir solo las filas visibles.
    category, city = selection_insights(frame.iloc[:1])
    assert category['names'] == 'Hogar'
    assert category['share'] == 100
    assert city['value'] == 100
    frame.loc[:1, 'amount_bob'] = 0
    frame.loc[:1, 'on_time'] = True
    category, city = selection_insights(frame)
    assert category['share'] is None
    assert city['names'] == 'La Paz, Tarija'
    assert 'empate' in city['title']
    assert selection_insights(frame.iloc[2:]) == []
    assert selection_insights(frame.iloc[:0]) == []


def test_category_colors_are_deterministic_and_chart_values_are_preserved():
    names = ['Moda', 'Tecnología', 'Hogar', 'Deportes']
    colors = category_colors(names)
    assert colors == category_colors(reversed(names))
    assert len(set(colors.values())) == len(names)
    figure = px.bar(x=[20, 80], y=['La Paz', 'Tarija'], orientation='h')
    styled = style_chart(figure, percent=True, horizontal=True)
    assert list(styled.data[0].x) == [20, 80]
    assert list(styled.layout.xaxis.range) == [0, 105]
    assert styled.layout.xaxis.showgrid
    assert not styled.layout.yaxis.showgrid
