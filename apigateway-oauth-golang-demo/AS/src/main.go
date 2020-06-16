package main

import (
	"github.com/dgrijalva/jwt-go"
	"github.com/lestrrat-go/jwx/jwk"
	"github.com/gin-gonic/gin"
	"encoding/json"
	"fmt"
	"log"
    "io/ioutil"
	"time"
	"net/http"
)

//生成私钥后，读取文件 openssl genrsa -out private.key 2048
var keyData, err = ioutil.ReadFile("./src/private.key")

// 或者直接填写类似以下格式的私钥信息
//var keyData = []byte("-----BEGIN RSA PRIVATE KEY-----\nMIxx0S2bYevRy7hGQmUJTyQm3j1zEUR5jpdbL83Fbq\n-----END RSA PRIVATE KEY-----")

func init()  {

	parsedKey, err := jwt.ParseRSAPrivateKeyFromPEM(keyData)
	if err != nil {
		log.Println(err)
	}
	publicKey, err := jwk.New(&parsedKey.PublicKey)

	if err != nil {
		log.Println(err)
	}

	jsonbuf, err := json.MarshalIndent(publicKey, "", "  ")
	if err != nil {
		log.Println(err)
	}
	fmt.Println("公钥：\n", string(jsonbuf))
}

type Claims struct {
	Username string `json:"username"`
	jwt.StandardClaims
}

func getToken()string{
	expirationTime := time.Now().Add(5 * time.Minute) // 设置过期时间
	claims := &Claims{
		Username: "admin",
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: expirationTime.Unix(),
		},
	}

	parsedKey, err := jwt.ParseRSAPrivateKeyFromPEM(keyData)
	if err != nil {
		log.Println("1111", err)
	}

	token := jwt.NewWithClaims(jwt.SigningMethodRS256, claims)
	tokenString, err := token.SignedString(parsedKey)
	if err != nil {
		log.Println("2222", err)
		log.Println("generate token error")
	}
    return tokenString
}

func setupRouter() *gin.Engine {
	r := gin.Default()
	r.GET("/token", func(c *gin.Context) {
		c.String(http.StatusOK, getToken())
	})
	return r
}
func main() {
	r := setupRouter()
	// Listen and Server in 0.0.0.0:8080
	r.Run(":8080")
}
