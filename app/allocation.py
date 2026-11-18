def proposal(sites, counts, available, reserves, limit):
    if sum(reserves.values()) > available:
        raise ValueError('实际库存无法满足既有预留')
    extras = max(0, min(limit, available - sum(reserves.values())))
    priority = sorted((row['id'] for row in sites), key=lambda key: (-counts.get(key, 0), key))
    return {'reserved': reserves, 'extra': {priority[0]: extras} if priority and extras else {}}
