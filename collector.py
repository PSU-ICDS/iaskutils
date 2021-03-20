import os
import subprocess
import shutil
import glob
import click
from progress.bar import Bar
from utils.special_print import print_good
from utils.special_print import print_bad
from utils.special_print import print_info
from utils.special_print import important_info
from utils.compression import Compression

# Global variables
home_env_var = os.getenv('HOME')
user_name = os.getenv('USER')


# Open file and write its output in the same directory
def readfile(path, filename):
    fin = open(path, "rt")
    content = fin.read()
    fin.close()
    fout = open(filename, "wt")
    fout.write(content)
    fout.close()


@click.command()
@click.option("-V", "--version", is_flag=True, help="Print version info.")
@click.option("--license", is_flag=True, help="Print licensing info.")
@click.option("-c", "--compression", type=click.Choice(["gzip", "bz2", "xz", "tar", "zip"]),
              default="zip", help="Compression algorithm to use (default: zip).")
@click.option("-d", "--directory", default="{}/scratch".format(home_env_var),
              help="Directory to save output to (default: ~/scratch).")
def collector(version, license, compression, directory):
    """collector: A simple script to collect information about your environment."""
    if version:
        click.echo("collector v1.1  Copyright (C) 2021  Jason C. Nucciarone \n\n"
                   "This program comes with ABSOLUTELY NO WARRANTY; \n"
                   "for more details type \"collector --license\". This is free software, \n"
                   "and you are welcome to redistribute it under certain conditions; \n"
                   "go to https://www.gnu.org/licenses/licenses.html for more details.")

    elif license:
        click.echo("""collector: A simple script to collect information about your environment.\n
    Copyright (C) 2021  Jason C. Nucciarone

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.""")

    else:
        # Change into directory specified by user to create $USER_info
        try:
            os.chdir(directory)

        except OSError:
            print_bad("Something went wrong when trying to change into {} ".format(directory) +
                      "Please contact i-ASK center at iask@ics.psu.edu.")
            exit()

        # Create $USER_info directory and then change into it
        user_info = "{}_info".format(user_name)
        full_path_to_dir = os.getcwd()

        try:
            os.mkdir(user_info)
            os.chdir(user_info)

        except FileExistsError:
            shutil.rmtree(user_info)
            os.mkdir(user_info)
            os.chdir(user_info)

        # Start gathering info on user's environment
        files_of_interest = [".bashrc", ".bash_history", ".bash_profile", ".bash_logout", ".bash_aliases",
                             "config.fish", ".cshrc", ".history", ".tcshrc", ".zshrc"]

        # Loop through each file of interest
        # .bashrc
        if os.path.isfile("{}/{}".format(home_env_var, files_of_interest[0])):
            readfile("{}/{}".format(home_env_var, files_of_interest[0]), "bashrc-{}.txt".format(user_name))
            print_good("Read .bashrc file at {}/{}".format(home_env_var, files_of_interest[0]))

        else:
            print_info("Did not find any .bashrc file")

        # .bash_history
        if os.path.isfile("{}/{}".format(home_env_var, files_of_interest[1])):
            readfile("{}/{}".format(home_env_var, files_of_interest[1]), "bash_history-{}.txt".format(user_name))
            print_good("Read .bash_history file at {}/{}".format(home_env_var, files_of_interest[1]))

        else:
            print_info("Did not find any .bash_history file")

        # .bash_profile
        if os.path.isfile("{}/{}".format(home_env_var, files_of_interest[2])):
            readfile("{}/{}".format(home_env_var, files_of_interest[2]), "bash_profile-{}.txt".format(user_name))
            print_good("Read .bash_profile file at {}/{}".format(home_env_var, files_of_interest[2]))

        else:
            print_info("Did not find any .bash_profile file")

        # .bash_logout
        if os.path.isfile("{}/{}".format(home_env_var, files_of_interest[3])):
            readfile("{}/{}".format(home_env_var, files_of_interest[3]), "bash_logout-{}.txt".format(user_name))
            print_good("Read .bash_logout file at {}/{}".format(home_env_var, files_of_interest[3]))

        else:
            print_info("Did not find any .bash_logout file")

        # .bash_aliases
        if os.path.isfile("{}/{}".format(home_env_var, files_of_interest[4])):
            readfile("{}/{}".format(home_env_var, files_of_interest[4]), "bash_aliases-{}.txt".format(user_name))
            print_good("Read .bash_aliases file at {}/{}".format(home_env_var, files_of_interest[4]))

        else:
            print_info("Did not find any .bash_aliases file")

        # config.fish
        if os.path.isfile("{}/{}".format(home_env_var, files_of_interest[5])):
            readfile("{}/.config/fish/{}".format(home_env_var, files_of_interest[5]),
                     "config.fish-{}.txt".format(user_name))
            print_good("Read config.fish file at {}/{}".format(home_env_var, files_of_interest[5]))

        else:
            print_info("Did not find any config.fish file")

        # .cshrc
        if os.path.isfile("{}/{}".format(home_env_var, files_of_interest[6])):
            readfile("{}/{}".format(home_env_var, files_of_interest[6]), "cshrc-{}.txt".format(user_name))
            print_good("Read .cshrc file at {}/{}".format(home_env_var, files_of_interest[6]))

        else:
            print_info("Did not find any .cshrc file")

        # .history
        if os.path.isfile("{}/{}".format(home_env_var, files_of_interest[7])):
            readfile("{}/{}".format(home_env_var, files_of_interest[7]), "history-{}.txt".format(user_name))
            print_good("Read .history file at {}/{}".format(home_env_var, files_of_interest[7]))

        else:
            print_info("Did not find any .history file")

        # .tcshrc
        if os.path.isfile("{}/{}".format(home_env_var, files_of_interest[8])):
            readfile("{}/{}".format(home_env_var, files_of_interest[8]), "tcshrc-{}.txt".format(user_name))
            print_good("Read .tcshrc file at {}/{}".format(home_env_var, files_of_interest[8]))

        else:
            print_info("Did not find any .tcshrc file")

        # .zshrc
        if os.path.isfile("{}/{}".format(home_env_var, files_of_interest[9])):
            readfile("{}/{}".format(home_env_var, files_of_interest[9]), "zshrc-{}.txt".format(user_name))
            print_good("Read .zshrc file at {}/{}\n".format(home_env_var, files_of_interest[9]))

        else:
            print_info("Did not find any .zshrc file\n")

        # Change into home directory and gather info about environment
        output_dir = os.getcwd()
        os.chdir(home_env_var)
        commands = ["check_aci_storage_quota", "ls -lha", "du -h --max-depth=1", "env"]

        bar = Bar("Collecting info on environment", max=len(commands))
        for command in commands:
            fout = open("{}/env_info-{}.txt".format(output_dir, user_name), "at")
            fout.write("\n\n#" + command + "\n\n")
            fout.close()
            subprocess.call("{} >> {}/env_info-{}.txt".format(command, output_dir, user_name), shell=True)
            bar.next()

        bar.finish()

        # Combine all the files in $USER_info together
        os.chdir(output_dir)
        text_files = glob.glob("*.txt")
        bar = Bar("Creating cumulative file", max=len(text_files))
        for text in text_files:
            fin = open(text, "rt")
            tmp = fin.read()
            fin.close()
            fout = open("all_info-{}.txt".format(user_name), "at")
            fout.write("# {}\n\n".format(text))
            fout.write(tmp + "\n\n")
            fout.close()
            bar.next()

        bar.finish()

        # Compress the $USER_info dir into an archive
        os.chdir(full_path_to_dir)
        compress_dir = output_dir.split("/")
        archive = Compression(compress_dir[-1], user_info, full_path_to_dir)

        if compression == "gzip":
            archive.togzip()

        elif compression == "bz2":
            archive.tobzip()

        elif compression == "xz":
            archive.toxz()

        elif compression == "tar":
            archive.totar()

        elif compression == "zip":
            archive.tozip()

        else:
            print_bad("There was an issue compressing your files! Please contact the i-ASK center at " +
                      "iask@ics.psu.edu")
            exit()

        # Wrap up and clean up
        print("\n" + archive.complete)
        shutil.rmtree(output_dir)


if __name__ == "__main__":
    collector()
