# PowerShell automation engine container
FROM mcr.microsoft.com/powershell:lts-alpine-3.20

WORKDIR /automation

# Install PowerShell modules
RUN pwsh -Command "Install-Module -Name PSFramework -Force -Scope AllUsers"

# Copy PowerShell modules
COPY modules/ ./modules/
COPY entrypoint.ps1 .

RUN chmod +x entrypoint.ps1

CMD ["pwsh", "./entrypoint.ps1"]
