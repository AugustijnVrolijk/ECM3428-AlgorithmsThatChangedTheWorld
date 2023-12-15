Presentation can also be found at: https://clipchamp.com/watch/eVoHCRkKboj


to test just run python SolomonReed.py

SolomonReed.py includes functions to:
	- encode a message into a Reed-Solomon code
	- decode a Reed-Solomon code into its original message
	- randomly corrupt a message to test the decoder

3 test cases are included, including:
	- [1,5,2,3,7]
	- "Hello"
	- "Hello world"

[1,5,2,3,7] and "Hello" are run with 2 random corruptions in the encoded message, this represents up to 16 bit flips in the best case, or 2 bit flips in the worst case.

"Hello world" is ran with no corruptions, encoding and then decoding, as well as with 1 corruption


To add test cases:
	under main():
		-call upon test() function:
			test(message, codedMessageLength: int, isWord: bool, toCorrupt: bool, 			     NumberOfCorruptions: int)
			where to run:   codedMessageLength > len(message)
					NumberOfCorruptions < codedMessageLength
				
			i.e. if you wanted to code and decode "Algorithm", with 2 random 			character corruptions
			- test("Algorithm", 12, True, True, 2)
			in this case three parity char would be added into the encoded 				message
