from Components.Menu import Menu

menu = Menu()
answer = ''

while True:
    answer1 = menu.get_answer()
    if isinstance(answer1, str):
        break
    answer2 = menu.launch_feature(answer1)
    if answer2.upper() == 'Q':
        break


