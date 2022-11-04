
        
        
/*
 * UVic CSC 360, Summer 2022
 * This code copyright 2022: Roshan Lasredo, Mike Zastre, David Clark
 *
 * Assignment 3
 * --------------------
 * 	Simulate a Multi-Level Feedback Queue with `3` Levels/Queues each 
 * 	implementing a Round-Robin scheduling policy with a Time Quantum
 * 	of `2`, `4` and `8` resp, and including a boost mechanism.
 * 
 * Input: Command Line args
 * ------------------------
 * 	./mlfq <input_test_case_file>
 * 	e.g.
 * 	     ./mlfq test1.txt
 * 
 * Input: Test Case file
 * ---------------------
 * 	Each line corresponds to an instruction and is formatted as:
 *
 * 	<event_tick>,<task_id>,<burst_time>
 * 
 * 	NOTE: 
 * 	1) All times are represented as `whole numbers`.
 * 	2) Special Case:
 * 	     burst_time =  0 -- Task Creation
 * 	     burst_time = -1 -- Task Termination
 * 
 * 
 * Assumptions: (For Multi-Level Feedback Queue)
 * -----------------------
 * 	1) On arrival of a Task with the same priority as the current 
 * 		Task, the current Task is not preempted.
 * 	2) A Task on being preempted is added to the end of its queue.
 * 	3) Arrival tick, Burst tick and termination tick for the same  
 * 		Task will never overlap. But the arrival/exit of one  
 * 		Task may overlap with another Task.
 * 	4) Tasks will be labelled from 1 to 10.
 * 	5) The event_ticks in the test files will be in sorted order.
 * 	6) Once a Task is assigned a queue, it will always continue to 
 * 		run in that queue for any new future bursts (Unless further 
 * 		demoted, or returned to queue 1 by a boost).
 * 	7) Task termination instruction will always come after the 
 * 		Task completion for the given test case.
 * 	8) Task arrival/termination/boosting does not consume CPU cycles.
 * 	9) A task is enqueued into one of the queues only if it requires
 * 		CPU bursts.
 * 	
 * Output:
 * -----------------------
 * 	NOTE: Do not modify the formatting of the print statements.
 * 
 */


#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <string.h>
#include <stdbool.h>

/*
 * A queue structure provided to you by the teaching team. This header
 * file contains the function prototypes; the queue routines are
 * linked in from a separate .o file (which is done for you via
 * the `makefile`).
 */
#include "queue.h"


/* 
 * Some constants related to assignment description.
 */
#define MAX_INPUT_LINE 100
#define MAX_TASKS 10
#define BOOST_INTERVAL 25
const int QUEUE_TIME_QUANTUMS[] = { 2, 4, 8 };


/*
 * Here are variables that are available to methods. Given these are 
 * global, you need not pass them as parameters to functions. 
 * However, you must be careful while initializing/setting these
 * global variables.
 */
Queue_t *queue_1;
Queue_t *queue_2;
Queue_t *queue_3;
Task_t task_table[MAX_TASKS];
Task_t *current_task;

int remaining_quantum = 0;		// Remaining Time Quantum for the current task

int index1=0;
int remain_burst_time=1;
int done=1;
int done1=1;
int done2=1;
int done3=1;
int done4=1;
int waiting_time1=1;
int turn_around_time1=1;
int i=0;
int position;
Task_t *new_task1;
int remainder;
Task_t *priority_task;
int end;
int after_boost=-1;
 Task_t *temp_task;
int arr[20];
int arr_index=0;
int is_inst_complete = false;
/*
 * Function: validate_args
 * -----------------------
 *  Validate the input command line args.
 *
 *  argc: Number of command line arguments provided
 *  argv: Command line arguments
 */
void validate_args(int argc, char *argv[]) {
	if(argc != 2) {
		fprintf(stderr, "Invalid number of input args provided! Expected 1, received %d\n", argc - 1);
		exit(1);
	}
}


/*
 * Function: initialize_vars
 * -------------------------
 *  Initialize the three queues.
 */
void initialize_vars() {
	queue_1 = init_queue();
	queue_2 = init_queue();
	queue_3 = init_queue();
}

/*
 * Function: read_instruction
 * --------------------------
 *  Reads a single line from the input file and stores the 
 *  appropriate values in the instruction pointer provided. In case
 *  `EOF` is encountered, the `is_eof` flag is set.
 *
 *  fp: File pointer to the input test file
 *  instruction: Pointer to store the read instruction details
 */
