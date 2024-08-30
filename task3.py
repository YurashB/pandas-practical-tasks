import pandas as pd

datafile = "aggregated_airbnb_data.csv"

data = pd.read_csv(datafile)

pivot_price_room_type_neigh = pd.pivot_table(data=data, index="room_type", columns="neighbourhood_group",
                                             values="price", aggfunc="mean")

melt_price_minimum_nights = pd.melt(data, id_vars=['id', 'name', 'host_id', 'host_name', 'neighbourhood_group',
                                                   'neighbourhood', 'latitude', 'longitude', 'room_type'],
                                    value_vars=["price", "minimum_nights"],
                                    var_name="metric", value_name="value")


def availability_status(availability):
    if availability < 50:
        return "Rarely Available"
    elif availability > 200:
        return "Highly Available"
    else:
        return "Occasionally Available"


data["availability_status"] = data["availability_365"].apply(availability_status)

melt_avail_price_numb_of_rev_neigh_group = pd.melt(data, id_vars="availability_status",
                                                   value_vars=["price", "number_of_reviews", "neighbourhood_group"],
                                                   var_name="metric", value_name="value")

description = data[["price", "minimum_nights", "number_of_reviews", ]].agg(["mean", "median", "std"])
data["last_review"] = pd.to_datetime(data["last_review"])
data.set_index("last_review", inplace=True)
identify_monthly_rends = data.resample("M").agg({
    "number_of_reviews": "sum",
    "price": "mean"
})

analyze_seasonal_patterns = data.resample("M").agg({
    "number_of_reviews": "mean",
    "price": "mean"
}).reset_index()

def print_dataframe_info(data, message=""):
    print(message + "\n" + str(data) + "\n")


print(pivot_price_room_type_neigh, "Using pivot_table func:")
print(melt_price_minimum_nights, "Using melt func:")
print(melt_avail_price_numb_of_rev_neigh_group, "Analyze availability status:")
print(description, "Perform description:")
print(identify_monthly_rends, "Identify Monthly Trends: ")
print(analyze_seasonal_patterns, "Analyze Seasonal Patterns: ")

analyze_seasonal_patterns.to_csv("time_series_airbnb_data.csv", index=True)
