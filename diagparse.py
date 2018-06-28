#!/usr/bin/env python3

import string
import csv


class Patient:

    def __init__(self, observations):
        self.obs = self.parse(observations)
        # self.print_obs()

    def __str__(self):
        self.print_obs()
        return ''

    def parse(self, observations):
        obs = []
        for token in observations.split(', '):
            token = token.strip()
            if token[0].islower() and len(obs) > 0:
                token = obs[-1] + ', ' + token
                obs[-1] = token
            else:
                obs.append(token)
        return obs

    def print_obs(self):
        for ob in self.obs:
            print(ob)


class Roster:

    def __init__(self):
        self.patients = []
        self.tally = dict()

    def add_patient(self, patient):
        self.patients.append(patient)

    def count_obs(self):
        for patient in self.patients:
            self.update_tally(patient.obs)

    def update_tally(self, obs):
        for ob in obs:
            self.tally[ob] = self.tally.setdefault(ob, 0) + 1

    def print_tally(self, sort=False):
        if sort == 'alpha':
            for key, value in sorted(self.tally.items()):
                print(value, key)
        elif sort == 'frequency':
            dict_view = sorted(self.tally.items(),
                               key=lambda x: x[1])
            for key, value in dict_view:
                print(value, key)
        else:
            for key, value in self.tally.items():
                print(value, key)

    def print_patients(self):
        for each in self.patients:
            print(each)

    def export_tally(self, filename):
        with open(filename, encoding='utf-8', mode='w', newline='\n') as f_out:

            writer = csv.writer(f_out)
            for key, value in self.tally.items():
                writer.writerow([key, value])


if __name__ == '__main__':
    fp = open('problem_list.txt', 'r')
    roster = Roster()

    for line in fp.readlines():
        if line != '\n':
            current_patient = Patient(line)
            roster.add_patient(current_patient)

    fp.close()
    roster.count_obs()
    roster.export_tally('tally.csv')