void read_instruction(FILE *fp, Instruction_t *instruction) {
	char line[MAX_INPUT_LINE];
	
	if(fgets(line, sizeof(line), fp) == NULL) {
		instruction->event_tick = -1;
		instruction->is_eof = true;
		return;
	}

	int vars_read = sscanf(line, "%d,%d,%d", &instruction->event_tick, 
	&instruction->task_id, &instruction->burst_time);
	instruction->is_eof = false;

	if(vars_read == EOF || vars_read != 3) {
		fprintf(stderr, "Error reading from the file.\n");
		exit(1);
	}

	if(instruction->event_tick < 0 || instruction->task_id < 0) {
		fprintf(stderr, "Incorrect file input.\n");
		exit(1);
	}
}




/*
 * Function: get_queue_by_id
 * -------------------------
 *  Returns the Queue associated with the given `queue_id`.
 *
 *  queue_id: Integer Queue identifier.
 */
Queue_t *get_queue_by_id(int queue_id) {
	switch (queue_id) {
		case 1:
			return queue_1;

		case 2:
			return queue_2;

		case 3:
			return queue_3;
	}
	return NULL;
}



/*
 * Function: handle_instruction
 * ----------------------------
 *  Processes the input instruction, depending on the instruction
 *  type:
 *      a. New Task (burst_time == 0)
 *      b. Task Completion (burst_time == -1)
 *      c. Task Burst (burst_time == <int>)
 *
 *  NOTE: 
 *	a. This method performs NO task scheduling, NO Preemption and NO
 *  	Updation of Task priorities/levels. These tasks would be   
 *		handled by the `scheduler`.
 *	b. A task once demoted to a level, retains that level for all 
 *		future bursts unless it is further demoted or boosted.
 *
 *  instruction: Input instruction
 *  tick: Clock tick (ONLY For Print statements)
 */

void handle_instruction(Instruction_t *instruction, int tick) {
	int task_id = instruction->task_id;

	
	if(instruction->burst_time == 0) {    
        Task_t *new_task1 = (Task_t*) malloc(sizeof(Task_t));  // Create a task pointer 
        
        new_task1->id=task_id;
        new_task1->burst_time=instruction->burst_time;
        task_table[index1]=*new_task1;            // Store the task in the task table
		printf("[%05d] id=%04d NEW\n", tick, task_id);
	
	} else if(instruction->burst_time == -1) { // When burst_time == -1, it means current task is finished then I will store the id in an array so I will not dequeue it in later. 
		// Task Termination
		int waiting_time;
		int turn_around_time;
        
        arr[arr_index]=priority_task->id;  // Store the finished id in an int array 
        arr_index++;
	
        
        waiting_time=task_table[position].total_wait_time; // Calculate waiting_time
        turn_around_time=task_table[position].total_execution_time+task_table[position].total_wait_time; // Calculate turn_around_time

   
		printf("[%05d] id=%04d EXIT wt=%d tat=%d\n", tick, task_id, 
			waiting_time, turn_around_time);
        current_task=NULL;
        
	} else {  // When the burst time != -1 or 0 


        Task_t *new_task = (Task_t*) malloc(sizeof(Task_t)); // Store the given to the pointer 
        
        new_task->id=task_id;
        new_task->burst_time=instruction->burst_time;
        new_task->total_wait_time=0;
        new_task->total_execution_time=0;
        new_task->current_queue=0;
        new_task->remaining_burst_time=new_task->burst_time-1;
        end=0;
        new_task1= new_task;
        
        for(int check=0; check<MAX_TASKS-1; check++){ // Check if we have the id already in the task table, if it is we will not store it in table and it will inherit previous information
            if((task_table[check].burst_time!=0) && (task_table[check].id == task_id)){
                 new_task->total_wait_time=task_table[check].total_wait_time;
                 new_task->total_execution_time=task_table[check].total_execution_time;
                 new_task->current_queue=task_table[check].current_queue;
                 break;
            }
            else if(check==MAX_TASKS-2){ // If it is not in the task table then store it in. 
              task_table[index1]=*new_task;
            }
        }
       
        remainder=1;    // Reset remainder for function scheduler
        remain_burst_time=1;
        index1++;
        enqueue(queue_1, new_task); // Enqueque the task to queue_1
        temp_task=priority_task;
        current_task=NULL;   // Set current_task to NULL
 



	}
}



