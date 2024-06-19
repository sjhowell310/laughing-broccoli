# from __future__ import annotations
# from collections import Counter
# combos = []
# for i in range(6):
#     for j in range(6):
#         for k in range(6):
#             for l in range(6):
#                 for m in range(6):
#                     for n in range(6):
#                         combos.append(
#                             ''.join(
#                                 sorted(
#                                     [
#                                         str(i + 1), str(j + 1), str(k + 1),
#                                         str(l + 1), str(m + 1), str(n + 1),
#                                     ],
#                                 ),
#                             ),
#                         )
#                     combos.append(
#                         ''.join(
#                             sorted([
#                                 str(i + 1), str(j + 1), str(k + 1),
#                                 str(l + 1), str(m + 1),
#                             ]),
#                         ),
#                     )
#                 combos.append(
#                     ''.join(
#                         sorted([str(i + 1), str(j + 1), str(k + 1), str(l + 1)]),
#                     ),
#                 )
#             combos.append(
#                 ''.join(sorted([str(i + 1), str(j + 1), str(k + 1)])),
#             )
#         combos.append(
#             ''.join(sorted([str(i + 1), str(j + 1)])),
#         )
#     combos.append(
#         ''.join(sorted([str(i + 1)])),
#     )
# super_combo_dict = {i+1: {} for i in range(6)}
# for combo in combos:
#     if not super_combo_dict.get(len(combo)).get(combo, {}):
#         super_combo_dict[len(combo)][combo] = {}
#         count = Counter()
#         for digit in combo:
#             count[digit] += 1
#         super_combo_dict[len(combo)][combo]['count'] = count
#     super_combo_dict[len(combo)][combo]['commonality'] = super_combo_dict.get(
#         len(combo),
#     ).get(combo, {}).get('commonality', 0) + 1
# score_dict = {}
# for i, combo_dict in super_combo_dict.items():
#     for combo, deets in combo_dict.items():
#         score = 0
#         if all(count == 2 for count in deets['count'].values()) and len(deets['count'].values()) == 3:
#             super_combo_dict[i][combo]['score'] = super_combo_dict.get(
#                 i,
#             ).get(combo, {}).get('score', 0) + 1500
#         if len(deets['count'].values()) == 6:
#             super_combo_dict[i][combo]['score'] = super_combo_dict.get(
#                 i,
#             ).get(combo, {}).get('score', 0) + 1500
#         for value, count in deets['count'].items():
#             if count == 6:
#                 if value != '1':
#                     super_combo_dict[i][combo]['score'] = super_combo_dict.get(
#                         i,
#                     ).get(combo, {}).get('score', 0) + 4000
#                 else:
#                     super_combo_dict[i][combo]['score'] = super_combo_dict.get(
#                         i,
#                     ).get(combo, {}).get('score', 0) + 8000
#             if count == 5:
#                 if value != '1':
#                     super_combo_dict[i][combo]['score'] = super_combo_dict.get(
#                         i,
#                     ).get(combo, {}).get('score', 0) + 2000
#                 else:
#                     super_combo_dict[i][combo]['score'] = super_combo_dict.get(
#                         i,
#                     ).get(combo, {}).get('score', 0) + 4000
#             if count == 4:
#                 if value != '1':
#                     super_combo_dict[i][combo]['score'] = super_combo_dict.get(
#                         i,
#                     ).get(combo, {}).get('score', 0) + 1000
#                 else:
#                     super_combo_dict[i][combo]['score'] = super_combo_dict.get(
#                         i,
#                     ).get(combo, {}).get('score', 0) + 2000
#             if count == 3:
#                 if value != '1':
#                     super_combo_dict[i][combo]['score'] = super_combo_dict.get(
#                         i,
#                     ).get(combo, {}).get('score', 0) + (100 * int(value))
#                 else:
#                     super_combo_dict[i][combo]['score'] = super_combo_dict.get(
#                         i,
#                     ).get(combo, {}).get('score', 0) + 1000
#             if (
#                 count in (1, 2)
#                 and not (all(count == 2 for count in deets['count'].values()) and len(deets['count'].values()) == 3)
#                 and not len(deets['count'].values()) == 6
#             ):
#                 if value == '1':
#                     super_combo_dict[i][combo]['score'] = super_combo_dict.get(
#                         i,
#                     ).get(combo, {}).get('score', 0) + 100 * count
#                 elif value == '5':
#                     super_combo_dict[i][combo]['score'] = super_combo_dict.get(
#                         i,
#                     ).get(combo, {}).get('score', 0) + 50 * count
#         if not super_combo_dict.get(i).get(combo).get('score', 0):
#             super_combo_dict[i][combo]['score'] = 0
#         if score_dict.get(super_combo_dict.get(i).get(combo, {}).get('score', 0), {}).get('rolls', []):
#             score_dict[
#                 super_combo_dict.get(i).get(
#                     combo, {},
#                 ).get('score', 0)
#             ]['rolls'].append(combo)
#         else:
#             score_dict[
#                 super_combo_dict.get(i).get(
#                     combo, {},
#                 ).get('score', 0)
#             ] = {}
#             score_dict[
#                 super_combo_dict.get(i).get(
#                     combo, {},
#                 ).get('score', 0)
#             ]['rolls'] = [combo]
# for score, _ in score_dict.items():
#     score_dict[score]['count'] = len(score_dict[score]['rolls'])
#     score_dict[score]['count']
# print({k[0]: k[1] for k in sorted(super_combo_dict.items())})
# print({k[0]: k[1] for k in sorted(score_dict.items())})
# # print({k[0]: k[1] for k in sorted(score_dict.items(), key=lambda x: x[1]["count"])})
from __future__ import annotations
