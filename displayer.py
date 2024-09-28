def menu():
    '''
    Menu
    creates a menu for the application
    args:None
    Returns:str

    '''
    while True:
        print(
            '''
            Grocery Store Inventory

            \n* View a single product\'s inventory(v)
            \r*Add a new product to the database (n)
            \r*View an Analysis(a)
            \r*Make a backup of the entire inventory(b)

            ''')
        choice = input('What would you like to do?: ')
        if choice in ['v', 'n', 'a', 'b']:
            return choice
        else:
            input(
                '''
                \rPlease enter one of the options above


                \rPress enter to try again:''')
        print()
