import os
import shutil

##################################################
# Some variables you can use for the paths below #
##################################################
project_directory = os.path.dirname(os.path.realpath(__file__))

###########################################################################
#                 Change those variables if you need to.                  #
#  src_path is the path that contains your source assets (e.g. psd files) #
#  build_path is the directory that will contain your built files (png)   #
###########################################################################
src_path = f"{project_directory}/src"
build_path = f"{project_directory}/assets"


#####################
# Utility functions #
#####################

# Installs the given package if it isn't installed
def install_pkg(package_name: str, import_name: str):
    import importlib, subprocess, sys
    try:
        importlib.import_module(import_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


# Converts in_file (psd) to out_file (png)
def convert_psd(in_file: str, out_file: str):
    if not in_file.endswith(".psd") or not out_file.endswith(".png"):
        return
    # Here, a few lines might error out in your IDE. This is fine, since PILLOW is installed at runtime
    from PIL import Image
    with Image.open(in_file) as img:
        img.save(out_file)
        print(f"Built psd '{in_file}' to '{out_file}'")


###############
# MAIN SCRIPT #
###############

# Install pillow if missing, required to convert psd files
install_pkg("pillow", "PIL")

# Making sure the Source path exists
if not os.path.exists(src_path):
    print("[Error] Could not find source folder 'src', exiting...")
    exit(1)

# (Re)create build directory.
if os.path.exists(build_path):
    shutil.rmtree(build_path, ignore_errors=True)
os.makedirs(build_path)

# Build psd files
for root, dirs, files in os.walk(src_path):
    for file in files:
        src_file = os.path.join(root, file)
        rel_path = os.path.relpath(src_file, src_path)
        dest_file = os.path.join(build_path, os.path.splitext(rel_path)[0] + ".png")
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        convert_psd(src_file, dest_file)

print("Done!")
