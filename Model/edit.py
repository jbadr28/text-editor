import pickle
with open('word_prob.pkl','rb') as f:
    probs = pickle.load(f)
print(probs)
