from names_dataset import NameDataset
nd = NameDataset()

print(nd.get_top_names(n=10000, country_alpha2='IN')['IN']['M'].index('Vatsal'))