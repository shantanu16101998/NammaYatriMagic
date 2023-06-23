echo "[+] Flushed Redis Main Cluster"
redis-cli -p 6379 FLUSHALL
echo "[+] Flushed Redis Cluster 1"
redis-cli -p 30001 FLUSHALL
echo "[+] Flushed Redis Cluster 2"
redis-cli -p 30002 FLUSHALL
echo "[+] Flushed Redis Cluster 3"
redis-cli -p 30003 FLUSHALL