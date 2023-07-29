# Project name: Knuth Morris Pratt (parallel)

# Programming language(s): Python

# Author: Viola Renne

# Expected outcome: design a Python script that implement the Knuth-Morris-Pratt algorithm:
# 1. Takes as input:
#   a. A file containing a genome (length ~10kbp)
#   b. A file containing a set of short sequences (order of 100 sequences), one per line
# 2. In parallel, using different multiprocessing, stores in a single file the list of matching sequences, one per line.
# 3. Uses a Lock to manage the access to the file


from optparse import OptionParser
import numpy as np
from multiprocessing import Pool, Manager
from Bio import SeqIO


def read_genome(file):
    """
    Reading the genome
    :param file: file containing the genome
    :return sequence: genome's sequence
    """
    records = list(SeqIO.parse(file, "fasta"))
    sequence = records[0]
    return sequence.seq


def compute_index(pattern):
    """
    Compute index of pattern
    :param pattern: pattern's sequence
    :return t: pattern's index
    """
    t = np.zeros(len(pattern), dtype=int)
    t[0] = 0
    pos = 1  # Position in the index
    cnd = 0  # Position in the pattern

    while pos < len(pattern):
        if pattern[pos] == pattern[cnd]:
            t[pos] = cnd + 1
            pos = pos + 1
            cnd = cnd + 1
        elif cnd > 0:
            cnd = t[cnd - 1]
        else:
            t[pos] = 0
            pos = pos + 1
    return t


def search_sequence(index, pattern, genome_sequence):
    """
    Search for a sequence in the genome
    :param index: pattern's index
    :param pattern: pattern's sequence
    :param genome_sequence: genome's sequence
    :return: true if the pattern is in the genome, false otherwise
    """
    i = 0
    j = 0
    present = False
    positions = []
    while j < len(genome_sequence) and i < len(pattern):
        if pattern[i] == genome_sequence[j]:
            i += 1
            j += 1
            if i == len(pattern):
                present = True
                positions.append(str(j - i))
                i = index[i - 1]
        else:
            if i > 0:
                i = index[i-1]
            else:
                j += 1
    return present, positions


def task(pattern, genome_sequence, lock_output, file):
    """
    Storing matching sequences
    :param pattern: pattern's sequence
    :param genome_sequence: genome's sequence
    :param lock_output: lock for output file
    :param file: output file
    """
    index = compute_index(pattern)
    flag, pos = search_sequence(index, pattern, genome_sequence)
    if flag:
        lock_output.acquire()
        o_file = open(file, 'a')
        o_file.write(f"{pattern} {' '.join(pos)}\n")
        o_file.close()
        lock_output.release()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = OptionParser()
    """ Adding all the options that can be given as parameters """
    parser.add_option("-g", action="store", type="string", dest="genome_file", help="file containing a genome")
    parser.add_option("-s", action="store", type="string", dest="sequences_file",
                      help="file containing a set of short sequences, one per line")
    parser.add_option("-o", action="store", type="string", dest="output_file", help="file containing the output")

    """ Reading parameters """
    (options, args) = parser.parse_args()
    genome_file = options.genome_file
    sequences_file = options.sequences_file
    output_file = options.output_file

    """ Reading the genome """
    genome = read_genome(genome_file)

    """ Creating a lock object for accessing the output file """
    manager = Manager()
    lock = manager.Lock()

    """ Reading the patterns """
    seq_file = open(sequences_file, 'r')
    sequences = seq_file.read().split('\n')
    seq_file.close()

    """ Cleaning the output file """
    output = open(output_file, 'w')
    output.close()

    """ Defining the arguments and starting the processes """
    arguments = [(sequence, genome, lock, output_file) for sequence in sequences]
    pool = Pool(6)
    result = pool.starmap(task, iterable=arguments)
    pool.close()
    pool.join()
