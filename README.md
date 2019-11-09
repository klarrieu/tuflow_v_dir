# Extract Velocity Direction Rasters from Tuflow Output
Extracts direction of velocity vectors from Tuflow outputs.

This script works on Windows machines with a standard installation of Python. It utilizes [executable Tuflow utilities `RES_to_RES` and `TUFLOW_to_GIS`](https://www.tuflow.com/FV%20All%20Download.aspx).

## Use

1. Download or clone this repository.
2. Run the `extract_vdir.py` script. This will open a GUI.
3. Use the GUI to select the directory containing the target Tuflow run results, e.g. for Tuflow run number `21` the `\results\21\` directory should be selected. (One output raster is produced for each subdirectory/run, using the last timestep of each run.)
4. Press the big button (`Create Velocity Direction Rasters`) and be patient. Progress will be printed out to the command line as well as a logfile in the directory of this repository.

## Outputs

Output rasters are saved to the same directory as the `extract_vdir.py` script in the ASCII format, using the same name convention as the corresponding Tuflow run with a suffix `_V_dir.asc`.

**Note**: Velocity direction in degrees from North: e.g. North = 0, East=90, West=-90, South=180/-180.

## Viewing Velocity Vectors in ArcGIS Pro

https://pro.arcgis.com/en/pro-app/help/data/imagery/vector-field-function.htm

ArcGIS Pro -> Imagery tab -> Raster Functions -> Raster Functions (opens on the right) -> Conversion -> Vector Field

Select:

Raster 1 = magnitude, Raster 2 = direction

Input Data Type = Magnitude-Direction-Input

Angular Reference System = Geographic

Output Data Type = whatever is suitable
