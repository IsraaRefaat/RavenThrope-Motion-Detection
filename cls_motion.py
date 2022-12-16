# Author        : Esraa Refaat
# Python        : 3.10.8
# OS            : Windows 11 22H2
# OS Build      : 22621.819
import os
import re
import pandas as pd


class ClsMotion(object):
    def __init__(self, sheetPath):
        self.sheetPath = sheetPath

    def process_frames(self, framesPath):
        '''
        :param framesPath: the path for the directory which we store the frames in it.
        :return: dict_frame_time: A dictionary of dictionaries "the key: the frame's number,
         the value: the frame's name without extension"
        '''
        frames = os.listdir(framesPath)
        dict_frame_time = {}
        for fileName in frames:
            frame_second = re.findall(r'\d+', fileName)
            frame_time = float(frame_second[0])
            dict_frame_time[frame_time] = os.path.splitext(fileName)[0].replace(frame_second[0], '')
        self.get_motion_per_time(dict_frame_time)

    def get_motion_per_time(self, dict_frame_time):
        '''
        :param dict_frame_time: A dictionary of dictionaries "the key: the frame's number,
         the value: the frame's name without extension"
        :return: dict_pose_startTime, dict_pose_endTime, dict_pose_change
        '''

        head = 0
        leg = 1
        wing = 2
        tail = 3
        center = 0
        right = 1
        left = 2
        none = -1
        down = 0
        up = 1
        off = 0
        on = 1
        change = []
        dict_pose_change = {head: False, leg: False, wing: False, tail: False}
        dict_pose_startTime = {head: 0.0, leg: 0.0, wing: 0.0, tail: 0.0}
        dict_pose_endTime = {head: 0.0, leg: 0.0, wing: 0.0, tail: 0.0}
        list_of_sorted_keys = list(sorted(dict_frame_time))
        for index, cur_time in enumerate(sorted(dict_frame_time)):
            if len(dict_frame_time) - index == 1:
                break
            else:
                frame_curr = dict_frame_time[cur_time]
                time_next = list_of_sorted_keys[index + 1]
                frame_next = dict_frame_time[time_next]
                birds_curr = self.get_pose(frame_curr)
                birds_next = self.get_pose(frame_next)
                # if there is a diff create a new obj that contain a time
                diff = self.get_difference(birds_curr, birds_next)
                if diff is not None:
                    for birdPart in diff.keys():
                        if not dict_pose_change[birdPart]:
                            dict_pose_startTime[birdPart] = time_next
                            dict_pose_change[birdPart] = True
                        else:
                            dict_pose_endTime[birdPart] = time_next
                            dict_pose_change[birdPart] = False
                            delta = dict_pose_endTime[birdPart] - dict_pose_startTime[birdPart]
                            obj = ((dict_pose_startTime[birdPart], delta), birdPart)
                            change.append(obj)
        self.Data_frame(dict_frame_time, change)

    def get_difference(self, first_dict, second_dict):
        '''
        i.e. [{head:right , leg:up, tail:left , wing:on }]
        i.e. [{head:left , leg:down, tail:left , wing:on }]
        result will be   [{head:left , leg:down}]
        :param first_dict:
        :param second_dict:
        :return: dict of the differences like [{head:left , leg:down}]
        '''
        try:
            first_dict = set(first_dict.items())
            second_dict = set(second_dict.items())
            return dict(first_dict - second_dict)
        except:
            pass

    def get_pose(self, file_name):
        '''
        i.e. '{head:right , leg:up, tail:left , wing:on }'
        i.e. {head:right , leg:up, tail:left , wing:on }
        :param file_name: Dictionary in the string format
        :return: Dictionary in its format
        '''
        head = 0
        leg = 1
        wing = 2
        tail = 3
        center = 0
        right = 1
        left = 2
        none = -1
        down = 0
        up = 1
        off = 0
        on = 1

        # if we take just one name
        try:
            file_name_trimmed = file_name.replace('.', ':').replace('_', ',').lower()
            file_name_trimmed = ('{%s}' % file_name_trimmed)
            file_name_trimmed = eval(file_name_trimmed)
            return file_name_trimmed
        except:
            pass

    def Data_frame(self, file_name, change):
        '''
        :param file_name: the bird pose
        :return: make Excel Sheet has the bird pose
        '''
        head = 0
        leg = 1
        wing = 2
        tail = 3
        center = 0
        right = 1
        left = 2
        none = -1
        down = 0
        up = 1
        off = 0
        on = 1
        # if we take a list
        # i.e. [{head:right , leg:up, tail:left , wing:on }]
        # convert the input string into the above format
        list_of_sorted_keys = list(sorted(file_name))
        birds = []

        try:
            for name in list_of_sorted_keys:
                file_name_trimmed = file_name[name].replace('.', ':').replace('_', ',').lower()
                # ('%f+i%f' % (r.real, r.image))
                file_name_trimmed = ('{%s}' % file_name_trimmed)
                file_name_trimmed = eval(file_name_trimmed)
                birds.append(file_name_trimmed)
        except:
            pass

        FinalResult = pd.DataFrame(birds)
        FinalResult["change"] = pd.Series(change)
        FinalResult.columns = ["Head", "Leg", "Wing", "Tail", "Movement_Record"]
        print(FinalResult)
        FinalResult.to_excel(excel_writer=self.sheetPath, sheet_name="sheet1",
                             index_label=["Time"])



if __name__ == '__main__':
    ob = ClsMotion(r"E:\D.Hussien's Project\sheet1.xlsx")      #  sheet path
    ob.process_frames(r"E:\D.Hussien's Project\Labelaing")     #  frames path 