/*
 * Function: peek_priority_task
 * ----------------------------
 *  Returns a reference to the Task with the highest priority.
 *  Does NOT dequeue the task.
 */
Task_t *peek_priority_task() { // I am work so hard to find an easier way but it didn't work, so I used the one which works but it looks ugly
    Task_t * temp = (Task_t*) malloc(sizeof(Task_t));

    if(is_empty(queue_1) != 1){       // Basically, the idea is check which queue is not empty start from queue_1 to queue_3 then return the corresponding id
   
          temp->id =1;
          return temp;
    }
    else if(is_empty(queue_1) == 1 && is_empty(queue_2) != 1){
   
          temp->id =2;
          return temp; 
    }
    
    else if(is_empty(queue_1) == 1 && is_empty(queue_2) == 1 && is_empty(queue_3) != 1){
 
           temp->id =3;
           return temp;
    }
        



	return NULL; // When all the queues are empty, return NULL
}



/*
 * Function: decrease_task_level
 * -----------------------------
 *  Updates the task to lower its level(Queue) by 1.
 */
void decrease_task_level(Task_t *task) {
	task->current_queue = task->current_queue == 3 ? 3 : task->current_queue + 1;
}
/*
 * Function: boost
 * -----------------------------
 *  If the current tick is a multiple of the BOOST_INTERVAL, perform a boost
 *  on all tasks in Queue 3, followed by a boost on all tasks in Queue
 *  2.  A boost is done by dequeuing the task from its current queue 
 *  and queuing it into Queue 1.  At the end of this process, all tasks
 *  with remaining CPU bursts should be in Queue 1.  The current task
 *  should be unaffected, except that its remaining quantum should be
 *  set to a maximum of 2 (or left unchanged if it's less than two). 
 *  Boosts do not take CPU time.
 */

void boost(int tick){   
 
     if (tick % BOOST_INTERVAL == 0){  // When tick ==25 

        for(int q3=0; q3<=queue_size(queue_3)-1; q3++){ // Go through every task in queue_3

            for(int arr_index2=0; arr_index2<arr_index-1; arr_index2++){ // Check if the task is finished or not, if it is finished then we dequeue it and not store back to queue_1
                 if(dequeue(queue_3)->id !=arr[arr_index2]){

                       enqueue(queue_1, dequeue(queue_3));
                 }
            }
        }
                    
        for(int q2=0; q2<queue_size(queue_2)-1; q2++){ // Go through every task in queue_2
            for(int arr_index3=0; arr_index3<arr_index-1; arr_index3++){ // Check if the task is finished or not, if it is finished then we dequeue it and not store back to queue_1
                 if(dequeue(queue_2)->id !=arr[arr_index3]){
                       enqueue(queue_1, dequeue(queue_2));
                 }
            }
            
        }

        if(current_task!=NULL){
         current_task->current_queue=1;   
        }
         
        after_boost=0; // Set after_boost =0 for scheduler
          
        printf("[%05d] BOOST\n", tick);
     }
                    
     
                   

}
Task_t *dequeue_priority_task(Task_t * temp) {  // The function I create for dequeue the task from queue by using the id from function peek_priority_task()
    Task_t * priority_task1;
      if(temp->id==1){                     // When id==1, dequeue queue_1 then return the task etc
          priority_task1=dequeue(queue_1);
          return priority_task1;
        }
       else if(temp->id==2){
           priority_task1=dequeue(queue_2);
           return priority_task1;
            }
      else {
            priority_task1=dequeue(queue_3);
          return priority_task1;
         }
    return NULL;
}
/*
 * Function: scheduler
 * -------------------
 *  Schedules the task having the highest priority to be the current 
 *  task. Also, for the currently executing task, decreases the task    
 *	level on completion of the current time quantum.
 *
 *  NOTE:
 *  a. The task to be currently executed is `dequeued` from one of the
 *  	queues.
 *  b. On Pre-emption of a task by another task, the preempted task 
 *  	is `enqueued` to the end of its associated queue.
 */
