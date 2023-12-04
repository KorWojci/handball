from modules import *

def is_number(s):
    """
    Check if a given string represents a valid number.

    Parameters:
        - s (str): The string to be checked.

    Returns:
        - bool: True if the string represents a valid number, False otherwise.
    """
    return bool(re.match(r'^-?\d+(?:\.\d+)?$', s))

def get_api_connection():
    """
    Create and return an API connection and headers for the Handball API.

    Returns:
        tuple: A tuple containing the API connection and headers.
    """

    connection = http.client.HTTPSConnection('v1.handball.api-sports.io') #api-handball.p.rapidapi.com v1.handball.api-sports.io
    headers = {
        'x-rapidapi-host': host_handball,
        'x-rapidapi-key': key_handball
    }
    return connection, headers

def get_today_games(conn, headers):
    """
    Retrieves today's games from the API using the provided connection and headers.

    Parameters:
    - conn: The connection object used to make the API request.
    - headers: The headers to be sent with the API request.

    Returns:
    - data: The response data received from the API, in JSON format.
    - number_of_games: The number of games retrieved from the API.
    """

    conn.request('GET', '/games?date=' + today_date, headers=headers)
    
    response = conn.getresponse()
    data = json.loads(response.read().decode("utf-8")) #response.read()
    number_of_games = data.get('results')
    matches = data.get('response')
    return matches, number_of_games

def get_match_h2h_api(conn, headers, row):
    """
	Get the head-to-head matches between two teams from an API.

	Parameters:
	- conn: The connection object for making HTTP requests.
	- headers: The headers to be included in the request.
	- row: The row containing information about the teams.

	Returns:
	- h2h_detailed_results: A list of tuples containing detailed match results.
	- h2h_draws_final: A list of tuples containing draws.
	- h2h_draws_1st_half: A list of tuples containing draws in the first half.
	- h2h_draws_2nd_half: A list of tuples containing draws in the second half.
	"""

    home_team = row.get('teams').get('home').get('id')
    away_team = row.get('teams').get('away').get('id')
    conn.request('GET', '/games/h2h?h2h=' + str(home_team) + '-' + str(away_team), headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode("utf-8"))
    h2h_matches = data.get('response')
    h2h_detailed_results = []
    h2h_draws_final = []
    h2h_draws_1st_half = []
    h2h_draws_2nd_half = []
    if h2h_matches:
        for h2h_match in h2h_matches:
            # Consider only finished matches full time matches
            if h2h_match.get('status').get('short') == 'FT':
                match_id = h2h_match.get('id')
                match_date = h2h_match.get('date')[0:10]
                date_split = match_date.split('-')
                match_date_formatted = date_split[2] + '-' + date_split[1] + '-' + date_split[0]
                match_time = h2h_match.get('time')
                match_timezone = h2h_match.get('timezone')
                match_country = h2h_match.get('country').get('name')
                match_home_team_id = h2h_match.get('teams').get('home').get('id')
                match_home_team_name = h2h_match.get('teams').get('home').get('name')
                match_away_team_id = h2h_match.get('teams').get('away').get('id')
                match_away_team_name = h2h_match.get('teams').get('away').get('name')
                match_score_home = h2h_match.get('scores').get('home')
                match_score_away = h2h_match.get('scores').get('away')
                match_1st_half_score_home = h2h_match.get('periods').get('first').get('home')
                match_1st_half_score_away = h2h_match.get('periods').get('first').get('away')
                match_2nd_half_score_home = h2h_match.get('periods').get('second').get('home')
                match_2nd_half_score_away = h2h_match.get('periods').get('second').get('away')

                h2h_detailed = (match_id, #0
                                match_date_formatted, #1
                                match_time, #2
                                match_timezone, #3
                                match_country, #4 
                                match_home_team_id, #5
                                match_home_team_name, #6
                                match_away_team_id, #7
                                match_away_team_name, #8
                                match_score_home, #9
                                match_score_away, #10
                                match_1st_half_score_home, #11
                                match_1st_half_score_away, #12
                                match_2nd_half_score_home, #13
                                match_2nd_half_score_away, #14
                )
                h2h_detailed_results.append(h2h_detailed)

                h2h_draws = (match_id, #0
                            match_date_formatted, #1
                            match_country, #2
                            match_home_team_name, #3
                            match_away_team_name, #4
                            match_score_home, #5
                            match_score_away, #6
                            match_1st_half_score_home, #7
                            match_1st_half_score_away, #8
                            match_2nd_half_score_home, #9
                            match_2nd_half_score_away, #10
                )
                if match_score_home == match_score_away:
                    h2h_draws_final.append(h2h_draws)
                if match_1st_half_score_home == match_1st_half_score_away:
                    h2h_draws_1st_half.append(h2h_draws)
                if match_2nd_half_score_home == match_2nd_half_score_away:
                    h2h_draws_2nd_half.append(h2h_draws)
                h2h_draws = ()
            else:
                pass

    return h2h_detailed_results, h2h_draws_final, h2h_draws_1st_half, h2h_draws_2nd_half

