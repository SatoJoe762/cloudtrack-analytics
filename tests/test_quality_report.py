import json
from pathlib import Path
import subprocess
import sys

import pytest
from scripts.quality_report import build_report

ROOT = Path(__file__).resolve().parents[1]
CSV = '''order_id,order_date,city,category,amount_bob,shipping_cost_bob,status,promised_date,delivered_date
A,2026-01-01,La Paz,Hogar,100,10,entregado,2026-01-03,2026-01-03
B,2026-01-02,Santa Cruz,Moda,200,20,entregado,2026-01-04,2026-01-06
C,2026-01-03,La Paz,Hogar,900,10,cancelado,2026-01-05,
'''


def run_report(*args):
    return subprocess.run([sys.executable, '-m', 'scripts.quality_report', *map(str, args)],
                          cwd=ROOT, capture_output=True, text=True, timeout=30)


def test_report_totals_dates_and_delays_match_manual_calculation():
    report = build_report(CSV.encode())
    assert report['validation'] == 'passed'
    assert report['orders'] == 3
    assert report['order_dates'] == {'from': '2026-01-01', 'to': '2026-01-03'}
    assert report['cities'] == {'La Paz': 2, 'Santa Cruz': 1}
    assert report['categories'] == {'Hogar': 2, 'Moda': 1}
    assert report['statuses'] == {'cancelado': 1, 'en_transito': 0, 'entregado': 2}
    for dimension in ['cities', 'categories', 'statuses']:
        assert sum(report[dimension].values()) == report['orders']
    assert report['metrics']['revenue_bob'] == 300
    assert report['metrics']['on_time_pct'] == 50
    assert report['delivery_delays'] == {'late_deliveries': 1, 'average_delay_days': 2}


def test_cli_json_and_human_output_do_not_modify_csv(tmp_path):
    source = tmp_path / 'orders.csv'
    source.write_bytes(CSV.encode())
    result = run_report(source, '--json')
    assert result.returncode == 0, result.stderr
    assert not result.stderr
    assert json.loads(result.stdout) == build_report(CSV.encode())
    human = run_report(source)
    assert human.returncode == 0, human.stderr
    assert 'Pedidos: 3' in human.stdout
    assert 'Entregados tardíos: 1' in human.stdout
    assert '2.00 días' in human.stdout
    assert source.read_bytes() == CSV.encode()


@pytest.mark.parametrize('invalid', [b'foo\nbar\n', CSV.replace('B,2026', 'A,2026').encode()])
def test_cli_rejects_invalid_file_without_reporting_success(tmp_path, invalid):
    source = tmp_path / 'invalid.csv'
    source.write_bytes(invalid)
    result = run_report(source, '--json')
    assert result.returncode == 2
    assert result.stdout == ''
    assert 'No se pudo generar el reporte' in result.stderr
    assert 'Traceback' not in result.stderr


def test_cli_missing_file_is_controlled(tmp_path):
    result = run_report(tmp_path / 'does-not-exist.csv')
    assert result.returncode == 2
    assert result.stdout == ''
    assert 'No se pudo generar el reporte' in result.stderr


def test_default_demo_report_is_valid_json():
    result = run_report('--json')
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    expected = build_report((ROOT / 'data/orders_demo.csv').read_bytes())
    assert report == expected
    assert sum(report['statuses'].values()) == report['orders']
    assert report['delivery_delays']['late_deliveries'] <= report['metrics']['delivered']