void scheduler() {
    
    if((current_task == NULL) && (index1 != 0) && (end!=1)){ // When current_task == NULL it means we have to find another priority_task, index1 to make sure the task table is not empty, end means whether we reach the end of input file
	         priority_task = dequeue_priority_task(peek_priority_task()); // Find priority_task

             
             int temp2=priority_task->burst_time-priority_task->remaining_burst_time; 
             if(temp2>=7){  // Check if the priority_task is in queue_3
                 enqueue(queue_3,priority_task); // enqueue back in case it being interrupted by other tasks before it is completed then we will lose it.
             }
             if(after_boost != -1){ // check if the process has been boost or not 
                priority_task->current_queue=1;
             }
             current_task=priority_task; 
    }

    if(current_task != NULL){
        
         remainder= current_task->burst_time - current_task->remaining_burst_time; // Check the used time for current task 

         if((remainder> current_task->burst_time)){ // If it is over its' burst_time then we have to stop it and go through next priority_task
    
             if((is_empty(queue_1)==1)&& (is_empty(queue_2)==1) && (is_empty(queue_3)==1)){ // If no more task in the queues, set current_task=NULL
                current_task=NULL;
             }
             else{ // If there exist other task then set current_task point to that 
                 
                 priority_task = temp_task;
                 remainder= priority_task->burst_time - priority_task->remaining_burst_time;
  
                 current_task=priority_task;

             }

         }
         
    }
    
    if((index1!= 0) && (remainder <3) && (current_task != NULL)){ // If the remainder is less than 3 it means it is in queue_1 in normal case
        if(current_task->current_queue<1){ // Increase the current_queue if it is less than 0 and boost not occur 
          current_task->current_queue=1;
        }

        if(after_boost !=-1){  // Special case if boost occur, then I use after_boost to trace it and use it for update current_task -> current_queue
            if(after_boost==2){ // 2 for queue_1 
             decrease_task_level(current_task);
                
            }
            if(after_boost==6){ // 4 for queue_2
                decrease_task_level(current_task);
              }
            after_boost++;
                 
            }
    }
    else if((3<=remainder) &&  (remainder<7) && (current_task != NULL)){ // If the remainder is between 3 and 7 it means it is in queue_2 in normal case
 
        if((after_boost ==-1) && (current_task->current_queue<2)){ // Increase the current_queue if it is less than 2 and boost not occur 

            decrease_task_level(current_task);
        }
        if(after_boost !=-1){   // Special case if boost occur, then I use after_boost to trace it and use it for update current_task -> current_queue
            if(after_boost==2){ // 2 for queue_1
             decrease_task_level(current_task);
                
            }
            if(after_boost==6){ // 4 for queue_2
                decrease_task_level(current_task);
              }
            after_boost++;
                 
            }
    }
    else if((7<=remainder )&& (current_task != NULL)){  // If the remainder is>= 7 it means it is in queue_2 in normal case
 
        if(current_task != NULL){
            
            if((after_boost ==-1) && (current_task->current_queue<3)){ // Increase the current_queue if it is less than 3 and boost not occur 
   
             decrease_task_level(current_task);
           }
           if(after_boost !=-1){ // Special case if boost occur, then I use after_boost to trace it and use it for update current_task -> current_queue
                if(after_boost==2){  // 2 for queue_1
                decrease_task_level(current_task);
                
                 }
                if(after_boost==6){ // 4 for queue_2
                   decrease_task_level(current_task);
                }
                after_boost++;
                 
            }


        }
      }
}



/*
 * Function: execute_task
 * ----------------------
 *  Executes the current task (By updating the associated remaining
 *  times). Sets the current_task to NULL on completion of the
 *	current burst.
 *
 *  tick: Clock tick (ONLY For Print statements)
 */
