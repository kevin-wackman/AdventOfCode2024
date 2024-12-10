from filehandling import open_data_file_as_lines
DATA_FILE = "day5in.txt"

def main():
    lines = open_data_file_as_lines(DATA_FILE)
    (rules, updates) = parse_lines_into_rules_updates(lines)
    part_1_sum = 0
    part_2_sum = 0
    for update in updates:
        n = score_line(rules, update)
        if n > 0:
            part_1_sum += n
        else:
            part_2_sum += score_incorrect_line(rules, update)
    print(part_1_sum)
    print(part_2_sum)

# This works on the assumption that the line is incorrect.
def score_incorrect_line(rules, update):
    sorted_list = partition_list(rules, update)
    return sorted_list[(len(sorted_list) - 1)//2]

def partition_list(rules, update):
    if len(update) <= 1:
        return update
    base = update[0]
    prereqs = []
    postreqs = []
    for val in update[1:]:
        if val in rules[base]:
            prereqs.append(val)
        else:
            postreqs.append(val)
    return partition_list(rules, prereqs) + [base] + partition_list(rules, postreqs)

def score_line(rules, update):
    if not is_valid_line(rules, update):
        return 0
    return update[(len(update) - 1)//2]

def is_valid_line(rules, update):
    if len(update) <= 1:
        return True
    for n in update[1:]:
        if n in rules[update[0]]:
            return False
    return is_valid_line(rules, update[1:])

def parse_lines_into_rules_updates(lines):
    in_rules = True
    rules = {}
    updates = []
    # Maintain the rules as tracking what pages cannot be after a given page.
    for line in lines:
        if in_rules:
            if len(line) < 4:
                in_rules = False
            else:
                pair = line.split('|')
                (x,y) = (int(pair[0]),int(pair[1]))
                if y not in rules:
                    rules[y] = []
                rules[y].append(x)
        else:
            print_order = [int(x) for x in line.split(',')]
            updates.append(print_order)
    return (rules, updates)




main()