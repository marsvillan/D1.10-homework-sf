import sys 
import requests



auth_params = {    
    'key': " ",    # вставте сюда свой ключ
    'token': " ",    # вставьте сюда свой токен
}
board_id = " "  # вставьте сюда короткий id доски

base_url = "https://api.trello.com/1/{}" 


#Получение и вывод всех колонок с задачами
def read():     
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Далее выведем название каждой колонки и всех заданий, которые с ней связанны:      
    for column in column_data:      
        print(column['name'])         
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue
        print("Всего задач в колонке '{}': {}".format(column['name'], len(task_data)))      
        for task in task_data:      
            print('\t' + task['name'])    


def column(name):
    # Создаем новую колонку с именем name
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': name, **auth_params})


def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()       
    
    # Перебираем данные обо всех колонках, пока не найдём нужную     
    for column in column_data:    
        if column['name'] == column_name:
            task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
            # Вспомогательная переменная flag, чтобы выскочить из внешнего цикла, если бдут совпадения
            flag = True
            for task in task_data:
                if task['name'] == name:
                    flag = False
                    print("Задача с таким именем уже создана")
                    break
            if not flag:
                break
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break  


def move(name, column_name):
    query = {}   
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Ищем все совпадения и заполяем словарь query по принципу:
    # {'Название колонки': {'name': 'Название задачи', 'id': 'ID задачи'}}      
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:
                query[column['name']] = {'name': task['name'], 'id': task['id']}    

    # UI часть
    print('Список всех найденных совпадений:')
    for key, value in query.items():
       print("В колонке '{}' найдена задача {} c ID {}".format(key, value['name'], value['id']))
    choise = input('Введи название колонки, в которой находится нужная тебе задача: ')

    # Проверяем есть ли в словаре query колонка введенная пользователем
    if choise in query:
        task_id = query[choise]['id']
        # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
        # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
        for column in column_data:
            if [column['name'] == column_name]:
                # И выполним запрос к API для перемещения задачи в нужную колонку    
                requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
                break
    else:
        print('Ошибка ввода')


if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'column':
        column(sys.argv[2])