from base_bot import BaseBot
from rules import Rules

class Player(BaseBot):
    '''
    Name/Author : Harsh Gupta
    '''

    def choose_card(self, top_card):
        def parse_card(card):
            if not card or len(card) < 2:
                return None, None
            if card[0] in {'W', 'P'} and len(card) == 2:
                return card[1], card[0]
            return card[0], card[1:]
        
        current_color, current_value = parse_card(top_card)
        
        color_counts = {'R': 0, 'G': 0, 'B': 0, 'Y': 0}
        
        action_cards = 0
        number_cards = 0
        wild_cards = 0
        
        for card in self.hand:
            if card == "WC" or card == "PC":
                wild_cards += 1
                continue
                
            card_color, card_value = parse_card(card)
            if card_color in color_counts:
                color_counts[card_color] += 1
                
            if card_value in ['S', 'R', 'P']:
                action_cards += 1
            elif card_value.isdigit():
                number_cards += 1

        best_color = 'R'
        if any(color_counts.values()):
            best_color = max(color_counts.items(), key=lambda x: x[1])[0]
        
        playable_numbers = [] 
        playable_skips = [] 
        playable_reverses = [] 
        playable_draw2s = []  
        playable_wilds = [] 
        playable_plus4s = []

        for card in self.hand:
            if card == "WC":
                playable_wilds.append(card)
                continue
                
            if card == "PC":
                playable_plus4s.append(card)
                continue
            
            card_color, card_value = parse_card(card)
            
            matches_color = card_color == current_color
            matches_value = card_value == current_value
            
            if matches_color or matches_value:
                if card_value == 'S':
                    playable_skips.append(card)
                elif card_value == 'R':
                    playable_reverses.append(card)
                elif card_value == 'P':
                    playable_draw2s.append(card)
                else:
                    playable_numbers.append(card)

        playable_actions = playable_skips + playable_draw2s + playable_reverses

        if len(self.hand) == 1:
            if playable_numbers or playable_actions:
                return self.hand[0]
            if playable_wilds:
                return f"W{best_color}"
            if playable_plus4s:
                return f"P{best_color}"

        if len(self.hand) == 2:
            if playable_skips:
                return playable_skips[0]
            if playable_draw2s:
                return playable_draw2s[0]
            if playable_reverses:
                return playable_reverses[0]
            if playable_numbers:
                return max(playable_numbers, key=lambda card: int(parse_card(card)[1]) if parse_card(card)[1].isdigit() else 0)
            if playable_wilds:
                return f"W{best_color}"
            if playable_plus4s:
                return f"P{best_color}"

        if playable_skips:
            return playable_skips[0]
            
        if playable_draw2s:
            return playable_draw2s[0]
            
        if playable_reverses:
            return playable_reverses[0]
            
        if playable_numbers:
            if len(playable_numbers) > 1:
                color_groups = {}
                for card in playable_numbers:
                    color = card[0]
                    if color not in color_groups:
                        color_groups[color] = []
                    color_groups[color].append(card)
                
                if color_groups:
                    largest_group_color = max(color_groups.items(), key=lambda x: len(x[1]))[0]
                    if len(color_groups[largest_group_color]) > 1:
                        return max(color_groups[largest_group_color], 
                                  key=lambda card: int(parse_card(card)[1]) if parse_card(card)[1].isdigit() else 0)
            
            return max(playable_numbers, key=lambda card: int(parse_card(card)[1]) if parse_card(card)[1].isdigit() else 0)
            
        if playable_wilds:
            return f"W{best_color}"
        if playable_plus4s:
            return f"P{best_color}"
        return None

if __name__ == "__main__":
    try:
        bot = Player(player_id=0)
        print("Enter your hand as space-separated cards:")
        bot.hand = input().strip().split()
        print("Enter the top card:")
        top_card = input().strip()

        print(f"Hand: {bot.hand}")
        print(f"Top Card: {top_card}")
        
        move = bot.choose_card(top_card)
        print(f"Chosen card: {move}")
    except Exception as e:
        print(f"Error: {e}")
