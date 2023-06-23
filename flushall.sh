echo "[+] Flushed Redis Main Cluster"
redis-cli -p 6379 FLUSHALL
echo "[+] Flushed Redis Cluster 1"
redis-cli -p 30001 FLUSHALL
echo "[+] Flushed Redis Cluster 2"
redis-cli -p 30002 FLUSHALL
echo "[+] Flushed Redis Cluster 3"
redis-cli -p 30003 FLUSHALL
# echo "[+] Flushed Redis Cluster 4"
# redis-cli -p 30004 FLUSHALL
# echo "[+] Flushed Redis Cluster 5"
# redis-cli -p 30005 FLUSHALL
# echo "[+] Flushed Redis Cluster 6"
# redis-cli -p 30006 FLUSHALL
# echo "[+] Flushed Redis Cluster 7"
# redis-cli -p 30007 FLUSHALL