import doctest

from ABC_tombola_11 import Tombola

import ABC_tombola_bingo_11, ABC_tombola_lotto_11, ABC_tombola_tombolist_11

TEST_FILE = '/mnt/c/Users/berne/Desktop/Books_to_learn-main/Books_to_learn-main/Python/tests/unit/tombola_tests.rst'
TEST_MSG = '{0:16} {1.attempted:2} tests, {1.failed:2} failed - {2}'
def main(argv):
    verbose = '-v' in argv
    real_subclasses = Tombola.__subclasses__()
    virtual_subclasses = list(Tombola._abc_registry)
    
    for cls in real_subclasses + virtual_subclasses:
        test(cls, verbose)

def test(cls, verbose=False):
    res = doctest.testfile(
        TEST_FILE,
        globs={'ConcreteTombola': cls},
        verbose=verbose,
        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    tag = 'FAIL' if res.failed else 'OK'
    print(TEST_MSG.format(cls.__name__, res, tag))
    
if __name__ == '__main__':
    import sys
    main(sys.argv)