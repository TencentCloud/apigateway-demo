if [ ! -f "./go.mod" ];then
    go mod init AS
fi
openssl genrsa -out ./src/private.key 2048
make build
