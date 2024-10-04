import sys
import csv
import asyncio
from wom import Client,PlayerDetail
from snake_and_ladder_calc import SnakesAndLadderPointsService


async def main():
    if len(sys.argv) < 3:
        print("Please provide both the CSV file names as arguments.")
        sys.exit(1)

    user_file_name = sys.argv[1]
    boss_file_name = sys.argv[2]
    user_list = get_usernames_from_csv(user_file_name)
    boss_filter_list = get_eligible_bosses_from_csv(boss_file_name)
    client = Client(user_agent="@z.engineer")
    users_boss_kc = {}

    try:
        await client.start()

        # Fetch all user details concurrently
        tasks = [player_fetch_details(client, user) for user in user_list]
        user_details = await asyncio.gather(*tasks)

        # Process the results
        for user, user_detail in zip(user_list, user_details):
            if isinstance(user_detail, str) and user_detail.startswith("ERROR"):
                print(f"Error fetching details for {user}: {user_detail}")
                continue
            users_boss_kc[user] = get_boss_kc(user_detail, boss_filter_list)

        # Calculate points using the service
        points_service = SnakesAndLadderPointsService(users_boss_kc)
        user_points = points_service.calculate_points()

        # Print the results
        for username, points in user_points.items():
            print(f"{username}: {points:.2f} points")

    finally:
        await client.close()


async def player_fetch_details(client, name):
    try:
        result = await client.players.get_details(name)
        if result.is_ok:
            return result.unwrap()
        else:
            return f"ERROR: {result.unwrap_err()}"
    except Exception as e:
        return f"ERROR: Unexpected error occurred: {str(e)}"


def get_usernames_from_csv(username_file):
    user_list = []
    with open(username_file, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            user_list.extend(row)
    return user_list

def get_eligible_bosses_from_csv(boss_file):
    boss_list = []
    with open(boss_file, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            boss_list.extend(row)
    return boss_list

def get_boss_kc(user_detail: PlayerDetail,boss_filter_list):
    total_boss_info = user_detail.latest_snapshot.data.bosses
    filtered_boss_kc = {}
    for eligible_boss in boss_filter_list:
        filtered_boss_kc[eligible_boss] = total_boss_info[eligible_boss].kills
    return filtered_boss_kc

if __name__ == '__main__':
    asyncio.run(main())