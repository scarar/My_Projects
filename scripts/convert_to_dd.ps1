$files = Get-ChildItem -Path '.' -Filter 'Tails.*' | Where-Object { $_.Extension -ne ".txt" } | Sort-Object Name

$outputPath = Join-Path (Get-Location) "Tails.dd"
$bufferSize = 10MB

Write-Host "Merging $($files.Count) files into $outputPath..."

try {
    $outputStream = [System.IO.File]::Open($outputPath, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write)

    foreach ($file in $files) {
        Write-Host "Merging file: $($file.Name)..."
        $inputStream = [System.IO.File]::OpenRead($file.FullName)

        try {
            $buffer = New-Object byte[] $bufferSize
            do {
                $read = $inputStream.Read($buffer, 0, $buffer.Length)
                if ($read -gt 0) {
                    $outputStream.Write($buffer, 0, $read)
                }
            } while ($read -gt 0)
        }
        finally {
            $inputStream.Close()
            $inputStream.Dispose()
        }
    }
}
finally {
    $outputStream.Flush()
    $outputStream.Close()
    $outputStream.Dispose()
}

# Explicit verification
if (Test-Path $outputPath) {
    Write-Host "Merge complete. File successfully created:" -ForegroundColor Green
    Get-Item $outputPath
} else {
    Write-Host "Merge failed. File not found." -ForegroundColor Red
}
