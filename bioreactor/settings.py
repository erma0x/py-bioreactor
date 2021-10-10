def settings():
        name_function=input('''
    --------------[ SETTINGS ]---------------------
    Which function do you want to set? 

            1 - Optical Density : measure the OD 
            2 - Food            : set the food
            3 - Salinity        : measure the salinity
            4 - PH              : measure the PH
            5 - Light           : set the light
            6 - Temperature     : measure the temperature
            7 - Waste           : set the waste recycler

    -----------------------------------------------
        ''')
        
        col = input ( 'Which column do you want to set?')
        
        if name_function=='1':
            num_day=input('How many times at day do you want to measure Optical Density?')
        
        if name_function=='2':
            food_times_each_day = input ( 'How many times at day do you want to give food?')
            food_grams_each_day = input ( 'How many grams of food each day?')

        if name_function=='3':
            salinity_measures_each_day = input ( 'How many times at day do you want to measure Salinity?' )
        
        if name_function=='4':
            ph_measures_each_day = input ('How many times at day do you want to measure pH?')
        
        if name_function=='5':
            pulse_or_continue = input('Do you want to use pulse light? [Y/y] or [N/n]  default = No ')
            if pulse_or_continue in ('Y','y'):
                pulse_frequency = input('Insert pulse frequency ')
                
            red = input('Set RED led intensity (0-255) ')
            green = input('Set GREEN led intensity (0-255) ')
            blue = input('Set BLUE led intensity (0-255) ')