import pandas as pd

data = {'Description':['Enhance Existing Support Programs',
					   'Optimize Existing Cultural Facilities',
					   'Find More & Different Kinds of Affordable Cultural Spaces',
					   'Integrate Heritage as Part of Cultural Vitality',
					   'Enhance Cultural Vitality at the Street Level',
					   'Build Personal Connections to Cultural Vitality',
				       'Measure Cultural Vitality & Understand the Outcomes',
				       'Capitalize on Culture for Tourism & the Economy',
				       'Convene & Connect the Cultural Community',
				       'Integrate Culture into Plans and Processes and Use Innovative Funding Approaches']}

# Creates pandas DataFrame.
df_goal = pd.DataFrame(data, index =['Goal 1','Goal 2','Goal 3','Goal 4','Goal 5','Goal 6','Goal 7','Goal 8','Goal 9','Goal 10'])
df_goal.reset_index(inplace=True)
df_goal.rename(columns={'index':'Goal'},inplace=True)
