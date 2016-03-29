import os


class GetLatestPackedControlFile(object):
    """
    1. .xml format control file.
    2. most latest under given folder path.
    """
    def __init__(self, folder_path):
        self.latest_packed_control_file = None
        control_log_file_name_list = []
        file_list = os.listdir(folder_path)#list all the file under the directory
        for file_name in  file_list:
            if file_name.startswith('CONTROL') and file_name.endswith('.XML'):
                control_log_file_name_list.append(os.path.join(folder_path,file_name))

        max_file_time = 0
        for item in control_log_file_name_list:
            if(os.path.getmtime(str(item)) > max_file_time):
                self.latest_packed_control_file = item
                max_file_time = os.path.getmtime(str(item))


    def get_latest_packed_control_file(self):
        return self.latest_packed_control_file


if __name__ == '__main__':
    control_file_folder_path = r'D:\01_Automation\20_Experiential_Conclusions_2015\53_Zhongshan_Aptio\01_Aptio\Log\Logs-150826'
    print GetLatestPackedControlFile(control_file_folder_path).get_latest_packed_control_file()

