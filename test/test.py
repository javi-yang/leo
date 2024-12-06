with open('/home/javi/python/trans/cmd_list.txt','r') as f:
	for data in f.readlines():
		data = data.strip('\n')
		print(data)

import datetime

# 获取当前日期和时间
current_datetime = datetime.datetime.now()

# 格式化当前日期和时间
formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

print(formatted_datetime)
