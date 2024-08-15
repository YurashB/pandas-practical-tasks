import pandas as pd

datafile = "AB_NYC_2019.csv"

data = pd.read_csv(datafile)


def print_dataframe_info(data, message=""):
    print(message + "\n" + str(data) + "\n")

def categorize_price(price):
    if price < 100:
        return "Low"
    elif 100 <= price < 300:
        return "Medium"
    else:
        return "High"
def categorize_stay(minimum_nights):
    if minimum_nights <= 3:
        return "Short-term"
    elif 4 <= minimum_nights <= 14:
        return "Medium-term"
    else:
        return "Long-term"



print_dataframe_info(message="Inspect the first few rows:", data=data.head(4))
print_dataframe_info(message="Number of entries:", data=data.info(verbose=False,
                                                                  show_counts=False))
print_dataframe_info(message="Missing values per column:", data=data.isna().sum())

data.fillna({"name" : "Unknown", "host_name" : "Unknown", "last_review" : "NaT"}, inplace=True)
data.drop(data[data["price"] == 0 ].index, inplace=True) # remove zero price rows
print_dataframe_info(message="Replace missing data in column [name, host_name , last_reviewed]:", data=data[data["name"] == "Unknown"])

data["price_category"] = data["price"].apply(categorize_price)
data["length_of_stay_category"] = data["minimum_nights"].apply(categorize_stay)
print_dataframe_info(message="Categorized data by price and a length_of_stay_category", data=data[["price", "price_category", "minimum_nights", "length_of_stay_category"]])

#data.to_csv("cleaned_airbnb_data.csv", index=True)