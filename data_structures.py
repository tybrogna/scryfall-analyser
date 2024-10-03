class TypeAndRarityCount:
    def __init__(self, set_name):
        self.set = set_name
        self.white = ColorCount('white')
        self.blue = ColorCount('blue')
        self.black = ColorCount('black')
        self.red = ColorCount('red')
        self.green = ColorCount('green')
        self.double = ColorCount('double')
        self.triple = ColorCount('triple')
        self.more = ColorCount('more')
        self.colorless = ColorCount('colorless')
        self.double_faced = ColorCount('two faces')

    def check_card(self, card):
        if card['type_line'].startswith('Basic'):
            return
        colors = []
        if 'colors' not in card:
            for c in card['card_faces'][0]['colors']:
                if c not in colors:
                    colors.append(c)
            for c in card['card_faces'][1]['colors']:
                if c not in colors:
                    colors.append(c)
        else:
            colors = card['colors']
        num_colors = len(colors)
        if num_colors == 0:
            self.colorless.check_type_and_rarity(card, False)
        elif num_colors == 1:
            match colors[0]:
                case 'W': self.white.check_type_and_rarity(card)
                case 'U': self.blue.check_type_and_rarity(card)
                case 'B': self.black.check_type_and_rarity(card)
                case 'R': self.red.check_type_and_rarity(card)
                case 'G': self.green.check_type_and_rarity(card)
        elif num_colors == 2:
            self.double.check_type_and_rarity(card)
        elif num_colors == 3:
            self.triple.check_type_and_rarity(card)
        else:
            self.more.check_type_and_rarity(card)

    def format(self):
        first_row = self.white.format()
        first_row[0] = self.set
        set_data = [first_row, self.blue.format(), self.black.format(), self.red.format(), self.green.format(),
                    self.double.format(), self.triple.format(), self.more.format(), self.colorless.format(),
                    self.double_faced.format()]
        return set_data

    def format_rarity(self):
        first_row = self.white.format_rarity()
        first_row[0] = self.set
        set_data = [first_row, self.blue.format_rarity(), self.black.format_rarity(), self.red.format_rarity(), self.green.format_rarity(),
                    self.double.format_rarity(), self.triple.format_rarity(), self.more.format_rarity(), self.colorless.format_rarity(),
                    self.double_faced.format_rarity()]
        return set_data

    def format_type(self):
        first_row = self.white.format_type()
        first_row[0] = self.set
        set_data = [first_row, self.blue.format_type(), self.black.format_type(), self.red.format_type(), self.green.format_type(),
                    self.double.format_type(), self.triple.format_type(), self.more.format_type(), self.colorless.format_type(),
                    self.double_faced.format_type()]
        return set_data


class ColorCount:
    def __init__(self, color=None):
        self.color = color
        self.mythic = 0
        self.rare = 0
        self.uncommon = 0
        self.common = 0
        self.creature = 0
        self.sorcery = 0
        self.enchantment = 0
        self.artifact = 0
        self.planeswalker = 0
        self.instant = 0
        self.battle = 0
        self.land = 0
        self.double_faced = 0

    def check_type_and_rarity(self, card, test=False):
        if card['type_line'].startswith('Basic'):
            return
        if test:
            print(card['rarity'])
            print(card['type_line'])
            if ' ' in card['type_line']:
                type = card['type_line'][0:card['type_line'].index('—') - 1]
        match card['rarity']:
            case 'common':
                self.common += 1
            case 'uncommon':
                self.uncommon += 1
            case 'rare':
                self.rare += 1
            case 'mythic':
                self.mythic += 1
        if 'card_faces' in card:
            self.double_faced += 1
            self.check_type(card['type_line'][0])
            self.check_type(card['type_line'][1])
        else:
            self.check_type(card['type_line'])

    def check_type(self, card_type_line):
        if '—' in card_type_line:
            card_type_line = card_type_line[0:card_type_line.index('—')-1]
        card_type_line = card_type_line.lower()
        if 'creature' in card_type_line:
            self.creature += 1
        if 'sorcery' in card_type_line:
            self.sorcery += 1
        if 'enchantment' in card_type_line:
            self.enchantment += 1
        if 'artifact' in card_type_line:
            self.artifact += 1
        if 'planeswalker' in card_type_line:
            self.planeswalker += 1
        if 'instant' in card_type_line:
            self.instant += 1
        if 'battle' in card_type_line:
            self.battle += 1
        if 'land' in card_type_line:
            self.land += 1

    def format(self):
        ret_val = [' ',
                   self.color, self.mythic, self.rare, self.uncommon, self.common,
                   '|', self.creature, self.sorcery, self.enchantment, self.artifact, self.planeswalker, self.instant, self.battle, self.land,
                   '|', self.double_faced]
        return ret_val

    def format_rarity(self):
        ret_val = [' ',
                   self.color, self.mythic, self.rare, self.uncommon, self.common]
        return ret_val

    def format_type(self):
        ret_val = [' ',
                   self.creature, self.sorcery, self.enchantment, self.artifact, self.planeswalker,
                   self.instant, self.battle, self.land, self.double_faced]
        return ret_val



