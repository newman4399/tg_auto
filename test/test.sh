# 1. 检查 DNS
getent hosts telegram.org

# 2. 检查 HTTPS 连接
curl -Iv --connect-timeout 10 https://my.telegram.org

# 3. 检查 Telegram Web 连接
curl -Iv --connect-timeout 10 https://web.telegram.org

# 4. 检查 IPv4
curl -4 -Iv --connect-timeout 10 https://my.telegram.org

# 5. 检查 IPv6
curl -6 -Iv --connect-timeout 10 https://my.telegram.org