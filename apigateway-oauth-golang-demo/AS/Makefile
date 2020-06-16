PROJECTMASTER="bin/token"
VERSION="v0.0.1"
DATE= `date +%FT%T%z`

date:
	@echo ${DATE}

version: date
	@echo ${VERSION}

master-build: version
	@GO111MODULE=on go build -o ${PROJECTMASTER}  -mod=vendor src/main.go

master-run: master-build
	@${PROJECTMASTER}


build: master-build
   
clean:
	@rm -f ${PROJECTMASTER} 

