import random

WIDTH = 800
HEIGHT = 600

screen_state = "menu"
background_music = True
sound_effects = True
paused = False
score = 0

# Menu buttons
button1 = {"x": 300, "y": 200, "width": 200, "height": 50, "text": "Iniciar", "color": "lightgreen"}
button2 = {"x": 300, "y": 275, "width": 200, "height": 50, "text": "Liga/Desliga Sons", "color": "lightyellow"}
button3 = {"x": 300, "y": 350, "width": 200, "height": 50, "text": "Sair", "color": "salmon"}

# Ship
ship = Actor("nave")
menu_ship = Actor("img_nave")
menu_ship.pos = (WIDTH // 2, button1["y"] - 60)
ship.pos = (WIDTH // 2, HEIGHT - 50)

# Lists
meteors = []
missiles = []
time_to_next_meteor = 0

def draw():
    screen.clear()
    if screen_state == "menu":
        draw_menu()
    elif screen_state == "game":
        draw_game()
        if paused:
            screen.draw.text("PAUSADO", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")
        
        # Score
        screen.draw.text(f"Pontos: {score}", topleft=(10, 10), fontsize=30, color="white")

        # Music Status
        screen.draw.text("M - Musica:", topright=(750, 10), fontsize=24, color="white")
        music_color = "green" if background_music else "red"
        screen.draw.filled_circle((760, 18), 8, music_color)

        # Sound Status
        screen.draw.text("S - Som:", topright=(750, 40), fontsize=24, color="white")
        sound_color = "green" if sound_effects else "red"
        screen.draw.filled_circle((760, 48), 8, sound_color)

def draw_menu():
    screen.fill("black")
    menu_ship.draw()
    
    for button in (button1, button2, button3):
        rect = Rect(button["x"], button["y"], button["width"], button["height"])
        screen.draw.filled_rect(rect, button["color"])
        screen.draw.text(button["text"], center=rect.center, color="black", fontsize=24)

def draw_game():
    screen.fill("black")
    ship.draw()
    for meteor in meteors:
        meteor.draw()
    for missile in missiles:
        missile.draw()

def inside_button(pos, button):
    x, y = pos
    return (button["x"] <= x <= button["x"] + button["width"] and
            button["y"] <= y <= button["y"] + button["height"])

def on_mouse_down(pos):
    global screen_state, background_music, sound_effects

    if screen_state == "menu":
        if inside_button(pos, button1):
            screen_state = "game"
            reset_game()

        elif inside_button(pos, button2):
            background_music = not background_music
            sound_effects = not sound_effects

            if background_music:
                music.play("musica_fundo")
            else:
                music.stop()

        elif inside_button(pos, button3):
            exit()

def on_key_down(key):
    global screen_state, paused, background_music, sound_effects

    if screen_state == "game":
        if key == keys.SPACE and not paused:
            create_missile()
            if sound_effects:
                sounds.tiro.play()

        elif key == keys.BACKSPACE:
            screen_state = "menu"
            meteors.clear()
            missiles.clear()
            paused = False

        elif key == keys.P:
            paused = not paused

        elif key == keys.M:
            background_music = not background_music
            if background_music:
                music.play("musica_fundo")
            else:
                music.stop()

        elif key == keys.S:
            sound_effects = not sound_effects

def update():
    global time_to_next_meteor, screen_state, score

    if screen_state == "game" and not paused:
        if keyboard.left:
            move_ship(-5)
        if keyboard.right:
            move_ship(5)

        time_to_next_meteor -= 1
        if time_to_next_meteor <= 0:
            spawn_meteor()
            time_to_next_meteor = 30

        # Update meteors
        for m in meteors:
            m.y += 4
            if m.colliderect(ship):
                screen_state = "menu"
                meteors.clear()
                missiles.clear()
                return
        meteors[:] = [m for m in meteors if m.y < HEIGHT]

        # Update missiles
        for missile in missiles:
            missile.y -= 8
        missiles[:] = [ms for ms in missiles if ms.y > 0]

        # Collision: missile vs meteor
        for missile in missiles[:]:
            for meteor in meteors[:]:
                if missile.colliderect(meteor):
                    missiles.remove(missile)
                    meteors.remove(meteor)
                    score += 1
                    break

def create_missile():
    missile = Actor("misil")
    missile.pos = (ship.x, ship.y - 30)
    missiles.append(missile)

def spawn_meteor():
    x = random.randint(50, WIDTH - 50)
    m = Actor("meteoro")
    m.x = x
    m.y = 0
    meteors.append(m)

def move_ship(step):
    new_x = ship.x + step
    if new_x < 50:
        new_x = 50
    if new_x > 750:
        new_x = 750
    ship.x = new_x

def reset_game():
    global meteors, missiles, time_to_next_meteor, paused, score
    meteors.clear()
    missiles.clear()
    time_to_next_meteor = 0
    paused = False
    score = 0

# Start background music
music.play("musica_fundo")
