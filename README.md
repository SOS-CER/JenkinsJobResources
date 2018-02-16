# JenkinsJobResources

JenkinsJobResources contains example job configuration files for 1) while the project is open, 2) to build a specific commit hash, and 3) to close a job for grading.  The jobs are generated using [`jobs/job_manager.py`](jobs/job_manager.py).

## Creating a Reference Job
While example configurations are provided, the best way to work with Jenkins jobs is to create a reference job.  Create a new Jenkins job to evaluate the teaching staff solution and include the appropriate checks for your build.  When the new job is done and tested, use the configuration as the base for generating student jobs.

## Identifiers
Update the configuration to include identifiers for string replacement when creating student jobs. 

### Permissions
Jenkins jobs should be configured with the `AuthorizationMatrixProperty`.  Remove the specific permissions and replace with the `$PERMISSIONS` identifier.

For example, the base config might look like:

```
    <hudson.security.AuthorizationMatrixProperty>
      <inheritanceStrategy class="org.jenkinsci.plugins.matrixauth.inheritance.InheritParentStrategy"/>
        <permission>hudson.model.Item.Read:sesmith5</permission>
        <permission>hudson.model.Item.Build:sesmith5</permission>
    </hudson.security.AuthorizationMatrixProperty>
```

and the updated config would look like:

```
    <hudson.security.AuthorizationMatrixProperty>
      <inheritanceStrategy class="org.jenkinsci.plugins.matrixauth.inheritance.InheritParentStrategy"/>
        $PERMISSIONS
    </hudson.security.AuthorizationMatrixProperty>
```

### GitHub Repository
The name of the GitHub Repository should replace the `$SSH_REPO_URL` identifier.  Additionally, the main URL path should be appropriate for all repositories.  The entire repository url may be replaced if needed.

For example, the base config might look like:

```
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.6.4">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>git@github.ncsu.edu:engr-csc216-staff/2017-fall-projects.git</url>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>**</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
```

and the updated config would look like:

```
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.6.4">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>git@github.ncsu.edu:engr-csc216-fall2017/$SSH_REPO_URL.git</url>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>**</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
```

### Email List
If jobs are set up to email students after each build, an environment variable can be created to hold student email addresses.

```
    <EnvInjectBuildWrapper plugin="envinject@2.1.5">
      <info>
        <propertiesContent>
        PROJECT_NAME=Project3
        TS_PROJECT_NAME=GetOutdoors
        EMAILS=$EMAIL_LIST
        </propertiesContent>
        <secureGroovyScript plugin="script-security@1.35">
          <script></script>
          <sandbox>false</sandbox>
        </secureGroovyScript>
        <loadFilesFromMaster>false</loadFilesFromMaster>
      </info>
    </EnvInjectBuildWrapper>
```

### Commit Hash
Sometimes you may want to build a certain commit from a student's repository.   The name of the commit can be provided:

The following will build any branch:

```
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.6.4">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <!-- TODO: Replace with leading URL string for GitHub repository -->
        <url>git@github.ncsu.edu:engr-csc216-fall2017/$SSH_REPO_URL.git</url>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>**</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
```

but if the contents of the `<name>` tag are updated, only specific branches or commits will build.

```
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.6.4">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <!-- TODO: Replace with leading URL string for GitHub repository -->
        <url>git@github.ncsu.edu:engr-csc216-fall2017/$SSH_REPO_URL.git</url>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>$COMMIT_HASH</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
```


## Student Jobs
The `jobs/job_manager.py` program supports creating the directory structure for Jenkins jobs.

`job_manager.py` runs on Python 2.7.

### Opening or Closing Student Jobs
To open or close student jobs, run `job_manager.py` with three command line arguments:

  * `-f`: file that contains repository and one or more student ids using the repository
  * `-a`: assignment prefix that will be added to the repository name to create the job name
  * `-c`: configuration file that is the base for all the jobs
  
```
# To open with open config in F17-P3-config.xml
python job_manager.py -f F17-P3-repos.txt -a P3 -c F17-P3-config.xml

# To close with close config in F17-P3-close.xml.  The assignment prefix has to match to overwrite 
# earlier job configs
python job_manager.py -f F17-P3-repos.txt -a P3 -c F17-P3-close.xml
```
  
The repository file contains a list of repositories with one or more student ids all separated by spaces.

```
repository-name-1 id1 id2 id3
repository-name-2 id4 id5
repository-name-3 id6 id7 id8 id9
repository-name-4 id10
```

After creating/updating jobs, restart Jenkins for the jobs to take effect.

### Creating Jobs for a Commit
To create a job for a specific commit, include the `-h` flag and use a different format for the file associated with the `-f` flag.

```
# To create jobs with a given commit hash create a base config like F17-P3-commit.xml
python job_manager.py -h -f F17-P3-repos.txt -a P3 -c F17-P3-commit.xml
```

The repository file contains a list of repositories and commit hashes separated by spaces.

```
repository-name-1 commithash
repository-name-2 commithash
```

## Automating Jobs
The creation and closing of jobs can be created using cron jobs.  Wrapping the commands up in a shell script can be useful for creating cron jobs.  An example script for closing jobs is provided in [`jobs/close.sh`](jobs/close.sh)