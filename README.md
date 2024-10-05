# osrs-clan-rantings
This application provides OSRS account rantings based on a list of given accounts. 

Feature list:
- Connects to WiseOldMan API for Player Details based on example_user_list.csv
- Filters boss KC based on eligible_boss_list.csv
- SnakeAndLadderPointsService currently uses the following formula to assign points for balancing teams.
    `min(1,(TOTAL Theatre of Blood KC (Normal + HM))/100) +
  min(1,(TOTAL Tombs of Amascut KC (Normal + Expert))/100) +
  min(1,(TOTAL Chambers of Xeric KC (Normal + CM))/100) +
  min(1,(Corrupted Gauntlet KC)/400)
`
