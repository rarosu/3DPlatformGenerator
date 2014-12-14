import re
import random

test_chromosome = "113113114188141777116CC611012345101011111111311141100012030405543211123451154321112345005432111111166611"

weight_valley = 2
weight_roof_valley = 4
weight_two_path = 6
weight_three_path = 6
weight_gaps = 2
weight_variable_gaps = 4
weight_multiple_gaps = 6
weight_pillar_gaps = 10
weight_stair_up = 1
weight_stair_down = 1
weight_empty_stair_valley = 1
weight_gap_stair_valley = 1
weight_unplayable = -100

def ScanChromosome(chromosome):
    valley_re = re.compile("[2345]1{1,5}(?=[2345])")
    #print(valley_re.findall(chromosome))

    roof_valley_re_1 = re.compile("[23]16{1,5}1(?=[23])")
    #print(roof_valley_re_1.findall(chromosome))

    roof_valley_re_2 = re.compile("(?:2|[234]1)(?:7{1,5})(?=(?:[2|1[234]))")
    #print(roof_valley_re_2.findall(chromosome))

    roof_valley_re_3 = re.compile("(?:[23]1?|[45]1)(?:8{1,5})(?=(?:1?[23]|1[45]))")
    #print(roof_valley_re_3.findall(chromosome))

    two_path_re = re.compile("[01]{2}[67]+[01]{2}")
    #print(two_path_re.findall(chromosome))

    three_path_re = re.compile("[01]{2}6+[01]?[CF]+[01]?6*[01]{2}")
    #print(three_path_re.findall(chromosome))

    gaps_re = re.compile("[^09ABF]{2}[09ABF](?=[^09ABF]{2})")
    #print(gaps_re.findall(chromosome))

    variable_gaps_re = re.compile("[^09ABF]{2}[09ABF]{2,3}(?=[^09ABF]{2})")
    #print(variable_gaps_re.findall(chromosome))

    multiple_gaps_re = re.compile("(?:[178E][09ABF](?=[178E])){2,}")
    #print(multiple_gaps_re.findall(chromosome))

    pillar_gaps_re = re.compile("[2345]0{1,3}(?=[2345])")
    #print(pillar_gaps_re.findall(chromosome))

    stair_up_re = re.compile("1?2345?")
    #print(stair_up_re.findall(chromosome))

    stair_down_re = re.compile("5?4321?")
    #print(stair_down_re.findall(chromosome))

    empty_stair_valley_re = re.compile("1?2345?1{1,3}5?4321?")
    #print(empty_stair_valley_re.findall(chromosome))

    gap_stair_valley_re = re.compile("1?2345?0{1,3}5?4321?")
    #print(gap_stair_valley_re.findall(chromosome))

    unplayable_re_1 = re.compile("0{4,}")
    unplayable_re_2 = re.compile("[01]{4,}[45]")
    unplayable_re_3 = re.compile("[012]{4,}5")

    #print(unplayable_re_1.findall(chromosome))
    #print(unplayable_re_2.findall(chromosome))
    #print(unplayable_re_3.findall(chromosome))

    return { "Valley" : len(valley_re.findall(chromosome)),
             "Roof Valley" : len(roof_valley_re_1.findall(chromosome)) + len(roof_valley_re_2.findall(chromosome)) + len(roof_valley_re_3.findall(chromosome)),
             "Two Path" : len(two_path_re.findall(chromosome)),
             "Three Path" : len(three_path_re.findall(chromosome)),
             "Gaps" : len(gaps_re.findall(chromosome)),
             "Variable Gaps" : len(variable_gaps_re.findall(chromosome)),
             "Multiple Gaps" : len(multiple_gaps_re.findall(chromosome)),
             "Pillar Gaps" : len(pillar_gaps_re.findall(chromosome)),
             "Stair Up" : len(stair_up_re.findall(chromosome)),
             "Stair Down" : len(stair_down_re.findall(chromosome)),
             "Empty Stair Valley" : len(empty_stair_valley_re.findall(chromosome)),
             "Gap Stair Valley" : len(gap_stair_valley_re.findall(chromosome)),
             "Unplayable" : len(unplayable_re_1.findall(chromosome)) + len(unplayable_re_2.findall(chromosome)) + len(unplayable_re_3.findall(chromosome))}

def Fitness(pattern_count):
    fitness = 0

    fitness += pattern_count["Valley"] * weight_valley
    fitness += pattern_count["Roof Valley"] * weight_roof_valley
    fitness += pattern_count["Two Path"] * weight_two_path
    fitness += pattern_count["Three Path"] * weight_three_path
    fitness += pattern_count["Gaps"] * weight_gaps
    fitness += pattern_count["Variable Gaps"] * weight_variable_gaps
    fitness += pattern_count["Multiple Gaps"] * weight_multiple_gaps
    fitness += pattern_count["Pillar Gaps"] * weight_pillar_gaps
    fitness += pattern_count["Stair Up"] * weight_stair_up
    fitness += pattern_count["Stair Down"] * weight_stair_down
    fitness += pattern_count["Empty Stair Valley"] * weight_empty_stair_valley
    fitness += pattern_count["Gap Stair Valley"] * weight_gap_stair_valley
    fitness += pattern_count["Unplayable"] * weight_unplayable

    return fitness

def RandomChromosome():
    s = ""
    for i in range(200):
        s += "%X" % random.randint(0,15)

    return s

if __name__ == "__main__":
   pattern_count = ScanChromosome(test_chromosome)
   fitness = Fitness(pattern_count)

   print(pattern_count)
   print(fitness)
