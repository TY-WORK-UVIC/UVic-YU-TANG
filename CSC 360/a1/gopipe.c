/* gopipe.c
 *
 * CSC 360, Summer 2022
 *
 * Execute up to four instructions, piping the output of each into the
 * input of the next.
 *
 * Please change the following before submission:
 *
 * Author: Luke Skywalker
 * Login:  usetheforce@uvic.ca 
 */


/* Note: The following are the **ONLY** header files you are
 * permitted to use for this assignment! */

#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <wait.h>
#include <dirent.h>





#define MAX_LENGTH 80
#define NUM_STRINGS 50
char* line_data(char* line){// Input the each line from file and take out the useless part and return only the part we needed
    const char sep[5]="bin"; // Seperate the input by "bin"
    const char sep2[5]="/";  // Seperate the input by "/"
    char* token;
    token = strtok(line,sep); // Seperate the input by "bin"
    char* temp[100];
    int i=0;
    while(token !=NULL){
      
       temp[i]=token;
       i++;
       token=strtok(NULL,sep);
     }
    char* token2;
    token2=strtok(temp[1],sep2); // Seperate the input by "/"
    int k=0;
    char *temp2[150];
    while(token2!=NULL){
       temp2[k]=token2;
       k++;
        
       token2=strtok(NULL,sep2); 
    }
  
    return temp2[0]; // Return the needed info 
}
int main() { 
    char buffer[256];  
    char path[80];
    char array[NUM_STRINGS][MAX_LENGTH] = {""};
    char array2[NUM_STRINGS][MAX_LENGTH] = {""};
    int i =0;
    
    for(int counter=0; counter<4; counter++){ // Can only take four inputs from keyboard 
       memset(buffer, '\0', sizeof(buffer)); // Empty the buffer every time 
       read(0,buffer,50);   // Read the input from the keyboard 
        
       if(strlen(buffer) ==1){ // When buffer is empty exit the for loop
          
           break;
       }     
       strncpy(path, buffer, 50);    // Store the buffer value in a char array
       strncpy(array[i], path,50);   // Storet the value from char array to array[i]
       
       i++; 
    }
    
    for(int j=0; j<i; j++){ // Read the order from the array
       
        if(i==1){  // If there is only one order, then run it 
            
            system(line_data(array[0])); // Use the data after seperate by line_data, and run by system 
        }
        else{
                if(j==0){ // The first order 
               
                array[j][strcspn(array[j], "\n")] = 0; // Take out the spaces from the end of line 
                strncpy(array2[0], line_data(array[j]),50);  // Store the info into an empty array 
                strncat(array2[0], " | ", 10);    // Concatenate arrray2 with "|" at end of line
                }
              
                else if(j==i-1){ // When it is the last order
                    
                    array[j][strcspn(array[j], "\n")] = 0; // Take out the spaces from the end of line
                    strncat(array2[0], line_data(array[j]), 80); // Concatenate arrray2 with array, don't need to add "|" because it is the last order
                }
                else{
                    array[j][strcspn(array[j], "\n")] = 0; // Take out the spaces from the end of line
                    strncat(array2[0], line_data(array[j]), 80); // Concatenate arrray2 with array
                    strncat(array2[0], " | ", 10);  // Concatenate arrray2 with "|" at end of line
                     
                } 
        }
    }
          
    system(array2[0]); // Use the system() to run the order 

    
    return 0;
}
