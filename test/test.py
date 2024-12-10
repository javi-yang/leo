with open('/home/javi/leo_share/reg00.txt','r') as f:
    for data in f.readlines():
        #data = data.strip('\n')
        if "i2cset" in data:
            print(data)
            with open('/home/javi/leo_share/test.txt','w') as r:
                r.write(data)
'''
import datetime

# 获取当前日期和时间
current_datetime = datetime.datetime.now()

# 格式化当前日期和时间
formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

with open('/home/javi/leo_share/test.txt','w') as f:
	f.write(formatted_datetime+'\n')
	#f.write('\n')
print(formatted_datetime)
'''