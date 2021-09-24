import os
import swmmio
from shutil import copyfile

data_dir = "./data/"

def get_input_file_for_calc_settings(calculation_settings):
    input_file_name = ''
    input_file_name += calculation_settings["flow_path"]
    input_file_name += "_"
    input_file_name += calculation_settings["roofs"]
    input_file_name += "_"
    input_file_name += str(calculation_settings["return_period"])
    input_file_name += ".inp"

    return input_file_name


def make_inp_file(calculation_settings):
    # initialize a baseline model object
    #raise NotImplementedError("This feature is currently not implemented. We will see if it will ever get used")
    input_file = get_input_file_for_calc_settings(calculation_settings)

    #APPLICATION OF MODEL UPDATES IS A FEATURE THAT IS NOT YET DEVELOPED IN FRONT_END
    baseline = swmmio.Model(data_dir + 'input_files/' + input_file)
    # create a dataframe of the model's subcatchments
    subs = baseline.inp.subcatchments

    # reads updates to model from user input and updates the swmmio model
    for update in calculation_settings["model_updates"]:
        # update the outlet_id in the row of subcatchment_id

        subs.loc[update["subcatchment_id"], ['Outlet']] = update['outlet_id']
        baseline.inp.subcatchments = subs

    """
    #THIS IS NOW ALREADY INCLUDED IN THE  INDIVIDUAL INPUT FILES - but we might need this later.
    # set the rain gage from user input as raingage for all subcatchments
    scenario_rain_gage_name = 'RG' + '_' + str(calculation_settings["return_period"]) + 'yr'
    for i, row in subs.iterrows():
        subs.at[i, 'Raingage'] = scenario_rain_gage_name 
    """

    # Save the new model with the adjusted data
    new_file_path = data_dir + 'scenario.inp'
    baseline.inp.save(new_file_path)
    