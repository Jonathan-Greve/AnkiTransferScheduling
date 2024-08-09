# Thanks to Shigeyuki for the script
import os
import zipfile
from datetime import datetime

def create_ankiaddon():
    current_dir = os.getcwd()
    current_dir_name = os.path.basename(os.path.normpath(current_dir))
    today = datetime.today().strftime('%Y%m%d')
    extension = ".ankiaddon"
    #extension = ".zip" # to check, for easy access by the file explorer
    zip_fixed_name = "addon.zip"
    zip_final_name = f'{current_dir_name}_{today}{extension}'

    # Exclusions
    exclude_dirs = ['__pycache__', '.vscode', ".git"]
    exclude_exts = ['.ankiaddon', ".swp"]
    exclude_files = ['meta.json', zip_fixed_name, ".gitignore", "anki_France_demo_S_Allain.gif", "anki_Parcs_demo_S_Allain.gif", "anki_pnr_demo_S_Allain.gif"]

    # Make zip
    with zipfile.ZipFile(zip_fixed_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(current_dir):
            # 除外するﾌｫﾙﾀﾞを除外
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                # 指定したﾌｧｲﾙ名と拡張子を除外
                if file not in exclude_files and os.path.splitext(file)[1] not in exclude_exts:
                    zipf.write(os.path.join(root, file),
                                os.path.relpath(os.path.join(root, file),
                                                current_dir))  # 親ﾃﾞｨﾚｸﾄﾘ名を除去

    # Ankiweb requires the zip to have .ankiaddon extension
    print("Rename " + str(zip_fixed_name) + " as " + str(zip_final_name))
    os.rename(zip_fixed_name, zip_final_name)

# Launch
create_ankiaddon()
