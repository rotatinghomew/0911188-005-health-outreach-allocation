import json
from .allocation import proposal
from .coverage import totals
from .inventory import balance


def run_workbench(action, directory, key, ledger):
    source = json.loads((directory / 'workbench.json').read_text())
    if action == 'coverage':
        return totals(source['contacts'], key or source['cutoff'])
    stock = balance(source['batches'], source['issues'])
    if action == 'stock':
        return stock
    counts = totals(source['contacts'], source['cutoff'])
    return proposal(source['sites'], counts, sum(stock.values()), source['reserves'], source['round_limit'])
