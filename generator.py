import re
import random
from math import sqrt

test_chromosome = "113113114188141777116CC611012345101011111111311141100012030405543211123451154321112345005432111111166611"

weights = {"Valley" : 2,
           "Roof Valley" : 4,
           "Two Path" : 6,
           "Three Path" : 6,
           "Gaps" : 2,
           "Variable Gaps" : 4,
           "Multiple Gaps" : 6,
           "Pillar Gaps" : 10,
           "Stair Up" : 1,
           "Stair Down" : 1,
           "Empty Stair Valley" : 1,
           "Gap Stair Valley" : 1,
           "Unplayable" : -100,
           "Respite" : 15,
           "Repeated" : -10,
           "Beginnings" : 5}

mutation_prob = 100
mutation_count = 1
population_size = 200
generation_count = 100
fresh_count = 10

def ScanChromosome(chromosome):
    valley_re = re.compile("[2345]1{1,5}(?=[2345])")
    start_re = re.compile("[2345]1")
    repeated = len(re.compile("(?:[2345]1){2,}").findall(chromosome))
    valleys = len(valley_re.findall(chromosome))
    beginning = len(start_re.findall(chromosome))
    #print(valley_re.findall(chromosome))

    roof_valley_re_1 = re.compile("[23]16{1,5}1(?=[23])")
    start_re = re.compile("[23]16")
    repeated += len(re.compile("(?:[23]16){2,}").findall(chromosome))
    roof_valleys = len(roof_valley_re_1.findall(chromosome))
    beginning += len(start_re.findall(chromosome))
    #print(roof_valley_re_1.findall(chromosome))

    roof_valley_re_2 = re.compile("(?:2|[234]1)(?:7{1,5})(?=(?:[2|1[234]))")
    start_re = re.compile("(?:2|[234]1)7")
    repeated += len(re.compile("(?:(?:2|[234]1)7){2,}").findall(chromosome))
    roof_valleys += len(roof_valley_re_2.findall(chromosome))
    beginning += len(start_re.findall(chromosome))
    #print(roof_valley_re_2.findall(chromosome))

    roof_valley_re_3 = re.compile("(?:[23]1?|[45]1)(?:8{1,5})(?=(?:1?[23]|1[45]))")
    start_re = re.compile("(?:[23]1?|[45]1)8")
    repeated += len(re.compile("(?:(?:[23]1?|[45]1)8){2,}").findall(chromosome))
    roof_valleys += len(roof_valley_re_3.findall(chromosome))
    beginning += len(start_re.findall(chromosome))
    #print(roof_valley_re_3.findall(chromosome))

    two_path_re = re.compile("[01]{2}[67]+[01]{2}")
    start_re = re.compile("[01]{2}[67]")
    repeated += len(re.compile("(?:[01]{2}[67]){2,}").findall(chromosome))
    two_paths = len(two_path_re.findall(chromosome))
    beginning += len(start_re.findall(chromosome))
    #print(two_path_re.findall(chromosome))

    three_path_re = re.compile("[01]{2}6+[01]?[CF]+[01]?6*[01]{2}")
    start_re = re.compile("[01]{2}6+[01]?[CF]")
    repeated += len(re.compile("(?:[01]{2}6+[01]?[CF]){2,}").findall(chromosome))
    three_paths = len(three_path_re.findall(chromosome))
    beginning += len(start_re.findall(chromosome))
    #print(three_path_re.findall(chromosome))

    gaps_re = re.compile("[^09ABF]{2}[09ABF](?=[^09ABF]{2})")
    start_re = re.compile("[^09ABF]{2}[09ABF]")
    repeated += len(re.compile("(?:[^09ABF]{2}[09ABF]){2,}").findall(chromosome))
    gaps = len(gaps_re.findall(chromosome))
    beginning += len(start_re.findall(chromosome)) * 3
    #print(gaps_re.findall(chromosome))

    variable_gaps_re = re.compile("[^09ABF]{2}[09ABF]{2,3}(?=[^09ABF]{2})")
    variable_gaps = len(variable_gaps_re.findall(chromosome))
    #print(variable_gaps_re.findall(chromosome))

    multiple_gaps_re = re.compile("(?:[178E][09ABF](?=[178E])){2,}")
    multiple_gaps = len(multiple_gaps_re.findall(chromosome))
    #print(multiple_gaps_re.findall(chromosome))

    pillar_gaps_re = re.compile("[2345]0{1,3}(?=[2345])")
    start_re = re.compile("[2345]0")
    repeated += len(re.compile("(?:[2345]0){2,}").findall(chromosome))
    pillar_gaps = len(pillar_gaps_re.findall(chromosome))
    beginning += len(start_re.findall(chromosome))
    #print(pillar_gaps_re.findall(chromosome))

    stair_up_re = re.compile("1?2345?")
    start_re = re.compile("1?23")
    repeated += len(re.compile("(?:1?23){2,}").findall(chromosome))
    stair_up = len(stair_up_re.findall(chromosome))
    beginning += len(start_re.findall(chromosome))
    #print(stair_up_re.findall(chromosome))

    stair_down_re = re.compile("5?4321?")
    start_re = re.compile("5?43")
    repeated += len(re.compile("(?:5?43){2,}").findall(chromosome))
    stair_down = len(stair_down_re.findall(chromosome))
    beginning += len(start_re.findall(chromosome))
    #print(stair_down_re.findall(chromosome))

    empty_stair_valley_re = re.compile("1?2345?1{1,3}5?4321?")
    start_re = re.compile("1?2345?1")
    repeated += len(re.compile("(?:1?2345?1){2,}").findall(chromosome))
    empty_stair_valleys = len(empty_stair_valley_re.findall(chromosome))
    beginning += len(start_re.findall(chromosome))
    #print(empty_stair_valley_re.findall(chromosome))

    gap_stair_valley_re = re.compile("1?2345?0{1,3}5?4321?")
    start_re = re.compile("1?2345?0")
    repeated += len(re.compile("(?:1?2345?0){2,}").findall(chromosome))
    gap_stair_valleys = len(gap_stair_valley_re.findall(chromosome))
    beginning += len(start_re.findall(chromosome))
    #print(gap_stair_valley_re.findall(chromosome))

    unplayable_re_1 = re.compile("0{4,}")
    unplayable = len(unplayable_re_1.findall(chromosome))
    unplayable_re_2 = re.compile("[01]{4,}[45]")
    unplayable += len(unplayable_re_2.findall(chromosome))
    unplayable_re_3 = re.compile("[012]{4,}5")
    unplayable += len(unplayable_re_3.findall(chromosome))

    respite_re = re.compile("1{3,}")
    respites = len(respite_re.findall(chromosome))

    #print(unplayable_re_1.findall(chromosome))
    #print(unplayable_re_2.findall(chromosome))
    #print(unplayable_re_3.findall(chromosome))

    return { "Valley" : valleys,
             "Roof Valley" : roof_valleys,
             "Two Path" : two_paths,
             "Three Path" : three_paths,
             "Gaps" : gaps,
             "Variable Gaps" : variable_gaps,
             "Multiple Gaps" : multiple_gaps,
             "Pillar Gaps" : pillar_gaps,
             "Stair Up" : stair_up,
             "Stair Down" : stair_down,
             "Empty Stair Valley" : empty_stair_valleys,
             "Gap Stair Valley" : gap_stair_valleys,
             "Unplayable" : unplayable,
             "Respite" : respites,
             "Repeated" : repeated,
             "Beginnings" : beginning}

