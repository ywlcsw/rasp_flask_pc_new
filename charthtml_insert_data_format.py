list=[]
i=-300
while(i<0):
    # x={"user_date_time":"{{all_data_list_upload[%d][0]}}"%i,"user_co2": "{{all_data_list_upload[%d][1]}}"%i,
    #    "user_temp": "{{all_data_list_upload[%d][2]}}"%i,"user_humidity":"{{all_data_list_upload[%d][3]}}"%i ,
    #    "user_illuminate": "{{all_data_list_upload[%d][4]}}"%i,"user_soil_temp": "{{all_data_list_upload[%d][5]}}"%i,
    #    "user_soil_humidity": "{{all_data_list_upload[%d][6]}}"%i} #列表数据
    # x='{{ all_data_list_upload[%d][0]}}'%i    #时间日期
    # x = '{{ all_data_list_upload[%d][1]}}' % i    #CO2
    # x = '{{ all_data_list_upload[%d][2]}}' % i  #温度
    # x = '{{ all_data_list_upload[%d][3]}}' % i  #湿度
    # x = '{{ all_data_list_upload[%d][4]}}' % i  #光照
    # x = '{{ all_data_list_upload[%d][5]}}' % i  #土壤温度
    x = '{{ all_data_list_upload[%d][6]}}' % i  #土壤湿度
    list.append(x)
    i+=1;

print(list,end='')
