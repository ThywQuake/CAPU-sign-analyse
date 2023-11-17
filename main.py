from analyse import Analyse


print('Welcome to the CAPUsign data System!\n')
flag1=True
flag2=True
while flag1:
    print('Please choose the function you want to use:\n'
        '1. Analyse the data of a certain period of time\n'
        '2. Analyse the data of a certain person\n'
        '3. quit\n')
    choice=input('Please enter the number of the function: \n')
    if flag2:
        a=Analyse()
    if choice=='1':
        a.show_signs()
        a.show_signs_heatmap(view='calendar')
        if input('Do you want to change the time period?[y/n]')=='n':
            flag2=False
    elif choice=='2':
        ID=input('Please enter the ID of the person: ')
        a.show_signer(ID)
        a.show_signer_heatmap(ID,view='calendar')
        if input('Do you want to change the time period?[y/n]')=='n':
            flag2=False
    elif choice=='3':
        flag1=False
    