def Fitness(chromosome):
    pattern_count = ScanChromosome(chromosome)

    fitness = 0
    for key in pattern_count:
        if pattern_count[key] > 0:
            fitness += (weights[key] * 2 - pattern_count[key] * 0.1)
        #if key != "Unplayable" and pattern_count[key] == 0:
        #    fitness -= 20



    return fitness

def RandomChromosome():
    s = ""
    for i in range(200):
        s += "%X" % random.randint(0,15)

    return s

def FlatChromosome():
    return "11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"

def Crossover(chr1, chr2):
    #convert to bitstrings
    bitc1 = ""
    bitc2 = ""
    for i in range(len(chr1)):
        bitc1 += "{0:0>4b}".format(int(chr1[i], 16))
        bitc2 += "{0:0>4b}".format(int(chr2[i], 16))
    assert(len(chr1) == len(chr2))
    assert(len(bitc1) == len(bitc2))
    #do cutoff
    cutoff = len(bitc1) / 2 #random.randint(0, len(bitc1) - 1)
    kids = []
    kids.append(bitc1[0:cutoff] + bitc2[cutoff:])
    kids.append(bitc2[0:cutoff] + bitc1[cutoff:])
    #print(kids)
    #mutate kids
    for kid in kids:
        r = random.randint(1, 100)
        if r <= 5:
            for i in range(r):
                mut = random.randint(0, len(kid) - 1)
                if kid[mut] == '0':
                    kid = kid[0:mut] + '1' + kid[mut + 1:]
                else:
                    kid = kid[0:mut] + '0' + kid[mut + 1:]
    hexkids = ["",""]
    assert(len(kids[0]) == len(kids[1]))
    for i in range(0, len(kids[0]), 4):
        hexkids[0] += "%X" % (int(kids[0][i:i + 4], 2))
        hexkids[1] += "%X" % (int(kids[1][i:i + 4], 2))

    return hexkids

def EvolvePopulation(population):

    new_pop = []
    for i in range(0, population_size / 2, 2): # - fresh_count):
        new_pop.append(population[i])
        new_pop.append(population[i + 1])
        kids = Crossover(population[i],
                         population[i + 1])
        new_pop.append(kids[0])
        new_pop.append(kids[1])

    #for i in range(fresh_count):
    #    new_pop.append(RandomChromosome())

    return new_pop

if __name__ == "__main__":
    population = []
    for i in range(population_size):
        population.append(RandomChromosome())

    population.sort(key = Fitness, reverse = True)

    for i in range(generation_count):
        population = EvolvePopulation(population)
        population.sort(key = Fitness, reverse = True)
        #if i % 100 == 0:
        print("Generation %d complete with highest fitness: %d" %(i, Fitness(population[0])))

    print("Winning fitness: %d" % Fitness(population[0]))
    print(ScanChromosome(population[0]))
    f = open("Assets/Levels/winner.txt", 'w')
    f.write(population[0])
    f.close()




    #pattern_count = ScanChromosome(test_chromosome)
    #fitness = Fitness(pattern_count)

    #print(pattern_count)
    #print(fitness)
    #print(Crossover(RandomChromosome(), RandomChromosome()))