class ColorIdentityCount:
    def __init__(self, set_code):
        self.set = set_code
        self.white = 0
        self.blue = 0
        self.black = 0
        self.red = 0
        self.green = 0
        self.azorius_wu = 0
        self.dimir_ub = 0
        self.rakdos_br = 0
        self.gruul_rg = 0
        self.selesnya_wg = 0
        self.orzhov_wb = 0
        self.izzet_ur = 0
        self.golgari_bg = 0
        self.boros_rw = 0
        self.simic_ug = 0
        self.bant_gwu = 0
        self.esper_wub = 0
        self.grixis_urb = 0
        self.jund_brg = 0
        self.naya_rgw = 0
        self.abzan_wbg = 0
        self.jeskai_urw = 0
        self.sultai_bgu = 0
        self.mardu_rwb = 0
        self.temur_gur = 0
        self.non_white = 0
        self.non_blue = 0
        self.non_black = 0
        self.non_red = 0
        self.non_green = 0
        self.five_color = 0
        self.colorless = 0

    def check_card(self, card):
        if card['type_line'].startswith('Basic'):
            return
        ci = card['color_identity']
        ci.sort()
        match ci:
            case ['W']:
                self.white += 1
            case ['U']:
                self.blue += 1
            case ['B']:
                self.black += 1
            case ['R']:
                self.red += 1
            case ['G']:
                self.green += 1
            case ['U', 'W']:
                self.azorius_wu += 1
            case ['B', 'U']:
                self.dimir_ub += 1
            case ['B', 'R']:
                self.rakdos_br += 1
            case ['G', 'R']:
                self.gruul_rg += 1
            case ['G', 'W']:
                self.selesnya_wg += 1
            case ['B', 'W']:
                self.orzhov_wb += 1
            case ['R', 'U']:
                self.izzet_ur += 1
            case ['R', 'W']:
                self.boros_rw += 1
            case ['B', 'G']:
                self.golgari_bg += 1
            case ['G', 'U']:
                self.simic_ug += 1
            case ['G', 'U', 'W']:
                self.bant_gwu += 1
            case ['B', 'U', 'W']:
                self.esper_wub += 1
            case ['B', 'R', 'U']:
                self.grixis_urb += 1
            case ['B', 'G', 'R']:
                self.jund_brg += 1
            case ['G', 'R', 'W']:
                self.naya_rgw += 1
            case ['B', 'G', 'W']:
                self.abzan_wbg += 1
            case ['R', 'U', 'W']:
                self.jeskai_urw += 1
            case ['B', 'G', 'U']:
                self.sultai_bgu += 1
            case ['B', 'R', 'W']:
                self.mardu_rwb += 1
            case ['G', 'R', 'U']:
                self.temur_gur += 1
            case ['B', 'G', 'R', 'U']:
                self.non_white += 1
            case ['B', 'G', 'R', 'W']:
                self.non_blue += 1
            case ['G', 'R', 'U', 'W']:
                self.non_black += 1
            case ['B', 'G', 'U', 'W']:
                self.non_red += 1
            case ['B', 'R', 'U', 'W']:
                self.non_green += 1
            case ['B', 'G', 'R', 'U', 'W']:
                self.five_color += 1
            case _:
                self.colorless += 1

    def format_one(self):
        ret_val = [self.set,
                   self.white, self.blue, self.black, self.red, self.green,
                   self.colorless]
        return ret_val

    def format_two(self):
        ret_val = [self.set,
                   self.azorius_wu, self.dimir_ub, self.rakdos_br, self.gruul_rg, self.selesnya_wg,
                   self.orzhov_wb, self.izzet_ur, self.boros_rw, self.golgari_bg, self.simic_ug]
        return ret_val

    def format_three(self):
        ret_val = [self.set,
                   self.bant_gwu, self.esper_wub, self.grixis_urb, self.jund_brg, self.naya_rgw,
                   self.abzan_wbg, self.jeskai_urw, self.sultai_bgu, self.mardu_rwb, self.temur_gur]
        return ret_val

    def format_the_rest(self):
        ret_val = [self.set,
                   self.non_white, self.non_blue, self.non_black, self.non_red, self.non_green,
                   self.five_color]
        return ret_val

    def format(self):
        ret_val = [' ',
                   self.white, self.blue, self.black, self.red, self.green,
                   self.azorius_wu, self.dimir_ub, self.rakdos_br, self.gruul_rg, self.selesnya_wg,
                   self.orzhov_wb, self.izzet_ur, self.boros_rw, self.golgari_bg, self.simic_ug,
                   self.bant_gwu, self.esper_wub, self.grixis_urb, self.jund_brg, self.naya_rgw,
                   self.abzan_wbg, self.jeskai_urw, self.sultai_bgu, self.mardu_rwb, self.temur_gur,
                   self.non_white, self.non_blue, self.non_black, self.non_red, self.non_green,
                   self.five_color, self.colorless]
        return ret_val


