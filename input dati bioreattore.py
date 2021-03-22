import scheduler

def settings():
    x='Y'
    while x=='Y' or x=='y':
        name_function=input('''Which function do you want to set? 
        1 - Optical Density
        2 - Food
        3 - Salinity
        4 - PH
        4 - Reservoir
        5 - Light
        6 - 
        ''')
        if name_function==1:
            col=input('Which column do you want to set? - ')
            num_day=input('How many times at day do you want to measure OD? - ')
        if name_function==2:
            col = input ( 'Which column do you want to set? - ' )
            num_day = input ( 'How many times at day do you want to measure OD? - ' )
        if name_function==3:
            col = input ( 'Which column do you want to set? - ' )
            num_day = input ( 'How many times at day do you want to measure OD? - ' )
        if name_function==4:
            col = input ( 'Which column do you want to set? - ' )
            num_day = input ( 'How many times at day do you want to measure pH? - ' )
        if name_function==5:
            col = input ( 'Which column do you want to set? - ' )
            num_day = input ( 'How many times at day do you want to measure OD? - ' )
        if name_function==6:
            col = input ( 'Which column do you want to set? - ' )
            num_day = input ( 'How many times at day do you want to measure OD? - ' )


