import json
from tabulate import tabulate
import data_structures as ds


def get_rarity_targets():
    return ['mythic', 'rare', 'uncommon', 'common']


def get_type_targets():
    return ['creature', 'artifact', 'enchantment', 'planeswalker',
             'instant', 'sorcery', 'battle', 'land', 'double_faced']


def get_ci_one_targets():
    return ['White', 'Blue', 'Black', 'Red', 'Green', 'Colorless']


def get_ci_double_targets():
    return ['Azorius W/U', 'Dimir U/B', 'Rakdos B/R', 'Gruul R/G', 'Selesnya W/G',
            'Orzhov W/B', 'Izzet U/R', 'Golgari B/G', 'Boros R/W', 'Simic U/G']


def get_ci_triple_targets():
    return ['Bant G/W/U', 'Esper W/U/B', 'Grixis U/B/R', 'Jund B/R/G', 'Naya R/G/W',
            'Abzan W/B/G', 'Jeskai U/R/W', 'Sultai B/G/U', 'Mardu R/W/B', 'Temur G/U/R']


def get_ci_four_or_more_targets():
    return ['Non-White', 'Non-Blue', 'Non-Black', 'Non-Red', 'Non-Green', 'Five Color']

def __card_already_found(cards, new_card):
    for card in cards:
        if card['name'] == new_card['name']:
            return True
    return False  # skip cards names already collected


def list_of_cards_in_sets(scryfall_all_cards, set_names):
    compiled_data = {}
    for s in set_names:
        compiled_data[s] = []
    for card in scryfall_all_cards:  # for each card
        if card['set'] not in set_names: continue  # skip cards not in relevant sets
        if __card_already_found(compiled_data[card['set']], card): continue  # skip cards names already collected
        if 'paper' not in card['games']: continue  # skip digital only cards and alters
        compiled_data[card['set']].append(card)
    return compiled_data


def avg_func(all_sets, color, *attrs):
    avgs = []
    for a in attrs:
        avg = sum(getattr(getattr(s, color), a) for s in all_sets) / len(all_sets)
        avgs.append(f'{avg:.2f}')
    return avgs


def cis_avg(all_sets, *colors):
    avgs = []
    for color in colors:
        avg = sum(getattr(s, color) for s in all_sets) / len(all_sets)
        avgs.append(f'{avg:.1f}')
    return avgs


def get_list_of_avgs(data_list, targets, color_find_list):
    processed_lists = []
    for color in color_find_list:
        new_list = [color]
        new_list.extend(avg_func(data_list, color, *targets))
        processed_lists.append(new_list)
    return processed_lists


def test_func(scryfall_all_cards):
    ts = list_of_cards_in_sets(scryfall_all_cards, ['one'])
    trc = ds.TypeAndRarityCount('one')
    for card in ts['one']:
        trc.check_card(card)


