# data loader for the CultureCentreDistances dataset
import pandas as pd

culture_centre_distances = pd.read_csv("datasets/CultureCentreDistances.csv")

centre_distances_vistors=culture_centre_distances.loc[:,["Culture Centre","C_Postal_Code","Distance (kms)"]].dropna().groupby(["Culture Centre","C_Postal_Code"]).agg(['mean','count'])
centre_distances_vistors=centre_distances_vistors.droplevel(0,axis=1).reset_index()

cumul_distances_visitors=culture_centre_distances.loc[:,["Culture Centre","C_Postal_Code","Distance (kms)","Postal Code"]].dropna().sort_values(["Culture Centre","C_Postal_Code","Distance (kms)"])
cumul_distances_visitor=cumul_distances_visitors.groupby(["Culture Centre","C_Postal_Code","Distance (kms)"]).count().reset_index()
cumul_distances_visitor=cumul_distances_visitor.rename(columns={'Postal Code':'#visitors'})
cumul_distances_visitor['cumul#vistors']=cumul_distances_visitor.groupby(["Culture Centre","C_Postal_Code"])["#visitors"].apply(lambda x: x.cumsum())
