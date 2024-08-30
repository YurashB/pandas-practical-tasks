import pandas as pd

datafile = "cleaned_airbnb_data.csv"

data = pd.read_csv(datafile)


def print_dataframe_info(data, message=""):
    print(message + "\n" + str(data) + "\n")

# ---- Aggregation and Grouping -------
grouped_1 = data.groupby(["neighbourhood_group", "price_category"]).agg({
    "price": ["mean"],
    "minimum_nights": ["mean"],
    "number_of_reviews": ["mean"],
    "availability_365": ["mean"]
}).reset_index()

grouped_1.columns = ["neighbourhood_group", "price_category", "avg_price", "avg_minimum_nights", "avg_number_of_reviews", "avg_availability_365"]
# ---- Aggregation and Grouping -------



# ---- Data Sorting and Ranking -------
grouped_2 = data.groupby("neighbourhood_group").agg({
    "id": "count",
    "price": "mean"
}).reset_index()

grouped_2.columns = ["neighbourhood_group", "total_listings", "average_price"]
grouped_2["listings_rank"] = grouped_2["total_listings"].rank(ascending=False)
grouped_2["price_rank"] = grouped_2["average_price"].rank(ascending=False)
ranked_neighbourhoods = grouped_2.sort_values(by=["listings_rank", "price_rank"])

print_dataframe_info(message="Using loc to find rows where price is 10: ",
                     data=data.loc[data["price"] == 10, ["price", "name"]])
print_dataframe_info(message="Using iloc to get some col and rows:", data=data.iloc[0:3, 0:3])
print_dataframe_info(message="Filter the dataset where neighborhood is Harlem:",
                     data=data.loc[data["neighbourhood"] == "Harlem", ["id", "name", "neighbourhood"]])
print_dataframe_info(message="Filter the dataset where price > $100 and a number_of_reviews > 10:", data=data.loc[
    (data["price"] > 100) & (data["number_of_reviews"] > 10), ["price", "number_of_reviews"]])

print_dataframe_info(
    message="Select specific columns",
    data=data.loc[:, ["neighbourhood_group", "price", "minimum_nights", "number_of_reviews", "availability_365"]])
print_dataframe_info(message="Calculate the average price and minimum_nights for each group:", data=grouped_1)
print_dataframe_info(message="Sort price in DESC:", data=data[["id", "price"]].sort_values(by="price", ascending=False))
print_dataframe_info(message="Sort minimum_nights in ASC:", data=data[["id", "minimum_nights"]].sort_values(by="minimum_nights", ascending=True))
print_dataframe_info(message="Ranking of neighborhoods based on the total number of listings and the average price:", data=ranked_neighbourhoods)

data.to_csv("aggregated_airbnb_data.csv", index=True)