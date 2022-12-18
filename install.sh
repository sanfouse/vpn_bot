echo "Installation VPNService started..."
echo "Check docker installatio status..."
docker -v

echo "Check docker-compose installation status...."

echo "Run installation..."
git clone https://github.com/sanfouse/vpn_bot.git
docker-compose up -d

echo "Installation finish with status success..."
