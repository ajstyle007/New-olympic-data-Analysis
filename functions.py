import pandas as pd

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

def preprocess1(df, region_df):
    
    
    #filtering for summer olympics
    df = df[df["Season"] == "Summer"]

    #merging with noc_regions data
    df = df.merge(region_df, on="NOC", how="left")

    #dropping duplicates
    df.drop_duplicates(inplace=True)

    #one hot encoding medal column
    dummy = pd.get_dummies(df["Medal"], dtype=int)

    #and concat dummy with original data 
    df = pd.concat([df, dummy], axis=1)

    return df

