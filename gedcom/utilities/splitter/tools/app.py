import PySimpleGUI as sg

from gedcom.utilities.splitter.splitter import Splitter
from gedcom.element.individual import IndividualElement

import os

class View(sg.Window):

    def __init__(self):

        layout = [[sg.T("1. Choose the GEDCOM file:")], 
                  [sg.Input(key="-INPUT-FILE2-" ,change_submits=False, size=(50, 1)), sg.FileBrowse(key="-INPUT-FILE-"), sg.Button("Load")],
                  [sg.T("2. Choose the root ancestor:")],
                  [sg.Input(size=(70, 1), enable_events=True, key='-INPUT-FILTER-', disabled=True)],
                  [sg.Listbox(values=[], enable_events=True, select_mode='single', key='-LISTBOX-ROOT-', size=(70, 6), disabled=True)],
                  [sg.T("3. Select output folder:")],
                  [sg.Input(key="-OUTPUT-FOLDER-" ,change_submits=False, size=(58, 1), disabled=True), sg.FolderBrowse(key="-OU-", disabled=True)],
                  [sg.T("4. Select output file name:")],
                  [sg.Input(key="-OUTPUT-FILE-", change_submits=False, size=(58, 1), disabled=True)],
                  [sg.Push(), sg.Button("Reset", disabled=True), sg.Button("Submit", disabled=True), sg.Push()],
                  [sg.Frame(title="Progress", layout=
                            [[sg.Push(), sg.Text('Status', key="-PROGRESS-TEXT-"), sg.Push()],
                             [sg.ProgressBar(100, orientation='h', size=(45,20), key='-PROG-BAR-')]])]]

        super().__init__("GEDCOM Splitter", layout, size=(500, 460))

        self.controller = None
        
    def set_controller(self, controller):
        
        self.controller = controller

class Controller:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.event_listener_running = True
        
        while True:
            event, values = view.read()
            
            if event == sg.WINDOW_CLOSED:
                break

            if event == 'Load':
                self.load_button_clicked(values['-INPUT-FILE2-'])
            
            if event == 'Submit':
                self.submit_button_clicked(values)
            
            if event == 'Reset':
                self.reset_button_clicked()

            if event == '-INPUT-FILTER-' and values['-INPUT-FILTER-'] != '':                         # if a keystroke entered in search field
                new_list = self.model.get_filter_person_list(values['-INPUT-FILTER-'])
                self.view['-LISTBOX-ROOT-'].update(new_list)     # display in the listbox

        view.close()
        
    def load_button_clicked(self, filename):
    
        if len(filename) == 0:
            sg.popup("Please select a file",title="Error")
        else:
            for x in ['-INPUT-FILTER-', '-LISTBOX-ROOT-', '-OUTPUT-FOLDER-', '-OUTPUT-FILE-', '-OU-', 'Submit', 'Reset']:
                self.view[x].update(disabled=False)
            
            self.model.load_file(filename, self.update_progress)
            
            self.view['-LISTBOX-ROOT-'].update(self.model.get_person_list())
            self.view["-OUTPUT-FOLDER-"].update(os.path.dirname(os.path.realpath(filename)))
            
            filename = os.path.basename(os.path.realpath(filename)).split('.')
            
            self.view["-OUTPUT-FILE-"].update(filename[0] + "_split.ged")
            

    def submit_button_clicked(self, values):

        if len(values['-INPUT-FILE2-']) == 0:
            sg.popup("Please select a file",title="Error")
        elif len(values['-LISTBOX-ROOT-']) == 0:
            sg.popup("Please select a root ancestor",title="Error")
        elif len(values['-OUTPUT-FOLDER-']) == 0:
            sg.popup("Please select an output folder",title="Error")
        elif len(values['-OUTPUT-FILE-']) == 0:
            sg.popup("Please select an output file name",title="Error")
        else:
            output_file = values['-OUTPUT-FOLDER-'] + "\\" + values['-OUTPUT-FILE-']
            
            self.model.split_and_save_file(values['-LISTBOX-ROOT-'], output_file, self.update_progress)
            self.update_progress("Complete", 1, 1)
            
            sg.popup("Complete",title="Success")
        
            self.reset_button_clicked()
            
            for x in ['-INPUT-FILTER-', '-LISTBOX-ROOT-', '-OUTPUT-FOLDER-', '-OUTPUT-FILE-', '-OU-', 'Submit', 'Reset']:
                self.view[x].update(disabled=True)

            self.update_progress("", 0, 1)


    def reset_button_clicked(self):
        
        self.view['-INPUT-FILE2-'].update('')
        self.view['-INPUT-FILTER-'].update('')
        self.view['-LISTBOX-ROOT-'].update([])
        self.view['-OUTPUT-FOLDER-'].update('')
        self.view['-OUTPUT-FILE-'].update('')
        
    def update_progress(self, message, progress, progress_total):
        self.view['-PROGRESS-TEXT-'].update(message)
        self.view['-PROG-BAR-'].update(progress / progress_total * 100)
        
        
class Model:
    
    def __init__(self):
        self.person_list = []
        self.parser = Splitter()
        
    def get_person_list(self):
        return self.person_list
    
    def get_filter_person_list(self, search):
        new_values = [x for x in self.get_person_list() if search in x]  # do the filtering
        
        return new_values
        
    def load_file(self, filename, progress_callback):

        self.parser.parse_file(filename, callback=progress_callback)
        
        self.person_list = []

        for element in self.parser.get_root_child_elements():
            if isinstance(element, IndividualElement):
                person = element.get_name()[1] + ", " + element.get_name()[0] + " ("
                if element.get_birth_year() > 0:
                    person += str(element.get_birth_year())
                else:
                    person += "?"
                    
                person += " - "

                if element.get_death_year() > 0:
                    person += str(element.get_death_year())
                
                person += ")"
                self.person_list.append(person)
        
        self.person_list.sort()

    def split_and_save_file(self, ancestor, file_name, progress_callback):
        
        temp = ancestor[0].split(", ")
        criteria = "surname=" + temp[0]
        
        temp = temp[1].split(" (")
        criteria += ":given_name=" + temp[0]
        
        temp = temp[1].split("-")
        if len(temp[0].strip()) > 0:
            criteria += ":birth=" + str(temp[0].strip())
            
        if len(temp[1][0:-1].strip()) > 0:
            criteria += ":death=" + str(temp[1][0:-1].strip())
        
        individual = self.parser.find_person(criteria)
        
        self.parser.split_gedcom(individual, True, progress_callback)        
        self.parser.write_file(file_name, progress_callback)
        
class App:
    
    def __init__(self):

        view = View()
        model = Model()
        controller = Controller(model, view)
        
        view.set_controller(controller)
        
if __name__ == "__main__":
    app = App()
    
    
    