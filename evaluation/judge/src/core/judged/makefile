all: judged.cc
	g++ -Wall -c -DOJ_USE_MYSQL -I/usr/local/mysql/include/mysql -I/usr/include/mysql  judged.cc
	g++ -Wall -o judged judged.o -L/usr/local/mysql/lib/mysql -L/usr/lib/mysql  -L/usr/lib64/mysql  -lmysqlclient

