import os
import shutil
import click
from utils.special_print import print_good
from utils.special_print import print_bad
from utils.special_print import print_info
from utils.special_print import important_info
from utils.special_print import printrichtext
from utils.print_license import licenseheader
from utils.print_license import licensebody
from utils.verifylocale import verifylocale


@click.command()
@click.option("-V", "--version", is_flag=True, help="Print version info.")
@click.option("--license", is_flag=True, help="Print licensing info.")
def setupcomsolsymlink(version, license):
    """setupcomsolsymlink: A simple script to relocate the COMSOL cache to the work directory."""
    if version:
        licenseheader("setupcomsolsymlink v1.2")

    elif license:
        licensebody("setupcomsolsymlink: A simple script to relocate the COMSOL cache to the work directory.")

    else:
        home_env_var = os.getenv('HOME')
        os.chdir(home_env_var)
        comsol_cache_path = "{}/.comsol".format(home_env_var)
        comsol_cache_symlink_path = "{}/work/.comsol".format(home_env_var)
        
        # Verify that .comsol exists
        if os.path.isdir(comsol_cache_path) and os.path.islink(comsol_cache_path) is False:
            # Move COMSOL cache to work and create symlink
            shutil.move(comsol_cache_path, comsol_cache_symlink_path)
            os.symlink(comsol_cache_symlink_path, comsol_cache_path)
            print_good("The COMSOL cache symlink has been established!")

        elif os.path.islink(comsol_cache_path):
            print_info("The COMSOL cache symlink already exists.")

        else:
            print_bad("The COMSOL cache does not exist in {}!".format(home_env_var))
            important_info("Please create the COMSOL cache by launching the COMSOL application.")

        return

if __name__ == "__main__":
    out, err = verifylocale()
    if err != None:
        printrichtext("Uh oh. Looks like the UTF-8 locale is not supported on your system! " +
                      "Please try using [bold blue]locale-gen en_US.UTF-8[/bold blue] before continuing.")
    
    else:
        setupcomsolsymlink()
