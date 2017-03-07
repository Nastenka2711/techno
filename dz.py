import json
import os
import random
import sys


def file_exists(filepath):
    return os.path.exists(filepath) and os.path.isfile(filepath)


def open_file(file_name):
    with open(file_name, 'r') as filepath:
        return json.load(filepath)


def count_teams(teams_list):
    if len(teams_list) != 16:
        print("Команд должно быть 16")
        exit(-1)


def playing_games(teams_list):
    i = 0
    list_games = []
    for k in range(int(len(teams_list)/2)):
        game = {}
        goal_team_1 = random.randint(0, 9)
        goal_team_2 = random.randint(0, 9)
        if goal_team_1 == goal_team_2:
            goal_team_1 += 1
        game['team_1'] = [teams_list[i], goal_team_1]
        game['team_2'] = [teams_list[i+1], goal_team_2]
        i += 2
        list_games.append(game)
    return(list_games)


def create_teams_list(list_games):
    teams_list = []
    i = 0
    for game in list_games:
        if(list_games[i]['team_1'][1] > list_games[i]['team_2'][1]):
            teams_list.append(list_games[i]['team_1'][0])
        else:
            teams_list.append(list_games[i]['team_2'][0])
        i += 1
    return(teams_list)


def input_team_name():
    if len(sys.argv) == 1:
        team_name = input("Введите название команды: ")
    else:
        team_name = sys.argv[1]
    return team_name.upper()


def output_info(team_name, results):
    stage = 8
    for st in range(4):
        print("\n1/" + str(stage) + ":")
        game = 0
        flag = 0
        for result in results[stage]:
            if results[stage][game]['team_2'][0] == team_name:
                print(team_name + "-" + results[stage][game]['team_1'][0])
                print(str(results[stage][game]['team_2'][1]) + ":" +
                      str(results[stage][game]['team_1'][1]))
                flag += 1
            elif results[stage][game]['team_1'][0] == team_name:
                print(team_name + "-" + results[stage][game]['team_2'][0])
                print(str(results[stage][game]['team_1'][1]) + ":" +
                      str(results[stage][game]['team_2'][1]))
                flag += 1
            game += 1
        if flag == 0:
            print("Команда выбыла")
        stage = int(stage/2)


if __name__ == '__main__':
    file_name = "teams.json"
    if not file_exists(file_name):
        print("Ошибка открытия файла")
        exit(-1)
    else:
        teams_list = open_file(file_name)
        count_teams(teams_list)
        random.shuffle(teams_list)

        team_name = None
        while teams_list.count(team_name) == 0:
            team_name = input_team_name()

        results = {}
        stage = 8
        for st in range(4):
            list_games = playing_games(teams_list)
            teams_list = create_teams_list(list_games)
            results[stage] = list_games
            stage = int(stage/2)
        output_info(team_name, results)
