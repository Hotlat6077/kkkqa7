
from index_calculation import *
from datetime import datetime
def ndarray2list0(data):
    list0=[]
    for temp in data:
        list0.append(temp.tolist())
    return list0
def ndarray2list1(data):
    list0=[]
    for temp in data:
        list0.append(temp.tolist())
    list1=[]
    for i in list0:
        for j in i:
            list1.append(j)
    return list1

def get_thr(model,group,machine,component,sensor):
    db = get_db()
    collectiont=db['threshold_data']
    group=int(group)
    machine=int(machine)
    component=int(component)
    sensor=int(sensor)
    data=collectiont.find({'machine': machine,'group':group,'component':component,'sensor':sensor,'model':model},{'thr':1})[0]
    return data
def update_home3(query_order,group,machine):
    db = get_db()
    collection=db['vibration_data']
    group=int(group)
    machine=int(machine)

    # result = {}
    result = {'fea_x': []}
# peak speed_rms
    thr1 = get_thr(model='rms',group=int(group),machine=int(machine),component=1,sensor=1)
    result['thr11'] = thr1['thr']['warning']
    result['thr12'] = thr1['thr']['fault']
    result['thr13'] = thr1['thr']['fault']*1.1
    thr2 = get_thr(model='kur',group=int(group),machine=int(machine),component=1,sensor=1)
    result['thr14'] = thr2['thr']['warning']
    result['thr15'] = thr2['thr']['fault']
    result['thr16'] = thr2['thr']['fault']*1.1
    thr3 = get_thr(model='std',group=int(group),machine=int(machine),component=1,sensor=1)
    result['thr17'] = thr3['thr']['warning']
    result['thr18'] = thr3['thr']['fault']
    result['thr19'] = thr3['thr']['fault']*1.1
    thr3_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=1,sensor=1)
    result['thr3_1'] = thr3_1['thr']['warning']
    result['thr3_2'] = thr3_1['thr']['fault']
    result['thr3_3'] = thr3_1['thr']['fault']*1.1
    thr3_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=1,sensor=1)
    result['thr3_4'] = thr3_2['thr']['warning']
    result['thr3_5'] = thr3_2['thr']['fault']
    result['thr3_6'] = thr3_2['thr']['fault']*1.1
    thr3_3 = get_thr(model='impulse',group=int(group),machine=int(machine),component=1,sensor=1)
    result['thr3_7'] = thr3_3['thr']['warning']
    result['thr3_8'] = thr3_3['thr']['fault']
    result['thr3_9'] = thr3_3['thr']['fault']*1.1

    thr4 = get_thr(model='rms',group=int(group),machine=int(machine),component=1,sensor=2)
    result['thr21'] = thr4['thr']['warning']
    result['thr22'] = thr4['thr']['fault']
    result['thr23'] = thr4['thr']['fault']*1.1
    thr5 = get_thr(model='kur',group=int(group),machine=int(machine),component=1,sensor=2)
    result['thr24'] = thr5['thr']['warning']
    result['thr25'] = thr5['thr']['fault']
    result['thr26'] = thr5['thr']['fault']*1.1
    thr6 = get_thr(model='std',group=int(group),machine=int(machine),component=1,sensor=2)
    result['thr27'] = thr6['thr']['warning']
    result['thr28'] = thr6['thr']['fault']
    result['thr29'] = thr6['thr']['fault']*1.1
    thr6_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=1,sensor=2)
    result['thr6_1'] = thr6_1['thr']['warning']
    result['thr6_2'] = thr6_1['thr']['fault']
    result['thr6_3'] = thr6_1['thr']['fault']*1.1
    thr6_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=1,sensor=2)
    result['thr6_4'] = thr6_2['thr']['warning']
    result['thr6_5'] = thr6_2['thr']['fault']
    result['thr6_6'] = thr6_2['thr']['fault']*1.1
    thr6_3 = get_thr(model='impulse',group=int(group),machine=int(machine),component=1,sensor=2)
    result['thr6_7'] = thr6_3['thr']['warning']
    result['thr6_8'] = thr6_3['thr']['fault']
    result['thr6_9'] = thr6_3['thr']['fault']*1.1

    thr7 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=1)
    result['thr31'] = thr7['thr']['warning']
    result['thr32'] = thr7['thr']['fault']
    result['thr33'] = thr7['thr']['fault']*1.1
    thr8 = get_thr(model='kur',group=int(group),machine=int(machine),component=2,sensor=1)
    result['thr34'] = thr8['thr']['warning']
    result['thr35'] = thr8['thr']['fault']
    result['thr36'] = thr8['thr']['fault']*1.1
    thr9 = get_thr(model='std',group=int(group),machine=int(machine),component=2,sensor=1)
    result['thr37'] = thr9['thr']['warning']
    result['thr38'] = thr9['thr']['fault']
    result['thr39'] = thr9['thr']['fault']*1.1
    thr9_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=2,sensor=1)
    result['thr9_1'] = thr9_1['thr']['warning']
    result['thr9_2'] = thr9_1['thr']['fault']
    result['thr9_3'] = thr9_1['thr']['fault']*1.1
    thr9_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=1)
    result['thr9_4'] = thr9_2['thr']['warning']
    result['thr9_5'] = thr9_2['thr']['fault']
    result['thr9_6'] = thr9_2['thr']['fault']*1.1
    thr9_3 = get_thr(model='impulse',group=int(group),machine=int(machine),component=2,sensor=1)
    result['thr9_7'] = thr9_3['thr']['warning']
    result['thr9_8'] = thr9_3['thr']['fault']
    result['thr9_9'] = thr9_3['thr']['fault']*1.1

    thr10 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=2)
    result['thr41'] = thr10['thr']['warning']
    result['thr42'] = thr10['thr']['fault']
    result['thr43'] = thr10['thr']['fault']*1.1
    thr11 = get_thr(model='kur',group=int(group),machine=int(machine),component=2,sensor=2)
    result['thr44'] = thr11['thr']['warning']
    result['thr45'] = thr11['thr']['fault']
    result['thr46'] = thr11['thr']['fault']*1.1
    thr12 = get_thr(model='std',group=int(group),machine=int(machine),component=2,sensor=2)
    result['thr47'] = thr12['thr']['warning']
    result['thr48'] = thr12['thr']['fault']
    result['thr49'] = thr12['thr']['fault']*1.1
    thr12_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=2,sensor=2)
    result['thr12_1'] = thr12_1['thr']['warning']
    result['thr12_2'] = thr12_1['thr']['fault']
    result['thr12_3'] = thr12_1['thr']['fault']*1.1
    thr12_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=2)
    result['thr12_4'] = thr12_2['thr']['warning']
    result['thr12_5'] = thr12_2['thr']['fault']
    result['thr12_6'] = thr12_2['thr']['fault']*1.1
    thr12_3 = get_thr(model='impulse',group=int(group),machine=int(machine),component=2,sensor=2)
    result['thr12_7'] = thr12_3['thr']['warning']
    result['thr12_8'] = thr12_3['thr']['fault']
    result['thr12_9'] = thr12_3['thr']['fault']*1.1

    thr13 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=3)
    result['thr51'] = thr13['thr']['warning']
    result['thr52'] = thr13['thr']['fault']
    result['thr53'] = thr13['thr']['fault']*1.1
    thr14 = get_thr(model='kur',group=int(group),machine=int(machine),component=2,sensor=3)
    result['thr54'] = thr14['thr']['warning']
    result['thr55'] = thr14['thr']['fault']
    result['thr56'] = thr14['thr']['fault']*1.1
    thr15 = get_thr(model='std',group=int(group),machine=int(machine),component=2,sensor=3)
    result['thr57'] = thr15['thr']['warning']
    result['thr58'] = thr15['thr']['fault']
    result['thr59'] = thr15['thr']['fault']*1.1
    thr15_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=2,sensor=3)
    result['thr15_1'] = thr15_1['thr']['warning']
    result['thr15_2'] = thr15_1['thr']['fault']
    result['thr15_3'] = thr15_1['thr']['fault']*1.1
    thr15_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=3)
    result['thr15_4'] = thr15_2['thr']['warning']
    result['thr15_5'] = thr15_2['thr']['fault']
    result['thr15_6'] = thr15_2['thr']['fault']*1.1
    thr15_3 = get_thr(model='impulse',group=int(group),machine=int(machine),component=2,sensor=3)
    result['thr15_7'] = thr15_3['thr']['warning']
    result['thr15_8'] = thr15_3['thr']['fault']
    result['thr15_9'] = thr15_3['thr']['fault']*1.1

    thr16 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=4)
    result['thr61'] = thr16['thr']['warning']
    result['thr62'] = thr16['thr']['fault']
    result['thr63'] = thr16['thr']['fault']*1.1
    thr17 = get_thr(model='kur',group=int(group),machine=int(machine),component=2,sensor=4)
    result['thr64'] = thr17['thr']['warning']
    result['thr65'] = thr17['thr']['fault']
    result['thr66'] = thr17['thr']['fault']*1.1
    thr18 = get_thr(model='std',group=int(group),machine=int(machine),component=2,sensor=4)
    result['thr67'] = thr18['thr']['warning']
    result['thr68'] = thr18['thr']['fault']
    result['thr69'] = thr18['thr']['fault']*1.1
    thr18_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=2,sensor=4)
    result['thr18_1'] = thr18_1['thr']['warning']
    result['thr18_2'] = thr18_1['thr']['fault']
    result['thr18_3'] = thr18_1['thr']['fault']*1.1
    thr18_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=4)
    result['thr18_4'] = thr18_2['thr']['warning']
    result['thr18_5'] = thr18_2['thr']['fault']
    result['thr18_6'] = thr18_2['thr']['fault']*1.1
    thr18_3 = get_thr(model='impulse',group=int(group),machine=int(machine),component=2,sensor=4)
    result['thr18_7'] = thr18_3['thr']['warning']
    result['thr18_8'] = thr18_3['thr']['fault']
    result['thr18_9'] = thr18_3['thr']['fault']*1.1

    thr19 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=5)
    result['thr71'] = thr19['thr']['warning']
    result['thr72'] = thr19['thr']['fault']
    result['thr73'] = thr19['thr']['fault']*1.1
    thr20 = get_thr(model='kur',group=int(group),machine=int(machine),component=2,sensor=5)
    result['thr74'] = thr20['thr']['warning']
    result['thr75'] = thr20['thr']['fault']
    result['thr76'] = thr20['thr']['fault']*1.1
    thr21 = get_thr(model='std',group=int(group),machine=int(machine),component=2,sensor=5)
    result['thr77'] = thr21['thr']['warning']
    result['thr78'] = thr21['thr']['fault']
    result['thr79'] = thr21['thr']['fault']*1.1
    thr21_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=2,sensor=5)
    result['thr21_1'] = thr21_1['thr']['warning']
    result['thr21_2'] = thr21_1['thr']['fault']
    result['thr21_3'] = thr21_1['thr']['fault']*1.1
    thr21_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=5)
    result['thr21_4'] = thr21_2['thr']['warning']
    result['thr21_5'] = thr21_2['thr']['fault']
    result['thr21_6'] = thr21_2['thr']['fault']*1.1
    thr21_3 = get_thr(model='impulse',group=int(group),machine=int(machine),component=2,sensor=5)
    result['thr21_7'] = thr21_3['thr']['warning']
    result['thr21_8'] = thr21_3['thr']['fault']
    result['thr21_9'] = thr21_3['thr']['fault']*1.1

    thr22 = get_thr(model='rms',group=int(group),machine=int(machine),component=3,sensor=1)
    result['thr81'] = thr22['thr']['warning']
    result['thr82'] = thr22['thr']['fault']
    result['thr83'] = thr22['thr']['fault']*1.1
    thr23 = get_thr(model='kur',group=int(group),machine=int(machine),component=3,sensor=1)
    result['thr84'] = thr23['thr']['warning']
    result['thr85'] = thr23['thr']['fault']
    result['thr86'] = thr23['thr']['fault']*1.1
    thr24 = get_thr(model='std',group=int(group),machine=int(machine),component=3,sensor=1)
    result['thr87'] = thr24['thr']['warning']
    result['thr88'] = thr24['thr']['fault']
    result['thr89'] = thr24['thr']['fault']*1.1
    thr24_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=3,sensor=1)
    result['thr24_1'] = thr24_1['thr']['warning']
    result['thr24_2'] = thr24_1['thr']['fault']
    result['thr24_3'] = thr24_1['thr']['fault']*1.1
    thr24_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=3,sensor=1)
    result['thr24_4'] = thr24_2['thr']['warning']
    result['thr24_5'] = thr24_2['thr']['fault']
    result['thr24_6'] = thr24_2['thr']['fault']*1.1
    thr24_3 = get_thr(model='impulse',group=int(group),machine=int(machine),component=3,sensor=1)
    result['thr24_7'] = thr24_3['thr']['warning']
    result['thr24_8'] = thr24_3['thr']['fault']
    result['thr24_9'] = thr24_3['thr']['fault']*1.1

    thr25 = get_thr(model='rms',group=int(group),machine=int(machine),component=3,sensor=2)
    result['thr91'] = thr25['thr']['warning']
    result['thr92'] = thr25['thr']['fault']
    result['thr93'] = thr25['thr']['fault']*1.1
    thr26 = get_thr(model='kur',group=int(group),machine=int(machine),component=3,sensor=2)
    result['thr94'] = thr26['thr']['warning']
    result['thr95'] = thr26['thr']['fault']
    result['thr96'] = thr26['thr']['fault']*1.1
    thr27 = get_thr(model='std',group=int(group),machine=int(machine),component=3,sensor=2)
    result['thr97'] = thr27['thr']['warning']
    result['thr98'] = thr27['thr']['fault']
    result['thr99'] = thr27['thr']['fault']*1.1
    thr27_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=3,sensor=2)
    result['thr27_1'] = thr27_1['thr']['warning']
    result['thr27_2'] = thr27_1['thr']['fault']
    result['thr27_3'] = thr27_1['thr']['fault']*1.1
    thr27_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=3,sensor=2)
    result['thr27_4'] = thr27_2['thr']['warning']
    result['thr27_5'] = thr27_2['thr']['fault']
    result['thr27_6'] = thr27_2['thr']['fault']*1.1
    thr27_3 = get_thr(model='impulse',group=int(group),machine=int(machine),component=3,sensor=2)
    result['thr27_7'] = thr27_3['thr']['warning']
    result['thr27_8'] = thr27_3['thr']['fault']
    result['thr27_9'] = thr27_3['thr']['fault']*1.1

    # data1 = list(collection.find({'machine': machine, 'group': group, 'component': 1, 'sensor': 1},
    #                             {'vib': 1}).sort([('datetime', -1)]).limit(1))[0]
    # vib_data1 = data1.get('vib')
    # signal_index1 = index_result(vib_data1, 1000)
    #
    # result[f'trend1'] = signal_index1[:, 4].ravel().tolist()
    # result[f'trend2'] = signal_index1[:, 9].ravel().tolist()
    # result[f'trend3'] = signal_index1[:, 1].ravel().tolist()
    # result[f'trend3_1'] = (signal_index1[:, 0]).ravel().tolist()
    # result[f'trend3_2'] = (signal_index1[:, 8]*100).ravel().tolist()
    # result[f'trend3_3'] = (signal_index1[:, 4]*1.2).ravel().tolist()
    #
    # data2 = list(collection.find({'machine': machine, 'group': group, 'component': 1, 'sensor': 2},
    #                             {'vib': 1}).sort([('datetime', -1)]).limit(1))[0]
    # vib_data2 = data2.get('vib')
    # signal_index2 = index_result(vib_data2, 1000)
    # result[f'trend4'] = signal_index2[:, 4].ravel().tolist()
    # result[f'trend5'] = signal_index2[:, 9].ravel().tolist()
    # result[f'trend6'] = (signal_index2[:, 1]*100).ravel().tolist()
    # result[f'trend6_1'] = signal_index2[:, 0].ravel().tolist()
    # result[f'trend6_2'] = (signal_index2[:, 8]*100).ravel().tolist()
    # result[f'trend6_3'] = (signal_index2[:, 4]*1.2).ravel().tolist()
    #
    # data3 = list(collection.find({'machine': machine, 'group': group, 'component': 2, 'sensor': 1},
    #                             {'vib': 1}).sort([('datetime', -1)]).limit(1))[0]
    # vib_data3 = data3.get('vib')
    # signal_index3 = index_result(vib_data3, 1000)
    # result[f'trend7'] = signal_index3[:, 4].ravel().tolist()
    # result[f'trend8'] = signal_index3[:, 9].ravel().tolist()
    # result[f'trend9'] = (signal_index3[:, 1]*100).ravel().tolist()
    # result[f'trend9_1'] = signal_index3[:, 0].ravel().tolist()
    # result[f'trend9_2'] = (signal_index3[:, 8]*100).ravel().tolist()
    # result[f'trend9_3'] = (signal_index2[:, 4]*1.2).ravel().tolist()
    #
    # data4 = list(collection.find({'machine': machine, 'group': group, 'component': 2, 'sensor': 2},
    #                             {'vib': 1}).sort([('datetime', -1)]).limit(1))[0]
    # vib_data4 = data4.get('vib')
    # signal_index4 = index_result(vib_data4, 1000)
    # result[f'trend10'] = signal_index4[:, 4].ravel().tolist()
    # result[f'trend11'] = signal_index4[:, 9].ravel().tolist()
    # result[f'trend12'] = (signal_index4[:, 1]*100).ravel().tolist()
    # result[f'trend12_1'] = signal_index4[:, 0].ravel().tolist()
    # result[f'trend12_2'] = (signal_index4[:, 8]*100).ravel().tolist()
    # result[f'trend12_3'] = (signal_index4[:, 4]*1.2).ravel().tolist()
    #
    # data5 = list(collection.find({'machine': machine, 'group': group, 'component': 2, 'sensor': 3},
    #                             {'vib': 1}).sort([('datetime', -1)]).limit(1))[0]
    # vib_data5 = data5.get('vib')
    # signal_index5 = index_result(vib_data5, 1000)
    # result[f'trend13'] = signal_index5[:, 4].ravel().tolist()
    # result[f'trend14'] = signal_index5[:, 9].ravel().tolist()
    # result[f'trend15'] = (signal_index5[:, 1]*100).ravel().tolist()
    # result[f'trend15_1'] = signal_index5[:, 0].ravel().tolist()
    # result[f'trend15_2'] = (signal_index5[:, 8]*100).ravel().tolist()
    # result[f'trend15_3'] = (signal_index5[:, 4]*1.2).ravel().tolist()
    #
    # data6 = list(collection.find({'machine': machine, 'group': group, 'component': 2, 'sensor': 4},
    #                             {'vib': 1}).sort([('datetime', -1)]).limit(1))[0]
    # vib_data6 = data6.get('vib')
    # signal_index6 = index_result(vib_data6, 1000)
    # result[f'trend16'] = signal_index6[:, 4].ravel().tolist()
    # result[f'trend17'] = signal_index6[:, 9].ravel().tolist()
    # result[f'trend18'] = (signal_index6[:, 1]*100).ravel().tolist()
    # result[f'trend18_1'] = signal_index6[:, 0].ravel().tolist()
    # result[f'trend18_2'] = (signal_index6[:, 8]*100).ravel().tolist()
    # result[f'trend18_3'] = (signal_index6[:, 4]*1.2).ravel().tolist()
    #
    # data7 = list(collection.find({'machine': machine, 'group': group, 'component': 2, 'sensor': 5},
    #                             {'vib': 1}).sort([('datetime', -1)]).limit(1))[0]
    # vib_data7 = data7.get('vib')
    # signal_index7 = index_result(vib_data7, 1000)
    # result[f'trend19'] = signal_index7[:, 4].ravel().tolist()
    # result[f'trend20'] = signal_index7[:, 9].ravel().tolist()
    # result[f'trend21'] = (signal_index7[:, 1]*100).ravel().tolist()
    # result[f'trend21_1'] = signal_index7[:, 0].ravel().tolist()
    # result[f'trend21_2'] = (signal_index7[:, 8]*100).ravel().tolist()
    # result[f'trend21_3'] = (signal_index6[:, 4]*1.2).ravel().tolist()
    #
    # data8 = list(collection.find({'machine': machine, 'group': group, 'component': 3, 'sensor': 1},
    #                             {'vib': 1}).sort([('datetime', -1)]).limit(1))[0]
    # vib_data8 = data8.get('vib')
    # signal_index8 = index_result(vib_data8, 1000)
    # result[f'trend22'] = signal_index8[:, 4].ravel().tolist()
    # result[f'trend23'] = signal_index8[:, 9].ravel().tolist()
    # result[f'trend24'] = (signal_index8[:, 1]*100).ravel().tolist()
    # result[f'trend24_1'] = signal_index8[:, 0].ravel().tolist()
    # result[f'trend24_2'] = (signal_index8[:, 8]*100).ravel().tolist()
    # result[f'trend24_3'] = (signal_index8[:, 4]*1.2).ravel().tolist()
    #
    # data9 = list(collection.find({'machine': machine, 'group': group, 'component': 3, 'sensor': 2},
    #                             {'vib': 1}).sort([('datetime', -1)]).limit(1))[0]
    # vib_data9 = data9.get('vib')
    # signal_index9 = index_result(vib_data9, 1000)
    # result[f'trend25'] = signal_index9[:, 4].ravel().tolist()
    # result[f'trend26'] = signal_index9[:, 9].ravel().tolist()
    # result[f'trend27'] = (signal_index9[:, 1]*100).ravel().tolist()
    # result[f'trend27_1'] = signal_index9[:, 0].ravel().tolist()
    # result[f'trend27_2'] = (signal_index9[:, 8]*100).ravel().tolist()
    # result[f'trend27_3'] = (signal_index9[:, 4]*1.2).ravel().tolist()
    signal1=[];signal2=[];signal3=[];signal4=[];signal5=[];signal6=[];signal7=[];signal8=[];signal9=[];
    signal10=[];signal11=[];signal12=[];signal13=[];signal14=[];signal15=[];signal16=[];signal17=[];signal18=[];
    signal19=[];signal20=[];signal21=[];signal22=[];signal23=[];signal24=[];signal25=[];signal26=[];signal27=[];
    signal3_1=[];signal3_2=[]; signal6_1=[];signal6_2=[]; signal9_1=[];signal9_2=[]; signal12_1=[];signal12_2=[];
    signal15_1 = [];signal15_2 = []; signal18_1=[];signal18_2=[]; signal21_1=[];signal21_2=[]; signal24_1=[];signal24_2=[];
    signal27_1 = [];signal27_2 = []; signal3_3=[];signal6_3=[];signal9_3=[];signal12_3=[];signal15_3=[];signal18_3=[];
    signal21_3 = [];signal24_3=[];signal27_3=[];
    collection2 = eval(f'db.indicator_data_{group}_{machine}')
    start_time_format = "2022-11-01 00:00:00"
    current_time = datetime.now()
    end_time_format = current_time.strftime("%Y-%m-%d %H:%M:%S")

    result_list1 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': f'SE_{group}_{machine}_1_1'}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'impulse': 1,'datetime': 1}))
    result_list2 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': f"SE_{group}_{machine}_1_2"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'impulse': 1,'datetime': 1}))
    result_list3 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': f"SE_{group}_{machine}_2_1"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'impulse': 1,'datetime': 1}))
    result_list4 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': f"SE_{group}_{machine}_2_2"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'impulse': 1,'datetime': 1}))
    result_list5 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': f"SE_{group}_{machine}_2_3"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'impulse': 1,'datetime': 1}))
    result_list6 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': f"SE_{group}_{machine}_2_4"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'impulse': 1,'datetime': 1}))
    result_list7 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': f"SE_{group}_{machine}_2_5"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'impulse': 1,'datetime': 1}))
    result_list8 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': f"SE_{group}_{machine}_3_1"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'impulse': 1,'datetime': 1}))
    result_list9 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': f"SE_{group}_{machine}_3_2"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'impulse': 1,'datetime': 1}))

    # print(result_list1)
    fea_x1,fea_x2,fea_x3,fea_x4,fea_x5,fea_x6,fea_x7,fea_x8,fea_x9=[],[],[],[],[],[],[],[],[]
    for s1 in result_list1:
        signal1.append(s1.get('rms'))
        signal2.append(s1.get('kur'))
        signal3.append(s1.get('std'))
        signal3_1.append(s1.get('peak'))
        signal3_2.append(s1.get('speed_rms'))
        signal3_3.append(s1.get('impulse'))
        fea_x1.append(s1.get('datetime'))
    for s2 in result_list2:
        signal4.append(s2.get('rms'))
        signal5.append(s2.get('kur'))
        signal6.append(s2.get('std'))
        signal6_1.append(s2.get('peak'))
        signal6_2.append(s2.get('speed_rms'))
        signal6_3.append(s2.get('impulse'))
        fea_x2.append(s2.get('datetime'))
    for s3 in result_list3:
        signal7.append(s3.get('rms'))
        signal8.append(s3.get('kur'))
        signal9.append(s3.get('std'))
        signal9_1.append(s3.get('peak'))
        signal9_2.append(s3.get('speed_rms'))
        signal9_3.append(s3.get('impulse'))
        fea_x3.append(s3.get('datetime'))
    for s4 in result_list4:
        signal10.append(s4.get('rms'))
        signal11.append(s4.get('kur'))
        signal12.append(s4.get('std'))
        signal12_1.append(s4.get('peak'))
        signal12_2.append(s4.get('speed_rms'))
        signal12_3.append(s4.get('impulse'))
        fea_x4.append(s4.get('datetime'))
    for s5 in result_list5:
        signal13.append(s5.get('rms'))
        signal14.append(s5.get('kur'))
        signal15.append(s5.get('std'))
        signal15_1.append(s5.get('peak'))
        signal15_2.append(s5.get('speed_rms'))
        signal15_3.append(s5.get('impulse'))
        fea_x5.append(s5.get('datetime'))
    for s6 in result_list6:
        signal16.append(s6.get('rms'))
        signal17.append(s6.get('kur'))
        signal18.append(s6.get('std'))
        signal18_1.append(s6.get('peak'))
        signal18_2.append(s6.get('speed_rms'))
        signal18_3.append(s6.get('impulse'))
        fea_x6.append(s6.get('datetime'))

    for s7 in result_list7:
        signal19.append(s7.get('rms'))
        signal20.append(s7.get('kur'))
        signal21.append(s7.get('std'))
        signal21_1.append(s7.get('peak'))
        signal21_2.append(s7.get('speed_rms'))
        signal21_3.append(s7.get('impulse'))
        fea_x7.append(s7.get('datetime'))
    for s8 in result_list8:
        signal22.append(s8.get('rms'))
        signal23.append(s8.get('kur'))
        signal24.append(s8.get('std'))
        signal24_1.append(s8.get('peak'))
        signal24_2.append(s8.get('speed_rms'))
        signal24_3.append(s8.get('impulse'))
        fea_x8.append(s8.get('datetime'))
    for s9 in result_list9:
        signal25.append(s9.get('rms'))
        signal26.append(s9.get('kur'))
        signal27.append(s9.get('std'))
        signal27_1.append(s9.get('peak'))
        signal27_2.append(s9.get('speed_rms'))
        signal27_3.append(s9.get('impulse'))
        fea_x9.append(s9.get('datetime'))
    signal1 = [item for sublist in signal1 for item in sublist]
    signal2 = [item for sublist in signal2 for item in sublist]
    signal3 = [item for sublist in signal3 for item in sublist]
    signal4 = [item for sublist in signal4 for item in sublist]
    signal5 = [item for sublist in signal5 for item in sublist]
    signal6 = [item for sublist in signal6 for item in sublist]
    signal7 = [item for sublist in signal7 for item in sublist]
    signal8 = [item for sublist in signal8 for item in sublist]
    signal9 = [item for sublist in signal9 for item in sublist]
    signal10 = [item for sublist in signal10 for item in sublist]
    signal11 = [item for sublist in signal11 for item in sublist]
    signal12 = [item for sublist in signal12 for item in sublist]
    signal13 = [item for sublist in signal13 for item in sublist]
    signal14 = [item for sublist in signal14 for item in sublist]
    signal15 = [item for sublist in signal15 for item in sublist]
    signal16 = [item for sublist in signal16 for item in sublist]
    signal17 = [item for sublist in signal17 for item in sublist]
    signal18 = [item for sublist in signal18 for item in sublist]
    signal19 = [item for sublist in signal19 for item in sublist]
    signal20 = [item for sublist in signal20 for item in sublist]
    signal21 = [item for sublist in signal21 for item in sublist]
    signal22 = [item for sublist in signal22 for item in sublist]
    signal23 = [item for sublist in signal23 for item in sublist]
    signal24 = [item for sublist in signal24 for item in sublist]
    signal25 = [item for sublist in signal25 for item in sublist]
    signal26 = [item for sublist in signal26 for item in sublist]
    signal27 = [item for sublist in signal27 for item in sublist]

    signal3_1 = [item for sublist in signal3_1 for item in sublist]
    signal3_2 = [item for sublist in signal3_2 for item in sublist]
    signal6_1 = [item for sublist in signal6_1 for item in sublist]
    signal6_2 = [item for sublist in signal6_2 for item in sublist]
    signal9_1 = [item for sublist in signal9_1 for item in sublist]
    signal9_2 = [item for sublist in signal9_2 for item in sublist]
    signal12_1 = [item for sublist in signal12_1 for item in sublist]
    signal12_2 = [item for sublist in signal12_2 for item in sublist]
    signal15_1 = [item for sublist in signal15_1 for item in sublist]
    signal15_2 = [item for sublist in signal15_2 for item in sublist]
    signal18_1 = [item for sublist in signal18_1 for item in sublist]
    signal18_2 = [item for sublist in signal18_2 for item in sublist]
    signal21_1 = [item for sublist in signal21_1 for item in sublist]
    signal21_2 = [item for sublist in signal21_2 for item in sublist]
    signal24_1 = [item for sublist in signal24_1 for item in sublist]
    signal24_2 = [item for sublist in signal24_2 for item in sublist]
    signal27_1 = [item for sublist in signal27_1 for item in sublist]
    signal27_2 = [item for sublist in signal27_2 for item in sublist]

    signal3_3 = [item for sublist in signal3_3 for item in sublist]
    signal3_3 = [abs(x) for x in signal3_3]
    signal6_3 = [item for sublist in signal6_3 for item in sublist]
    signal6_3 = [abs(x) for x in signal6_3]
    signal9_3 = [item for sublist in signal9_3 for item in sublist]
    signal9_3 = [abs(x) for x in signal9_3]
    signal12_3 = [item for sublist in signal12_3 for item in sublist]
    signal12_3 = [abs(x) for x in signal12_3]
    signal15_3 = [item for sublist in signal15_3 for item in sublist]
    signal15_3 = [abs(x) for x in signal15_3]
    signal18_3 = [item for sublist in signal18_3 for item in sublist]
    signal18_3 = [abs(x) for x in signal18_3]
    signal21_3 = [item for sublist in signal21_3 for item in sublist]
    signal21_3 = [abs(x) for x in signal21_3]
    signal24_3 = [item for sublist in signal24_3 for item in sublist]
    signal24_3 = [abs(x) for x in signal24_3]
    signal27_3 = [item for sublist in signal27_3 for item in sublist]
    signal27_3 = [abs(x) for x in signal27_3]
    result[f'trend1'] = signal1
    result[f'trend2'] = signal2
    result[f'trend3'] = signal3
    result[f'trend4'] = signal4
    result[f'trend5'] = signal5
    result[f'trend6'] = signal6
    result[f'trend7'] = signal7
    result[f'trend8'] = signal8
    result[f'trend9'] = signal9
    result[f'trend10'] = signal10
    result[f'trend11'] = signal11
    result[f'trend12'] = signal12
    result[f'trend13'] = signal13
    result[f'trend14'] = signal14
    result[f'trend15'] = signal15
    result[f'trend16'] = signal16
    result[f'trend17'] = signal17
    result[f'trend18'] = signal18
    result[f'trend19'] = signal19
    result[f'trend20'] = signal20
    result[f'trend21'] = signal21
    result[f'trend22'] = signal22
    result[f'trend23'] = signal23
    result[f'trend24'] = signal24
    result[f'trend25'] = signal25
    result[f'trend26'] = signal26
    result[f'trend27'] = signal27

    result[f'trend3_1'] = signal3_1
    result[f'trend3_2'] = signal3_2
    result[f'trend6_1'] = signal6_1
    result[f'trend6_2'] = signal6_2
    result[f'trend9_1'] = signal9_1
    result[f'trend9_2'] = signal9_2
    result[f'trend12_1'] = signal12_1
    result[f'trend12_2'] = signal12_2
    result[f'trend15_1'] = signal15_1
    result[f'trend15_2'] = signal15_2
    result[f'trend18_1'] = signal18_1
    result[f'trend18_2'] = signal18_2
    result[f'trend21_1'] = signal21_1
    result[f'trend21_2'] = signal21_2
    result[f'trend24_1'] = signal24_1
    result[f'trend24_2'] = signal24_2
    result[f'trend27_1'] = signal27_1
    result[f'trend27_2'] = signal27_2

    result[f'trend3_3'] = signal3_3
    result[f'trend6_3'] = signal6_3
    result[f'trend9_3'] = signal9_3
    result[f'trend12_3'] = signal12_3
    result[f'trend15_3'] = signal15_3
    result[f'trend18_3'] = signal18_3
    result[f'trend21_3'] = signal21_3
    result[f'trend24_3'] = signal24_3
    result[f'trend27_3'] = signal27_3

    result[f'trend27_3'] = signal27_3
    ###横轴日期
    # result_listd = list(collection2.find({"$and": [{"datetime": {"$gte": str(start_time_format), "$lte": str(end_time_format)}},
    #                                                {'sensorID': f'SE_{group}_{machine}_1_1'}]},
    #                                      {'datetime': 1}))
    # for i in range(0, len(result_listd)):
    #     result['fea_x'].append(result_listd[i].get('datetime'))
    # result['fea_x'] = [datetime.strptime(dt, '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d/%H:%M:%S') for dt in result['fea_x']]
    result['fea_x1'] = fea_x1
    result['fea_x2'] = fea_x2
    result['fea_x3'] = fea_x3
    result['fea_x4'] = fea_x4
    result['fea_x5'] = fea_x5
    result['fea_x6'] = fea_x6
    result['fea_x7'] = fea_x7
    result['fea_x8'] = fea_x8
    result['fea_x9'] = fea_x9
    return result






