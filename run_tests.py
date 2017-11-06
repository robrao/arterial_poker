import sys
import unittest


def run_tests():
    suite = unittest.TestLoader().discover('./tests')
    results = unittest.TextTestRunner().run(suite)
    if results.errors or results.failures:
        print "Tests failed."
        sys.exit(1)
    print "Tests passed."

if __name__ == '__main__':
    run_tests()
