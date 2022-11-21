import sys
import random
import math


def generate_shingles(file_path, k):
  docs = open(file_path, "r").readlines()
  docs = [doc.split(" ", 1) for doc in docs]
  docs = [[k, v.lower()] for k,v in docs]
  docs = [[k, "".join(ch for ch in v if (ch.isalpha() or ch.isspace()))] for k,v in docs ]
  # docs = [[k, " ".join(v.split())] for k,v in docs ]

  for i in range(len(docs)):
    templist = []
    for j in range(len(docs[i][1]) - (k - 1)):
      templist.append(docs[i][1][j:(j+k)])
    docs[i] = [docs[i][0], templist]
  
  return docs

def all_uniq_shingles(docs):
  output = []
  for doc in docs:
    output = list(set(output) | set(doc[1]))
  return output


def permutations(n, num_of_signatures):
  c = n
  while True:
    c_is_prime = True
    for i in range(2,c):
      if (c%i) == 0:
        c_is_prime = False
        break
    if (c_is_prime == True):
        break
    else:
        c += 1

  all_permutations = []
  for i in range(num_of_signatures):
    k = random.randint(0, c-1)
    l = random.randint(0, c-1)
    each_permutation = []
    for j in range(n):
      each_permutation.append((k*j + l) % c)
    all_permutations.append(each_permutation)
  
  return all_permutations


def generate_signatures(docs, uniq_shingles, all_permutations):
  num_of_docs = len(docs)
  num_of_signatures = len(all_permutations)
  num_of_rows = len(uniq_shingles)

  signature_matrix = [[math.inf]*num_of_signatures for _ in range(num_of_docs)]

  for r in range(num_of_rows):
    for c in range(num_of_docs):
      if (uniq_shingles[r] in docs[c][1]):
        for i in range(num_of_signatures):
          signature_matrix[c][i] = min(signature_matrix[c][i], all_permutations[i][r])
  
  return signature_matrix


def lsh_technique(signature_matrix, b, r):
  num_of_docs = len(docs)
  general_band_matrix = []

  i = 0
  for j in range(b):
    single_band_matrix = []
    for column in signature_matrix:
      single_band_matrix.append(column[i:((j+1)*r)])
    general_band_matrix.append(single_band_matrix)
    i += r

  index_candidate_pairs = []
  for band in general_band_matrix:
    for x in range(num_of_docs-1):
      for y in range(x+1, num_of_docs):
        if (band[x] == band[y]):
          if ((x, y) not in index_candidate_pairs):
            index_candidate_pairs.append((x, y))

  return index_candidate_pairs

def jaccard_filtering(docs, signature_matrix, index_candidate_pairs, threshold):
  similar_pairs = []
  for (i1, i2) in index_candidate_pairs:
    intersection_size = len(set(signature_matrix[i1]) & set(signature_matrix[i2]))
    union_size = len(set(signature_matrix[i1]) | set(signature_matrix[i2]))
    jaccard_sim = (intersection_size/union_size)
    if (jaccard_sim >= threshold):
      similar_pairs.append([docs[i1][0], docs[i2][0]])
  
  return similar_pairs

filePath = sys.argv[1]
docs = generate_shingles(filePath, 3)
uniq_shingles = all_uniq_shingles(docs)
b = 6
r = 20
all_permutations = permutations(len(uniq_shingles), b*r)
signature_matrix = generate_signatures(docs, uniq_shingles, all_permutations)
candidate_pairs = lsh_technique(signature_matrix, b, r)
similar_pairs = jaccard_filtering(docs, signature_matrix, candidate_pairs, 0.9)

for (id1, id2) in similar_pairs:
    print(id1 + "\t" + id2)

