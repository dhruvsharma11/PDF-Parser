import os


def check_file_names(folder1, folder2):
    # Get the list of files in each folder
    files1 = {
        os.path.splitext(f)[0] for f in os.listdir(folder1) if f.endswith(".jpeg")
    }
    files2 = {os.path.splitext(f)[0] for f in os.listdir(folder2) if f.endswith(".txt")}

    # Find files that are in folder1 but not in folder2
    missing_in_folder2 = files1 - files2
    # Find files that are in folder2 but not in folder1
    missing_in_folder1 = files2 - files1

    return missing_in_folder1, missing_in_folder2


# Replace these with the paths to your folders
folder1 = "../../train_model/data/images/val"
folder2 = "../../train_model/data/labels/val"

missing_in_folder1, missing_in_folder2 = check_file_names(folder1, folder2)

if missing_in_folder1:
    print(f"Files in {folder2} but not in {folder1}:")
    for file in missing_in_folder1:
        print(file + ".txt")

if missing_in_folder2:
    print(f"Files in {folder1} but not in {folder2}:")
    for file in missing_in_folder2:
        print(file + ".jpeg")

if not missing_in_folder1 and not missing_in_folder2:
    print("All files match between the two folders.")
