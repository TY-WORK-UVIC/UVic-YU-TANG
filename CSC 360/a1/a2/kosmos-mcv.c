/*
 * kosmos-mcv.c (mutexes & condition variables)
 *
 * For UVic CSC 360, Summer 2022
 *
 * Here is some code from which to start.
 *
 * PLEASE FOLLOW THE INSTRUCTIONS REGARDING WHERE YOU ARE PERMITTED
 * TO ADD OR CHANGE THIS CODE. Read from line 133 onwards for
 * this information.
 */

#include <assert.h>
#include <pthread.h>
#include <sched.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "logging.h"



/* Random # below threshold indicates H; otherwise C. */
#define ATOM_THRESHOLD 0.55
#define DEFAULT_NUM_ATOMS 40

#define MAX_ATOM_NAME_LEN 10
#define MAX_KOSMOS_SECONDS 5

/* Global / shared variables */
int  cNum = 0, hNum = 0;
long numAtoms;



/* Function prototypes */
void kosmos_init(void);
void *c_ready(void *);
void *h_ready(void *);
void make_radical(int, int, int, char *);
void wait_to_terminate(int);


/* Needed to pass legit copy of an integer argument to a pthread */
int *dupInt( int i )
{
	int *pi = (int *)malloc(sizeof(int));
	assert( pi != NULL);
	*pi = i;
	return pi;
}


int main(int argc, char *argv[])
{
	long seed;
	numAtoms = DEFAULT_NUM_ATOMS;
	pthread_t **atom;
	int i;
	int status;

	if ( argc < 2 ) {
		fprintf(stderr, "usage: %s <seed> [<num atoms>]\n", argv[0]);
		exit(1);
	}

	if ( argc >= 2) {
		seed = atoi(argv[1]);
	}

	if (argc == 3) {
		numAtoms = atoi(argv[2]);
		if (numAtoms < 0) {
			fprintf(stderr, "%ld is not a valid number of atoms\n",
				numAtoms);
			exit(1);
		}
	}

    kosmos_log_init();
	kosmos_init();

	srand(seed);
	atom = (pthread_t **)malloc(numAtoms * sizeof(pthread_t *));
	assert (atom != NULL);
	for (i = 0; i < numAtoms; i++) {
		atom[i] = (pthread_t *)malloc(sizeof(pthread_t));
		if ( (double)rand()/(double)RAND_MAX < ATOM_THRESHOLD ) {
			hNum++;
			status = pthread_create (
					atom[i], NULL, h_ready,
					(void *)dupInt(hNum)
				);
		} else {
			cNum++;
			status = pthread_create (
					atom[i], NULL, c_ready,
					(void *)dupInt(cNum)
				);
		}
		if (status != 0) {
			fprintf(stderr, "Error creating atom thread\n");
			exit(1);
		}
	}

    /* Determining the maximum number of ethynyl radicals is fairly
     * straightforward -- it will be the minimum of the number of
     * hNum and cNum/2.
     */

    int max_radicals = (hNum < cNum/2 ? hNum : (int)(cNum/2));
#ifdef VERBOSE
    printf("Maximum # of radicals expected: %d\n", max_radicals);
#endif

    wait_to_terminate(max_radicals);
}


/*
* Now the tricky bit begins....  All the atoms are allowed
* to go their own way, but how does the Kosmos ethynyl-radical
* problem terminate? There is a non-zero probability that
* some atoms will not become part of a radical; that is,
* many atoms may be blocked on some condition variable of
* our own devising. How do we ensure the program ends when
* (a) all possible radicals have been created and (b) all
* remaining atoms are blocked (i.e., not on the ready queue)?
*/


/*
 * ^^^^^^^
 * DO NOT MODIFY CODE ABOVE THIS POINT.
 *
 *************************************
 *************************************
 *
 * ALL STUDENT WORK MUST APPEAR BELOW.
 * vvvvvvvv
 */


/* 
 * DECLARE / DEFINE NEEDED VARIABLES IMMEDIATELY BELOW.
 */

pthread_mutex_t mutex;
pthread_mutex_t mutex1;
pthread_mutex_t mutex2;
pthread_mutex_t mutex3;
pthread_mutex_t mutex4;
pthread_cond_t cond;

int radicals =0;
int num_free_c;
int num_free_h;

int combining_c1;
int combining_c2;
int combining_h;
int combiner_c[MAX_ATOM_NAME_LEN];
int combiner_h[MAX_ATOM_NAME_LEN];


int nextin=0;
int nextout=0;
int counter_c=0;
int counter_h=0;
int total_counter_h=0;
int total_counter_c=0;
int total_counter_c_in=0;
int total_counter_h_in=0;

