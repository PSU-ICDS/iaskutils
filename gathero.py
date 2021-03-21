import os
import subprocess
import multiprocessing
import shutil
import glob
from xml.dom import minidom
import click
from progress.bar import Bar
from utils.special_print import print_good
from utils.special_print import print_bad
from utils.special_print import print_info
from utils.special_print import important_info
from utils.special_print import printrichtext
from utils.compression import Compression

# Global variables
home_env_var = os.getenv('HOME')


def checkjob(checkjob_path, job_id, root_dir):
    """Execute checkjob on the command line and then write to output file."""
    print_info("Running checkjob on {}".format(job_id))
    checkjob_out = subprocess.run(["sudo", "{}".format(checkjob_path), "{}".format(job_id), "-v", "--timeout=300"],
                                  capture_output=True, text=True)

    # Change into output directory and create output file
    os.chdir(root_dir)
    fout = open("{}_checkjob-output.txt".format(job_id), "wt")
    fout.write(str(checkjob_out.stdout))
    fout.close()


def checkjob_xml(checkjob_path, job_id, root_dir):
    """Execute checkjob on the command line, retrieve xml output, and then write to xml outfile."""
    checkjob_out = subprocess.run(["sudo", "{}".format(checkjob_path), "{}".format(job_id), "-v", "--timeout=300", "--xml"],
                                  capture_output=True, text=True)
    os.chdir(root_dir)
    fout = open("{}.xml".format(job_id), "wt")
    fout.write(str(checkjob_out.stdout))
    fout.close()


@click.command()
@click.option("-V", "--version", is_flag=True, help="Print version info.")
@click.option("--license", is_flag=True, help="Print licensing info.")
@click.argument("job", default=None, nargs=-1)
@click.option("-n", "--name", default="gathero_output", help="Name of output directory and archive (default: "
                                                             "gathero_output).")
@click.option("-c", "--compression", type=click.Choice(["gzip", "bz2", "xz", "tar", "zip"]),
              default="zip", help="Compression algorithm to use (default: zip).")
@click.option("-d", "--directory", default="{}/scratch".format(home_env_var),
              help="Directory to save output to (default: ~/scratch).")
