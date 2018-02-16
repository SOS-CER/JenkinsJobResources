import os
import errno
import sys
import getopt

########################################################################################
# job_manager.py will create the folder structure and config files for Jenkins
# jobs given:
#  - a list of repositories with either student(s) or commit hash
#  - an assignment prefix
#  - a base configuration file
#
# To create jobs for students/teams, use 
#  % python job_manager.py -f <student_repo_file> -a <assignment_name> -c <config_file>
#
# To create jobs to build a specific commit hash for a repo, use
#  % python job_manager.py -h -f <commit_repo_file> -a <assignment_name> -c <config_file>
#
# (Python 2.7)
########################################################################################

# Creates a dictionary of repositories by reading *_repo_file.
# The repository is the key for either the list of students or the commit hash for
# a specific build.
# The file is in the format of the repository name followed by whitespace followed by
# one or more whitespace delimited strings.
def make_list(repo_file):
    f = open(repo_file, 'r');
    repos = dict()
    for line in f:
       tokens = line.split(None, 1)
       if len(tokens) == 2:
          repos.update({tokens[0]:tokens[1].strip()})
    f.close()
    return repos


# Creates the XML configuration file for a Jenkins job with the given repository and 
# a space separate list of student ids.
def make_student_xml(config_file, ssh_repo_url, student_id_list):
    # Defaults to giving students Read and Build permissions.  Add lines for 
    # any additional permissions that each user should have.
    read = "<permission>hudson.model.Item.Read:$STUDENTID</permission>"
    build = "<permission>hudson.model.Item.Build:$STUDENTID</permission>"
    permissions = ""
    emails = ""

    # For all students assiged to a repo, create the appropriate permissions and
    # email values.
    tokens = student_id_list.split()
    for t in tokens:
        permissions = "%s\n%s\n%s"%(permissions, read.replace("$STUDENTID", t), build.replace("$STUDENTID", t))
        # Update email_post with value appropriate for institution
        email_post = "@ncsu.edu"
        emails = "%s,%s%s"%(emails, t, email_post)

    # Read the configuration file
    xml = file(config_file,"r").read()
    
    # Make the replacements in the XML file.
    xml = xml.replace("$SSH_REPO_URL",ssh_repo_url)
    xml = xml.replace("$PERMISSIONS", permissions)
    xml = xml.replace("$EMAIL_LIST", emails[1:])

    return xml
    
# Creates the XML configuration file for a Jenkins job with the given repository and 
# a commit hash
def make_commit_xml(config_file, ssh_repo_url, commit_hash):
    xml = file(config_file,"r").read()
    xml = xml.replace("$SSH_REPO_URL",ssh_repo_url)
    xml = xml.replace("$COMMIT_HASH", commit_hash)

    return xml


def main(argv):
    # Init needed variables
    job_path = "/var/lib/jenkins/jobs/"
    repo_file = ''
    assignment = ''
    config_file = ''
    commit_hash = 0

    # Handle command line arguments
    try:
        opts, args = getopt.getopt(argv, "hf:a:c:")
    except getopt.GetoptError:
        print "create_jobs.py [-h] -f <student file> -a <homework name> -c <config file>"
        sys.exit(1)

    # Update variables from command line arg info
    for opt, arg in opts:
        if opt == '-f':
            repo_file = arg
        if opt == '-a':
            assignment = arg 
        if opt == '-c':
            config_file = arg
        if opt == '-h':
            commit_hash = 1

    i = 0
    # Get repos and other info from repo_file
    repos = make_list(repo_file);
    
    # For each repository, create the appropriate folder and config file.
    for r in repos:
        i += 1
        # Folder is a combination of the assignment command line arg and the repo name
        assignment_path = "%s%s-%s"%(job_path, assignment, r)
        
        try:
            os.makedirs(assignment_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise            
        
        # Create the config.xml file in the assignment_path
        f = file("%s/config.xml"%(assignment_path),"w")
        if commit_hash:
            f.write(make_commit_xml(config_file, r, repos[r]))
        else: 
            f.write(make_student_xml(config_file, r, repos[r]))
        f.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
