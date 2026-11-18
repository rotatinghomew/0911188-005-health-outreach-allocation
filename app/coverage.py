from collections import Counter


def totals(contacts, cutoff):
    return dict(Counter(row['site'] for row in contacts if row['state'] == 'complete' and row['reported'] <= cutoff))
