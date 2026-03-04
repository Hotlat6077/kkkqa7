##删除没用的数据
from mydb.get_mongo import get_db

if __name__ == '__main__':
    db = get_db()
    db['alert_data'].delete_many({})
    db['current_fault_sensors'].delete_many({})
    db['day_index'].delete_many({})
    db['event_data'].delete_many({})
    db['export_data_logs'].delete_many({})
    db['fault_info'].delete_many({})
    db['hour_index'].delete_many({})
    db['indicator_data_1_1'].delete_many({})
    db['indicator_data_1_2'].delete_many({})
    db['indicator_import'].delete_many({})
    db['month_index'].delete_many({})

    db['qny_table_data'].delete_many({})
    db['vibration_data'].delete_many({})
    db['vibration_data_import'].delete_many({})
    db['year10_index'].delete_many({})
    db['year_index'].delete_many({})