void execute_task(int tick) {
	if(current_task != NULL) { 

       if( (remainder<3) && (remainder<=current_task->burst_time)){ // If the remainder is less than 3 it means it is in queue_1 in normal case, and make sure it is nor over its' burst_time 
           if((remainder==2) && (current_task->burst_time >2)){ // If the remainder ==2 it means it will be dequeued from queue_1 and enqueue to queue_2, if current_task->burst_time >2, it means it will stay in queue_1 because it run only one time 
               
              enqueue(queue_2, priority_task);
              
           }
                    
           printf("[%05d] id=%04d req=%d used=%d queue=%d\n", tick, 
			current_task->id, current_task->burst_time, 
			(current_task->burst_time - current_task->remaining_burst_time), 
			current_task->current_queue);
           current_task->remaining_burst_time=current_task->remaining_burst_time-1;
           if((remainder==2) || (after_boost==2)){ // When remainder or after_boost equal to 2, it means we have to find another priority_task therefore set current_task to NULL
               
               current_task=NULL;
     
           }
         
       }
       else if( (3<=remainder) && (remainder<7) && (remainder<=current_task->burst_time)){ // If the remainder is between 3 to 7 it means it is in queue_2 in normal case
           if(remainder==6){  // If the remainder ==6 it means it will be dequeued from queue_2 and enqueue to queue_3
               enqueue(queue_3, priority_task);
               
           }
           printf("[%05d] id=%04d req=%d used=%d queue=%d\n", tick, 
			current_task->id, current_task->burst_time, 
			(current_task->burst_time - current_task->remaining_burst_time), 
			current_task->current_queue);
           current_task->remaining_burst_time=current_task->remaining_burst_time-1;
           if((remainder==6) || (after_boost==6)){ // When remainder or after_boost equal to 6, it means we have to find another priority_task therefore set current_task to NULL
               current_task=NULL;
           }
          
       }
       else if( (7<=remainder) && (remainder<=current_task->burst_time)){ // If the remainder is >=7 it means it is in queue_1 in normal case, and make sure it is nor over its' burst_time 
           
           
           printf("[%05d] id=%04d req=%d used=%d queue=%d\n", tick, 
			current_task->id, current_task->burst_time, 
			(current_task->burst_time - current_task->remaining_burst_time), 
			current_task->current_queue);
           
           current_task->remaining_burst_time=current_task->remaining_burst_time-1;
       }
           
		
		else if(current_task->remaining_burst_time == 0) {
			current_task = NULL;
		}

	} else { // When current_task = NULL, just print tick 
		printf("[%05d] IDLE\n", tick);
	}
}



/*
 * Function: update_task_metrics
 * -----------------------------
 * 	Increments the waiting time/execution time for the tasks 
 * 	that are currently scheduled (In the queue). These values would  
 * 	be later used for the computation of the task waiting time and  
 *	turnaround time.
 */
void update_task_metrics() {

    if(index1!=0 && current_task != NULL){ 
     for(int in =0; in<MAX_TASKS-1; in++){
        if(current_task->id == task_table[in].id){// We increase total_execution_time by one if the current task == one of the task in table 
            task_table[in].total_execution_time=task_table[in].total_execution_time+1;
            if(current_task->burst_time <=2){
                 task_table[in].total_wait_time=0;
            }
            position=in; // The position used when burst time == -1
            
        }
        else{
            task_table[in].total_wait_time=task_table[in].total_wait_time+1; // We increase the waiting time of other tasks. 
            
        }
    }

    }
}



/*
 * Function: main
 * --------------
 * argv[1]: Input file/
 test case.
 */
int main(int argc, char *argv[]) {
	int tick = 1;
	//int is_inst_complete = false;
	
	validate_args(argc, argv);
	initialize_vars();

	FILE *fp = fopen(argv[1], "r");

	if(fp == NULL) {
		fprintf(stderr, "File \"%s\" does not exist.\n", argv[1]);
		exit(1);
	}

	Instruction_t *curr_instruction = (Instruction_t*) malloc(sizeof(Instruction_t));
	
	// Read First Instruction
	read_instruction(fp, curr_instruction);

	if(curr_instruction->is_eof) {
		fprintf(stderr, "Error reading from the file. The file is empty.\n");
		exit(1);
	}

	while(true) {
		while(curr_instruction->event_tick == tick) {
			handle_instruction(curr_instruction, tick);

			// Read Next Instruction
			read_instruction(fp, curr_instruction);
			if(curr_instruction->is_eof) { // Empty evertying when we reach the end of file 
				is_inst_complete = true; 
         
                for(int rest=0; rest<=queue_size(queue_1)-1; rest++){
                    dequeue(queue_1);
                }
                for(int rest1=0; rest1<=queue_size(queue_2)-1; rest1++){
                    dequeue(queue_2);
                }
                for(int rest2=0; rest2<=queue_size(queue_3)-1; rest2++){
                    dequeue(queue_3);
                }
                end=1;
                
			}
		}
		
		boost(tick);	

		scheduler();

		update_task_metrics();

		execute_task(tick);

		
		if(is_inst_complete && is_empty(queue_1) && is_empty(queue_2) && is_empty(queue_3) && current_task == NULL) {
			break;
		}

		tick++;
	}

	fclose(fp);
	deallocate(curr_instruction);
	deallocate(queue_1);
	deallocate(queue_2);
	deallocate(queue_3);
}
