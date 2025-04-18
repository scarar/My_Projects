# PowerShell Script for HTTP Server

$rootPath = Get-Location  # Serve files from the current directory
$url = 'http://localhost:8080/'  # Listening URL/port

# Create and start the listener
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($url)
$listener.Start()

Write-Host "Serving $rootPath at $url ... (Ctrl+C to stop)"

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()  # Wait for a request

        $requestPath = $context.Request.Url.LocalPath.TrimStart('/')
        $filePath = Join-Path $rootPath $requestPath

        if (Test-Path $filePath -PathType Leaf) {
            # Serve the file
            $content = [System.IO.File]::ReadAllBytes($filePath)
            $context.Response.ContentType = [System.Web.MimeMapping]::GetMimeMapping($filePath)
            $context.Response.OutputStream.Write($content, 0, $content.Length)
        } else {
            # 404 Not Found
            $context.Response.StatusCode = 404
            $responseText = [System.Text.Encoding]::UTF8.GetBytes("File not found")
            $context.Response.OutputStream.Write($responseText, 0, $responseText.Length)
        }

        $context.Response.Close()
    }
} finally {
    $listener.Stop()
}
