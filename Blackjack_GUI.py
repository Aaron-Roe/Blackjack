import pygame
from Blackjack import Game, Card


pygame.init()

# Audio commands 
pygame.mixer.init()  
pygame.mixer.music.load("Audio/BJ_music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
card_sound = pygame.mixer.Sound("Audio/flipcard.mp3")

# Sets caption, display size, font for the game
pygame.display.set_caption("Blackjack Game")

width, height = 1400, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Creates the background for the game and scales it to our display size
table_bg = pygame.image.load("Blackjack_images/table_bg.jpeg")
table_bg = pygame.transform.scale(table_bg, (width, height))

game = Game()  
round_active = False
round_over = False

# Plays card flipping sound
def play_card_sound():
    card_sound.play()

# Storage for all the card images  
card_images = {}  

# Button images dictionary for normal and pressed states
button_images = {
    "doubleDown": {
        "normal": pygame.image.load("Buttons/doubleDown_button_blue.png"),
        "pressed": pygame.image.load("Buttons/doubleDown_button_blue_fade.png")
    },
    "hit": {
        "normal": pygame.image.load("Buttons/hit_button_blue.png"),
        "pressed": pygame.image.load("Buttons/hit_button_blue_fade.png")
    },
    "split": {
        "normal": pygame.image.load("Buttons/split_button_blue.png"),
        "pressed": pygame.image.load("Buttons/split_button_blue_fade.png")
    },
    "stand": {
        "normal": pygame.image.load("Buttons/stand_button_blue.png"),
        "pressed": pygame.image.load("Buttons/stand_button_blue_fade.png")
    },
    "play": {
        "normal": pygame.image.load("Buttons/play_button_blue.png"),
        "pressed": pygame.image.load("Buttons/play_button_blue_fade.png")
    },
    "undoBet": {
        "normal": pygame.image.load("Buttons/undobet_button_blue.png"),
        "pressed": pygame.image.load("Buttons/undobet_button_blue_fade.png")
    }
}

# Tracks button press to determine when to show pressed version and how long it shows for
press_time = {}
FADE_DURATION = 500

# Chip values with images
chip_values = [5, 10, 50, 100]
chip_images = {}
for i in chip_values:
    key = str(i)
    chip_images[key] = {
        "normal": pygame.image.load(f"Chips/chip_{i}.png"),
        "pressed": pygame.image.load(f"Chips/chip_{i}_fade.png")
    }

player_wager = 0
busted_message = ""

# Creates images dictionary for quick card image access
face_values = {"J": "jack", "Q": "queen", "K": "king", "A": "ace"}
def load_card_images():
    images = {}

    for rank in [str(num) for num in range(2, 11)]:
        for i in Card.Suits:
            key = f"{rank}_{i.lower()}"
            images[key] = pygame.image.load(f"Blackjack_images/{key}.png")

    for i in face_values.items():
        suit = i[1]
        valid_suits = ["clubs", "hearts", "spades", "diamonds"]
        for i in valid_suits:
            key = f"{suit}_{i}"
            images[key] = pygame.image.load(f"Blackjack_images/{key}.png")
    images["back_of_card"] = pygame.image.load("Blackjack_images/back_card.png")
    return images

# Helper functio for text in game 
def draw_text(text, x, y, size=24, color=(255, 255, 255)):
    font = pygame.font.Font('freesansbold.ttf', size)
    word = font.render(text, True, color)
    screen.blit(word, (x, y))


card_images = load_card_images()

# Helper function for rendering game hands 
def render_hand(hand, x, y):
    for i in enumerate(hand):
        x_shift = i[0]
        card = i[1]
        rank_key = face_values.get(card.rank, card.rank.lower())
        key = f"{rank_key}_{card.suit.lower()}"
        img = card_images.get(key)
        screen.blit(img, (x + x_shift * 100, y))

# Logic for Dealer hand in seperating cards each deal so cards are offsetting
def render_dealer_hand(x, y, show_cards=False):
    face_values = {"J": "jack", "Q": "queen", "K": "king", "A": "ace"}
    dealer_hand = game.dealer.hand[0]
    for i in range(len(dealer_hand)):
        if i == 1 and show_cards == False:
            back_card = card_images.get("back_of_card")
            screen.blit(back_card, (x + i * 100, y + 40))
        else:
            card = dealer_hand[i]
            rank = face_values.get(card.rank, card.rank.lower())
            key = f"{rank}_{card.suit.lower()}"
            screen.blit(card_images.get(key), (x + i * 100, y + 40))

    if show_cards == False and len(dealer_hand) > 0:
        value = dealer_hand[0].value
    else:
        value = game.dealer.get_hand_value(0)

    draw_text(f"Value: {value}", x, y, size=24, color=(255,255,0))

# Logic for player hand in seperating cards each deal so cards are offsetting
def render_player_hands(hands, x, y):
    hand_value = game.get_hand_value(0)
    draw_text(f"Value: {hand_value}", x, y - 40, size=24, color=(255,255,0))
    render_hand(hands[0], x, y)
    
# Pulls pressed and unpressed buttons from the card image dictionary 
def draw_button(button_name, location):
    current_time = pygame.time.get_ticks()
    if button_name in press_time and current_time - press_time[button_name] < FADE_DURATION:
        img = button_images.get(button_name).get("pressed")
        screen.blit(img, location)
    else:
        img = button_images.get(button_name).get("normal")
        screen.blit(img, location)

# Returns chip location for pressing chips to add wager
def get_chip_location():
    gap = 20
    key = str(chip_values[0])
    img = chip_images.get(key).get("normal")
    chip_width = img.get_width()
    chip_height = img.get_height()
    total_height = len(chip_values) * chip_height + (len(chip_values) - 1) * gap
    y = (height - total_height) // 2
    margin_x = 50
    x = width - chip_width - margin_x
    chip_location = {}
    for value in chip_values:
        key = str(value)
        location = pygame.Rect(x, y, chip_width, chip_height)
        chip_location[key] = location
        y += chip_height + gap
    return chip_location

# Pressing chips allows for faded and non faded versions
def draw_chip_buttons():
    chip_location = get_chip_location()
    current_time = pygame.time.get_ticks()
    for value in chip_values:
        key = str(value)
        location = chip_location.get(key)
        if f"chip_{value}" in press_time and current_time - press_time[f"chip_{value}"] < FADE_DURATION:
            img = chip_images[key]["pressed"]
        else:
            img = chip_images[key]["normal"]
        screen.blit(img, (location.x, location.y))
    return chip_location

# Creates buttons for each function(ex. Hit, Stand, DoubleDown, Split) and returns a list with the action pressed and the location for that button
def get_action_buttons():
    actions = []
    x = 639
    y = 700
    spacing = 130
    if len(game.hand[0]) == 2 and game.hand[0][0].rank == game.hand[0][1].rank:
        actions.append("split")
    actions.append("doubleDown")
    actions.append("stand") 
    actions.append("hit")
    button_location = []
    for i in enumerate(actions):
        shift_x = i[0]
        action = i[1]
        location = pygame.Rect(x + shift_x * spacing, y, 120, 50)
        button_location.append((action, location))
    return button_location

# Creates all of the buttons functions by calling the draw_button function
def draw_action_buttons():
    buttons = get_action_buttons()
    for i in buttons:
        action = i[0] 
        location = i[1]
        draw_button(action, location)

# returns the location of the play button 
def draw_next_play_button():
    location = pygame.Rect(50, 700, 150, 50)
    draw_button("play", location)
    return location

# returns the location of the undoBet button 
def draw_next_undoBet_button():
    if player_wager > 0 and not round_active:
        location = pygame.Rect(210, 700, 150, 50)
        draw_button("undoBet", location)
        return location
    else:
        return None

# Game loop
def main():
    game.reset_round()
    global player_wager, busted_message, round_active, round_over
    running = True
    result_message = ""
    dealer_value = None
    current_hand_index = 0



    while running:
        screen.blit(table_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if round_active == False:
                    new_round_location = pygame.Rect(50, 700, 150, 50)
                    if new_round_location.collidepoint(mouse_pos):
                        press_time["play"] = pygame.time.get_ticks()
                        if player_wager > 0 and game.place_wager(player_wager) == True:
                            game.reset_round()
                            game.deal_initial_cards()
                            play_card_sound()
                            busted_message = ""
                            result_message = ""
                            round_active = True
                            round_over = False
                            current_hand_index = 0
                            dealer_value = None
                            game.player_wager = [player_wager]
                            if game.has_blackjack(0):
                                result_message = "BlackJack!"
                                round_active = False
                                round_over = True

                    undoBet_button = draw_next_undoBet_button()
                    if undoBet_button and undoBet_button.collidepoint(mouse_pos):
                        press_time["undoBet"] = pygame.time.get_ticks()
                        player_wager = 0

                    chip_location = get_chip_location()
                    for i in chip_values:
                        key = str(i)
                        location = chip_location.get(key)
                        if location and location.collidepoint(mouse_pos):
                            press_time[f"chip_{i}"] = pygame.time.get_ticks()
                            if round_active == False and game.player_balance >= i:
                                player_wager += i

                if round_active == True and round_over == False:
                    buttons = get_action_buttons()
                    for i in buttons:
                        action = i[0]
                        location = i[1]
                        if location.collidepoint(mouse_pos):
                            press_time[action] = pygame.time.get_ticks()

                            if action == "split":
                                if game.can_split(0) == True and game.player_balance >= game.player_wager[0]:
                                    game.player_balance -= game.player_wager[0]
                                    game.split_hand(0)

                            elif action == "doubleDown":
                                if game.player_balance >= game.player_wager[0]:
                                    game.player_balance -= game.player_wager[0]
                                    game.player_wager[0] *= 2
                                    hit = game.player_hit(0)
                                    busted = hit[2]
                                    play_card_sound()
                                    if busted == True:
                                        busted_message = "Busted!"
                                        if len(game.hand) > 1:
                                            game.hand.pop(0)
                                            game.player_wager.pop(0)
                                            current_hand_index = 0
                                        else:
                                            current_hand_index += 1
                                    else:
                                        current_hand_index += 1
                                else:
                                    busted_message = "Insufficient funds for double down!"

                            elif action == "hit":
                                hit = game.player_hit(0)
                                busted = hit[2]
                                play_card_sound()
                                if busted:
                                    busted_message = "Busted!"
                                    if len(game.hand) > 1:
                                        game.hand.pop(0)
                                        game.player_wager.pop(0)
                                        current_hand_index = 0
                                    else:
                                        current_hand_index += 1

                            elif action == "stand":
                                if len(game.hand) > 1:
                                    game.hand.pop(0)
                                    game.player_wager.pop(0)
                                    current_hand_index = 0
                                else:
                                    current_hand_index += 1

                    if current_hand_index >= len(game.hand):
                        round_active = False
                        round_over = True

        if round_active == False:
            draw_next_play_button()
            draw_next_undoBet_button()
            draw_chip_buttons()
        else:
            draw_action_buttons()

        draw_text("Dealer's Hand", 100, 60, size=24)
        render_dealer_hand(100, 100, show_cards=round_over)
        draw_text("Player's Hand", 100, 420, size=24)
        render_player_hands(game.hand, 100, 500)
        draw_text(f"Balance: ${game.player_balance}", 1100, 50)
        draw_text(f"Wagered: ${player_wager}", 1100, 80)

        if len(busted_message) > 0:
            draw_text(busted_message, 645, 50, size=36, color=(255, 0, 0))
        if len(result_message) > 0:
            draw_text(result_message, 639, 90, size=36, color=(0, 255, 0))

        if round_over == True and 'dealer_value' in locals() and dealer_value is None:
            dealer_run = game.dealer_turn()
            dealer_value = dealer_run[1]
            actions = dealer_run[3]
            for i in actions:
                play_card_sound()
            results = []
            for i in range(len(game.hand)):
                payouts = game.handle_payouts(i, game.player_wager[i])
                result = payouts[0]
                results.append(f"You {result}")
            result_message = " | ".join(results)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()