def gathero(version, license, job, name, compression, directory):
    """gathero: A script to collect essential information about a user's job(s)."""
    if version:
        click.echo("gathero v1.2  Copyright (C) 2021  Jason C. Nucciarone \n\n"
                   "This program comes with ABSOLUTELY NO WARRANTY; \n"
                   "for more details type \"gathero --license\". This is free software, \n"
                   "and you are welcome to redistribute it under certain conditions; \n"
                   "go to https://www.gnu.org/licenses/licenses.html for more details.")

    elif license:
        click.echo("""gathero: A script to collect essential information about a user's job(s).\n
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
        # Change into the directory specified by the user to create $NAME
        try:
            os.chdir(directory)

        except OSError:
            print_bad("Something went wrong when trying to change into {} ".format(directory) +
                      "Please contact i-ASK center at iask@ics.psu.edu.")
            return

        # Create $NAME directory and then move into it.
        # Also save path above output dir because we
        # will need it later.
        dir_above_output = os.getcwd()
        try:
            os.mkdir(name)
            os.chdir(name)

        except FileExistsError:
            shutil.rmtree(name)
            os.mkdir(name)
            os.chdir(name)

        # Get system path to checkjob and mam-* executables
        checkjob_path = subprocess.getoutput("command -v checkjob")
        mam_list_funds_path = subprocess.getoutput("command -v mam-list-funds")
        mam_list_accounts_path = subprocess.getoutput("command -v mam-list-accounts")

        # If the user specified no job ids on the command line
        if job is None:
            printrichtext("No job ID found. Please enter job ID(s). \n"
                        "Use [bold blue]gathero --help[/bold blue] or contact the i-ASK center \n"
                        "at iask@ics.psu.edu if you need help.")
            return

        print_good("Executing checkjob on given job ids.")
        process_list = list()
        for jobs in job:
            try:
                process = multiprocessing.Process(target=checkjob,
                                                  args=(checkjob_path, jobs, os.getcwd()))
                process_list.append(process)
                process.start()

            except multiprocessing.ProcessError:
                print_bad("Something went wrong running checkjob. \n"
                          "Please contact i-ASK center for help!")

        # Block until all checkjobs have been completed
        for process in process_list:
            process.join()

        # Once checkjob has finished running
        print_good("All checkjobs have been successful!")
        print_good("Collecting allocation and user info.")
        
        # Run checkjob again, but this time pull the xml
        os.mkdir("tmp")
        above_tmp_dir = os.getcwd()
        os.chdir("tmp")

        process_list_2 = list()
        for jobs in job:
            try:
                process = multiprocessing.Process(target=checkjob_xml,
                                                  args=(checkjob_path, jobs, os.getcwd()))
                process_list_2.append(process)
                process.start()

            except multiprocessing.ProcessError:
                print_bad("Something went wrong collecting allocation and user info. \n"
                          "Please contact i-ASK center for help!")

        # Block until process 2 jobs are done
        for process in process_list_2:
            process.join()

        # After XML files have been collected, pull allocation name and user info
        xml_files = glob.glob("*.xml")
        alloc_name = list()
        user_id = list()

        for xml_file in xml_files:
            doc = minidom.parse(xml_file)
            data = doc.getElementsByTagName("job")

            for datum in data:
                if datum.attributes['Account'].value not in alloc_name:
                    alloc_name.append(datum.attributes['Account'].value)
                
                if datum.attributes['User'].value not in user_id:
                    user_id.append(datum.attributes['User'].value)

        # Process allocation and user info
        os.chdir(above_tmp_dir)
        shutil.rmtree("tmp")

        if len(alloc_name) != 0:
            for alloc in alloc_name:
                fout = open("{}-info.txt".format(alloc), "wt")
                # Run showq
                showq = subprocess.run(["showq", "-w", "acct={}".format(alloc)], 
                                        capture_output=True, text=True)
                fout.write("showq -w acct={}\n".format(alloc))
                fout.write(str(showq.stdout) + "\n")
                fout.close()

        if len(user_id) != 0:
            for user in user_id:
                fout = open("{}-info.txt".format(user), "wt")
                # Run account_quota_check
                account_quota_check = subprocess.run(["account_quota_check", "{}".format(user)], 
                                                        capture_output=True, text=True)
                fout.write("account_quota_check {}\n".format(user))
                fout.write(str(account_quota_check.stdout) + "\n\n")

                # Run qstat
                qstat = subprocess.run(["qstat", "-u", "{}".format(user)], 
                                        capture_output=True, text=True)
                fout.write("qstat -u {}\n".format(user))
                fout.write(str(qstat.stdout) + "\n\n")

                # Run mam-list-accounts
                mam_list_accounts = subprocess.run(["sudo", "{}".format(mam_list_accounts_path), "-u", "{}".format(user)],
                                                    capture_output=True, text=True)
                fout.write("mam-list-accounts -u {}\n".format(user))
                fout.write(str(mam_list_accounts.stdout) + "\n\n")

                # Run mam-list-funds
                mam_list_funds = subprocess.run(["sudo", "{}".format(mam_list_funds_path), "-u", "{}".format(user)],
                                                    capture_output=True, text=True)
                fout.write("mam-list-funds -u {}\n".format(user))
                fout.write(str(mam_list_funds.stdout))

        # Compress the gathero_output directory
        os.chdir(dir_above_output)
        compress_dir = above_tmp_dir.split("/")
        archive = Compression(compress_dir[-1], name, above_tmp_dir)

        if compression == "gzip":
            archive.togzip()
            shutil.move("{}/{}.tar.gz".format(dir_above_output, name), "{}/{}.tar.gz".format(above_tmp_dir, name))

        elif compression == "bz2":
            archive.tobzip()
            shutil.move("{}/{}.tar.bz2".format(dir_above_output, name), "{}/{}.tar.bz2".format(above_tmp_dir, name))

        elif compression == "xz":
            archive.toxz()
            shutil.move("{}/{}.tar.xz".format(dir_above_output, name), "{}/{}.tar.xz".format(above_tmp_dir, name))

        elif compression == "tar":
            archive.totar()
            shutil.move("{}/{}.tar".format(dir_above_output, name), "{}/{}.tar".format(above_tmp_dir, name))

        elif compression == "zip":
            archive.tozip()
            shutil.move("{}/{}.zip".format(dir_above_output, name), "{}/{}.zip".format(above_tmp_dir, name))

        else:
            print_bad("There was an issue compressing your files! Please contact the i-ASK center at " +
                      "iask@ics.psu.edu")
            return

        print_good("All done!")


if __name__ == "__main__":
    gathero()
