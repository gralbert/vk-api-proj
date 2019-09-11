from multiprocessing import Process
from GroupsClass import Group, Group2, Group3
import time

from vklancer import api

MY_TOKEN = '0688a8b20688a8b20688a8b22206e05b9e' \
               '006880688a8b25afd5bad0eb94304d8447dc4'

vk = api.API(MY_TOKEN)

print('Задача: "Какое соотношение мужчин и женщин в тематических пабликах вк?"')
print('Ожидаем подключение к интернету...')

group_1 = Group('python_community', 1000)
group_2 = Group2('javatutorial', 1000)
group_3 = Group3('javascript_forum', 1000)

print('Успешно! Исполняем процессы...')

process_one = Process(target=group_1.new_statistic)
process_two = Process(target=group_2.new_statistic)
process_three = Process(target=group_3.new_statistic)


start_time_one = time.time()
process_one.start()
start_time_two = time.time()
process_two.start()
start_time_three = time.time()
process_three.start()

process_one.join()
print("Последовательно: %s seconds" % (time.time() - start_time_one))
process_two.join()
print("С очередью: %s seconds" % (time.time() - start_time_two))
process_three.join()
print("С условными переменными: %s seconds" % (time.time() - start_time_three))