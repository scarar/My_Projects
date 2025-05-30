﻿$listener = New-Object System.Net.HttpListener
$port = 8080
$webroot = "C:\Users\"  # Change this to your directory

$listener.Prefixes.Add("http://+:$port/")
$listener.Start()
Write-Host "HTTP server running at http://localhost:$port/"
Write-Host "Serving files from: $webroot"
Write-Host "Press Ctrl+C to stop the server."

while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    $requestedPath = $request.Url.AbsolutePath -replace "%20", " " # Handle spaces in URLs

    if ($requestedPath -eq "/") {
        # List files in the directory
        $files = Get-ChildItem -Path $webroot
        $fileListHtml = "<html><body><h2>Files in $webroot</h2><ul>"
        foreach ($file in $files) {
            $fileListHtml += "<li><a href='/$($file.Name)'>$($file.Name)</a></li>"
        }
        $fileListHtml += "</ul></body></html>"
        $buffer = [System.Text.Encoding]::UTF8.GetBytes($fileListHtml)
    } else {
        # Serve the requested file
        $filePath = Join-Path $webroot $requestedPath.TrimStart("/")
        if (Test-Path $filePath -PathType Leaf) {
            $buffer = [System.IO.File]::ReadAllBytes($filePath)
            $response.ContentType = "application/octet-stream"  # Forces download
        } else {
            $buffer = [System.Text.Encoding]::UTF8.GetBytes("<html><body><h2>404 Not Found</h2></body></html>")
            $response.StatusCode = 404
        }
    }

    # Send response
    $response.ContentLength64 = $buffer.Length
    $response.OutputStream.Write($buffer, 0, $buffer.Length)
    $response.OutputStream.Close()
}
