
import pandas as pd

# Mock ads data
ads = [
    {"ad_id": 1, "height": 3, "width": 2, "value": 50},
    {"ad_id": 2, "height": 2, "width": 3, "value": 40},
    {"ad_id": 3, "height": 5, "width": 5, "value": 110},
    {"ad_id": 4, "height": 6, "width": 4, "value": 105},
    {"ad_id": 5, "height": 7, "width": 3, "value": 95},
]

ads_df = pd.DataFrame(ads)

# Initialize DP table
dp = [{} for _ in range(len(ads) + 1)]
dp[0][tuple([(6, 8)])] = 0  # Initial state: one large rectangle (6x8)

# Record selected ads for each state
selected_ads = [{} for _ in range(len(ads) + 1)]

# update remaining space by appending ads to the right(first choice) or below (alternative)
def split_space_left_to_right(space, ad_height, ad_width):
    h, w = space[0]  # Current space dimensions
    new_spaces = []
    if w >= ad_width and h >= ad_height:
        # Place ad to the right
        if w > ad_width:
            new_spaces.append((h, w - ad_width))
        # Remaining space below
        if h > ad_height:
            new_spaces.append((h - ad_height, w))
    return new_spaces

# DP process
for i in range(1, len(ads) + 1):
    ad_id, ad_height, ad_width, ad_value = ads_df.loc[i - 1, ["ad_id", "height", "width", "value"]]

    for prev_space, prev_value in dp[i - 1].items():
        # Option 1: Do not select the ad
        if prev_space not in dp[i] or dp[i][prev_space] < prev_value:
            dp[i][prev_space] = prev_value
            selected_ads[i][prev_space] = selected_ads[i - 1].get(prev_space, [])

        # Option 2: Seelect the Ad
        for j, rect in enumerate(prev_space):
            if ad_height <= rect[0] and ad_width <= rect[1]:
                # Update remaining space
                new_spaces = split_space_left_to_right([rect], ad_height, ad_width)
                new_space = tuple(sorted(list(prev_space[:j]) + new_spaces + list(prev_space[j + 1 :])))

                # Update DP table if the new value is higher
                new_value = prev_value + ad_value
                if new_space not in dp[i] or dp[i][new_space] < new_value:
                    dp[i][new_space] = new_value
                    selected_ads[i][new_space] = selected_ads[i - 1].get(prev_space, []) + [ad_id]

# Find maximum profit and selected ads
max_profit = 0
best_space = None
for space, profit in dp[len(ads)].items():
    if profit > max_profit:
        max_profit = profit
        best_space = space

# Output results
print("Maximum Profit:", max_profit)
print("Selected Ads:", selected_ads[len(ads)][best_space])