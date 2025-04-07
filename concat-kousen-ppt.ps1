# 入力フォルダと出力ファイル
$sourceFolder = "C:\Users\user\OneDrive\【高専】\【高専】情報理論と符号化\2024年度資料"
$outputFile = "$sourceFolder\merged.pptx"

# PowerPointを起動
$pptApp = New-Object -ComObject PowerPoint.Application
$pptApp.Visible = 1

# 新しいプレゼンを作成
$mergedPresentation = $pptApp.Presentations.Add()

# pptxファイル一覧を取得
$pptFiles = Get-ChildItem -Path $sourceFolder -Filter *.pptx

foreach ($file in $pptFiles) {
    try {
        Write-Host "処理中: $($file.Name)"
        $presentation = $pptApp.Presentations.Open($file.FullName, $false, $false, $false)

        for ($i = 1; $i -le $presentation.Slides.Count; $i++) {
            $presentation.Slides.Item($i).Copy()
            $mergedPresentation.Slides.Paste()
        }

        $presentation.Close()
    } catch {
        Write-Host "⚠ エラーが発生したためスキップ: $($file.Name)"
    }
}

# スライドがあるなら保存処理を試みる
try {
    if ($mergedPresentation.Slides.Count -gt 0) {
        $mergedPresentation.SaveAs($outputFile)
        Write-Host "✅ 保存完了: $outputFile"
    } else {
        Write-Host "⚠ スライドが1つも見つかりませんでした。"
    }

    # クローズ処理（念のため）
    $mergedPresentation.Close()
} catch {
    Write-Host "❌ 保存またはクローズ処理でエラーが発生しました。"
}

# PowerPoint終了とCOM解放
$pptApp.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($pptApp) | Out-Null
Remove-Variable pptApp
