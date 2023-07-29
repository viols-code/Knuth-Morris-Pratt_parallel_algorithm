# Knuth Morris Pratt parallel

## :bookmark_tabs: Menu
* [Overview](#overview)
* [Description](#description)
* [Implementation](#implementation)
* [Usage](#usage)

## Overview
This is a project proposed by the Scientific Programming course by Politecnico di Milano

## Description
**Project name:** Knuth Morris Pratt (parallel)
**Programming language:** Python  
**Short description:** In string computation, the exact pattern matching problem is the problem of
finding all the occurrences of a pattern (string) P, in a text (string) S, where usually P is much
shorter than S. For example the pattern could be the world “stella” and the text the whole Divina
Commedia, or P can be the CCATTGTG motif and the text the human genome.  
One strategy to speed up the computation is to create an index on the pattern P and use this index to
scan the text S in a more efficient way.  
The Knuth-Morris-Pratt algorithm uses this approach. It first of all builds an index on P and then
uses it to scan S, applying simple rules to the index to decide how to shift the pattern.  
**Expected outcome**: design a Python script that:
1. Takes as input:  
a. A file containing a genome (length ~10kbp) in fasta format  
b. A txt file containing a set of short sequences (order of 100 sequences), one per line
2. In parallel, using different multiprocessing, stores in a single txt file the list of matching
sequences and their position in the genome, one per line.
3. Uses a Lock to manage the access to the file

## Implementation
A Knuth Morris Pratt parallel algorithm have been implemented.
Also, some unit tests have been implemented, mainly to verify the correctness of reading genome, computing index and search pattern functions.

## Usage

1. **Install the requirements.**  
    In order to install the requirements, use:  
    ```bash
    pip install -r requirements.txt
    ```
   
2. **Add options.**  
In order to see the possible options, open a terminal, cd into project directory and type:
   ```bash
   python main.py --help 
   ```

3. **Standard simulation.**
Open a terminal into project directory and type:
   ```bash
   python main.py -g genome_file -s sequences_file -o output_file
   ```
   Example:
   ```bash
   python main.py -g data/genome.fasta -s data/sequences.txt -o output/match.txt
   ```
   
4. **Tests.**
Open a terminal into project directory and type:
   ```bash
    python -m unittest -v
   ```