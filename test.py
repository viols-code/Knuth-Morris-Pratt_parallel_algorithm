import unittest
import numpy as np

from main import compute_index, search_sequence, read_genome


class TestMain(unittest.TestCase):

    def test_compute_index_1(self):
        pattern = 'ACGGAC'
        index = compute_index(pattern)
        np.testing.assert_array_equal(index, np.array([0, 0, 0, 0, 1, 2]))

    def test_compute_index_2(self):
        pattern = 'AAAA'
        index = compute_index(pattern)
        np.testing.assert_array_equal(index, np.array([0, 1, 2, 3]))

    def test_compute_index_3(self):
        pattern = 'ABCDE'
        index = compute_index(pattern)
        np.testing.assert_array_equal(index, np.array([0, 0, 0, 0, 0]))

    def test_compute_index_4(self):
        pattern = 'AABAACAABAA'
        index = compute_index(pattern)
        np.testing.assert_array_equal(index, np.array([0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5]))

    def test_compute_index_5(self):
        pattern = 'AAACAAAAAC'
        index = compute_index(pattern)
        np.testing.assert_array_equal(index, np.array([0, 1, 2, 0, 1, 2, 3, 3, 3, 4]))

    def test_compute_index_6(self):
        pattern = 'AAABAAA'
        index = compute_index(pattern)
        np.testing.assert_array_equal(index, np.array([0, 1, 2, 0, 1, 2, 3]))

    def test_search_sequence_1(self):
        txt = 'AAAAAAAAAAAAAAAAAB'
        pattern = 'AAAAB'
        index = compute_index(pattern)
        (present, pos) = search_sequence(index, pattern, txt)
        self.assertTrue(present)
        self.assertEqual(pos, ['13'])

    def test_search_sequence_2(self):
        txt = 'ABABABCABABABCABABABC'
        pattern = 'ABABAC'
        index = compute_index(pattern)
        (present, pos) = search_sequence(index, pattern, txt)
        self.assertFalse(present)
        self.assertEqual(pos, [])

    def test_search_sequence_3(self):
        txt = 'ABABDABACDABABCABAB'
        pattern = 'ABABCABAB'
        index = compute_index(pattern)
        (present, pos) = search_sequence(index, pattern, txt)
        self.assertTrue(present)
        self.assertEqual(pos, ['10'])

    def test_search_sequence_4(self):
        txt = 'AAAAAA'
        pattern = 'A'
        index = compute_index(pattern)
        (present, pos) = search_sequence(index, pattern, txt)
        self.assertTrue(present)
        self.assertEqual(pos, ['0', '1', '2', '3', '4', '5'])

    def test_read_genome(self):
        sequence = read_genome('data/genome.fasta')
        file = open('data/genome.fasta', 'r')
        file.readline()
        text = ''
        for line in file:
            text += line.strip('\n')
        file.close()
        self.assertEqual(sequence, text)


if __name__ == '__main__':
    unittest.main()
