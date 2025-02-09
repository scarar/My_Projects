$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://+:8080/")
$listener.Start()
Write-Host "Listening on http://localhost:8080/"

while ($listener.IsListening) {
    $context = $listener.GetContext()
    $response = $context.Response
    $responseString = "<html><body><h1>Hello from PowerShell HTTP Server!</h1></body></html>"
    $buffer = [System.Text.Encoding]::UTF8.GetBytes($responseString)
    $response.ContentLength64 = $buffer.Length
    $response.OutputStream.Write($buffer, 0, $buffer.Length)
    $response.OutputStream.Close()
}
