
import pandas as pd
import os


class CSVConverter:
    ''' Factory class for csv files from xlsx'''

    def __init__(self, storage_dir = 'data/iom_dtm_reports/csv'):
        assert os.path.isdir(storage_dir) != True, "Something wrong with directories, try removing /csv"
        os.mkdir(storage_dir)

    def convert_to_csv(self, prefix, start = 1, end = 91):
        error_list = []
        for i in range(start, end + 1):
            s_i = str(i)
            file_path = 'data/iom_dtm_reports/' + prefix + s_i + '.xlsx'
            output_name = 'data/iom_dtm_reports/csv' + '/' + prefix + s_i + '.csv'
            try:
                df = pd.read_excel(file_path) # go to the sheet
                df.to_csv(output_name)
            except Exception as e:
                error_list.append(e)

##    check_paths('data/errors')
##    if len(error_list) > 0:
##        error_file = "data/errors/error_messages.txt"
##        if os.path.isfile(error_file):
##            pass
##        else:
##            os.path.
##        with open() as f:
##            f.write("\n".join(error_list))
        
        
                 
if __name__ == "__main__":
    c = CSVConverter()
    for i in ['r', 'd']:
        c.convert_to_csv(prefix = i)


