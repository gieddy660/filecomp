import argparse
from collections import defaultdict
# we assume that dicts are ordered -
#  newly added elements are at the end of the dict


def get_rows(current_row):
    global rows_dict1  # not necessary, just to signal that it modifies rows_dict1
    res = []
    current_index = KeyError('all elements were None')
    for row_index, val in rows_dict1[current_row].items():
        if val is not None:
            current_index = row_index
            break
    while rows_dict1[current_row][current_index] is not None:
        res.append((current_index, current_row))
        t = rows_dict1[current_row][current_index]
        rows_dict1[current_row][current_index] = None
        current_row = t
        current_index -= 1
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='text compare tool')
    parser.add_argument('path1', help='path of file 1')
    parser.add_argument('path2', help='path of file 2')
    parser.add_argument('-m', '--middle', type=int, default=70, help='position of the middle line')
    parser.add_argument('--rows1', type=int, default=4, help='digits of max line-count of file 1')
    parser.add_argument('--rows2', type=int, default=4, help='digits of max line-count of file 2')
    args = parser.parse_args()
    path1 = args.path1
    path2 = args.path2
    mid_position = args.middle
    max_row1l = args.rows1
    max_row2l = args.rows2

    with open(path1, 'r') as f1, open(path2, 'r') as f2:
        rows_dict1 = defaultdict(dict)
        rows_dict1[0] = {-1: None}  # dummy row for the second part
        t = 0
        for index, row in enumerate(f1):
            rows_dict1[row][index] = t
            t = row
        last_row, last_index = row, index

        for index, row in enumerate(f2):
            if row in rows_dict1 and any(None is not val for val in rows_dict1[row].values()):
                rows_to_print = get_rows(row)
                for ind_, row_ in reversed(rows_to_print[1:]):  # could be done without slicing, just being lazy
                    print('{: >{ns1}}: {: <{size}}-|{:+>{size2}}'.format(ind_, row_.rstrip(), '',
                                                                         size=mid_position - 1,
                                                                         size2=mid_position + max_row2l + 2,
                                                                         ns1=max_row1l))
                ind_, row_ = rows_to_print[0]
                print('{: >{ns1}}: {: <{size}}| {: >{ns2}}: {}'.format(ind_, row_.rstrip(),
                                                                       index, row.rstrip(),
                                                                       size=mid_position,
                                                                       ns1=max_row1l, ns2=max_row2l))
            else:
                print('{:+>{size}}|+{: >{ns2}}: {}'.format('', index, row.rstrip(),
                                                           size=mid_position+max_row1l+2, ns2=max_row2l))

        if rows_dict1[last_row][last_index] is not None:
            rows_to_print = get_rows(last_row)
            for ind_, row_ in reversed(rows_to_print):
                print('{: >{ns1}}: {: <{size}}-|{:+>{size2}}'.format(ind_, row_.rstrip(), '',
                                                                     size=mid_position - 1,
                                                                     size2=mid_position + max_row2l + 2,
                                                                     ns1=max_row1l))
