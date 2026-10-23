import pandas as pd
from cloudtrack.presentation import selection_insights


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
