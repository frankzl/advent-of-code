import re
import sys
import time
from collections import namedtuple
from functools import reduce
from typing import Dict, List, Set, Tuple

# Handy Haversacks
#
# - bags must be color-coded
# - bags must contain specific quantities of other color-coded bags
#
# - own bag is shiny gold
# - to carry it in at least one other bag, how many colors would eventually be valid for the outermost bag?
#
# Test code
# 1. bright white -> shiny gold
# 2. muted yellow -> shiny gold (+x)
# 3. dark orange -> bright white -> shiny gold
#                `-> muted yellow -> shiny gold
# 4. light red -> bright white -> shiny gold
#              `-> muted yellow -> shiny gold

# A) Read and parse rules, build bag container rule tree; important: allow traversal in both directions!

# parents: List[str], children: Dict[str, int]
BagRule = namedtuple("BagRule", ["parents", "children"])

bag_name_ptn = r"(\w|\s)+"


def parse_rule(rule_definition: str) -> Tuple[str, BagRule]:
    m1 = re.fullmatch(f"({bag_name_ptn})" r" bags contain (.+)\.", l[:-1])
    if not m1:
        raise ValueError()

    parent: str
    rule: str
    parent, _, rule = m1.groups()

    bag_rule: BagRule = BagRule(parents=[], children=dict())

    if rule == "no other bags":
        # Empty rule means no children defined
        return parent, bag_rule

    while rule:
        m2 = re.fullmatch(r"(\d+)" f" ({bag_name_ptn})" r" bags*(, (.+))*", rule)
        if not m2:
            raise ValueError()
        number: str
        kind: str
        # bag_name_ptn contains an extra group, and we are only interested in the inner group at the end
        number, kind, _, _, rule = m2.groups()

        # Save rule
        bag_rule.children[kind] = number

    # We are done when all rules have been parsed and saved into `bag_rule`
    return parent, bag_rule


t0 = time.perf_counter()

bag_containment: Dict[str, BagRule] = dict()

# First, we parse all in one direction (parent -> child)
# with open(sys.argv[1], "r") as f:
print("TEMP TEMP TEMP!")
with open("input7small", "r") as f:
    for l in f:
        parent: str
        rule: BagRule
        parent, rule = parse_rule(l[:-1])
        # We assume that only one rule line exists per parent
        bag_containment[parent] = rule

# Second, we add the (child -> parent) relationships

t1 = time.perf_counter()

for parent, rule in bag_containment.items():
    for child, _ in rule.children.items():
        bag_containment[child].parents.append(parent)


# B) Count the number.

t2 = time.perf_counter()

# First, we get all possible paths that end in shiny gold.

raise NotImplementedError()

# Second, we remove duplicates and count.

raise NotImplementedError()


from util import tf

print(
    f"Result: {0}\n\n"
    f"1-----------------------: {tf(t1-t0)}\n"
    f"2: {tf(t2-t1)}\n"
    f"Total: {tf(t2-t0)}"
)
