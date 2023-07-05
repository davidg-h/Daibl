import json
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
import nltk
nltk.download('punkt')

warnings.filterwarnings(action = 'ignore')

import gensim
from gensim.models import Word2Vec


rawtext = ""
with open('videoParametersRecipe.json') as json_file:
        data = json.load(json_file)
    
        
        for videodata in data:
            
            if videodata and videodata["recipeName"].strip() != videodata["recipeText"].strip() and len(videodata["recipeName"]) > 50:
                rawtext += videodata["recipeText"] + " "

# print(rawtext)



# iterate through each sentence in the file
for i in sent_tokenize(rawtext):
	temp = []
	
	# tokenize the sentence into words
	for j in word_tokenize(i):
		temp.append(j.lower())

	data.append(temp)

# Create CBOW model
model1 = gensim.models.Word2Vec(data, min_count = 1,
							vector_size = 100, window = 5)

first =     "cinnamon"
second =    "tasty"

# Print results
print(f"Cosine similarity between '{first}' " +
			f"and '{second}' - CBOW : ",
	model1.wv.similarity(first, second))

# Create Skip Gram model
model2 = gensim.models.Word2Vec(data, min_count = 1, vector_size = 100,
											window = 5, sg = 1)


# Print results


print(f"Cosine similarity between '{first}' " +
			f"and '{second}' - Skip Gram : ",
	model2.wv.similarity(first, second))

