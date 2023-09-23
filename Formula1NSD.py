
import numpy as np
import pandas as pd

# in this file to analyse F1 competitiveness I calculated standard deviation of each point table at the end of the
# season, the points awarding was normalised using the modern points system and based of the race standings obtained
# from csv file. At the end i created list of all standard deviations and determined the lowest standard deviation
# what indicates scores closer to the mean which suggests less domination by one driver and high competitiveness
# between the drivers

# reading the files


results = pd.read_csv('results.csv') #, names = ["resultId", "raceId", "driverId", "constructorId", "number", "grid", "position", "positionText", "positionOrder", "points", "laps", "time", "milliseconds", "fastestLap", "rank", "fastestLapTime", "fastestLapSpeed", "statusId"], header = None)
drivers = pd.read_csv('drivers.csv') #, names = ["driverId", "driverRef", "number", "code", "forename", "surname", "dob", "nationality", "url"], header = None)
races = pd.read_csv("races.csv") #, names = ["raceId", "year", "round", "circuitId", "name", "date", "time", "url", "fp1_date", "fp1_time", "fp2_date", "fp2_time", "fp3_date", "fp3_time", "quali_date", "quali_time", "sprint_date", "sprint_time"], header = None)
driver_standings = pd.read_csv("driver_standings.csv") #, names = ["driverStandingsId", "raceId", "driverId", "points", "position", "positionText", "wins"], header = None)

# assigning race ids to each year

grouped_data = races.groupby('year')['raceId'].apply(list)
race_ids_by_year = np.array(grouped_data)
race_ids_by_year = race_ids_by_year[:-4]

points_system = {
    1: 25,
    2: 18,
    3: 15,
    4: 12,
    5: 10,
    6: 8,
    7: 6,
    8: 4,
    9: 2,
    10: 1
}

def assign_race_points(season_df, race_df):
    for i in range(0, len(race_df)):
        points_to_add = race_df.loc[i, "Points"]
        if not race_df.loc[i, "driverId"] in season_df["driverId"].tolist():

            new_driver_id = race_df.loc[i, "driverId"]
            new_row = pd.DataFrame([{"driverId": new_driver_id, "points": 0}])
            season_df = pd.concat([season_df, new_row], ignore_index=True)

        driver_id = drivers_positions.loc[i, "driverId"]
        index = season_df[season_df['driverId'] == driver_id].index[0]
        season_df.loc[index, "points"] = season_df.loc[index, "points"] + race_df.loc[i, "Points"]


    return season_df

std_list = []

for year_ids in race_ids_by_year:
    driver_standings_year = driver_standings[driver_standings['raceId'] == year_ids[0]]
    drivers_year = driver_standings_year['driverId']

    points = pd.DataFrame({'points': [0] * len(driver_standings_year)})

    drivers_year.reset_index(drop=True, inplace=True)
    points.reset_index(drop=True, inplace=True)
    drivers_year_table = pd.concat([drivers_year, points], axis=1)

    for race_id in year_ids:

        drivers_positions = driver_standings[driver_standings['raceId'] == race_id]
        drivers_positions = drivers_positions[["driverId", "position"]]
        drivers_positions = drivers_positions.sort_values(by='position')
        drivers_positions['Points'] = drivers_positions['position'].map(points_system)
        drivers_positions['Points'].fillna(0, inplace=True)
        drivers_positions.reset_index(drop=True, inplace=True)
        drivers_year_table = assign_race_points(drivers_year_table, drivers_positions)




    drivers_year_table = drivers_year_table.sort_values(by='points', ascending=False)
    std = drivers_year_table["points"].std()
    std_list.append(std)




print(std_list)
print(min(std_list))
























# def get_name(id):
#     # Filter the DataFrame to find the row with the matching driverId
#     driver_info = drivers[drivers['driverId'] == id]
#
#     if not driver_info.empty:
#         # Extract the forename and surname from the DataFrame
#         forename = driver_info['forename'].values[0]
#         surname = driver_info['surname'].values[0]
#
#         return forename, surname

