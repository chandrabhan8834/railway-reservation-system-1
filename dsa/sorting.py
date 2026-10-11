def merge_sort(items, key=lambda x: x):
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    return merge(left, right, key)


def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def sort_trains(trains, sort_by='departure_time'):
    # Sorting layer: This uses merge sort to sort trains by the selected field.
    if sort_by == 'fare':
        return merge_sort(trains, key=lambda t: float(t['fare']))
    if sort_by == 'arrival_time':
        return merge_sort(trains, key=lambda t: t['arrival_time'])
    if sort_by == 'available_seats':
        return merge_sort(trains, key=lambda t: int(t['available_seats']))
    return merge_sort(trains, key=lambda t: t['departure_time'])
