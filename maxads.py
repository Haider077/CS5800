import pandas as pd

# Mock ads data with ad id, height, length and corresponding value
# the value of the ad has a positive correlation with the ad's size
ads = [
    {"ad_id": 1, "height": 3, "width": 2, "value": 50},
    {"ad_id": 2, "height": 2, "width": 3, "value": 40},
    {"ad_id": 3, "height": 4, "width": 4, "value": 70},
    {"ad_id": 4, "height": 5, "width": 5, "value": 60},
    {"ad_id": 5, "height": 6, "width": 3, "value": 80},
    {"ad_id": 6, "height": 2, "width": 6, "value": 65},
    {"ad_id": 7, "height": 7, "width": 7, "value": 120},
    {"ad_id": 8, "height": 3, "width": 3, "value": 45},
    {"ad_id": 9, "height": 8, "width": 4, "value": 100},
    {"ad_id": 10, "height": 5, "width": 6, "value": 95},
]

ads_df = pd.DataFrame(ads)

# The length and width of the area for ads display, assume l = w = 8 for now
max_length = 8
max_width = 8

# Initialize the 3D dynamic programming table
n = len(ads)  # Number of ads
dp = [[[0] * (max_width + 1) for _ in range(max_length + 1)] for _ in range(n + 1)]

# dp process
for i in range(1, n + 1):
    for l in range(max_length + 1):
        for w in range(max_width + 1):
            ad_height = ads_df.loc[i - 1, "height"]
            ad_width = ads_df.loc[i - 1, "width"]
            ad_value = ads_df.loc[i - 1, "value"]

            if ad_height <= l and ad_width <= w:
                # Option 1: Do not select the current ad, value remains unchanged
                # Option 2: Select the current ad, add its value to the remaining capacity
                dp[i][l][w] = max(
                    dp[i - 1][l][w],  # Without current ad
                    dp[i - 1][l - ad_height][w - ad_width] + ad_value  # With current ad
                )
            else:
                # Ad cannot fit in the remaining capacity, keep the previous value
                dp[i][l][w] = dp[i - 1][l][w]

# Maximum value achievable
max_value = dp[n][max_length][max_width]

# Trace back to find the selected ads
selected_ads = []
l, w = max_length, max_width
for i in range(n, 0, -1):
    if dp[i][l][w] != dp[i - 1][l][w]:  # Value changed, meaning ad was selected
        selected_ads.append(ads_df.loc[i - 1, "ad_id"])
        l -= ads_df.loc[i - 1, "height"]
        w -= ads_df.loc[i - 1, "width"]

selected_ads.reverse() # Reverse the list of selected ads to maintain correct order

print(selected_ads)

