class SnakesAndLadderPointsService:
    def __init__(self, users_boss_kc):
        self.users_boss_kc = users_boss_kc

    def calculate_points(self):
        user_points = {}
        for username, boss_kc in self.users_boss_kc.items():
            points = self._calculate_user_points(boss_kc)
            user_points[username] = points
        return user_points

    def _calculate_user_points(self, boss_kc):
        # Calculate total KC for bosses with two versions
        total_chambers = boss_kc.get('chambers_of_xeric', 0) + boss_kc.get('chambers_of_xeric_challenge_mode', 0)
        total_tombs = boss_kc.get('tombs_of_amascut', 0) + boss_kc.get('tombs_of_amascut_expert', 0)
        total_theatre = boss_kc.get('theatre_of_blood', 0) + boss_kc.get('theatre_of_blood_hard_mode', 0)
        corrupted_gauntlet = boss_kc.get('the_corrupted_gauntlet', 0)

        # Apply the formula
        points = (
            min(1, total_theatre / 100) +
            min(1, total_tombs / 100) +
            min(1, total_chambers / 100) +
            min(1, corrupted_gauntlet / 400)
        )

        return points