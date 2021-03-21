import os
import shutil
import click
from utils.special_print import print_good
from utils.special_print import print_bad
from utils.special_print import print_info
from utils.special_print import important_info
from utils.compression import Compression


@click.command()
@click.option("-V", "--version", is_flag=True, help="Print version info.")
@click.option("--license", is_flag=True, help="Print licensing info.")
def main(version, license):
    """relinkworkscratch: A simple script to reestablish the work and scratch directory symlinks in a user's home directory."""
    if version:
        click.echo("relinkworkscratch v1.1  Copyright (C) 2021  Jason C. Nucciarone \n\n"
                   "This program comes with ABSOLUTELY NO WARRANTY; \n"
                   "for more details type \"relinkworkscratch --license\". This is free software, \n"
                   "and you are welcome to redistribute it under certain conditions; \n"
                   "go to https://www.gnu.org/licenses/licenses.html for more details.")

    elif license:
        click.echo("""relinkworkscratch: A simple script to reestablish the work and scratch directory symlinks in a user's home directory.\n
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
        # Grab important info for system
        home_env_var = os.getenv('HOME')
        user_name = os.getenv('USER')
        work_dir = "/storage/work/{}".format(user_name)
        scratch_dir = "/gpfs/scratch/{}".format(user_name)

        # Verify that user work and scratch directories exist
        if os.path.isdir(work_dir) is False:
            print_bad("Hm. It looks like {} does not exist. Please contact the i-ASK center for help.".format(work_dir))
            return

        if os.path.isdir(scratch_dir) is False:
            print_bad("Hm. It looks like {} does not exist. Please contact the i-ASK center for help.".format(scratch_dir))
            return

        # If checks are good, continue
        try:
            os.chdir(home_env_var)

        except OSError:
            print_bad("Could not change into home directory. Please contact the i-ASK center for help.")
            return

        # Fix work symlink
        work_symlink_path = "{}/work".format(home_env_var)
        if os.path.isdir(work_symlink_path) and os.path.islink(work_symlink_path) is False:
            # Compress fake work to tar.gz archive and then delete old directory
            compressor = Compression("work", "old-work", home_env_var)
            compressor.togzip()
            shutil.rmtree("work")

            # Create new symlink
            os.symlink(work_dir, work_symlink_path)
            print_good("Work symlink has been fixed!")

        elif os.path.islink(work_symlink_path) is False:
            os.symlink(work_dir, work_symlink_path)
            print_good("Work symlink has been fixed!")

        else:
            print_info("No action needed for work directory.")

        # Fix scratch symlink
        scratch_symlink_path = "{}/scratch".format(home_env_var)
        if os.path.isdir(scratch_symlink_path) and os.path.islink(scratch_symlink_path) is False:
            # Compress fake scratch to tar.gz archive and then delete old directory
            compressor = Compression("scratch", "old-scratch", home_env_var)
            compressor.togzip()
            shutil.rmtree("scratch")

            # Create new symlink
            os.symlink(work_dir, scratch_symlink_path)
            print_good("Scratch symlink has been fixed!")

        elif os.path.islink(scratch_symlink_path) is False:
            os.symlink(work_dir, scratch_symlink_path)
            print_good("Scratch symlink has been fixed!")

        else:
            print_info("No action needed for scratch directory.")

        print_good("All done!")


if __name__ == "__main__":
    main()
