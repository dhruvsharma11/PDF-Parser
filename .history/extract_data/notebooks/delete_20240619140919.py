import os
import shutil


def delete_files_in_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"The directory {directory} does not exist.")


def main():
    directories = [
        "../training_boxes/",
        "../boundary/",
        "../pdf_images/",
        "../dilate",
        "../results",
    ]
    for directory in directories:
        delete_files_in_directory(directory)
        print(f"All files in {directory} have been deleted.")


if __name__ == "__main__":
    main()
