from openpyxl import Workbook
import os



def excel_file(dict_list:list,output_filename:str,sheet_name:str='Flats'):
    if not os.path.exists('excel_files'):
        os.makedirs('excel_files')

    filepath=os.path.join('excel_files',output_filename)
    
    wb=Workbook()
    ws=wb.active
    ws.title=sheet_name
    if dict_list:
        ws.append(['Ccылка','Статус','Цена','Описание','Год постройки'])
        for row in dict_list:
            ws.append(list(row))    
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 4)
        ws.column_dimensions[column].width = adjusted_width

    
    wb.save(filepath)
    return filepath

# excel_file(select_from_info_flats(),output_filename='test2.xlsx')