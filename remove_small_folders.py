from pathlib import Path
import os
import shutil
import sys

# if anyone wants to automate the whole process, (e.g. piping outputs,etc.) set the above value to True


data = {"folders_searched": 0, "folders_flagged": 0, "folders_moved": 0, "files_searched": 0, "files_moved": 0,
        "folders_deleted": 0}

# ^ is used for end of script metric list
# not super important but I felt like adding it

settings = {"root_path": "path", "threshold": 0, "prompt_override": True, "folders_get_prefixed": False,
            "files_get_prefixed": False}


# I left the threshold value in the global dict in case anyone felt like tweaking it for some possibly insane (imo) file management
# threshold determines the maximum number of files or folders inside a parent folder before the parent folder gets deleted
# the higher the threshold value, the less items need to be in a folder before the folder gets removed by the script


def menu():
    print("###################################")
    print("The current file is " + os.path.basename(__file__))
    print("The current file is located (and will run) at " + os.getcwd())
    print("The dependencies of this script are all part of the python standard library,")
    print("so it should be executable from anywhere, provided python has been installed correctly on the host device.")
    print()
    print("This script will find any folders containing less than " + str(settings["threshold"]) + " files or folders")
    print("It will then the contents of said folder into the parent of said folder, then delete said folder.")
    print("Would you like a better explanation of what this script does?")

    if confirm():
        print("https://github.com/M-T-1/remove-small-folders/README.md")

    clear()
    print()
    print("Please confirm you wish to proceed.")
    print("The script will list all the folders that will be removed.")
    print("The script will then prompt for confirmation, ")
    print("relocate the contents of the folders and then delete the folders altogether.")
    print("THERE IS NO UNDO BUTTON")
    print(
        "If you want to undo the actions of this script, you can write a script to replace the dashes in the file-names with backslashes. ")
    print(
        "I hope you have success in any attempt to create a script to do this because I currently have no intention of making one.")
    if not confirm():
        clear()
        print("runtime cancelled by user")
        sys.exit()
    print("#####")
    clear()


def main():
    # run menu
    menu()
    subdirectories = []
    print("Your current location is: " + os.getcwd())
    while not os.path.exists(settings["root_path"]):
        print("enter path\n")
        settings["root_path"] = input()
    print("Settings value preset to: " + settings["root_path"])
    # testing paths
    # settings["root_path"] = Path("T:" + chr(92) + "###x" + chr(92))
    # settings["root_path"] = Path("T:" + chr(92))
    # print(settings["root_path"].parent)
    for dir_path, dirs, files in os.walk(settings["root_path"], topdown=True):
        for name in dirs:
            data["folders_searched"] += 1
            # used to stop SVI folders from being included, they can't be read, the script will throw access denied errs
            if ("System Volume Information" not in name) & ("$RECYCLE.BIN" not in name):
                subdirectories.append(os.path.join(dir_path, name) + chr(92))
    # sort subdirectories to make output easier to follow
    subdirectories.sort(key=len, reverse=True)
    # lists all subdirectories
    # for s in subdirectories:
    # print(s)
    # pre-allocating variable name for removable subdirectory list

    removable_subdirectories = []
    for s in subdirectories:
        x = 0
        for _ in os.listdir(s):
            if os.path.isdir(_):
                data["folders_searched"] += 1
            else:
                data["files_searched"] += 1
            x += 1
        if x <= settings["threshold"]:
            print("- - - -")
            print("Directory : " + s)
            print("Object count : " + str(x))
            print("All Objects will be moved to parent : " + str(Path(s).parent))
            removable_subdirectories.append(s)
    # sort directories
    removable_subdirectories.sort(key=len, reverse=True)
    # for each folder in removable-subdirectories (is a root, contents need moving up)
    print("#####")
    print("Above is a list of the folders  that will be removed (and a count of their contents)")
    print("Please confirm you wish to proceed. Any changes made after this point cannot be reversed.")
    print("THERE IS NO UNDO BUTTON")
    if not confirm():
        print("runtime cancelled by user")
        sys.exit()
    print("#####")

    for f in removable_subdirectories:
        for temp in os.scandir(f):
            if temp.is_dir():
                print("Source: " + temp.path)

                if settings["folders_get_prefixed"]:
                    print("Destination: " + str(Path(f).parent) + chr(92) + Path(temp).parent.name + "-" + str(
                        Path(temp).name))
                    shutil.move(temp.path,
                                str(Path(f).parent) + chr(92) + Path(temp).parent.name + "-" + str(Path(temp).name))
                else:
                    print("Destination: " + str(Path(f).parent))
                    shutil.move(temp.path, str(Path(f).parent) + chr(92) + str(Path(temp).name))
                data["folders_moved"] += 1
                print("moved the contents of " + str(Path(f)) + " moved to " + str(Path(f).parent))
            else:
                # moves individual files
                print("Source: " + temp.path)

                data["files_moved"] += 1
                if settings["files_get_prefixed"]:
                    print("Destination: " + str(
                        Path(str(Path(f).parent) + chr(92) + Path(temp).parent.name + "-" + str(Path(temp).name))))
                    shutil.move(temp.path,
                                Path(str(Path(f).parent) + chr(92) + Path(temp).parent.name + "-" + str(
                                    Path(temp).name)))
                else:
                    print("Destination: " + str(
                        Path(str(Path(f).parent) + chr(92) + str(Path(temp).name))))
                    shutil.move(temp.path,
                                Path(str(Path(f).parent) + chr(92) + str(
                                    Path(temp).name)))
        # remove empty directory
        data["folders_deleted"] += 1
        os.rmdir(Path(f))
        print("Directory \"" + str(f) + "\" has been emptied and removed")
        # separator line
    for _ in range(0, 50):
        print()
    # end of operation, time to print stats and results:
    runtime_stats()


def runtime_stats():
    print("###################################")
    print("Runtime Data:")
    print("This script is " + os.path.basename(__file__))
    print("The root path for folder alteration is " + str(settings["root_path"]))
    print("For a folder to be deleted, it must contain less than " + str(settings["threshold"] + 1) + " items")
    print(str(data["folders_searched"]) + " folder(s) have been indexed during runtime")
    print(str(data["files_searched"]) + " file(s) have been indexed during runtime")
    print()
    print(str(data["folders_deleted"]) + " folder(s) have been deleted during runtime")
    print(" - the contents of these folders have been moved prior to deletion")
    print(" -- " + str(data["folders_moved"]) + " folder(s) have been moved during runtime")
    print(" -- " + str(data["files_moved"]) + " file(s) have been moved during runtime")
    print("End Of Script")


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def confirm():
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    # global override value for non-interactive running (e.g. for piping outputs,etc.)
    if settings["prompt_override"]:
        answer = "y"
    while answer not in ["y", "n"]:
        answer = input("[Y/N]? ").lower()
    return answer == "y"


if __name__ == "__main__":
    main()
