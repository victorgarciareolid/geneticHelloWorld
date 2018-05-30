#
#    Title:
#       Genetic Algorithm Hello World
#    Description:
#        In this program I want to make the chromosome to say 'HOLA'.
#    Author:
#        Victor Garcia Reolid
#

import numpy as np


# We are going to compute the distance between the chromosome and the target string
# I assume they have the same length
# The lit
def fitness(chromosome_string, target_string):
    fit = 0
    for i in range(len(target_string)):
        fit += np.power(ord(target_string[i]) - ord(chromosome_string[i]), 2)

    return np.sqrt(fit)


def random_char():
    p = np.random.randint(0, 2)
    i = p*np.random.randint(65, 91) + (1 - p)*np.random.randint(97, 123)
    return chr(i)


class Chromosome:
    word = ""
    target_word = ""
    size = 0
    fitness = 0

    def __init__(self, size, target_word):
        self.size = size
        self.target_word = target_word

        for i in range(size):
            self.word += random_char()
        self.perform()

    def setWord(self, word):
        self.word = word
        self.perform()

    def perform(self):
        self.fitness = fitness(self.word, self.target_word)

    def reproduce(self, partner, crossover, mutation_probability):
        child1 = Chromosome(self.size, self.target_word)
        child2 = Chromosome(self.size, self.target_word)

        child1_word_list = list(self.word)
        child2_word_list = list(partner.word)

        for i in range(crossover):
            if np.random.random_sample() < mutation_probability :
                # Mutation
                child1_word_list[i] = random_char()
                child2_word_list[i] = random_char()
            else:
                child1_word_list[i] = list(partner.word)[i]
                child1_word_list[i] = list(self.word)[i]


        child1.setWord("".join(child1_word_list))
        child2.setWord("".join(child2_word_list))

        return [child1, child2]  # We return two childs

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __str__(self):
        return "Ch: (" + self.word + ")";


class Population:
    individuals =[]
    target_word = ""
    drops = 0

    def __init__(self, N, chromosome_size, target_word, drops):
        for i in range(N):
            self.individuals.append(Chromosome(chromosome_size, target_word))

        self.target_word = target_word
        self.drops = drops

    def evolve(self, crossover, mutation_probability):
        # Select fittest individuals - sort by best performance
        self.individuals.sort()  # Sort from low to high (the lowest the better)

        # We take the first individuals
        aux = self.individuals[0:self.drops]

        self.individuals = list(aux)

        for i in range(len(aux)):
            for j in range(len(aux)):
                if j != i:
                    self.individuals.extend(aux[i].reproduce(aux[j], crossover, mutation_probability))

    def __str__(self):
        s = "["

        for i in range(len(self.individuals) - 1):
            s += self.individuals[i].__str__() + " "

        s += self.individuals[len(self.individuals) - 1].__str__() + "]"
        return s


def main():
    p = Population(5, 4, "hola", 5)

    print(p)

    s = ""
    while s != "hola":
        p.evolve(4, 0.25)
        s = p.individuals[0].word
        print(s)

    print(p)


if __name__ == "__main__":
    main()