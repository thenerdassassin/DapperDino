import pandas as pd


dinoTraitReader = pd.read_csv('../dapper_dino_traits.csv')

dinoTraitReader = dinoTraitReader[dinoTraitReader.Classification == 'Karma']
dinoTraitReader = dinoTraitReader[['Dino Number', 'Image', 'Classification']]

#split string at 'K'
dinoTraitReader['Image'] = dinoTraitReader.Image.apply(lambda x: x.split('K')[-1])
#split string at '.'
dinoTraitReader['Image'] = dinoTraitReader.Image.apply(lambda x: x.split('.')[-2])

 #remove (classification) reorder and rename remaining columns
dinoTraitReader = dinoTraitReader[['Image', 'Dino Number']]
dinoTraitReader.columns = ['KarmaNumber', 'DinoNumber']

# Sort values by Dino Number and Export to CSV
dinoTraitReader.sort_values(by = 'DinoNumber')
dinoTraitReader.to_csv("../dapper_karma_to_dino.csv", index=False)