def update_home3_2(query_order,group,machine):
    signal1=[];signal2=[];signal3=[];signal4=[];signal5=[];signal6=[];signal7=[];signal8=[];signal9=[];
    signal10=[];signal11=[];signal12=[];signal13=[];signal14=[];signal15=[];signal16=[];signal17=[];signal18=[];
    signal19=[];signal20=[];signal21=[];signal22=[];signal23=[];signal24=[];signal25=[];signal26=[];signal27=[];
    signal3_1=[];signal3_2=[]; signal6_1=[];signal6_2=[]; signal9_1=[];signal9_2=[]; signal12_1=[];signal12_2=[];
    signal15_1 = [];signal15_2 = []; signal18_1=[];signal18_2=[]; signal21_1=[];signal21_2=[]; signal24_1=[];signal24_2=[];
    signal27_1 = [];signal27_2 = [];

    db = get_db()
    collection2 = eval(f'db.indicator_data_{group}_{machine}')
    group=int(group)
    machine=int(machine)
    start_time = query_order.get("start_time")
    end_time = query_order.get("end_time")
    result = {'fea_x': []}

    start_time_format = str(start_time)
    end_time_format = str(end_time)
    # print('2023-11-01 00:00:00')
    # print('2024-11-02 18:24:05')
    result_list1 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': "SE_1_1_1_1"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'datetime': 1}))
    result_list2 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': "SE_1_1_1_2"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'datetime': 1}))
    result_list3 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': "SE_1_1_2_1"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'datetime': 1}))
    result_list4 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': "SE_1_1_2_2"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'datetime': 1}))
    result_list5 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': "SE_1_1_2_3"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'datetime': 1}))
    result_list6 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': "SE_1_1_2_4"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'datetime': 1}))
    result_list7 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': "SE_1_1_2_5"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'datetime': 1}))
    result_list8 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': "SE_1_1_3_1"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'datetime': 1}))
    result_list9 = list(collection2.find({"$and": [{"datetime": {"$gte": start_time_format, "$lte": end_time_format}},
                                   {'sensorID': "SE_1_1_3_2"}]},
                         {'sensorID': 1, 'rms': 1, 'kur': 1, 'std': 1, 'peak':1, 'speed_rms':1,'datetime': 1}))
    for s1 in result_list1:
        signal1.append(s1.get('rms'))
        signal2.append(s1.get('kur'))
        signal3.append(s1.get('std'))
        signal3_1.append(s1.get('peak'))
        signal3_2.append(s1.get('speed_rms'))
    for s2 in result_list2:
        signal4.append(s2.get('rms'))
        signal5.append(s2.get('kur'))
        signal6.append(s2.get('std'))
        signal6_1.append(s1.get('peak'))
        signal6_2.append(s1.get('speed_rms'))
    for s3 in result_list3:
        signal7.append(s3.get('rms'))
        signal8.append(s3.get('kur'))
        signal9.append(s3.get('std'))
        signal9_1.append(s1.get('peak'))
        signal9_2.append(s1.get('speed_rms'))
    for s4 in result_list4:
        signal10.append(s4.get('rms'))
        signal11.append(s4.get('kur'))
        signal12.append(s4.get('std'))
        signal12_1.append(s1.get('peak'))
        signal12_2.append(s1.get('speed_rms'))
    for s5 in result_list5:
        signal13.append(s5.get('rms'))
        signal14.append(s5.get('kur'))
        signal15.append(s5.get('std'))
        signal15_1.append(s1.get('peak'))
        signal15_2.append(s1.get('speed_rms'))
    for s6 in result_list6:
        signal16.append(s6.get('rms'))
        signal17.append(s6.get('kur'))
        signal18.append(s6.get('std'))
        signal18_1.append(s1.get('peak'))
        signal18_2.append(s1.get('speed_rms'))
    for s7 in result_list7:
        signal19.append(s7.get('rms'))
        signal20.append(s7.get('kur'))
        signal21.append(s7.get('std'))
        signal21_1.append(s1.get('peak'))
        signal21_2.append(s1.get('speed_rms'))
    for s8 in result_list8:
        signal22.append(s8.get('rms'))
        signal23.append(s8.get('kur'))
        signal24.append(s8.get('std'))
        signal24_1.append(s1.get('peak'))
        signal24_2.append(s1.get('speed_rms'))
    for s9 in result_list9:
        signal25.append(s9.get('rms'))
        signal26.append(s9.get('kur'))
        signal27.append(s9.get('std'))
        signal27_1.append(s1.get('peak'))
        signal27_2.append(s1.get('speed_rms'))

    signal1 = [item for sublist in signal1 for item in sublist]
    signal2 = [item for sublist in signal2 for item in sublist]
    signal3 = [item for sublist in signal3 for item in sublist]
    signal4 = [item for sublist in signal4 for item in sublist]
    signal5 = [item for sublist in signal5 for item in sublist]
    signal6 = [item for sublist in signal6 for item in sublist]
    signal7 = [item for sublist in signal7 for item in sublist]
    signal8 = [item for sublist in signal8 for item in sublist]
    signal9 = [item for sublist in signal9 for item in sublist]
    signal10 = [item for sublist in signal10 for item in sublist]
    signal11 = [item for sublist in signal11 for item in sublist]
    signal12 = [item for sublist in signal12 for item in sublist]
    signal13 = [item for sublist in signal13 for item in sublist]
    signal14 = [item for sublist in signal14 for item in sublist]
    signal15 = [item for sublist in signal15 for item in sublist]
    signal16 = [item for sublist in signal16 for item in sublist]
    signal17 = [item for sublist in signal17 for item in sublist]
    signal18 = [item for sublist in signal18 for item in sublist]
    signal19 = [item for sublist in signal19 for item in sublist]
    signal20 = [item for sublist in signal20 for item in sublist]
    signal21 = [item for sublist in signal21 for item in sublist]
    signal22 = [item for sublist in signal22 for item in sublist]
    signal23 = [item for sublist in signal23 for item in sublist]
    signal24 = [item for sublist in signal24 for item in sublist]
    signal25 = [item for sublist in signal25 for item in sublist]
    signal26 = [item for sublist in signal26 for item in sublist]
    signal27 = [item for sublist in signal27 for item in sublist]

    signal3_1 = [item for sublist in signal3_1 for item in sublist]
    signal3_2 = [item for sublist in signal3_2 for item in sublist]
    signal6_1 = [item for sublist in signal6_1 for item in sublist]
    signal6_2 = [item for sublist in signal6_2 for item in sublist]
    signal9_1 = [item for sublist in signal9_1 for item in sublist]
    signal9_2 = [item for sublist in signal9_2 for item in sublist]
    signal12_1 = [item for sublist in signal12_1 for item in sublist]
    signal12_2 = [item for sublist in signal12_2 for item in sublist]
    signal15_1 = [item for sublist in signal15_1 for item in sublist]
    signal15_2 = [item for sublist in signal15_2 for item in sublist]
    signal18_1 = [item for sublist in signal18_1 for item in sublist]
    signal18_2 = [item for sublist in signal18_2 for item in sublist]
    signal21_1 = [item for sublist in signal21_1 for item in sublist]
    signal21_2 = [item for sublist in signal21_2 for item in sublist]
    signal24_1 = [item for sublist in signal24_1 for item in sublist]
    signal24_2 = [item for sublist in signal24_2 for item in sublist]
    signal27_1 = [item for sublist in signal27_1 for item in sublist]
    signal27_2 = [item for sublist in signal27_2 for item in sublist]

    result[f'trend1'] = signal1
    result[f'trend2'] = signal2
    result[f'trend3'] = signal3
    result[f'trend4'] = signal4
    result[f'trend5'] = signal5
    result[f'trend6'] = signal6
    result[f'trend7'] = signal7
    result[f'trend8'] = signal8
    result[f'trend9'] = signal9
    result[f'trend10'] = signal10
    result[f'trend11'] = signal11
    result[f'trend12'] = signal12
    result[f'trend13'] = signal13
    result[f'trend14'] = signal14
    result[f'trend15'] = signal15
    result[f'trend16'] = signal16
    result[f'trend17'] = signal17
    result[f'trend18'] = signal18
    result[f'trend19'] = signal19
    result[f'trend20'] = signal20
    result[f'trend21'] = signal21
    result[f'trend22'] = signal22
    result[f'trend23'] = signal23
    result[f'trend24'] = signal24
    result[f'trend25'] = signal25
    result[f'trend26'] = signal26
    result[f'trend27'] = signal27

    result[f'trend3_1'] = signal3_1
    result[f'trend3_2'] = signal3_2
    result[f'trend6_1'] = signal6_1
    result[f'trend6_2'] = signal6_2
    result[f'trend9_1'] = signal9_1
    result[f'trend9_2'] = signal9_2
    result[f'trend12_1'] = signal12_1
    result[f'trend12_2'] = signal12_2
    result[f'trend15_1'] = signal15_1
    result[f'trend15_2'] = signal15_2
    result[f'trend18_1'] = signal18_1
    result[f'trend18_2'] = signal18_2
    result[f'trend21_1'] = signal21_1
    result[f'trend21_2'] = signal21_2
    result[f'trend24_1'] = signal24_1
    result[f'trend24_2'] = signal24_2
    result[f'trend27_1'] = signal27_1
    result[f'trend27_2'] = signal27_2


