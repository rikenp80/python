<#
example execution

C:\Users\rpatel3\Documents\GitHubNew\databases\scripts\dump_and_restore\pg_dump_and_restore.ps1 `
-source_db_instance "reimagine-dev-canada.cluster-c514w15qevsg.ca-central-1.rds.amazonaws.com" `
-target_db_instance "clone-reimagine-dev-canada-instance-1-cluster.cluster-c514w15qevsg.ca-central-1.rds.amazonaws.com" `
-source_db_user "" `
-target_db_user "" `
-source_db_password "" `
-target_db_password "" `
-db_list "'addresses','associate','configuration_can','customer','identity','jobs','notifications','orders'" `
-dump_type 'data', 'schema'
#>


param
(
$source_db_instance,
$target_db_instance,
$source_db_user,
$target_db_user,
$source_db_password,
$target_db_password,
$db_list,
$dump_type = ('data','schema') #option are data and/or schema
)



#set DB connection strings
$source_db_connection = "postgresql://" + $source_db_user + ":" + $source_db_password + "@" + $source_db_instance + "/postgres"
$target_db_connection = "postgresql://" + $target_db_user + ":" + $target_db_password + "@" + $target_db_instance + "/postgres"



#create a directory for the dump files
$date = (get-date).ToString("yyyyMMdd_HHmmss")
$source_db_instance_part = $source_db_instance -replace ".rds.amazonaws.com",""

$dump_directory = $home + "\Documents\dumps\" + $source_db_instance_part + "\" + $date
write-output "dump directory: $dump_directory"

$null = New-Item -Path $dump_directory -ItemType Directory


#set flags for pg_dump command
if ($dump_type -eq "data" -and $dump_type -eq "schema")
	{
		$dump_flags = ''
	}	
elseif ($dump_type -eq "schema")
	{
		$dump_flags = '-s' 
	}


#loop through each database
foreach ($database in $db_list)
{
    if ($database -ne "")
    {
		
        $database = $database.trim()
        write-output "`n======= $database ======="



        #set environment variable for source DB password to execute dump commands
		$env:PGPASSWORD = $source_db_password


        #create DB dump and format files as UTF8
        $Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False

        $dump_filename = $dump_directory + "\" + $database + ".dump"
        $dump_command = "pg_dump -h " + $source_db_instance + " -U " + $source_db_user + " -E UTF8 $dump_flags " + $database + " > " + $dump_filename

        write-output $dump_command

        Invoke-Expression $dump_command

        $dump_file = Get-Content $dump_filename
        $dump_filename_utf8 = $dump_directory + "\" + $database + "_utf8.dump"
        [System.IO.File]::WriteAllLines($dump_filename_utf8, $dump_file, $Utf8NoBomEncoding)



        #if dump_type is for schema only dump, still dump and restore data for __EFMigrationsHistory table
        if ($dump_flags -eq '-s')
        {
            $dump_EFMigrationsHistory_filename = $dump_directory + "\" + $database + "__EFMigrationsHistory.dump"        
            $dump_EFMigrationsHistory_command = 'pg_dump -h ' + $source_db_instance + ' -U ' + $source_db_user + ' -E UTF8 -a -t \`"__EFMigrationsHistory\`" ' + $database + ' > ' + $dump_EFMigrationsHistory_filename

            write-output $dump_EFMigrationsHistory_command

            Invoke-Expression $dump_EFMigrationsHistory_command

            $dump_EFMigrationsHistory_file = Get-Content $dump_EFMigrationsHistory_filename
            $dump_EFMigrationsHistory_filename_utf8 = $dump_directory + "\" + $database + "__EFMigrationsHistory_utf8.dump"
            [System.IO.File]::WriteAllLines($dump_EFMigrationsHistory_filename_utf8, $dump_EFMigrationsHistory_file, $Utf8NoBomEncoding)
        }

     		
	
		
        #drop and recreate empty target database
        $query = "select pg_terminate_backend(pid) from pg_stat_activity where datname = '" + $database + "';"
        psql --dbname=$target_db_connection -t -q -c $query

        $query = "drop database " + $database + ";"
        psql --dbname=$target_db_connection -t -c $query

        $query = "create database " + $database + ";"
        psql --dbname=$target_db_connection -t -c $query
		
		
		
		#build command to set permissions on new target DB with create roles and users with random password.
		#schema parameter is empty as that will be populated later
		$random_password1 = (("123456789ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz".tochararray() | sort {Get-Random})[0..20] -join '')
		$random_password2 = (("123456789ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz".tochararray() | sort {Get-Random})[0..20] -join '')


		$SetPermissions_ScriptPath = $PSScriptRoot + "\SetPermissions.sql"
		
		$set_permissions_command = 'psql -U reimagineUser -h ' + $target_db_instance + ' -d postgres -f "' + $SetPermissions_ScriptPath + '"' +
		' -v v_rw_role="' + $database + '_readwrite"' +
		' -v v_rw_user="' + $database + '"' +
		' -v v_rw_user_password="'+$random_password1+'"' +
		' -v v_ci_user="' + $database + '_ci_user"' +
		' -v v_ci_user_password="'+$random_password2+'"' +
		' -v v_read_role="' + $database + '_readonly"' +
		' -v v_dbname="' + $database + '"' +
		' -v v_schema='
		

		#run set permissions script for public schema first as the restore will fail if the users and roles do not exist
		$public_permissions_command = $set_permissions_command.replace('v_schema=', 'v_schema="public"')
		write-output "===SET PERMISSIONS `n $public_permissions_command"

		#set environment variable for target DB password and execute set permissions command
		$env:PGPASSWORD = $target_db_password
		Invoke-Expression $public_permissions_command
		


        #run command to restore dump file to target DB
        $restore_command = "psql -h " + $target_db_instance + " -U " + $target_db_user + " -d " + $database + " -f """ + $dump_filename_utf8 + """"        
		write-output "===RESTORE COMMAND `n $restore_command"

		Invoke-Expression $restore_command
		
		
		#run command to restore EFMigrationsHistory table data if this was a schema dump_type
		if ($dump_flags -eq '-s')
		{
			$restore_EFMigrationsHistory_command = "psql -h " + $target_db_instance + " -U " + $target_db_user + " -d " + $database + " -f """ + $dump_EFMigrationsHistory_filename_utf8 + """"        
			write-output "===RESTORE EFMigrationsHistory COMMAND `n $restore_EFMigrationsHistory_command"

			Invoke-Expression $restore_EFMigrationsHistory_command
		}



		#get user schemas and run set permissions script against those schemas which will set the permissions specifically for that schema
		$query = "SELECT nspname FROM pg_catalog.pg_namespace where nspowner <> 10 and nspname <> 'public'"
		$schemas = psql -h $target_db_instance -U $target_db_user -d $database -t -c $query | Where-Object({ $_ -ne "" })

		
		foreach($schema in $schemas)
		{
			$schema = $schema.trim()
			$user_permissions_command = $set_permissions_command.replace('v_schema=', 'v_schema="'+ $schema +'"')

			write-output "===SET PERMISSIONS `n $user_permissions_command"
			Invoke-Expression $user_permissions_command
		}
    }
}