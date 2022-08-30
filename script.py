import pandas as pd

def hello(df_ex):
    return df_ex.loc[(df_ex['role']=="manager") & (df_ex['text'].str.contains("здравствуйте"))].index.to_list()

def say_name(df_ex):
    return df_ex.loc[(df_ex['role']=="manager") & (df_ex['text'].str.contains("зовут"))].index.to_list()

def good_bye(df_ex):
    return df_ex.loc[(df_ex['role']=="manager") & (df_ex['text'].str.contains("до свидания"))].index.to_list()

def get_manager_and_company_name(df_ex, lst_name):
    managers_names = []
    company_names = []
    for line in df_ex.loc[df_ex.index.isin(lst_name), 'text'].to_list():
        line_list = line.split()
        x = line_list.index('зовут')
        if line_list[x + 1] == 'компания':
            name = line_list[x - 1].capitalize()
        else:
            name = line_list [x + 1].capitalize()
        if name not in managers_names:
            managers_names.append(name)

        company_name = line[line.index('компания') + 8 :line.index('бизнес') + 6].strip()
        if company_name not in company_names:
            company_names.append(company_name)
        
    print('\n____________Имена менеджеров_________________')
    print(*managers_names, sep=', ')
    print('\n____________Названия компаний_________________')
    print(*company_names, sep=', ')
    

def main():
    df = pd.read_csv('test_data.csv')
    df_ex = df.copy()
    df_ex['text'] = df_ex['text'].str.lower()
    
    print('\n____________________Реплики в которых менеджер поздоровался____________________')
    print(df.loc[df.index.isin(hello(df_ex)), ['dlg_id', 'line_n', 'text']])
    
    print('\n____________________Реплики в которых менеджер представил себя____________________')
    name_str_index_list = say_name(df_ex)
    df_names = df.loc[df.index.isin(name_str_index_list), ['dlg_id', 'line_n', 'text']]
    print(df_names)
    
    get_manager_and_company_name(df_ex, name_str_index_list)
    good_bye_index = good_bye(df_ex)

    print('\n____________________Реплики в которых менеджер попращался____________________')
    df_good_bye = df.loc[df.index.isin(good_bye_index), ['dlg_id', 'line_n', 'text']]
    print(df_good_bye)

    print('\n____________________DLG_ID диалогов в которых менеджер поздоровался и попрощался____________________')
    answer_list = list(set(df_names['dlg_id'].to_list()) & set(df_good_bye['dlg_id'].to_list()))
    print(', '.join([str(i) for i in answer_list]))

if __name__ == '__main__':
    main()