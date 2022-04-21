#C:\Users\rpatel3\Documents\GitHubNew\databases\scripts\set_awscli_env_region.ps1 -env "UAT" -region "us-west-2"
#okta-awscli --profile default

param
(
  $env = "DEV",
  $region = "ca-central-1"
)

write-output "$env | $region"


if ($env -eq "DEMO") {$role = "role = arn:aws:iam::908947454082:role/AWS_PR_LkSup_Dev_RW_Access"}
if ($env -eq "DEV") {$role = "role = arn:aws:iam::497886394954:role/AWS_PR_LkSup_Dev_RW_Access"}
if ($env -eq "UAT") {$role = "role = arn:aws:iam::824346612374:role/AWS_PR_LkSup_Dev_RW_Access"}
if ($env -eq "PROD") {$role = "role = arn:aws:iam::108272573989:role/AWS_PR_LkSup_RW_Access"}



#update credential file setting for given environment
$path = "C:\Users\rpatel3\.aws\credentials"
$content = Get-Content -path $path

$line = $content | Select-String "aws_access_key_id = " | Select-Object -ExpandProperty Line
(Get-Content -path $path) -replace $line,"aws_access_key_id = " | Set-Content -Path $path


$line = $content | Select-String "aws_secret_access_key = " | Select-Object -ExpandProperty Line
(Get-Content -path $path) -replace $line,"aws_secret_access_key = " | Set-Content -Path $path



#update okta-aws file setting for given role
$path = "C:\Users\rpatel3\.okta-aws"
$content = Get-Content -path $path

$line = $content | Select-String "role =" | Select-Object -ExpandProperty Line
(Get-Content -path $path) -replace $line,$role | Set-Content -Path $path



#update config file setting for given region
$path = "C:\Users\rpatel3\.aws\config"
$content = Get-Content -path $path

$line = $content | Select-String "region" | Select-Object -ExpandProperty Line
$region = "region=" + $region

(Get-Content -path $path) -replace $line,$region | Set-Content -Path $path
