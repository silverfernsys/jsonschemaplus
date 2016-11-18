from jsonschemaplus.gen import ParserIterator
import sys, unittest


class TestParserIterator(unittest.TestCase):
	def test_iterator(self):
		flattened = list(range(200, 205))
		flattened.extend(list(range(400, 405)))

		p = ParserIterator([range(200, 205), range(400, 405)])
		self.assertEqual(flattened[0], p.lookahead())
		self.assertEqual(p.lookahead(), p.next())
		self.assertEqual(flattened[1:], list(p))
		self.assertEqual(p.lookahead(), None)
		self.assertRaises(StopIteration, p.next)


if __name__ == '__main__':
	unittest.main()