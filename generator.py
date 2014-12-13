import re

test_chromosome = "113113114188141777116CC6110123451010111111113111411000120304055432111234511543211123450054321"

valley_max_length = 5

def ScanChromosome(chromosome):
    valley_re = re.compile("[2345]1{1,5}(?=[2345])")
    print(valley_re.findall(chromosome))
    
    roof_valley_re_1 = re.compile("[23]16{1,5}1(?=[23])")
    print(roof_valley_re_1.findall(chromosome))
    
    roof_valley_re_2 = re.compile("(?:2|[234]1)(?:7{1,5})(?=(?:[2|1[234]))")
    print(roof_valley_re_2.findall(chromosome))
    
    roof_valley_re_3 = re.compile("(?:[23]1?|[45]1)(?:8{1,5})(?=(?:1?[23]|1[45]))")
    print(roof_valley_re_3.findall(chromosome))
    
    two_path_re = re.compile("[01]{2}[67]+[01]{2}")
    print(two_path_re.findall(chromosome))
    
    three_path_re = re.compile("[01]{2}6+[01]?[CF]+[01]?6*[01]{2}")
    print(three_path_re.findall(chromosome))
    
    
    #
    #
    #roof_valley_re_3 = re.compile("2|3|(21)|(31)|(41)8{1,5}2|3|(12)|(13)|(14)")
    #print(roof_valley_re_3.findall(chromosome))
    
    
    #valley = ScanValley(chromosome)
    #print(valley)
    #roof_valley = ScanRoofValleys(chromosome)
    #path2 = Scan2Paths(chromosome)
    #path3 = Scan3Paths(chromosome)
    #gaps = ScanGaps(chromosome)
    # ...

#def ScanValley(chromosome):
#    count = 0
#    length = -1
#    for allele in chromosome:
#        if length == -1:
#            if (allele == 2 or
#                allele == 3 or
#                allele == 4 or
#                allele == 5):
#                length = 0
#        else:
#            # Check for an end of the valley
#            if (allele == 2 or
#                allele == 3 or
#                allele == 4 or
#                allele == 5):
#                if length > 0 and length <= valley_max_length:
#                    count += 1
#                
#                # Start searching for a new valley...
#                length = 0
#            # Check for allowable intermediate valley alleles
#            elif (allele == 1 or
#                  allele == 0xB):
#                  length += 1
#            # Abort the valley check if no end is in sight...
#            else:
#                length = -1
#    return count
#    
#def ScanRoofValley(chromosome):
#    count = 0
#    length = -1
#    roof_allele = -1
#    empty_bordered_roof = False
#    
#    for i in range(len(chromosome)):
#        if length == -1 and len(chromosome) - i >= 3:
#            if chromosome[i] == 2:
#                if chromosome[i + 1] == 1:
#                    if chromosome[i + 2] == 6:
#                        roof_allele = 6
#                        length = 0
#                        empty_bordered_roof = True
#                    if chromosome[i + 2] == 7:
#                        roof_allele = 7
#                        length = 0
#                        empty_bordered_roof = True
#                    if chromosome[i + 2] == 8:
#                        roof_allele = 8
#                        length = 0
#                        empty_bordered_roof = True
#                if chromosome[i + 1] == 7:
#                    roof_allele = 7
#                    length = 0
#                if chromosome[i + 1] == 8:
#                    roof_allele = 8
#                    length = 0
#            if chromosome[i] == 3:
#                if chromosome[i + 1] == 1:
#                    if chromosome[i + 2] == 6:
#                        roof_allele = 6
#                        length = 0
#                        empty_bordered_roof = True
#                    if chromosome[i + 2] == 7:
#                        roof_allele = 7
#                        length = 0
#                        empty_bordered_roof = True
#                    if chromosome[i + 2] == 8:
#                        roof_allele = 8
#                        length = 0
#                        empty_bordered_roof = True
#                if chromosome[i + 1] == 8:
#                    roof_allele = 8
#                    length = 0
#            if chromosome[i] == 4:
#                if chromosome[i + 1] == 1:
#                    if chromosome[i + 2] == 7:
#                        roof_allele = 7
#                        length = 0
#                        empty_bordered_roof = True
#                    if chromosome[i + 2] == 8:
#                        roof_allele = 8
#                        length = 0
#                        empty_bordered_roof = True
#            if chromosome[i] == 5:
#                if chromosome[i + 1] == 1:
#                        if chromosome[i + 2] == 8:
#                            roof_allele = 8
#                            length = 0
#                            empty_bordered_roof = True
#        else:
#            if length == 0:
#                length += 1
#            if length == 1:
#                if empty_bordered_roof:
#                    length += 1
#                else:
#                    if chromosome[i] == roof_allele and length <= valley_max_length:
#                        length += 1
#                    else:
#                        length = -1

        
if __name__ == "__main__":
    #s = "aaaabbaaaaabfkaaakaaka"
    #f = "aa"
    #p = re.compile("[a]{3,6}")
    #print(p.findall(s))
    #print(p.findall(f))
    
    #s = "5111561116"
    #
    #s1 = "ab"
    #s2 = "ac"
    #f = "ad"
    #
    #r = re.compile("[56]1{1,5}[56]")
    #print(r.findall(s))
    #print(r.findall(s2))
    #print(r.findall(f))

      
   ScanChromosome(test_chromosome)