import os


def build_folder_structure(root_folder):
    """
        Builds a hierarchical representation of the folder structure containing files.

        This function recursively traverses through the provided root folder and its
        subfolders to construct a nested dictionary that represents the folder
        structure containing files. Subfolders and filenames are organized as keys
        within their respective parent folders.

        Args:
            root_folder (str): The path to the root folder for which to build the structure.

        Returns:
            dict: A nested dictionary representing the folder structure containing files.
                  The keys of the dictionary represent folder names, and subfolders
                  and filenames are organized as nested dictionaries within their
                  respective parent folders. Files are represented by 'None' values.

        Example:
            folder_structure = build_folder_structure('/path/to/your/folder')
            print(folder_structure)
        """
    folder_structure = {}

    for folder_name, subfolders, filenames in os.walk(root_folder):
        if filenames:
            folder_structure[folder_name] = {}
            for filename in filenames:
                folder_structure[folder_name][filename] = None

    return folder_structure


def build_folder_structure_all(root_folder):
    folder_structure = {}

    for folder_name, subfolders, filenames in os.walk(root_folder):
        subfolder_structure = {}

        for subfolder in subfolders:
            subfolder_structure[subfolder] = {}

        for filename in filenames:
            subfolder_structure[filename] = None

        folder_structure[folder_name] = subfolder_structure

    return folder_structure