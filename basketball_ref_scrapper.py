# Modules
import urllib
from bs4 import BeautifulSoup
import re
import pandas as pd

# Dataset URL (2020-2021 NBA Player Total Stats) From basketball-reference.com
br_url = urllib.request.urlopen('https://www.basketball-reference.com/leagues/NBA_2021_totals.html#totals_stats::1')
br_raw = br_url.read()

# Scraping Static Web data
soup = BeautifulSoup(br_raw, 'html.parser')
raw_results = soup.find_all(class_="full_table")

# Regular expression to extract certain features for each nba player
player_pattern = re.compile('class="left" csk="(.*)" data-append')
pos_pattern = re.compile('"pos">([A-Z]*-?[A-Z]*?)<')
age_pattern = re.compile('"age">(\d*)<')
team_pattern = re.compile('"team_id"><.*>([A-Z]{3})')
g_pattern = re.compile('"g">(\d*)<')
gs_pattern = re.compile('"gs">(\d*)<')
mp_pattern = re.compile('"mp">(\d*)<')
fg_pattern = re.compile('"fg">(\d*)<')
fga_pattern = re.compile('"fga">(\d*)<')
fg_pct_pattern = re.compile('"fg_pct">(.\d*)<')
fg3_pattern = re.compile('"fg3">(\d*)<')
fg3a_pattern = re.compile('"fg3a">(\d*)<')
fg3_pct_pattern = re.compile('"fg3_pct">(.\d*)<')
fg2_pattern = re.compile('"fg2">(\d*)<')
fg2a_pattern = re.compile('"fg2a">(\d*)<')
fg2a_pct_pattern = re.compile('"fg2_pct">(.\d*)<')
efg_pct_pattern = re.compile('"efg_pct">(.\d*)<')
ft_pattern = re.compile('"ft">(\d*)<')
fta_pattern = re.compile('"fta">(\d*)<')
ft_pct_pattern = re.compile('"ft_pct">(.\d*)<')
orb_pattern = re.compile('"orb">(\d*)<')
drb_pattern = re.compile('"drb">(\d*)<')
trb_pattern = re.compile('"trb">(\d*)<')
ast_pattern = re.compile('"ast">(\d*)<')
stl_pattern = re.compile('"stl">(\d*)<')
blk_pattern = re.compile('"blk">(\d*)<')
tov_pattern = re.compile('"tov">(\d*)<')
pf_pattern = re.compile('"pf">(\d*)<')
pts_pattern = re.compile('"pts">(\d*)<')


basketball_reference_data = []

for line in raw_results:
    # Player and Stats Values
    re_player = re.findall(player_pattern, str(line))
    re_pos = re.findall(pos_pattern, str(line))
    re_age = re.findall(age_pattern, str(line))
    re_team = re.findall(team_pattern, str(line))  # blank if played on multiple teams
    re_g = re.findall(g_pattern, str(line))
    re_gs = re.findall(gs_pattern, str(line))
    re_mp = re.findall(mp_pattern, str(line))
    re_fg = re.findall(fg_pattern, str(line))
    re_fga = re.findall(fga_pattern, str(line))
    re_fg_pct = re.findall(fg_pct_pattern, str(line))
    re_fg3 = re.findall(fg3_pattern, str(line))
    re_fg3a = re.findall(fg3a_pattern, str(line))
    re_fg3_pct = re.findall(fg3_pct_pattern, str(line))
    re_fg2 = re.findall(fg2_pattern, str(line))
    re_fg2a = re.findall(fg2a_pattern, str(line))
    re_fg2a_pct = re.findall(fg2a_pct_pattern, str(line))
    re_efg_pct = re.findall(efg_pct_pattern, str(line))
    re_ft = re.findall(ft_pattern, str(line))
    re_fta = re.findall(fta_pattern, str(line))
    re_ft_pct = re.findall(ft_pct_pattern, str(line))
    re_orb = re.findall(orb_pattern, str(line))
    re_drb = re.findall(drb_pattern, str(line))
    re_trb = re.findall(trb_pattern, str(line))
    re_ast = re.findall(ast_pattern, str(line))
    re_stl = re.findall(stl_pattern, str(line))
    re_blk = re.findall(blk_pattern, str(line))
    re_tov = re.findall(tov_pattern, str(line))
    re_pf = re.findall(pf_pattern, str(line))
    re_pts = re.findall(pts_pattern, str(line))

    # Adding player and stats to list
    basketball_reference_data.append([re_player, re_pos, re_age, re_team, re_g, re_gs, re_mp, re_fg, re_fga,
                                     re_fg_pct, re_fg3, re_fg3a, re_fg3_pct, re_fg2, re_fg2a, re_fg2a_pct,
                                     re_efg_pct, re_ft, re_fta, re_ft_pct, re_orb, re_drb, re_trb, re_ast, re_stl,
                                     re_blk, re_tov, re_pf, re_pts])

# Converting to pandas dataframe
columns = 'Player','Pos','Age','Tm','G','GS','MP','FG','FGA','FG%','3P','3PA','3P%','2P','2PA','2P%','eFG%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS'
basketball_df = pd.DataFrame(basketball_reference_data, columns=columns)

# Converting columns to appropriate data type for further analysis
string_list = 'Player', 'Pos', 'Tm'
float_list = 'FG%', '3P%', '2P%', 'eFG%', 'FT%'
for column in basketball_df.columns:
    basketball_df[column] = basketball_df[column].str[0]
    if column not in string_list:
        if column not in float_list:
            basketball_df[column] = basketball_df[column].astype('int')
        else:
            basketball_df[column] = basketball_df[column].astype('float')
    else:
        basketball_df[column] = basketball_df[column].astype('string')

# Saving as txt file if needed
check_save = input('Would you like to save the table as a text file y/n ').lower()
if check_save == 'y':
    outfile = open('br_data.txt', 'w')  # basketball reference data
    for player in basketball_df.values:
        for attr in player:
            outfile.write(str(attr) + ' ')
        outfile.write('\n')
    outfile = open('br_col.txt', 'w')  # basketball reference column names
    for col in basketball_df:
        outfile.write(col + ' ')
    outfile.close()
