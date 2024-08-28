import os
import time

def delete_bullet_games(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    total_games = 0
    deleted_games = 0
    new_lines = []
    game = []
    is_bullet = False

    for line in lines:
        if line.startswith("[Event"):
            total_games += 1
            if "bullet" in line.lower():
                is_bullet = True
            else:
                is_bullet = False

        if is_bullet:
            if line.strip() == "":
                deleted_games += 1
                is_bullet = False
            continue

        game.append(line)
        if line.strip() == "":
            new_lines.extend(game)
            game = []

    with open(file_path, 'w') as file:
        for i in range(0, len(new_lines), 8192):
            file.write(''.join(new_lines[i:i+8192]))
            time.sleep(0.1)  # Slow down the process

    return total_games, deleted_games

def process_folder(folder_path):
    log = []
    total_games_overall = 0
    total_deleted_overall = 0

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pgn'):
            file_path = os.path.join(folder_path, file_name)
            total_games, deleted_games = delete_bullet_games(file_path)
            total_games_overall += total_games
            total_deleted_overall += deleted_games
            log.append(f"{file_name}: Total games: {total_games}, Deleted games: {deleted_games}")

    log.append(f"Total games overall: {total_games_overall}, Total deleted overall: {total_deleted_overall}")

    with open('deletion_log.txt', 'w') as log_file:
        log_file.write('\n'.join(log))

if __name__ == "__main__":
    current_folder = os.getcwd()
    process_folder(current_folder)