def get_rarity_color_fields():
    return ['white', 'blue', 'black', 'red', 'green',
            'double', 'triple', 'more', 'colorless', 'double_faced']
    # keys = list(self.set_rarities[0].__dict__.keys())
    # keys.remove('set')
    # return keys


def get_type_color_fields():
    return ['white', 'blue', 'black', 'red', 'green',
            'double', 'triple', 'more', 'colorless', 'double_faced']


def get_ci_one_color_fields():
    return ['white', 'blue', 'black', 'red', 'green', 'colorless']


def get_ci_two_color_fields():
    return ['azorius_wu', 'dimir_ub', 'rakdos_br', 'gruul_rg', 'selesnya_wg',
            'orzhov_wb', 'izzet_ur', 'golgari_bg', 'boros_rw', 'simic_ug']


def get_ci_three_color_fields():
    return ['bant_gwu', 'esper_wub', 'grixis_urb', 'jund_brg', 'naya_rgw',
            'abzan_wbg', 'jeskai_urw', 'sultai_bgu', 'mardu_rwb', 'temur_gur']


def get_ci_four_plus_color_fields():
    return ['non_white', 'non_blue', 'non_black', 'non_red', 'non_green', 'five_color']


class TabulatedSetData:
    def __init__(self):
        self.set_rarities = []
        self.set_types = []
        self.set_cis = []
        self.set_cards_analyzed_count = []
        self.tabulate_rarity = []
        self.tabulate_types = []
        self.tabulate_one_color = []
        self.tabulate_two_color = []
        self.tabulate_three_color = []
        self.tabulate_four_plus_color = []

    def fill_tabulate_data(self, scryfall_sets_data):
        for set_code, cards in scryfall_sets_data.items():
            set_rarity_and_type_data = TypeAndRarityCount(set_code)
            set_ci_data = ColorIdentityCount(set_code)
            self.set_cards_analyzed_count.append(len(cards))
            for card in cards:
                set_rarity_and_type_data.check_card(card)
                set_ci_data.check_card(card)
            self.tabulate_rarity.extend(set_rarity_and_type_data.format_rarity())
            self.tabulate_types.extend(set_rarity_and_type_data.format_type())
            self.tabulate_one_color.append(set_ci_data.format_one())
            self.tabulate_two_color.append(set_ci_data.format_two())
            self.tabulate_three_color.append(set_ci_data.format_three())
            self.tabulate_four_plus_color.append(set_ci_data.format_the_rest())
            self.set_types.append(set_rarity_and_type_data)
            self.set_rarities.append(set_rarity_and_type_data)
            self.set_cis.append(set_ci_data)