int index_h=0;
int index_c=0;
time_t random;
int index_example=0;
int example[MAX_ATOM_NAME_LEN];
/*
 * FUNCTIONS YOU MAY/MUST MODIFY.
 */

void kosmos_init() {  // Initialize all the semaphores
    pthread_mutex_init(&mutex,NULL);
    pthread_mutex_init(&mutex1,NULL);
    pthread_mutex_init(&mutex2,NULL);
    pthread_mutex_init(&mutex3,NULL);
    pthread_mutex_init(&mutex4,NULL);
    
    
}

int contains(int list1[], int a, int b, int index_example){ // Check if the number appear in the list if not return 1
    int result=1;
    for(int i =0; i<index_example; i++){
        if(list1[i]==a || list1[i]==b){
            result=0;
            break;
        }
        
    }
            
    return result;
    
}
int contains_c(int list1 [], int a,int index_example){ // Check if the number appear in the list if not return 1
    int result=1;
    for(int i =0; i<index_example; i++){
        if(list1[i]==a){
            result=0;
            break;
        }
        
    }
            
    return result;
    
}
void *h_ready( void *arg ) 
{
	int id = *((int *)arg);
    char name[MAX_ATOM_NAME_LEN];
    

   
    sprintf(name, "h%03d", id);
    
#ifdef VERBOSE
    pthread_mutex_lock(&mutex2); // Lock the shared variables and store the hydrogens into a list and increase the counter and index
    total_counter_h++;
    combiner_h[index_h]=id;
    index_h++;
    pthread_mutex_unlock(&mutex2);
    
   
    if((total_counter_c>=2) && (total_counter_h>=1)){// Whenever there are at least 2 carbons and 1 hydrogen we can add them to log
       
        pthread_mutex_lock(&mutex1); // Lock to avoid other thread to use it 
        radicals++;                  
        srand((unsigned) time(&random)); // Create random numbers 
        int c= rand() % index_c;
        int d= rand() % index_c;
         
        while((contains(example,c,d,index_example) ==0) | (c==d)){ // Check I used the number of not and check if they are equal, if one of them is true keep getting random number 
            
            c= rand() % index_c;
            d= rand() % index_c;
        }
        
        pthread_mutex_lock(&mutex4); // Lock the list, then store the used number into list and increas the index
        example[index_example]=c;
        example[index_example+1]=d;
        index_example+=2;
        pthread_mutex_unlock(&mutex4);
        
       
        
        kosmos_log_add_entry(radicals,combiner_c[c],combiner_c[d],id,name);
        total_counter_c=total_counter_c-2;  // Reduce the number of Carbons and hydrogens
    
        total_counter_h--;
        pthread_mutex_unlock(&mutex1);
        
    }
    
#endif
    
	return NULL;
}


void *c_ready( void *arg )
{
	int id = *((int *)arg);
    char name[MAX_ATOM_NAME_LEN];
    
    
    sprintf(name, "c%03d", id);
    
    pthread_mutex_lock(&mutex3); // Lock the shared variables and store the carbons into a list and increase the counter and index
    total_counter_c++;
    combiner_c[index_c]=id;
    index_c++;
    pthread_mutex_unlock(&mutex3);
    
    if((total_counter_c>=2) && (total_counter_h>=1)){ // Whenever there are at least 2 carbons and 1 hydrogen we can add them to log
        
        pthread_mutex_lock(&mutex); // Lock to avoid other thread to use it 
        radicals++;
        srand((unsigned) time(&random)); // Create random numbers
        int c= rand() % index_c;
        while((contains_c(example,c,index_example) ==0) || (combiner_c[c]==id)){// Check I used the number of not and check if it equal to current id, if one of them is true keep getting random number
            
            c= rand() % index_c;
        }
        pthread_mutex_lock(&mutex4); // Lock the list, then store the used number into list and increas the index
        example[index_example]=c;
        
        index_example++;
        pthread_mutex_unlock(&mutex4);
        
        kosmos_log_add_entry(radicals,id,combiner_c[c],combiner_h[index_h-1],name);
        total_counter_c=total_counter_c-2;  // Reduce the number of Carbons and hydrogens

        total_counter_h--;
        pthread_mutex_unlock(&mutex);
        
    }
   
	return NULL;
}


void wait_to_terminate(int expected_num_radicals) {
    /* A rather lazy way of doing it, but good enough for this assignment. */
    sleep(MAX_KOSMOS_SECONDS);
    kosmos_log_dump();
    exit(0);
}
