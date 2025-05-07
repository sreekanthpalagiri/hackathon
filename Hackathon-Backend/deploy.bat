@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo Submitting build to Google Cloud...
echo ========================================================

:: Submit build, capture logs and extract LAST digest (only SHA part)
powershell -Command ^
    "$buildOutput = gcloud builds submit --region=us-central1 --tag us-central1-docker.pkg.dev/az-hackathon2025-tcs-458822/hackathon-repo/hackathon-backend:v1 2>&1 | Tee-Object -Variable out; $out | Out-File build_output.txt; $digestLines = $out | Select-String 'digest: sha256'; if ($digestLines.Count -gt 0) { $fullDigest = ($digestLines[-1] -split 'digest: ')[1].Trim(); $sha = $fullDigest.Split(' ')[0]; Write-Output $sha } else { Write-Output 'ERROR_NO_DIGEST' }" > digest.txt

:: Read the digest from digest.txt
set /p DIGEST=<digest.txt

if "%DIGEST%"=="ERROR_NO_DIGEST" (
    echo ERROR: Could not find sha256 digest in build output.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo Found image digest: %DIGEST%
echo ========================================================

:: Construct the full image reference
set IMAGE=us-central1-docker.pkg.dev/az-hackathon2025-tcs-458822/hackathon-repo/hackathon-backend@%DIGEST%

echo.
echo ========================================================
echo Deploying to Cloud Run using image: %IMAGE%
echo ========================================================

gcloud run deploy hackathon-backend ^
  --image=%IMAGE% ^
  --allow-unauthenticated ^
  --port=8080 ^
  --service-account=727170048524-compute@developer.gserviceaccount.com ^
  --timeout=1200 ^
  --cpu=4 ^
  --memory=8Gi ^
  --min-instances=1 ^
  --max-instances=1 ^
  --no-cpu-throttling ^
  --region=us-central1 ^
  --project=az-hackathon2025-tcs-458822

echo.
echo ========================================================
echo DEPLOYMENT COMPLETE
echo ========================================================
pause
endlocal
