#include<stdio.h>
#include<stdlib.h>

FILE *fin;
FILE *fout;

typedef struct _Queue {
	int* key;
	int first, rear, qsize, max_queue_size;
}Queue;

Queue* MakeNewQueue(int X){
	Queue* newqueue = NULL;
	newqueue = (Queue*)malloc(sizeof(Queue));
	newqueue->max_queue_size = X;
	newqueue->qsize = 0;
	newqueue->first = 1;
	newqueue->rear = 0;
	newqueue->key = (int*)malloc(sizeof(int) * X);
	printf("%d %d %d %d\n", newqueue->first, newqueue->max_queue_size, newqueue->qsize, newqueue->rear);
	return newqueue;
}

int IsEmpty(Queue* Q){
	if(Q->qsize) return 0;
	else return 1;
}

int Dequeue(Queue* Q){
	int i = Q->first;
	Q->qsize--;
	Q->first = (Q->first + 1) % Q->max_queue_size;
	printf("%d %d\n", i, Q->key[i]);
	return Q->key[i];
}

void Enqueue(Queue* Q, int X){
	Q->qsize++;
	Q->rear = (Q->rear+1) % Q->max_queue_size;
	Q->key[Q->rear] = X;
	printf("enqueue %d %d\n", Q->rear, Q->key[Q->rear]);
}

void DeleteQueue(Queue* Q){
	free(Q->key);
	free(Q);
}

int main(){
	Queue* Q;
	Q = MakeNewQueue(6);
	for(int i = Q->first; i <= Q->rear; i++) printf("%d ", Q->key[i]);
	printf("\n");
	Enqueue(Q, 0);
	for(int i = Q->first; i <= Q->rear; i++) printf("%d ", Q->key[i]);
	printf("\n");
	Enqueue(Q, 5);
	for(int i = Q->first; i <= Q->rear; i++) printf("%d ", Q->key[i]);
	printf("\n");
	return 0;
}