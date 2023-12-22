#!/usr/bin/env python
"""A module encapsulating the WildDictionary code."""
__author__ = 'Cian Synnott'
__copyright__ = 'Copyright 2011, Cian Synnott'
__license__ = 'MIT'

class WildDictionary(object):
  """Represents a dictionary against with "wildcarded" lookups.

  Lookups are Scrabble-style. For example,
  >>> w = WildDictionary('/home/me/my_dictionary')
  ...
  >>> w.lookup('T?')
  ['TO', 'ET', 'AT', 'TA', 'IT', 'TI', 'UT']
  """


  def __init__(self, filename):
    """Loads the dictionary from disk..
    
    Slurps a dictionary consisting of one word per line into an internal
    representation for later lookup.

    Words in the input file must be uppercase and alphabet only.

    Args:
      filename: str, the name of the file containing our dictionary.
    """
    # Our internal dictionary representation is of the form
    #   { number : ['word', ...], ... }
    # such that each word in the value list produces the key number if we
    # treat each letter as a prime number and multiply it out.
    self._dictionary = {}

    f = open(filename)
    for l in f.readlines():
      word = l.strip()
      number = self._letters_to_number(list(word))
      if number in self._dictionary:
        self._dictionary[number].append(word)
      else:
        self._dictionary[number] = [word]
    f.close()


  def _combine_disregarding_order(self, letters):
    """Creates a list of combinations from the letters supplied.

    For example, from ['a', 'b', 'c'] we want to get
      ['a', 'b', 'c', 'ab', 'ac', 'bc', 'abc']
    
    Args:
      letters: [str], a list of the letters to combine.
    Returns:
      [str], a list of the combinations as described above.
    """

    # I originally used Python 2.6 itertools.permutation for this,
    # but it was the slowest part of the whole program - permutations
    # get very much harder as you increase the number of items, and
    # I only need the unique combinations disregarding order. This
    # little algorithm is snappy and does the trick.
    results = []
    for l in letters:
      new_results = []
      for r in results:
        new_results.append(r + l)
      new_results.append(l)
      results.extend(new_results)
    return results


  _letter_to_prime = {
    'A' : 2,  'B' : 3,  'C' : 5,  'D' : 7,  'E' : 11, 'F' : 13, 'G' : 17,
    'H' : 19, 'I' : 23, 'J' : 29, 'K' : 31, 'L' : 37, 'M' : 41, 'N' : 43,
    'O' : 47, 'P' : 53, 'Q' : 59, 'R' : 61, 'S' : 67, 'T' : 71, 'U' : 73,
    'V' : 79, 'W' : 83, 'X' : 89, 'Y' : 97, 'Z' : 101 }
  def _letters_to_number(self, letters):
    """Convert a list of letters to a number.

    Treating each letter as a prime per the map above, we return a
    representation of the word as a product of primes.

    This disregards considerations of order, which suits us just fine.

    Args:
      letters: [str], the letters to convert and multiply.
    Returns:
      int, the product of the prime representations of the letters.
    """
    numbers = [self._letter_to_prime[l] for l in letters]
    return reduce(lambda x, y: x * y, numbers)


  _primes = _letter_to_prime.values()
  def _generate_candidates(self, wildcarded_word):
    """Generate candidate number representations for a word.

    Args:
      wildcarded_word: str, the word to generate candidates for.
    Returns:
      [int], candidate numbers for words matched by rearrangements
             of the argument.
    """
    letters = list(wildcarded_word)
    wildcards = len([c for c in letters if c == '?'])
    letters = [c for c in letters if c != '?']

    combinations = self._combine_disregarding_order(letters)
    candidates = set([self._letters_to_number(l) for l in combinations])

    # Where no wildcards are present, we're finished. Otherwise, for
    # each wildcard, we extend the candidates list by multiplying each
    # candidate by the prime representation of each alphabetic character.
    # This is a bit of a combinatoric explosion, but it works well for
    # Scrabble-length words and blank tiles.
    for i in range(0, wildcards):
      new_candidates = set()
      for candidate in candidates:
        for i in range(0, len(self._primes)):
          new_candidates.add(candidate * self._primes[i])
      candidates.update(new_candidates)
  
    return candidates


  def lookup(self, word):
    """Find matches in the dictionary for the passed word.

    The word must consist of uppercase alphabetic letters, and
    may have wildcards represented by the question mark character.

    Args:
      word: str, the word to lookup.
    Returns:
      [str], words matched by rearrangementsof the argument.
    """
    results = []
    for candidate in self._generate_candidates(word):
      if candidate in self._dictionary:
        results.extend(self._dictionary[candidate])

    return results
