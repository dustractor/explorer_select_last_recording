
import obspython as obs
import datetime
import pathlib
import subprocess

class Data:
    OutputDir = None
    Extension = None

def frontend_event_handler(data):
    if data == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        path = pathlib.Path(Data.OutputDir)
        if path.exists():
            now_ts = datetime.datetime.now()
            if Data.Extension:
                dirlist = filter(
                    lambda _:str(_).endswith(Data.Extension),
                    path.iterdir())
            else:
                dirlist = path.iterdir()
            t = None
            for t in sorted([(
                    ( now_ts-datetime.datetime.fromtimestamp(_.stat().st_mtime)
                     ).total_seconds(),_) for _ in dirlist]):
                break
            if t:
                ign,thefile = t
                print(thefile)
                subprocess.run('explorer /select,"%s"'%str(thefile))
        return True

def script_update(settings):
    Data.OutputDir = obs.obs_data_get_string(settings,"outputdir")
    Data.Extension = obs.obs_data_get_string(settings,"extension")

def script_description():
    return ("Choose the folder where recordings are saved."
        " When recording is stopped, the most-recent file"
            " will be shown selected in Windows Explorer."
            " (Leave blank the extension field to always"
            " select a file, or set to a non-existant"
            " extension to never select a file.)")

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_path(
        props, "outputdir", "Recordings folder", obs.OBS_PATH_DIRECTORY,
        None, str(pathlib.Path.home()))
    obs.obs_properties_add_text(
        props,"extension","File extension",obs.OBS_TEXT_DEFAULT)
    return props

obs.obs_frontend_add_event_callback(frontend_event_handler)

