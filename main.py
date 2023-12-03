from functions import *

connection, headers = get_api_connection()
matches, number_of_games = get_today_games(connection, headers)

if number_of_games <= 95:
    # Use handball api
    h2h_short_results = []
    h2h_detailed_results = []
    h2h_final_string = ''
    h2h_1st_string = ''
    h2h_2nd_string = ''
    for match in matches:
        # Get all head-to-head matches, matches with draws in 1st, 2nd or full time
        h2h_detailed, h2h_draws_final, h2h_draws_1st_half, h2h_draws_2nd_half = get_match_h2h_api(connection, headers, match)
        for h2h_detailed_line in h2h_detailed:
            h2h_detailed_results.append(h2h_detailed_line)

        # Merge all draws in full time into one string
        for h2h_draw in h2h_draws_final:
            if h2h_final_string == '':
                h2h_final_string = h2h_draw[1]
            else:
                h2h_final_string = h2h_final_string + ', ' + h2h_draw[1]
        
        # Merge all draws in first half into one string
        for h2h_draw in h2h_draws_1st_half:
            if h2h_1st_string == '':
                h2h_1st_string = h2h_draw[1]
            else:
                h2h_1st_string = h2h_1st_string + ', ' + h2h_draw[1]
        
        # Merge all draws in second half into one string
        for h2h_draw in h2h_draws_2nd_half:
            if h2h_2nd_string == '':
                h2h_2nd_string = h2h_draw[1]
            else:
                h2h_2nd_string = h2h_2nd_string + ', ' + h2h_draw[1]

        # Prepare data for excel list of draws in matches
        h2h_short_match = (today_date_format, #0
                            match.get('time'), #1
                            match.get('timezone'), #2
                            match.get('teams').get('home').get('name'), #3
                            match.get('teams').get('away').get('name'), #4
                            h2h_1st_string, #5
                            h2h_2nd_string, #6
                            h2h_final_string, #7
                            )
        h2h_short_results.append(h2h_short_match)
        h2h_1st_string = ''
        h2h_2nd_string = ''
        h2h_final_string = ''

    # Save data to excel file
    save_data_to_excel(h2h_short_results, h2h_detailed_results)
    

else:
    # Use scrapper
    print('Scrapping')