if __name__ == "__main__":
    with open('default-cards.json', 'r', encoding='utf-8') as json_cards:
        scryfall_all_cards = json.load(json_cards)
    draft_booster_set_names = ['eld', 'thb', 'iko', 'm21', 'znr', 'khm', 'stx', 'mh2', 'afr', 'mid', 'vow', 'neo', 'snc', 'dmu', 'bro', 'one', 'mom', 'ltr', 'woe', 'lci']
    play_booster_set_names = ['mkm', 'otj', 'mh3', 'blb']
    # test_func(scryfall_all_cards)
    draft_booster_sets_and_cards = list_of_cards_in_sets(scryfall_all_cards, draft_booster_set_names)
    play_booster_sets_and_cards = list_of_cards_in_sets(scryfall_all_cards, play_booster_set_names)
    tnr_headers = ['set', 'color', 'mythic', 'rare', 'uncommon', 'common', '|', 'creature', 'sorcery', 'enchantment',
                   'artifact', 'planeswalker', 'instant', 'battle', 'land', '|', 'double face']
    rarity_headers = ['set', 'color', 'mythic', 'rare', 'uncommon', 'common']
    type_headers = ['set', 'color', 'creature', 'sorcery', 'enchantment',
                    'artifact', 'planeswalker', 'instant', 'battle', 'land', 'double face']
    ci_one_headers = ['set', 'White', 'Blue', 'Black', 'Red', 'Green', 'colorless']
    ci_two_headers = ['Azorius W/U', 'Dimir U/B', 'Rakdos B/R', 'Gruul R/G', 'Selesnya W/G',
                      'Orzhov W/B', 'Izzet U/R', 'Golgari B/G', 'Boros R/W', 'Simic U/G']
    ci_three_headers = ['Bant G/W/U', 'Esper W/U/B', 'Grixis U/B/R', 'Jund B/R/G', 'Naya R/G/W',
                        'Abzan W/B/G', 'Jeskai U/R/W', 'Sultai B/G/U', 'Mardu R/W/B', 'Temur G/U/R']
    ci_the_rest_headers = ['Non-White', 'Non-Blue', 'Non-Black', 'Non-Red', 'Non-Green', 'Five Color']

    draft_booster_processed_data = ds.TabulatedSetData()
    draft_booster_processed_data.fill_tabulate_data(draft_booster_sets_and_cards)
    play_booster_processed_data = ds.TabulatedSetData()
    play_booster_processed_data.fill_tabulate_data(play_booster_sets_and_cards)

    # IO functions start here
    with open('draft_booster_results.txt', 'w') as file:
        draft_rarity_analysis = tabulate(draft_booster_processed_data.tabulate_rarity, headers=rarity_headers)
        draft_type_analysis = tabulate(draft_booster_processed_data.tabulate_types, headers=type_headers)
        draft_one_color_analysis = tabulate(draft_booster_processed_data.tabulate_one_color, headers=ci_one_headers)
        draft_two_color_analysis = tabulate(draft_booster_processed_data.tabulate_two_color, headers=ci_two_headers)
        draft_three_color_analysis = tabulate(draft_booster_processed_data.tabulate_three_color, headers=ci_three_headers)
        draft_the_rest_analysis = tabulate(draft_booster_processed_data.tabulate_four_plus_color, headers=ci_the_rest_headers)
        file.write('Rarities\n')
        file.write(draft_rarity_analysis)
        file.write('\n\n\n')
        file.write('Types\n')
        file.write(draft_type_analysis)
        file.write('\n\n\n')
        file.write('One Color\n')
        file.write(draft_one_color_analysis)
        file.write('\n\n\n')
        file.write('Two Color\n')
        file.write(draft_two_color_analysis)
        file.write('\n\n\n')
        file.write('Three Color\n')
        file.write(draft_three_color_analysis)
        file.write('\n\n\n')
        file.write('Four or More Color\n')
        file.write(draft_the_rest_analysis)

    with open('play_booster_results.txt', 'w') as file:
        play_rarity_analysis = tabulate(play_booster_processed_data.tabulate_rarity, headers=rarity_headers)
        play_type_analysis = tabulate(play_booster_processed_data.tabulate_types, headers=type_headers)
        play_one_color_analysis = tabulate(play_booster_processed_data.tabulate_one_color, headers=ci_one_headers)
        play_two_color_analysis = tabulate(play_booster_processed_data.tabulate_two_color, headers=ci_two_headers)
        play_three_color_analysis = tabulate(play_booster_processed_data.tabulate_three_color, headers=ci_three_headers)
        play_the_rest_analysis = tabulate(play_booster_processed_data.tabulate_four_plus_color, headers=ci_the_rest_headers)
        file.write('Rarity\n')
        file.write(play_rarity_analysis)
        file.write('\n\n\n')
        file.write('Types\n')
        file.write(play_type_analysis)
        file.write('\n\n\n')
        file.write('One Color\n')
        file.write(play_one_color_analysis)
        file.write('\n\n\n')
        file.write('Two Color\n')
        file.write(play_two_color_analysis)
        file.write('\n\n\n')
        file.write('Three Color\n')
        file.write(play_three_color_analysis)
        file.write('\n\n\n')
        file.write('Four or More Color\n')
        file.write(play_the_rest_analysis)

    with open('draft_analysis.txt', 'w') as file:
        # rarity averages
        # rarity_targets = ['mythic', 'rare', 'uncommon', 'common']
        rarity_targets = get_rarity_targets()
        rarity_fields = ds.get_rarity_color_fields()
        rarity_avgs = get_list_of_avgs(draft_booster_processed_data.set_rarities, rarity_targets, rarity_fields)
        rarity_targets.insert(0, 'color')
        file.write(tabulate(rarity_avgs, headers=rarity_targets))
        file.write('\n\n\n')
        # type averages
        # type_targets = ['creature', 'sorcery', 'enchantment', 'artifact', 'planeswalker', 'instant', 'battle', 'land', 'double_faced']
        type_targets = get_type_targets()
        type_fields = ds.get_type_color_fields()
        type_avgs = get_list_of_avgs(draft_booster_processed_data.set_types, type_targets, type_fields)
        type_targets.insert(0, 'color')
        file.write(tabulate(type_avgs, headers=type_targets))
        file.write('\n\n\n')
        # Color Identity Averages
        ci_one_targets = get_ci_one_targets()
        ci_one_fields = ds.get_ci_one_color_fields()
        ci_one_avgs = cis_avg(draft_booster_processed_data.set_cis, *ci_one_fields)
        file.write(tabulate([ci_one_avgs], headers=ci_one_targets))
        file.write('\n\n\n')
        ci_two_targets = get_ci_double_targets()
        ci_two_fields = ds.get_ci_two_color_fields()
        ci_two_avgs = cis_avg(draft_booster_processed_data.set_cis, *ci_two_fields)
        file.write(tabulate([ci_two_avgs], headers=ci_two_targets))
        file.write('\n\n\n')
        ci_three_targets = get_ci_triple_targets()
        ci_three_fields = ds.get_ci_three_color_fields()
        ci_three_avgs = cis_avg(draft_booster_processed_data.set_cis, *ci_three_fields)
        file.write(tabulate([ci_three_avgs], headers=ci_three_targets))
        file.write('\n\n\n')
        ci_four_targets = get_ci_four_or_more_targets()
        ci_four_fields = ds.get_ci_four_plus_color_fields()
        ci_four_avgs = cis_avg(draft_booster_processed_data.set_cis, *ci_four_fields)
        file.write(tabulate([ci_four_avgs], headers=ci_four_targets))

    with open('play_analysis.txt', 'w') as file:
        rarity_targets = get_rarity_targets()
        rarity_fields = ds.get_rarity_color_fields()
        rarity_avgs = get_list_of_avgs(play_booster_processed_data.set_rarities, rarity_targets, rarity_fields)
        rarity_targets.insert(0, 'color')
        file.write(tabulate(rarity_avgs, headers=rarity_targets))
        file.write('\n\n\n')
        type_targets = get_type_targets()
        type_fields = ds.get_type_color_fields()
        type_avgs = get_list_of_avgs(play_booster_processed_data.set_types, type_targets, type_fields)
        type_targets.insert(0, 'color')
        file.write(tabulate(type_avgs, headers=type_headers))
        file.write('\n\n\n')
        # Color Identity Averages
        ci_one_targets = get_ci_one_targets()
        ci_one_fields = ds.get_ci_one_color_fields()
        ci_one_avgs = cis_avg(play_booster_processed_data.set_cis, *ci_one_fields)
        file.write(tabulate([ci_one_avgs], headers=ci_one_targets))
        file.write('\n\n\n')
        ci_two_targets = get_ci_double_targets()
        ci_two_fields = ds.get_ci_two_color_fields()
        ci_two_avgs = cis_avg(play_booster_processed_data.set_cis, *ci_two_fields)
        file.write(tabulate([ci_two_avgs], headers=ci_two_targets))
        file.write('\n\n\n')
        ci_three_targets = get_ci_triple_targets()
        ci_three_fields = ds.get_ci_three_color_fields()
        ci_three_avgs = cis_avg(play_booster_processed_data.set_cis, *ci_three_fields)
        file.write(tabulate([ci_three_avgs], headers=ci_three_targets))
        file.write('\n\n\n')
        ci_four_targets = get_ci_four_or_more_targets()
        ci_four_fields = ds.get_ci_four_plus_color_fields()
        ci_four_avgs = cis_avg(play_booster_processed_data.set_cis, *ci_four_fields)
        file.write(tabulate([ci_four_avgs], headers=ci_four_targets))
