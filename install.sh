echo "Installation VPNService started..."
echo "Check docker installatio status..."
docker -v

echo "Check docker-compose installation status...."

echo "Run installation..."
docker-compose up -d

echo "Installation finish with status success..."
