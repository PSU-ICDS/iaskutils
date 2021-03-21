import os
import shutil
import click
from utils.special_print import print_good
from utils.special_print import print_bad
from utils.special_print import print_info
from utils.special_print import important_info


@click.command()
@click.option("-V", "--version", is_flag=True, help="Print version info.")
@click.option("--license", is_flag=True, help="Print licensing info.")
def main(version, license):
    """setupcondasymlink: A simple script to relocate the conda cache to the work directory."""
    if version:
        click.echo("setupcondasymlink v1.1  Copyright (C) 2021  Jason C. Nucciarone \n\n"
                   "This program comes with ABSOLUTELY NO WARRANTY; \n"
                   "for more details type \"setupcondasymlink --license\". This is free software, \n"
                   "and you are welcome to redistribute it under certain conditions; \n"
                   "go to https://www.gnu.org/licenses/licenses.html for more details.")

    elif license:
        click.echo("""setupcondasymlink: A simple script to relocate the conda cache to the work directory.\n
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
        home_env_var = os.getenv('HOME')
        os.chdir(home_env_var)
        conda_cache_path = "{}/.conda".format(home_env_var)
        conda_cache_symlink_path = "{}/work/.conda".format(home_env_var)
        
        # Verify that .conda exists
        if os.path.isdir(conda_cache_path) and os.path.islink(conda_cache_path) is False:
            # Move conda cache to work and create symlink
            shutil.move(conda_cache_path, conda_cache_symlink_path)
            os.symlink(conda_cache_symlink_path, conda_cache_path)
            print_good("The conda cache symlink has been established!")

        elif os.path.islink(conda_cache_path):
            print_info("The conda cache symlink already exists.")

        else:
            print_bad("The conda cache does not exist in {}!".format(home_env_var))
            important_info("Please initialize the conda cache by creating an environment using conda.")

        return

if __name__ == "__main__":
    main()
