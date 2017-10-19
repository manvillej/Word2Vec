#imports aka libraries of reusable code
import numpy as np #numerical programming library
from nltk.stem import PorterStemmer #normalizes words
import re #regex
import string #to get rid of all punctuation
import pandas as pd



def main():

	# opens the file you want
	print("loading file and getting contents...")
	textfile = open("./THELONBOXHEALTHLAWS.txt", 'r')

	#get contents in an array
	contents = getWordArray(textfile)
	textfile.close()

	print("Cleaning, stemming, and splitting content...")
	#clean and stem the words
	contents = sorted(stemWords(contents))


	print("Creating dictionary from contents...")
	#get unique words
	uniqueWords = getUniqueWordList(contents)


	print("Saving dictionary...")
	#save the unique words in dictionary
	df = pd.DataFrame(uniqueWords, columns=["Dictionary:"])
	df.to_csv('dictionary.csv', index=False)

	textfile = open("./dictionary.csv", 'r')

	print("Loading dictionary...")
	#get the dictionary words
	words = textfile.readlines()
	words.pop(0)
	textfile.close()

	#Creating dictionary of values
	i = 0
	dictionary = {}
	for word in words:
			value = word.split()
			dictionary[value[0]] = i
			i = i + 1

	count = np.zeros(len(dictionary))


	print("Getting word count...")
	for word in contents:
		i = dictionary[word]
		count[i] = count[i]+1
	
	inverseDictionary = {v: k for k, v in dictionary.items()}


	print("Creating word2Frequency file...")
	outputFile = open('word2Frequency.csv', 'w')
	print('Word: Count')
	for i in range(count.shape[0]):
		print('{}: {}'.format(inverseDictionary[i],int(count[i])))
		outputFile.write('{}, {},\n'.format(inverseDictionary[i],int(count[i])))

	outputFile.close()	



def getWordArray(file):
	#reads the contents into a variable
	contents = file.read()

	#sets all text to lower case
	contents = contents.lower()

	#remove all numbers
	numRegex = re.compile('[0-9]+')
	contents = numRegex.sub('', contents)

	#remove all punctuations
	contents = contents.strip(string.punctuation)
	
	#remove all punctuation
	punctuationRegex = re.compile('[^\w\s]|_')
	contents = punctuationRegex.sub('', contents)

	#split the contents into an array of words
	contents = contents.split()
	return contents	

def stemWords(wordArray):
	#stem the word
	
	#word vector to be returned
	wordVector = []
	
	#create instance of word stemmer
	ps = PorterStemmer()
	
	#stem each word in the word array
	for word in wordArray:
		word = ps.stem(word)
		wordVector.append(word)
	
	#return word vector 
	return wordVector

def getUniqueWordList(wordArray):
	#get unique list of words in array
	vocab = set(wordArray)
	return list(vocab)


if __name__ == '__main__':
	main()