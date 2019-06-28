import os
import shutil
import logging
import tkinter as tk
from tkinter import filedialog

def extract_vdirs(model_results_path):
    """
    Extracts velocity direction rasters from Tuflow output data.
    Output rasters are saved in this script directory in ASCII format.
    Velocity direction in degrees from North: e.g. North = 0, East=90, West=-90, South=180/-180
    """
    script_dir = os.path.dirname(__file__)
    r2r_path = os.path.join(script_dir, "res_to_res\\res_to_res_w64.exe")
    t2g_path = os.path.join(script_dir, "tuflow_to_gis\\TUFLOW_to_GIS_w64.exe")

    for run in os.listdir(model_results_path):
        run_dir = os.path.join(model_results_path, run)
        for run_file in os.listdir(run_dir):
            if run_file.endswith(".xmdf"):

                out_file_name = run_file.replace(".xmdf", "_V_dir")
                data_path = os.path.join(run_dir, run_file)

                logging.info(">>> Converting:")
                logging.info("\t>>> Input: %s" % data_path)
                logging.info("\t>>> Output: %s\n" % out_file_name)

                logging.info(">>> Getting timesteps...")
                # -times: get times
                os.system("%s -b -times -typeV %s" % (r2r_path, data_path))
                # determine final timestep value
                with open(os.path.join(script_dir, "times.txt"), "r") as f:
                    content = f.readlines()
                    times = [float(val) for val in content]
                    max_time = max(times)
                logging.info(">>> OK.\n>>> Using final time t=%s" % str(max_time))

                logging.info(">>> Extracting velocity data from .xmdf, converting to .dat...")
                # -conv: convert to .dat
                os.system("%s -b -typeV -conv %s" % (r2r_path, data_path))
                logging.info(">>> OK.")

                logging.info(">>> Extracting vector angles at time %s..." % str(max_time))
                # -va: get vector angles
                in_v_dat = os.path.join(run_dir, run_file.replace(".xmdf", "_v.dat"))
                os.system("%s -b -va -t%s %s" % (r2r_path, str(max_time), in_v_dat))
                logging.info(">>> OK.")

                logging.info(">>> Copying .2dm data...")
                # make copy of .2dm to match velocity data name so SMS can find it
                path_2_2dm = data_path.replace(".xmdf", ".2dm")
                copy_2dm = path_2_2dm.replace(".2dm", "_v.2dm")
                if not os.path.exists(copy_2dm):
                    shutil.copy(path_2_2dm, copy_2dm)
                logging.info(">>> OK.")

                logging.info(">>> Converting to ASCII output...")
                # -asc: convert to ascii data
                in_va = os.path.join(run_dir, run_file.replace(".xmdf", "_v_va.dat"))
                os.system("%s -b -asc %s -out %s" % (t2g_path, in_va, out_file_name))
                logging.info(">>> OK.")

    logging.info(">>> Finished! :)")


# opens window in GUI to browse for folder or file
def browse(root, entry, select='file', ftypes=[('All files', '*')]):
    """GUI button command: opens browser window and adds selected file/folder to entry"""
    if select == 'file':
        filename = filedialog.askopenfilename(parent=root, title='Choose a file', filetypes=ftypes)
        if filename != None:
            entry.delete(0, tk.END)
            entry.insert(tk.END, filename)

    elif select == 'files':
        files = filedialog.askopenfilenames(parent=root, title='Choose files', filetypes=ftypes)
        l = root.tk.splitlist(files)
        entry.delete(0, tk.END)
        entry.insert(tk.END, l)

    elif select == 'folder':
        dirname = filedialog.askdirectory(parent=root, initialdir=entry.get(), title='Choose a directory')
        if len(dirname) > 0:
            entry.delete(0, tk.END)
            entry.insert(tk.END, dirname + '/')


if __name__ == "__main__":

    # initialize logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="logfile.log", filemode='w', level=logging.INFO)
    stderrLogger = logging.StreamHandler()
    stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    logging.getLogger().addHandler(stderrLogger)

    # initialize GUI
    root = tk.Tk()
    root.wm_title("Extract Tuflow Velocity Direction Rasters")

    L1 = tk.Label(root, text="Tuflow Model Results Directory: ")
    L1.grid(sticky=tk.W, row=0, column=0)
    E1 = tk.Entry(root, bd=5)
    E1.grid(row=0, column=1)
    B1 = tk.Button(root, text='Browse',
                   command=lambda: browse(root, E1, select='folder', ftypes=[('Comma-delimited text', '.csv'),
                                                                             ('All files', '*')]
                                          )
                   )
    B1.grid(sticky=tk.W, row=0, column=2)

    B2 = tk.Button(root, text="\tCreate Velocity Direction Rasters\t",
                   command=lambda: extract_vdirs(E1.get()))
    B2.grid(sticky=tk.W, row=1, column=0, columnspan=3)

    root.mainloop()
