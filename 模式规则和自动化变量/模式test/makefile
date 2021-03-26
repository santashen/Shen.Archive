CC = gcc
targets = main1 main2
objects = bar.o foo.o 
.PHONY : all
all : $(targets)

main1 : main1.o $(objects)
	$(CC) -o $@ $^
main2 : main2.o $(objects)
	$(CC) -o $@ $^
%.o : %.c
	$(CC) -c $< -o $@