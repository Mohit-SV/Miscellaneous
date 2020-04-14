def similarity_score_2strings(company1, company2):
  """returns a similarity score (normalized) between two formatted strings (2 company names) i.e. without special characters"""

  list_matched_letters = [] 
  score = 0
  list_company1_letters = list(company1) 
  index = 0 
  for i, letter in enumerate(company2):  
    # letter passes try only if it is found in company1
    try:    
      pos_in_company1 = list_company1_letters.index(letter) 
      # bonus just for being matched
      score += 2 
      list_matched_letters.append(pos_in_company1)
      # to handle repeating matched letters
      list_company1_letters[pos_in_company1] = "#"
      # score given wrt diff btw indexes of letter matched in company1 and company2
      weight1 = (list_matched_letters[index]-i)
      score += 5/(abs(weight1)+1)
      # score given wrt how close the letters matched in company1
      if index>0:
        weight2 = (list_matched_letters[index]-list_matched_letters[index-1])
        if weight2>0:
          score += 3/(weight2)
        elif weight2<0:
          score -= ((-weight2)*(1/5))
      index += 1
    except:
      pass
  spect = (''.join(list_company1_letters)).split()
  # print(spect)
  try:
    score -= (len((spect[0]))-(spect[0]).count("#"))*10
  except:
    score += 0
  
  # highest possible score
  norm_val = 0
  for word in company2.split():
    norm_val += ((10*len(word)-3)/((i+1)**2))*40

  return score/norm_val


print('similarity_score: ', similarity_score_2strings("sjwjn sjw", "stwjn sjwamm"))