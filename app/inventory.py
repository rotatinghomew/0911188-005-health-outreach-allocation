def balance(batches, issues):
    remaining = {row['id']: row['received'] for row in batches}
    used = set()
    for row in issues:
        if row['id'] in used:
            continue
        used.add(row['id'])
        remaining[row['batch']] -= row['units']
        if remaining[row['batch']] < 0:
            raise ValueError('批次库存不足')
    return remaining
