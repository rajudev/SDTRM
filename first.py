import pandas as pd
import regex as re
from collections import OrderedDict

pd.set_option('display.max_rows', 500)
file_list = ['/Users/akarshan/Desktop/LTU_4_MUMBAI.xlsx', '/Users/akarshan/Desktop/Mumbai_2.xlsx',
             '/Users/akarshan/Desktop/Mumbai_4.xlsx']

final_dict = []
final_total_values = []
final_total_places = []
final_list = []


def filter_1(df):
    dict_company = OrderedDict()
    for i in range(df.shape[0]):
        a = str(df.iloc[i, 0])
        if a != 'nan' and a != 'Tin No.':
            if not bool(re.match('([0-9]){10,12}([a-zA-Z]){1}|([0-9]){6}\/([A-Z]){1}\/([0-9]){4}', a)):
                dict_company.update({a: i})
    return dict_company


def filter_2(df, dict_company):
    li_total_places = []
    li_total_values = []

    for j in range(df.shape[0]):
        a = str(df.iloc[j, 2])
        if bool(re.match('([Gg][Rr][Aa][Nn][Dd] )?[Tt][Oo][Tt][Aa][Ll]', a)) or a == 'current total':
            li_total_places.append(j)
            temp_li = []
            for z in range(4, 14):
                temp_li.append(df.iloc[j, z])
            li_total_values.append(temp_li)
        if a == 'Payment for the Month' or a == 'Amount reduced' or a == 'Addition During the Month':
            dict_company.update({a: [j, 2]})
    return li_total_places, li_total_values, dict_company


def function(file_list):
    raw_data = pd.read_excel(file_list[0])
    df_alpha = pd.DataFrame(raw_data)

    raw_data = pd.read_excel(file_list[1])
    df_beta = pd.DataFrame(raw_data)

    dict_company_alpha = filter_1(df_alpha)
    dict_company_beta = filter_1(df_beta)

    li_total_places_alpha, li_total_values_alpha, dict_company_alpha = filter_2(df_alpha, dict_company_alpha)
    li_total_places_beta, li_total_values_beta, dict_company_beta = filter_2(df_beta, dict_company_beta)

    print dict_company_alpha
    print dict_company_beta

    for key in dict_company_alpha:
        if key in dict_company_beta:
            if key == 'Payment for the Month':
                break
            else:
                df_alpha_new = df_alpha.iloc[dict_company_alpha[key]:li_total_places_alpha[dict_company_alpha.keys().index(key)]]
                df_beta_new = df_beta.iloc[dict_company_beta[key]:li_total_places_beta[dict_company_beta.keys().index(key)]]
                print df_beta_new
                print "------"
                final_list.append(df_alpha_new)
                final_list.append(df_beta_new)
    result = pd.concat(final_list, ignore_index=True)
    writer = pd.ExcelWriter('/Users/akarshan/Desktop/final.xlsx')
    df_gamma = pd.DataFrame(result)
    df_gamma.to_excel(writer,'Feb. sheet 8')
    writer.save()



for i in range(len(file_list) - 1):
    function([file_list[i], file_list[i + 1]])
    file_list.remove(file_list[i])
    file_list.remove(file_list[i + 1])
    break









    # dfalpha = df.iloc[dict_company.values()[0][0]:li_total[0]]


    # frames = [df_beta, df_alpha]


    # result = pd.concat(frames, ignore_index=True)
    # print result
    # writer = pd.ExcelWriter('/Users/akarshan/Desktop/finally.xlsx')
    # df3 = pd.DataFrame(result)
    # df3.to_excel(writer,'Sheet')
    # writer.save()
