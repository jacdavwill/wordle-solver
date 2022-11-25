import sys
import time

#data = sys.stdin.read()
file = open('wordle-dictionary.txt', 'r')
data = file.read()

validGuesses = data.split('\n')[:-1]
print("Orig guesses:",len(validGuesses))
validSolutions = validGuesses[:2315] # 
print("Orig Solutions:",len(validSolutions))

#validGuesses = ["momma", "admit"]
#validSolutions = ["momma", "admit"]

results = {}

def evaluateGuess(solution, guess):
	grey = []
	yellow = []
	green = []
	wrongPos = []
	
	for i, letter in enumerate(guess):
		if solution[i] == letter:
			green.append((letter, i))
		else:
			wrongPos.append(i)
			
	for i in wrongPos:
		letter = guess[i]
		if letter not in solution:
			grey.append((letter,i))
		else:
			if solution.count(letter) > (guess[:i].count(letter) + [x[0] for x in green].count(letter)):
				yellow.append((letter,i))
			else:
				grey.append((letter,i))
				
	
	return grey, yellow, green


def evaluateGuessX(solution, guess):
	grey = {}
	yellow = {}
	green = {}
	wrongPos = []
	
	for i, letter in enumerate(guess):
		if solution[i] == letter:
			if (green.get(letter) != None):
				green[letter].append(i)
			else:
				green[letter] = [i]
		else:
			wrongPos.append(i)
			
	for i in wrongPos:
		letter = guess[i]
		if letter not in solution:
			if (grey.get(letter) != None):
				grey[letter].append(i)
			else:
				grey[letter] = [i]
		else:
			if solution.count(letter) > (guess[:i].count(letter) + [x[0] for x in green].count(letter)):
				if (yellow.get(letter) != None):
					yellow[letter].append(i)
				else:
					yellow[letter] = [i]
			else:
				if (grey.get(letter) != None):
					grey[letter].append(i)
				else:
					grey[letter] = [i]
				
	
	return grey, yellow, green
			
			
def pruneOpts(evals, opts, debug = False):
	results = []
	for word in opts:
		if keepWordX(evals, word, debug):
			results.append(word)
	return results
			
			
def keepWordX(evals, word, debug):
	if debug:
		return True
	for eval in evals:
		(grey, yellow, green) = eval
		for key in green:
			for pos in green[key]:
				if word[pos] != key:
					return False
		for key in yellow:
			if len(yellow[key]) > word.count(key):
				return False
			for pos in yellow[key]:
				if word[pos] == key:
					return False
		for key in grey:
			ySize = 0
			greenSize = 0
			if yellow.get(key) != None:
				ySize = len(yellow[key])
			if green.get(key) != None:
				greenSize = len(green[key])
			if word.count(key) > ySize + greenSize:
				return False
			for pos in grey[key]:
				if word[pos] == key:
					return False
	return True

def keepWord(evals, word, debug):
	if debug:
		return True
	for eval in evals:
		(grey, yellow, green) = eval
		for entry in green:
			if word[entry[1]] != entry[0]:
				return False
		for entry in grey:
			if word[entry[1]] == entry[0] or (word.count(entry[0]) > [x[0] for x in yellow].count(entry[0]) + [x[0] for x in green].count(entry[0])):
				return False
		for entry in yellow:
			if word[entry[1]] == entry[0]:
				return False
			if [x[0] for x in yellow].count(entry[0]) > word.count(entry[0]):
				return False
	return True

for word in validSolutions:
	if word[-1] == 'y' and word[1] == 'o' and word.count("o") < 2:
		print(word)


asdf

currentEval = [
	#({"c":[0],"r":[1],"n":[3],"e":[4]},
	#{"a":[2]},
	#{}),
	
	#({"l":[0],"b":[3],"s":[4]},
	#{"a":[1]},
	#{"m":[2]})
]

start = time.time()
validSolutions = pruneOpts(currentEval, validSolutions)
validGuesses = pruneOpts(currentEval, validGuesses)
initPrune = time.time()

print("Guesses:", len(validGuesses))
print("Solutions:", len(validSolutions))
print("Iterations:", len(validSolutions)*len(validSolutions)*len(validSolutions))
				
for x, solution in enumerate(validSolutions):
	print(x, "/", len(validSolutions))
	#if x % 10 == 0:
	#	print(x, "/", len(validSolutions))
	totSolutionsLeft = 0
	for guess in validSolutions:
		eval = evaluateGuessX(solution, guess)
		solutionsLeft = pruneOpts(currentEval + [eval], validSolutions, debug=False)
		totSolutionsLeft += len(solutionsLeft)
	results[solution] = totSolutionsLeft
end = time.time()

print()
print("Summary")
print("Inital prune:", initPrune - start, "seconds")
print("Solve       :", end - initPrune, "seconds")
print(sorted(results.items(), key=lambda item: item[1])[:10])

# results
# init prune :   0.03 seconds
# no-op solve:   3.07 seconds
# solve      : 105.08 seconds

# gen-X (remove keepword .counts)
# init prune :   0.01 seconds
# no-op solve:   3.24 seconds
# solve      :  57.24 seconds


# solution: admit
# crane: 274 left - 134 left (1200 guesses)
# lambs: 2 left - 