###横轴日期
    result_listd = list(collection2.find({"$and": [{"datetime": {"$gte": str(start_time),"$lte": str(end_time)}},
                                                   {'sensorID':'SE_1_1_1_1'}]},
                                                   {'datetime':1}))
    for i in range(0,len(result_listd)):
        result['fea_x'].append(result_listd[i].get('datetime'))
    # 阈值
    thr1 = get_thr(model='rms',group=int(group),machine=int(machine),component=1,sensor=1)
    result['thr11'] = thr1['thr']['warning']
    result['thr12'] = thr1['thr']['fault']
    result['thr13'] = thr1['thr']['fault']*1.1
    thr2 = get_thr(model='kur',group=int(group),machine=int(machine),component=1,sensor=1)
    result['thr14'] = thr2['thr']['warning']
    result['thr15'] = thr2['thr']['fault']
    result['thr16'] = thr2['thr']['fault']*1.1
    thr3 = get_thr(model='std',group=int(group),machine=int(machine),component=1,sensor=1)
    result['thr17'] = thr3['thr']['warning']
    result['thr18'] = thr3['thr']['fault']
    result['thr19'] = thr3['thr']['fault']*1.1
    thr3_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=1,sensor=1)
    result['thr3_1'] = thr3_1['thr']['warning']
    result['thr3_2'] = thr3_1['thr']['fault']
    result['thr3_3'] = thr3_1['thr']['fault']*1.1
    thr3_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=1,sensor=1)
    result['thr3_4'] = thr3_2['thr']['warning']
    result['thr3_5'] = thr3_2['thr']['fault']
    result['thr3_6'] = thr3_2['thr']['fault']*1.1

    thr4 = get_thr(model='rms',group=int(group),machine=int(machine),component=1,sensor=2)
    result['thr21'] = thr4['thr']['warning']
    result['thr22'] = thr4['thr']['fault']
    result['thr23'] = thr4['thr']['fault']*1.1
    thr5 = get_thr(model='kur',group=int(group),machine=int(machine),component=1,sensor=2)
    result['thr24'] = thr5['thr']['warning']
    result['thr25'] = thr5['thr']['fault']
    result['thr26'] = thr5['thr']['fault']*1.1
    thr6 = get_thr(model='std',group=int(group),machine=int(machine),component=1,sensor=2)
    result['thr27'] = thr6['thr']['warning']
    result['thr28'] = thr6['thr']['fault']
    result['thr29'] = thr6['thr']['fault']*1.1
    thr6_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=1,sensor=2)
    result['thr6_1'] = thr6_1['thr']['warning']
    result['thr6_2'] = thr6_1['thr']['fault']
    result['thr6_3'] = thr6_1['thr']['fault']*1.1
    thr6_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=1,sensor=2)
    result['thr6_4'] = thr6_2['thr']['warning']
    result['thr6_5'] = thr6_2['thr']['fault']
    result['thr6_6'] = thr6_2['thr']['fault']*1.1


    thr7 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=1)
    result['thr31'] = thr7['thr']['warning']
    result['thr32'] = thr7['thr']['fault']
    result['thr33'] = thr7['thr']['fault']*1.1
    thr8 = get_thr(model='kur',group=int(group),machine=int(machine),component=2,sensor=1)
    result['thr34'] = thr8['thr']['warning']
    result['thr35'] = thr8['thr']['fault']
    result['thr36'] = thr8['thr']['fault']*1.1
    thr9 = get_thr(model='std',group=int(group),machine=int(machine),component=2,sensor=1)
    result['thr37'] = thr9['thr']['warning']
    result['thr38'] = thr9['thr']['fault']
    result['thr39'] = thr9['thr']['fault']*1.1
    thr9_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=2,sensor=1)
    result['thr9_1'] = thr9_1['thr']['warning']
    result['thr9_2'] = thr9_1['thr']['fault']
    result['thr9_3'] = thr9_1['thr']['fault']*1.1
    thr9_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=1)
    result['thr9_4'] = thr9_2['thr']['warning']
    result['thr9_5'] = thr9_2['thr']['fault']
    result['thr9_6'] = thr9_2['thr']['fault']*1.1

    thr10 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=2)
    result['thr41'] = thr10['thr']['warning']
    result['thr42'] = thr10['thr']['fault']
    result['thr43'] = thr10['thr']['fault']*1.1
    thr11 = get_thr(model='kur',group=int(group),machine=int(machine),component=2,sensor=2)
    result['thr44'] = thr11['thr']['warning']
    result['thr45'] = thr11['thr']['fault']
    result['thr46'] = thr11['thr']['fault']*1.1
    thr12 = get_thr(model='std',group=int(group),machine=int(machine),component=2,sensor=2)
    result['thr47'] = thr12['thr']['warning']
    result['thr48'] = thr12['thr']['fault']
    result['thr49'] = thr12['thr']['fault']*1.1
    thr12_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=2,sensor=2)
    result['thr12_1'] = thr12_1['thr']['warning']
    result['thr12_2'] = thr12_1['thr']['fault']
    result['thr12_3'] = thr12_1['thr']['fault']*1.1
    thr12_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=2)
    result['thr12_4'] = thr12_2['thr']['warning']
    result['thr12_5'] = thr12_2['thr']['fault']
    result['thr12_6'] = thr12_2['thr']['fault']*1.1

    thr13 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=3)
    result['thr51'] = thr13['thr']['warning']
    result['thr52'] = thr13['thr']['fault']
    result['thr53'] = thr13['thr']['fault']*1.1
    thr14 = get_thr(model='kur',group=int(group),machine=int(machine),component=2,sensor=3)
    result['thr54'] = thr14['thr']['warning']
    result['thr55'] = thr14['thr']['fault']
    result['thr56'] = thr14['thr']['fault']*1.1
    thr15 = get_thr(model='std',group=int(group),machine=int(machine),component=2,sensor=3)
    result['thr57'] = thr15['thr']['warning']
    result['thr58'] = thr15['thr']['fault']
    result['thr59'] = thr15['thr']['fault']*1.1
    thr15_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=2,sensor=3)
    result['thr15_1'] = thr15_1['thr']['warning']
    result['thr15_2'] = thr15_1['thr']['fault']
    result['thr15_3'] = thr15_1['thr']['fault']*1.1
    thr15_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=3)
    result['thr15_4'] = thr15_2['thr']['warning']
    result['thr15_5'] = thr15_2['thr']['fault']
    result['thr15_6'] = thr15_2['thr']['fault']*1.1

    thr16 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=4)
    result['thr61'] = thr16['thr']['warning']
    result['thr62'] = thr16['thr']['fault']
    result['thr63'] = thr16['thr']['fault']*1.1
    thr17 = get_thr(model='kur',group=int(group),machine=int(machine),component=2,sensor=4)
    result['thr64'] = thr17['thr']['warning']
    result['thr65'] = thr17['thr']['fault']
    result['thr66'] = thr17['thr']['fault']*1.1
    thr18 = get_thr(model='std',group=int(group),machine=int(machine),component=2,sensor=4)
    result['thr67'] = thr18['thr']['warning']
    result['thr68'] = thr18['thr']['fault']
    result['thr69'] = thr18['thr']['fault']*1.1
    thr18_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=2,sensor=4)
    result['thr18_1'] = thr18_1['thr']['warning']
    result['thr18_2'] = thr18_1['thr']['fault']
    result['thr18_3'] = thr18_1['thr']['fault']*1.1
    thr18_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=4)
    result['thr18_4'] = thr18_2['thr']['warning']
    result['thr18_5'] = thr18_2['thr']['fault']
    result['thr18_6'] = thr18_2['thr']['fault']*1.1

    thr19 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=5)
    result['thr71'] = thr19['thr']['warning']
    result['thr72'] = thr19['thr']['fault']
    result['thr73'] = thr19['thr']['fault']*1.1
    thr20 = get_thr(model='kur',group=int(group),machine=int(machine),component=2,sensor=5)
    result['thr74'] = thr20['thr']['warning']
    result['thr75'] = thr20['thr']['fault']
    result['thr76'] = thr20['thr']['fault']*1.1
    thr21 = get_thr(model='std',group=int(group),machine=int(machine),component=2,sensor=5)
    result['thr77'] = thr21['thr']['warning']
    result['thr78'] = thr21['thr']['fault']
    result['thr79'] = thr21['thr']['fault']*1.1
    thr21_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=2,sensor=5)
    result['thr21_1'] = thr21_1['thr']['warning']
    result['thr21_2'] = thr21_1['thr']['fault']
    result['thr21_3'] = thr21_1['thr']['fault']*1.1
    thr21_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=2,sensor=5)
    result['thr21_4'] = thr21_2['thr']['warning']
    result['thr21_5'] = thr21_2['thr']['fault']
    result['thr21_6'] = thr21_2['thr']['fault']*1.1

    thr22 = get_thr(model='rms',group=int(group),machine=int(machine),component=3,sensor=1)
    result['thr81'] = thr22['thr']['warning']
    result['thr82'] = thr22['thr']['fault']
    result['thr83'] = thr22['thr']['fault']*1.1
    thr23 = get_thr(model='kur',group=int(group),machine=int(machine),component=3,sensor=1)
    result['thr84'] = thr23['thr']['warning']
    result['thr85'] = thr23['thr']['fault']
    result['thr86'] = thr23['thr']['fault']*1.1
    thr24 = get_thr(model='std',group=int(group),machine=int(machine),component=3,sensor=1)
    result['thr87'] = thr24['thr']['warning']
    result['thr88'] = thr24['thr']['fault']
    result['thr89'] = thr24['thr']['fault']*1.1
    thr24_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=3,sensor=1)
    result['thr24_1'] = thr24_1['thr']['warning']
    result['thr24_2'] = thr24_1['thr']['fault']
    result['thr24_3'] = thr24_1['thr']['fault']*1.1
    thr24_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=3,sensor=1)
    result['thr24_4'] = thr24_2['thr']['warning']
    result['thr24_5'] = thr24_2['thr']['fault']
    result['thr24_6'] = thr24_2['thr']['fault']*1.1

    thr25 = get_thr(model='rms',group=int(group),machine=int(machine),component=3,sensor=2)
    result['thr91'] = thr25['thr']['warning']
    result['thr92'] = thr25['thr']['fault']
    result['thr93'] = thr25['thr']['fault']*1.1
    thr26 = get_thr(model='kur',group=int(group),machine=int(machine),component=3,sensor=2)
    result['thr94'] = thr26['thr']['warning']
    result['thr95'] = thr26['thr']['fault']
    result['thr96'] = thr26['thr']['fault']*1.1
    thr27 = get_thr(model='std',group=int(group),machine=int(machine),component=3,sensor=2)
    result['thr97'] = thr27['thr']['warning']
    result['thr98'] = thr27['thr']['fault']
    result['thr99'] = thr27['thr']['fault']*1.1
    thr27_1 = get_thr(model='peak',group=int(group),machine=int(machine),component=3,sensor=2)
    result['thr27_1'] = thr27_1['thr']['warning']
    result['thr27_2'] = thr27_1['thr']['fault']
    result['thr27_3'] = thr27_1['thr']['fault']*1.1
    thr27_2 = get_thr(model='rms',group=int(group),machine=int(machine),component=3,sensor=2)
    result['thr27_4'] = thr27_2['thr']['warning']
    result['thr27_5'] = thr27_2['thr']['fault']
    result['thr27_6'] = thr27_2['thr']['fault']*1.1

    return result


# 测点颜色变化
from collections import Counter
def sensors_state(group,machine):
    db = get_db()
    collection = db['state_data']
    state1 = list(collection.find({'group':int(group),'machine':int(machine)}, {'state':1}))
    state2 = [item['state'] for item in state1]
    data={}
    data[f'group_state_list']=state2
    return data

