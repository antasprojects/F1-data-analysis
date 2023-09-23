
import numpy as np
import pandas as pd

# In this file I looked at unique grand prix winners to decide which year in formula 1 was the most competitive. I
# obtained grand prix winners from each season note unique ones and then divided them by number of grand prix to
# eliminate bias resulted from various number of grand prixes in each season. The highest coefficient indicates more
# unique winners per race what suggests competitiveness



# reading the files

races = pd.read_csv("races.csv", names = ["raceId", "year", "round", "circuitId", "name", "date", "time", "url", "fp1_date", "fp1_time", "fp2_date", "fp2_time", "fp3_date", "fp3_time", "quali_date", "quali_time", "sprint_date", "sprint_time"], header = None)
driver_standings = pd.read_csv("driver_standings.csv", names = ["driverStandingsId", "raceId", "driverId", "points", "position", "positionText", "wins"], header = None)

winners = driver_standings.loc[driver_standings["position"] == "1", ["raceId", "driverId"]]

grouped_data = races.groupby('year')['raceId'].apply(list)
race_id_by_year = np.array(grouped_data)
race_id_by_year = race_id_by_year[:-4]

# print(race_id_by_year)
# print(winners)



# assigning race ids to the appropriate years
winners_id_by_year = []
for index, year in enumerate(race_id_by_year):
    winners_id_by_year.append([])
    for raceid in year:
        current_race = winners[winners['raceId'] == raceid]
        current_winner_id = current_race.iloc[0][1]
        winners_id_by_year[index].append(current_winner_id)
        # print(current_race)
        # print(current_winner_id)


# calculating and listing coefficients
coefficients = []
for winners_list in winners_id_by_year:
    winners_set = set(winners_list)
    unique_winners_coefficient = len(winners_set) / len(winners_list)
    coefficients.append(round(unique_winners_coefficient, 3))


# creating list of years
years = []
for i in range(len(coefficients)):
    years.append(1950 + i)



# finding maximum
max = max(coefficients)

# finding the indexes of the maximum
x = [i for i in range(len(coefficients)) if coefficients[i] == max]

# converting data into data frame
data = {'Year': years, 'Coefficient': coefficients}
df = pd.DataFrame(data)
print(df)


# line for exporting the data frame to csv file
# df.to_csv('table.csv', index=False)





