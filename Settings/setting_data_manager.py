"""
Class manages saving and loading Setting Profiles. As well as handling the structures
"""
from Control_Module_Comm.Structures import Module_Individual, DAQ_Configuration, Sensor_Individual
import csv
from os import path
import pandas as pd
from PyQt5 import QtWidgets
import GUI_Handler
log = 0

def verify_file_exists(file_path: str):
    exists = path.isfile(file_path)
    if not exists and (file_path != ''):
        QtWidgets.QMessageBox().critical(GUI_Handler.main_window, 'WARNING', 'File does not exist')
    return exists


class Setting_File_Manager:
    def __init__(self, mod_con: [], sens_con: [], daq_con: DAQ_Configuration):
        self.module_configs = mod_con
        self.sensor_configs = sens_con
        self.daq_config = daq_con

    def set_filename(self, filename: str):
        """
        Sets an Object File Name for dealing with multiple loads and saves at a time.

        :param filename :  The path of the desired file.
        """
        self.filename = filename
        return filename

    def store_daq_configs(self, filename: str):
        """
        Stores Test Recording Configuration in specified File Name.

        :param filename : The The path of the desired file.
        """
        daq_file = 'Config/DAQ/' + filename

        # # Generate Test ID
        # if not self.daq_config.recording_configs["test_ID"]:
        #     self.daq_config.recording_configs["test_ID"] = DAQ_Configuration.generate_ID(
        #         self.daq_config.recording_configs['test_name'])

        # if verify_file_exists(daq_file):
        with open(daq_file, 'w', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(self.daq_config.signal_configs.keys())
            writer.writerow(self.daq_config.signal_configs.values())

            writer.writerow(self.daq_config.recording_configs.keys())
            writer.writerow(self.daq_config.recording_configs.values())

            writer.writerow(self.daq_config.data_handling_configs.keys())
            writer.writerow(self.daq_config.data_handling_configs.values())

            writer.writerow(self.daq_config.location_configs.keys())
            writer.writerow(self.daq_config.location_configs.values())

            writer.writerow(self.daq_config.specimen_location.keys())
            writer.writerow(self.daq_config.specimen_location.values())

            if log: print('Save Daq Configs : SUCCESSFUL')
        # else:
        #     if log: print('File Error')

        f.close()

    def load_daq_configs(self, filename: str):
        """
        Loads setting data from settings file.

        :param filename : the path and name of the file.

        :return list of DAQ Configs
        """
        daq_file = 'Config/DAQ/' + filename
        if verify_file_exists(daq_file):
            self.daq_config.signal_configs = pd.read_csv(daq_file, header=0, nrows=1).to_dict('r')[0]
            self.daq_config.recording_configs = pd.read_csv(daq_file, header=2, nrows=1).to_dict('r')[0]
            self.daq_config.data_handling_configs = pd.read_csv(daq_file, header=4, nrows=1).to_dict('r')[0]
            self.daq_config.location_configs = \
                pd.read_csv(daq_file, header=6, nrows=1, dtype={'longitude': str, 'latitude': str,
                                                                'hour': str, 'minute': str,
                                                                'second': str}).to_dict('r')[0]
            self.daq_config.specimen_location = pd.read_csv(daq_file, header=8, nrows=1).to_dict('r')[0]

            if log: print('Load Daq Configs : SUCCESSFUL')
        else:
            if log: print('File Error')

        return [self.daq_config.signal_configs, self.daq_config.recording_configs, self.daq_config.data_handling_configs,
                self.daq_config.location_configs, self.daq_config.specimen_location]

    def store_recording_configs(self, filename: str):
        """
        Store Only data for Recording.

        :param filename : the path and name of the file.
        """
        rec_file = 'Config/DAQ/Recording/' + filename

        # if verify_file_exists(rec_file):

        with open(rec_file, 'w', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(self.daq_config.recording_configs.keys())
            writer.writerow(self.daq_config.recording_configs.values())

            writer.writerow(self.daq_config.data_handling_configs.keys())
            writer.writerow(self.daq_config.data_handling_configs.values())

            if log: print('store Recording Config Successful')

        f.close()

        # else:
        #     if log: print('Storing Recording Configuration FAILED')

    def load_recording_configs(self, filename: str):
        filename

        if verify_file_exists(filename):
            self.daq_config.recording_configs = pd.read_csv(filename, header=0, nrows=1).to_dict('r')[0]

            if log: print('Load Recording Settings Successful')
        else:
            if log: print('Load Recording Configuration FILE DOES NOT EXISTS')

        return self.daq_config.recording_configs

    def store_location_configs(self, filename: str):
        """
        Store Only data for Location.

        :param filename : the path and name of the file.
        """
        loc_file = 'Config/DAQ/Location/' + filename

        if verify_file_exists(loc_file):
            with open(loc_file, 'w', newline='') as f:
                writer = csv.writer(f)

                writer.writerow(self.daq_config.location_configs.keys())
                writer.writerow(self.daq_config.location_configs.values())

                writer.writerow(self.daq_config.specimen_location.keys())
                writer.writerow(self.daq_config.specimen_location.values())

                if log: print('Storing Location Configuration Successful')

            f.close()
        else:
            if log: print('Storing Location Configuration FAILED')

    def load_location_configs(self, filename: str):
        """
        Loads Location Configuration from settings file.

        :param filename : the path and name of the file.

        :return Location Configuration Dictionary
        """
        loc_file = 'Config/DAQ/Location/' + filename

        if verify_file_exists(loc_file):
            self.daq_config.location_configs = pd.read_csv(loc_file, header=0, nrows=1, dtype=str).to_dict('r')[0]
            self.daq_config.specimen_location = pd.read_csv(loc_file, header=2, nrows=1, dtype=str).to_dict('r')[0]

            if log: print('Load Location Configuration Successful')
        else:
            if log: print('Load Location Configuration FILE DOES NOT EXISTS')

        return [self.daq_config.location_configs, self.daq_config.specimen_location]

    def store_signal_params(self, filename):
        """
        Store Only Signal Parameters in CSV File.

        :param filename: The desires File Name.
        """
        sig_file = 'Config/DAQ/Signal/' + filename

        if verify_file_exists(sig_file):
            with open(sig_file, 'w', newline='') as f:
                writer = csv.writer(f)

                writer.writerow(self.daq_config.signal_configs.keys())
                writer.writerow(self.daq_config.signal_configs.values())

                if log: print('Storing Signal Configuration Successful')

            f.close()
        else:
            if log: print('Storing Location Configuration FAILED')

    def load_signal_params(self, filename):
        """
        Loads Signal Parameters from settings file.

        :param filename : the path and name of the file.

        :return Signal Parameter Dictionary
        """
        sig_file = 'Config/DAQ/Signal/' + filename

        if verify_file_exists(sig_file):
            self.daq_config.signal_configs = pd.read_csv(sig_file).to_dict('r')[0]

            if log:
                print('Load Location Configuration Successful')
        else:
            if log: print('Load Signal Parameters FILE DOES NOT EXISTS')

        return self.daq_config.signal_configs

    def store_module_configs(self, filename: str, module: Module_Individual):
        module_file = 'Config/Module/' + filename
        if verify_file_exists(module_file):
            with open(module_file, 'w+', newline='') as f:
                writer = csv.writer(f)

                # for x in range(0, 1000000, 1):  # TESTING to make sure it is the same always. [PASSED]
                if log: print(list(module.channel_info.keys())[0])
                if log: print(type(module.channel_info.keys()))

                # Marroneo -  Store values in temp dict so that it will be stored like a word in csv.
                temp_dict = {list(module.channel_info.keys())[0]: module.channel_info['channel_name']}
                if log: print('WRITE Channel Settings: ' + str(temp_dict))
                writer.writerow(temp_dict.keys())
                writer.writerow(temp_dict.values())

                writer.writerow(module.channel_info['Sensor 1'].sensor_info.keys())
                writer.writerow(module.channel_info['Sensor 1'].sensor_info.values())

                writer.writerow(module.channel_info['Sensor 2'].sensor_info.keys())
                writer.writerow(module.channel_info['Sensor 2'].sensor_info.values())

                writer.writerow(module.channel_info['Sensor 3'].sensor_info.keys())
                writer.writerow(module.channel_info['Sensor 3'].sensor_info.values())

                writer.writerow(module.channel_info['Sensor 4'].sensor_info.keys())
                writer.writerow(module.channel_info['Sensor 4'].sensor_info.values())

                if log: print('Save Module Configs : SUCCESSFUL')
        else:
            if log: print('File Error')

        f.close()

    def load_module_config(self, filename: str):
        module_file = 'Config/Module/' + filename
        if verify_file_exists(module_file):
            name_dict = pd.read_csv(module_file, header=0, nrows=1).to_dict('r')[0]
            sensor_1 = pd.read_csv(module_file, header=2, nrows=1).to_dict('r')[0]
            sensor_2 = pd.read_csv(module_file, header=4, nrows=1).to_dict('r')[0]
            sensor_3 = pd.read_csv(module_file, header=6, nrows=1).to_dict('r')[0]
            sensor_4 = pd.read_csv(module_file, header=8, nrows=1).to_dict('r')[0]

            if log: print(name_dict)
            if log: print(sensor_1)
            if log: print(sensor_2)
            if log: print(sensor_3)
            if log: print(sensor_4)

            self.channel_config = Module_Individual.Module(name_dict['channel_name'], sensor_1, sensor_2, sensor_3, sensor_4)

            if log: print('Load Module Configs : SUCCESSFUL')

        else:
            if log: print('File Error')

        return self.channel_config

    # def store_sensor_config(self, filename: str, sensors: []):
    #     """
    #     Stores all sensor configurations in a single file.
    #     Should only store 4 and load as necessary in each module window.
    #     """
    #     sensor_file = 'Config/Sensor/' + filename
    #     if verify_file_exists(sensor_file):
    #         with open(sensor_file, 'w+', newline='') as f:
    #             writer = csv.writer(f)
    #
    #             for sen in sensors:
    #                 writer.writerow(sen.sensor_info.keys())
    #                 writer.writerow(sen.sensor_info.values())
    #
    #             if log: print('Save Sensor Configs : SUCCESSFUL')
    #     else:
    #         if log: print('File Error')
    #
    #     f.close()
    #
    # # TODO IMPLEMENT WITH 4 SENSORS.
    # def load_sensor_config(self, filename: str):
    #     sensor_file = 'Config/Sensor/' + filename
    #     if verify_file_exists(sensor_file):
    #         self.sensor_config = pd.read_csv(sensor_file, header=0, nrows=1).to_dict('r')[0]
    #
    #         if log: print('Load Sensor Configs : SUCCESSFUL')
    #
    #     else:
    #         if log: print('File Error')
    #
    #     return self.sensor_config

    def settings_to_string(self):
        """
        Reads Data from CSV file and converts it to comma and semi-colon separated STRING

        :return: comma and semi-colon separated STRING
        """
        new_line = ';'
        string = 'Test ID:' + new_line + DAQ_Configuration.generate_ID(self.daq_config.recording_configs['test_name']) + new_line

        string += ','.join(self.daq_config.recording_configs.keys()) + new_line
        string += ','.join(str(elem) for elem in self.daq_config.recording_configs.values()) + new_line

        string += ','.join(self.daq_config.signal_configs.keys()) + new_line
        string += ','.join(self.daq_config.signal_configs.values()) + new_line

        string += ','.join(self.daq_config.location_configs.keys()) + new_line
        string += ','.join(self.daq_config.location_configs.values()) + new_line

        string += ','.join(self.daq_config.specimen_location.keys()) + new_line
        string += ','.join(str(elem) for elem in self.daq_config.specimen_location.values()) + new_line

        # Modules information
        for module in self.module_configs:
            string += 'Module Name' + new_line
            string += module.channel_info['channel_name'] + new_line

            string += ','.join(module.channel_info['Sensor 1'].sensor_info.keys()) + new_line
            string += ','.join(module.channel_info['Sensor 1'].sensor_info.values()) + new_line

            string += ','.join(module.channel_info['Sensor 2'].sensor_info.keys()) + new_line
            string += ','.join(module.channel_info['Sensor 2'].sensor_info.values()) + new_line

            string += ','.join(module.channel_info['Sensor 3'].sensor_info.keys()) + new_line
            string += ','.join(module.channel_info['Sensor 3'].sensor_info.values()) + new_line

            string += ','.join(module.channel_info['Sensor 4'].sensor_info.keys()) + new_line
            string += ','.join(module.channel_info['Sensor 4'].sensor_info.values()) + new_line

        if log: print(string)
        return string

# TESTING
sc1 = Sensor_Individual.Sensor('S1', 0)
sc2 = Sensor_Individual.Sensor('S2', 0)
sc3 = Sensor_Individual.Sensor('S3', 0)
sc4 = Sensor_Individual.Sensor('S4', 0)
# sc5 = Sensor_Individual.Sensor('S5', 0)
# sc6 = Sensor_Individual.Sensor('S6', 0)
# sc7 = Sensor_Individual.Sensor('S7', 0)
# sc8 = Sensor_Individual.Sensor('S8', 0)
# sc9 = Sensor_Individual.Sensor('S9', 0)
# sc10 = Sensor_Individual.Sensor('S10', 0)
# sc11 = Sensor_Individual.Sensor('S11', 0)
# sc12 = Sensor_Individual.Sensor('S12', 0)
# sc13 = Sensor_Individual.Sensor('S13', 0)
# sc14 = Sensor_Individual.Sensor('S14', 0)
# sc15 = Sensor_Individual.Sensor('S15', 0)
# sc16 = Sensor_Individual.Sensor('S16', 0)
# sc17 = Sensor_Individual.Sensor('S17', 0)
# sc18 = Sensor_Individual.Sensor('S18', 0)
# sc19 = Sensor_Individual.Sensor('S19', 0)
# sc20 = Sensor_Individual.Sensor('S20', 0)
# sc21 = Sensor_Individual.Sensor('S21', 0)
# sc22 = Sensor_Individual.Sensor('S22', 0)
# sc23 = Sensor_Individual.Sensor('S23', 0)
# sc24 = Sensor_Individual.Sensor('S24', 0)
# sc25 = Sensor_Individual.Sensor('S25', 0)
# sc26 = Sensor_Individual.Sensor('S26', 0)
# sc27 = Sensor_Individual.Sensor('S27', 0)
# sc28 = Sensor_Individual.Sensor('S28', 0)
# sc29 = Sensor_Individual.Sensor('S29', 0)
# sc30 = Sensor_Individual.Sensor('S30', 0)
# sc31 = Sensor_Individual.Sensor('S31', 0)
# sc32 = Sensor_Individual.Sensor('S32', 0)
cc = Module_Individual.Module('mName', sc1, sc2, sc3, sc4)
daq = DAQ_Configuration.DAQconfigs()
sfm = Setting_File_Manager([cc,cc,cc,cc,cc,cc,cc,cc], sc1, daq)
# print(cc.channel_info)
# print(sc.sensor_info)
# print(daq.signal_configs)
# print(daq.testing_configs)
# print(daq.data_handling_configs)

# print(sfm.channel_config.channel_info)
# print(sfm.Sensor_config.sensor_info)
# print(sfm.daq_config.signal_configs)
# print(sfm.daq_config.testing_configs)
# print(sfm.daq_config.data_handling_configs)

filename = r'Default_Configuration.csv'  # Directory set in methods

# sfm.daq_config.specimen_location['1'] = 'Something ELse'

# sfm.store_daq_configs(filename)
# d = sfm.load_daq_configs(filename)
# print(d)

# for x in range(0, len(d), 1):
#     print(d[x])
# print('\n' + str(type(d[0])))

# sfm.store_module_configs(filename)
# print(sfm.load_module_config(filename).channel_info)
# print(verify_file_exists(filename))


# sfm.store_sensor_config(filename, [sc1, sc2, sc3, sc4, sc5, sc6, sc7, sc8, sc9, sc10, sc11, sc12, sc13, sc14, sc15, sc16,
#                                    sc17,sc18,sc19,sc20,sc21,sc22,sc23,sc24,sc25,sc26,sc27,sc28,sc29,sc30,sc31,sc32])
# print(sfm.load_sensor_config(filename))

# sfm.settings_to_string()