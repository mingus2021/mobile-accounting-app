# PowerShell script to push final fix
Set-Location "f:\work\electron-accounting\mobile-app"

Write-Host "Adding updated GitHub Actions workflow..." -ForegroundColor Green
git add .github/workflows/build-apk.yml

Write-Host "Committing changes..." -ForegroundColor Green
git commit -m "Fix: Complete GitHub Actions workflow with proper Android SDK setup"

Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: Updated workflow pushed to GitHub!" -ForegroundColor Green
    Write-Host "Visit: https://github.com/mingus2021/mobile-accounting-app/actions" -ForegroundColor Cyan
    Write-Host "The new build should start automatically and succeed!" -ForegroundColor Yellow
} else {
    Write-Host "ERROR: Push failed" -ForegroundColor Red
}

Read-Host "Press Enter to exit"