def prepare_worksheet(content, tab_name, file):
    """
    Prepares a worksheet in the given file with the provided content and tab name.

    Parameters:
    - content (list of lists): The content to be written in the worksheet.
    - tab_name (str): The name of the tab for the worksheet.
    - file (File): The file object representing the Excel file.

    Returns:
    None
    """
    worksheet = file.add_worksheet(tab_name)
    cell_bold = file.add_format()
    cell_bold.set_bold()
    cell_number = file.add_format()
    cell_number.set_num_format(0) 
    cell_prcnt = file.add_format({'num_format': '0%'})

    row = 0
    col = 0

    col_count = len(content[0])

    for line in content:
        # Header line
        if row == 0:
            for col in range(0, col_count):
                worksheet.write(row, col, line[col], cell_bold)
        # Regular line
        else:
            for col in range(0, col_count):
                if col <= 8:
                    if is_number(str(line[col])):
                        worksheet.write(row, col, int(line[col]), cell_number)
                    else:
                        worksheet.write(row, col, line[col])
                else:
                    if is_number(str(line[col])):
                        worksheet.write(row, col, int(line[col]), cell_prcnt)
                    else:
                        worksheet.write(row, col, line[col])
        row = row + 1
    worksheet.autofit()

def save_data_to_excel(h2h_short_results, h2h_detailed_results):
    """
    Saves the given h2h_short_results and h2h_detailed_results to an Excel file.

    Parameters:
        h2h_short_results (list): A list of lists containing the short results data.
        h2h_detailed_results (list): A list of lists containing the detailed results data.

    Returns:
        None
    """
    date_split = today_date_format.split('-')
    date = date_split[0] + '_' + date_split[1] + '_' + date_split[2]
    
    file_path = 'dane/api/Handball_' + date + '.xlsx'
    workbook = xlsxwriter.Workbook(file_path)
    
    h2h_short_header = ( 'Date', #0
                         'Time', #1
                         'Timezone', #2
                         'Home', #3
                         'Away', #4
                         '1st Half Draws', #5
                         '2nd Half Draws', #6
                         'Final Time Draws', #7
                         'Matches Count', #8
                         'Full Time Draws %', #9
                         '1st Half Draws %', #10
                         '2nd Half Draws %', #11
                         'Total Draws %', #12
    )
    h2h_short_results.insert(0, h2h_short_header)

    h2h_detailed_header = ( 'Match ID', #0
                            'Date', #1
                            'Time', #2
                            'Timezone', #3
                            'Country', #4
                            'Home Team ID', #5
                            'Home Team Name', #6
                            'Away Team ID', #7
                            'Away Team Name', #8
                            'Score Home', #9
                            'Score Away', #10
                            '1st Half Score Home', #11
                            '1st Half Score Away', #12
                            '2nd Half Score Home', #13
                            '2nd Half Score Away', #14
    )
    h2h_detailed_results.insert(0, h2h_detailed_header)

    prepare_worksheet(h2h_short_results, 'Draws', workbook)
    prepare_worksheet(h2h_detailed_results, 'Detailed Results', workbook)
    workbook.close()
    print('Excel file saved to ' + file_path)