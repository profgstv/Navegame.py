import pygame
import csv
from pygame.locals import *
from sys import exit

scores_history = []

def reading_data():
    global scores_history
    global highscore
    with open('./saves/general_scores.csv', 'r') as scores_file:
        reader = csv.reader(scores_file)
        for line in reader:
            for index in line:
                new_score(index)
        highscore = scores_history[0]

def writing_data():
    global scores_history
    writing_scores = []

    for index in range(len(scores_history)):
        writing_scores.append([scores_history[index]])

    with open('./saves/general_scores.csv', 'w', newline='') as scores_file:
        writer = csv.writer(scores_file)
        writer.writerows(writing_scores)

def new_score(new):
    global scores_history
    global highscore
    if not new in scores_history:
        scores_history.append(int(new))
    scores_history.sort(reverse = True)
    highscore = scores_history[0]